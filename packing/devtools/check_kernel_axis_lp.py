"""Independently check a rational lower bound for the fixed BC264 feature family.

Only ``check_packet`` and the fixed CLI construct the scientific source, lazily.
The synthetic API binds a caller's unrelated source and never implies a packing bound.
No producer, geometry package, numerical solver, or external field is imported.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import stat
import sys
from collections.abc import Sequence
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import cast

FORMAT = "bc264-axis-objective/v1"
SCIENTIFIC_SOURCE = "five-tight-axis-grids-v1"
SYNTHETIC_SOURCE = "synthetic-axis-poses-v1"
MAX_POSES = 45
MAX_PAIRS = 990
MAX_INPUT_BYTES = 2 * 1024 * 1024
MAX_SOURCE_BITS = 128
MAX_CERTIFICATE_BITS = 4096
MAX_ARITHMETIC_BITS = 32768
MAX_SOURCE_CHARS = 80
MAX_CERTIFICATE_CHARS = 2500
_KEYS = frozenset(("format", "source", "side", "poses", "alpha", "beta", "bound"))
_RATIONAL = re.compile(r"(?:0|-?[1-9][0-9]*)(?:/[1-9][0-9]*)?\Z", re.ASCII)

type Pose = tuple[Fraction, Fraction]
type Matrix = tuple[tuple[Fraction, ...], ...]
type Pair = tuple[int, int, Fraction]


class KernelCertificateError(ValueError):
    """The packet does not establish the requested, source-bound objective bound."""


@dataclass(frozen=True)
class Projection:
    """Dual blocks paired with A4, B2 and the three scalar kernel coefficients."""

    a: Matrix
    t: Matrix
    scalars: tuple[Fraction, ...]


def _bounded(value: Fraction) -> Fraction:
    if max(value.numerator.bit_length(), value.denominator.bit_length()) > MAX_ARITHMETIC_BITS:
        raise KernelCertificateError("exact arithmetic limit exceeded")
    return value


def _rational(raw: object, *, source: bool = False) -> Fraction:
    bits = MAX_SOURCE_BITS if source else MAX_CERTIFICATE_BITS
    chars = MAX_SOURCE_CHARS if source else MAX_CERTIFICATE_CHARS
    if type(raw) is not str or len(raw) > chars or not _RATIONAL.fullmatch(raw):
        raise KernelCertificateError("noncanonical or oversized rational string")
    parts = raw.split("/")
    numerator = int(parts[0])
    denominator = int(parts[1]) if len(parts) == 2 else 1
    if max(numerator.bit_length(), denominator.bit_length()) > bits:
        raise KernelCertificateError("rational bit limit exceeded")
    value = Fraction(numerator, denominator)
    if str(value) != raw:
        raise KernelCertificateError("noncanonical rational string")
    return value


def _caller_rational(value: object, *, source: bool = False) -> Fraction:
    if type(value) is not Fraction:
        raise KernelCertificateError("caller must supply exact Fractions")
    bits = MAX_SOURCE_BITS if source else MAX_CERTIFICATE_BITS
    if max(value.numerator.bit_length(), value.denominator.bit_length()) > bits:
        raise KernelCertificateError("caller rational bit limit exceeded")
    return _rational(str(value), source=source)


def _poses(raw: object, side: Fraction) -> tuple[Pose, ...]:
    if type(raw) is not list or not 1 <= len(raw) <= MAX_POSES:
        raise KernelCertificateError("pose inventory size is invalid")
    result: list[Pose] = []
    half = Fraction(1, 2)
    for item in raw:
        if type(item) is not list or len(item) != 2:
            raise KernelCertificateError("pose must have two coordinates")
        point = (_rational(item[0], source=True), _rational(item[1], source=True))
        if any(value < half or value > side - half for value in point):
            raise KernelCertificateError("unit square violates closed containment")
        if result and point <= result[-1]:
            raise KernelCertificateError("poses must be strictly sorted and distinct")
        result.append(point)
    return tuple(result)


def scientific_source() -> tuple[Fraction, list[list[str]]]:
    """Construct only the fixed five-grid source, when explicitly checking science."""
    side = Fraction(96, 25)
    low = Fraction(1, 2)
    high = side - Fraction(5, 2)
    points = {
        (base_x + i, base_y + j)
        for base_x in (low, high)
        for base_y in (low, high)
        for i in range(3)
        for j in range(3)
    }
    center = side / 2
    points.update((center + i, center + j) for i in (-1, 0, 1) for j in (-1, 0, 1))
    return side, [[str(x), str(y)] for x, y in sorted(points)]


def axis_features(point: Pose, side: Fraction) -> tuple[Fraction, ...]:
    """Retain the full eleven-feature order, including angular zero and repeated one."""
    u, v = (_bounded(value - side / 2) for value in point)
    u2, v2 = _bounded(u * u), _bounded(v * v)
    values = (
        Fraction(1),
        u2 + v2,
        u2 * v2,
        Fraction(1),
        Fraction(0),
        u2 - v2,
        u * v,
        u,
        v,
        u * v2,
        u2 * v,
    )
    return tuple(_bounded(value) for value in values)


def _index(value: object, size: int) -> int:
    if type(value) is not int or not 0 <= value < size:
        raise KernelCertificateError("pair index is invalid")
    return value


def _pairs(raw: object, poses: tuple[Pose, ...]) -> tuple[Pair, ...]:
    if type(raw) is not list or len(raw) > MAX_PAIRS:
        raise KernelCertificateError("pair inventory size is invalid")
    result: list[Pair] = []
    previous = (-1, -1)
    for item in raw:
        if type(item) is not dict or len(item) != 3 or set(item) != {"i", "j", "weight"}:
            raise KernelCertificateError("pair fields are invalid")
        i, j = _index(item["i"], len(poses)), _index(item["j"], len(poses))
        if i >= j or (i, j) <= previous:
            raise KernelCertificateError("pairs must be strictly sorted with i < j")
        weight = _rational(item["weight"])
        if weight <= 0:
            raise KernelCertificateError("sparse pair weights must be positive")
        if not any(abs(a - b) >= 1 for a, b in zip(poses[i], poses[j], strict=True)):
            raise KernelCertificateError("positive-weight pair has overlapping interiors")
        result.append((i, j, weight))
        previous = (i, j)
    return tuple(result)


def _sum(values: Sequence[Fraction]) -> Fraction:
    total = Fraction(0)
    for value in values:
        total = _bounded(total + value)
    return total


def projected_matrices(
    features: Sequence[Sequence[Fraction]], alpha: Sequence[Fraction], beta: Sequence[Pair]
) -> Projection:
    """Reconstruct the dual projection; T is a block trace, not half that trace."""
    if (
        not 1 <= len(features) <= MAX_POSES
        or len(alpha) != len(features)
        or len(beta) > MAX_PAIRS
    ):
        raise KernelCertificateError("projection inventory size is invalid")
    for row in features:
        if len(row) != 11 or any(type(value) is not Fraction for value in row):
            raise KernelCertificateError("projection requires eleven exact feature values")
        for value in row:
            _bounded(value)
    for value in alpha:
        if type(value) is not Fraction or value < 0:
            raise KernelCertificateError("projection weights must be nonnegative Fractions")
        _bounded(value)
    terms = [(i, i, weight) for i, weight in enumerate(alpha) if weight]
    for i, j, weight in beta:
        _index(i, len(features))
        _index(j, len(features))
        if i >= j or type(weight) is not Fraction or weight <= 0:
            raise KernelCertificateError("projection pair is invalid")
        terms.append((i, j, _bounded(weight)))
    a = [[Fraction(0) for _ in range(4)] for _ in range(4)]
    t = [[Fraction(0) for _ in range(2)] for _ in range(2)]
    scalars = [Fraction(0) for _ in range(3)]
    for i, j, weight in terms:
        left, right = features[i], features[j]
        for r in range(4):
            for c in range(4):
                cross = _bounded(left[r] * right[c] + right[r] * left[c])
                a[r][c] = _bounded(a[r][c] + _bounded(weight * cross / 2))
        for k in range(3):
            scalars[k] = _bounded(scalars[k] + _bounded(weight * left[4 + k] * right[4 + k]))
        for r in range(2):
            for c in range(2):
                cross = _sum(
                    tuple(
                        _bounded(
                            left[7 + 2 * r + axis] * right[7 + 2 * c + axis]
                            + right[7 + 2 * r + axis] * left[7 + 2 * c + axis]
                        )
                        for axis in range(2)
                    )
                )
                t[r][c] = _bounded(t[r][c] + _bounded(weight * cross / 2))
    return Projection(tuple(map(tuple, a)), tuple(map(tuple, t)), tuple(scalars))


def check_psd(matrix: Sequence[Sequence[Fraction]]) -> int:
    """Exact Schur elimination, with mandatory zero-pivot residual-row checks."""
    size = len(matrix)
    if not 1 <= size <= 4 or any(len(row) != size for row in matrix):
        raise KernelCertificateError("PSD block size is invalid")
    work: list[list[Fraction]] = []
    for row in matrix:
        if any(type(value) is not Fraction for value in row):
            raise KernelCertificateError("PSD block must be rational")
        work.append([_bounded(value) for value in row])
    if any(work[i][j] != work[j][i] for i in range(size) for j in range(size)):
        raise KernelCertificateError("PSD block is not symmetric")
    rank = 0
    for k in range(size):
        pivot = work[k][k]
        if pivot < 0:
            raise KernelCertificateError("PSD block has a negative pivot")
        if not pivot:
            if any(work[k][j] for j in range(k + 1, size)):
                raise KernelCertificateError("PSD zero pivot has a nonzero residual row")
            continue
        rank += 1
        for i in range(k + 1, size):
            for j in range(i, size):
                value = _bounded(work[i][j] - _bounded(work[i][k] * work[k][j] / pivot))
                work[i][j] = value
                work[j][i] = value
    return rank


def _envelope(raw: object, source: str) -> dict[str, object]:
    if type(raw) is not dict or len(raw) != len(_KEYS) or set(raw) != _KEYS:
        raise KernelCertificateError("packet fields are invalid")
    data = cast(dict[str, object], raw)
    if data["format"] != FORMAT or data["source"] != source:
        raise KernelCertificateError("packet format or source is invalid")
    return data


def _check(
    raw: object, *, source: str, side: Fraction, poses: object, minimum_bound: Fraction
) -> dict[str, object]:
    data = _envelope(raw, source)
    side = _caller_rational(side, source=True)
    minimum_bound = _caller_rational(minimum_bound)
    if side < 1 or minimum_bound < 1:
        raise KernelCertificateError("side and minimum threshold must be at least one")
    expected = _poses(poses, side)
    if _rational(data["side"], source=True) != side:
        raise KernelCertificateError("side does not match caller-bound source")
    actual = _poses(data["poses"], side)
    if actual != expected:
        raise KernelCertificateError("pose inventory does not match caller-bound source")
    raw_alpha = data["alpha"]
    if type(raw_alpha) is not list or len(raw_alpha) != len(actual):
        raise KernelCertificateError("alpha inventory size is invalid")
    alpha = tuple(_rational(value) for value in raw_alpha)
    if any(value < 0 for value in alpha) or _sum(alpha) != 1:
        raise KernelCertificateError("alpha must be nonnegative and normalized exactly")
    beta = _pairs(data["beta"], actual)
    bound = _rational(data["bound"])
    if bound != _bounded(1 + _sum(tuple(weight for _, _, weight in beta))):
        raise KernelCertificateError("bound does not equal one plus pair-weight sum")
    projection = projected_matrices(
        tuple(axis_features(pose, side) for pose in actual), alpha, beta
    )
    ranks = (check_psd(projection.a), check_psd(projection.t))
    if any(value < 0 for value in projection.scalars):
        raise KernelCertificateError("projected scalar is not PSD")
    if bound < minimum_bound:
        raise KernelCertificateError("verified lower bound is below the required threshold")
    return {
        "status": "verified_objective_bound",
        "source": source,
        "side": str(side),
        "bound": str(bound),
        "minimum_bound": str(minimum_bound),
        "pose_count": len(actual),
        "pair_count": len(beta),
        "projected_psd_verified": True,
        "projected_ranks": list(ranks),
        "scientific_family_refuted": source == SCIENTIFIC_SOURCE and bound >= 11,
        "new_packing_bound": False,
    }


def check_packet(raw: object) -> dict[str, object]:
    """Check only the fixed scientific source and the fixed threshold eleven."""
    _envelope(raw, SCIENTIFIC_SOURCE)
    side, poses = scientific_source()
    return _check(
        raw, source=SCIENTIFIC_SOURCE, side=side, poses=poses, minimum_bound=Fraction(11)
    )


def check_synthetic_packet(
    raw: object, *, side: Fraction, poses: object, minimum_bound: Fraction = Fraction(9)
) -> dict[str, object]:
    """Verify a caller-bound synthetic control, without any scientific-source access."""
    return _check(
        raw, source=SYNTHETIC_SOURCE, side=side, poses=poses, minimum_bound=minimum_bound
    )


def _json_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise KernelCertificateError("duplicate JSON object key")
        result[key] = value
    return result


def _json_integer(raw: str) -> int:
    if len(raw) > 3:
        raise KernelCertificateError("JSON integer is too large")
    return int(raw)


def _reject_json_number(_raw: str) -> object:
    raise KernelCertificateError("JSON floating-point values are forbidden")


def load_packet(path: Path) -> object:
    """Read at most two MiB from a regular file; reject duplicate keys and JSON floats."""
    descriptor = os.open(path, os.O_RDONLY | getattr(os, "O_NONBLOCK", 0))
    with os.fdopen(descriptor, "rb") as stream:
        if not stat.S_ISREG(os.fstat(stream.fileno()).st_mode):
            raise KernelCertificateError("packet input must be a regular file")
        raw = stream.read(MAX_INPUT_BYTES + 1)
    if len(raw) > MAX_INPUT_BYTES:
        raise KernelCertificateError("packet byte limit exceeded")
    text = raw.decode("utf-8")
    depth, quoted, escaped = 0, False, False
    for char in text:
        if quoted:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                quoted = False
        elif char == '"':
            quoted = True
        elif char in "[{":
            depth += 1
            if depth > 8:
                raise KernelCertificateError("JSON nesting limit exceeded")
        elif char in "]}":
            depth -= 1
    try:
        return json.loads(
            text,
            object_pairs_hook=_json_object,
            parse_int=_json_integer,
            parse_float=_reject_json_number,
            parse_constant=_reject_json_number,
        )
    except (json.JSONDecodeError, RecursionError) as exc:
        raise KernelCertificateError("malformed JSON packet") from exc


def main(argv: Sequence[str] | None = None) -> int:
    """The command line has no synthetic-source, side, or threshold override."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    arguments = parser.parse_args(None if argv is None else list(argv))
    try:
        result = check_packet(load_packet(arguments.input))
    except (KernelCertificateError, OSError, UnicodeError) as exc:
        print(f"kernel certificate refused: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
