"""Measure a decimal pose's least pair separation and wall clearance, and a declared dilation.

A decimal report states a side and, for each square, a centre and an angle in degrees,
in David Ellsworth's text format: a line ``s: SIDE`` (``Final s: SIDE`` in some
exports), then one line ``Square K: x=X, y=Y, deg=D`` per square, with the box centred at
the origin. It is the input of his ``check_packing.py``, the format of the
certificates issue #470 offers, and of the 50- and 60-digit exports other sources ship
beside their exact certificates.

Such a file is not an exact witness. Its digits are rounded, so squares that touch in
the author's computation can overlap by about the last printed place, and the printed
side can sit below the pose's extent. Before an import turns one into a rational
witness (the record's pattern is `sqpack.witness.promote_rational`: round to rationals,
dilate about the centre, take the side as the extent), it needs to know how far the
published digits are from a packing, and whether the slack the report declares pays for
the difference.

This tool measures that, rigorously. Every printed decimal is read exactly, and each
angle's cosine and sine are enclosed by outward-rounded interval arithmetic
(`mpmath.iv`, through `sqpack.promote.interval`) at a declared working precision. For
the side the file prints, and for a declared target side ``T``, it reports enclosures
of two quantities:

- **The least wall clearance**, ``T/2 - max(|x|, |y|) - (|cos| + |sin|)/2`` over every
  square, which is the least clearance of any corner from the container.
- **The least pair separation**, over every pair whose centres lie within 2 of each
  other: the best separating-axis gap, ``max_u |u . (c_j - c_i)| - 1/2 - R``, where
  ``u`` runs over the four edge normals of the two squares and
  ``R = (|cos(t_i - t_j)| + |sin(t_i - t_j)|)/2`` is either square's half-width along
  the other's normals. It is negative exactly when the interiors overlap, and is then
  minus the least penetration depth along an edge normal, the "depth" Ellsworth's
  checker prints. Two unit squares whose centres are more than 2 apart are separated by
  more than ``sqrt(2) - 1/2 - sqrt(2)/2 > 0.2071`` along an edge normal of either, so
  such a pair never sets the least separation of a packing that has touching squares.

At the target side the centres are dilated about the box centre by
``lambda = T / s``, so the pose scales with its box while every rotation is kept: that
is the declared dilation. Dilation by ``lambda >= 1`` only moves centres apart, so the
near pairs at the printed side include every near pair at ``T``.

Every measurement ends in one of three verdicts: ``packing`` when every pair and every
wall is proved nonnegative, ``not-a-packing`` when some pair or wall is proved negative,
and ``undecided`` otherwise. A ``packing`` verdict at ``T`` is an interval-arithmetic
proof that the dilated published pose packs ``n`` unit squares in a square of side
``T``. It is not an exact witness: an exact route still decides any witness built from
it, and this tool decides nothing else about the source's claim.

``measure`` writes a receipt, in `sqpack.retained_json`'s layout, that binds each
measured file's SHA-256 and size.
``check`` re-measures every file the receipt names under a root, and refuses a file
whose bytes differ or a receipt whose numbers a fresh measurement does not reproduce.

Usage, from ``packing/``::

    uv run --frozen --all-extras --group dev python -m devtools.decimal_pose_margins \\
        measure --root CHECKOUT --target-places 12 FILE... [--output RECEIPT]
    uv run --frozen --all-extras --group dev python -m devtools.decimal_pose_margins \\
        check RECEIPT --root CHECKOUT
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import sys
from collections import defaultdict
from collections.abc import Iterator, Sequence
from contextlib import contextmanager
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path, PurePosixPath
from typing import Any

import mpmath as mp
from strif import atomic_write_text

from sqpack import retained_json
from sqpack.promote.interval import (
    Interval,
    cos_degrees,
    decimal_string,
    from_endpoints,
    interval,
    sin_degrees,
)

FORMAT = "decimal-pose-margins-v1"

#: Working decimal digits of the interval arithmetic unless the caller declares more.
DEFAULT_DIGITS = 60
#: Fewer working digits than this cannot separate the 40-digit poses sources publish.
MIN_DIGITS = 30
#: Significant digits of each rendered enclosure endpoint, rounded outward.
RENDER_DIGITS = 8
#: How many of the worst pairs and walls a measurement lists by name.
LISTED = 10
#: Centres more than this far apart are a far pair, separated by more than 0.2071.
NEAR = 2

_DECIMAL = r"[-+]?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?"
_SIDE = re.compile(rf"(?:Final )?s:\s*({_DECIMAL})")
_SQUARE = re.compile(
    rf"Square\s+(\d+):\s*x=({_DECIMAL}),?\s+y=({_DECIMAL}),?\s+deg=({_DECIMAL}),?"
)


class PoseError(ValueError):
    """A pose file, target or receipt this tool refuses to measure or admit."""


@dataclass(frozen=True)
class Pose:
    """One square as printed: its label, exact centre and angle in degrees."""

    label: int
    x: Fraction
    y: Fraction
    degrees: Fraction


@dataclass(frozen=True)
class PoseFile:
    """A parsed decimal pose: the printed side, verbatim and exact, and its squares."""

    side_text: str
    side: Fraction
    squares: tuple[Pose, ...]


def parse_pose(text: str) -> PoseFile:
    """The side and squares of Ellsworth's text format, refusing anything else."""
    side_text: str | None = None
    squares: list[Pose] = []
    labels: set[int] = set()
    for number, raw in enumerate(text.splitlines(), start=1):
        line = raw.strip()
        if not line:
            continue
        if (side := _SIDE.fullmatch(line)) is not None:
            if side_text is not None or squares:
                message = f"line {number}: a second side line, or a side after the squares"
                raise PoseError(message)
            side_text = side.group(1)
            continue
        square = _SQUARE.fullmatch(line)
        if square is None:
            message = f"line {number} is neither the side nor a square: {line[:80]!r}"
            raise PoseError(message)
        label = int(square.group(1))
        if label in labels:
            message = f"line {number}: square {label} appears twice"
            raise PoseError(message)
        labels.add(label)
        x, y, degrees = (Fraction(square.group(index)) for index in (2, 3, 4))
        squares.append(Pose(label, x, y, degrees))
    if side_text is None:
        message = "the file states no side"
        raise PoseError(message)
    side = Fraction(side_text)
    if side <= 0:
        message = f"the side must be positive, not {side_text}"
        raise PoseError(message)
    if not squares:
        message = "the file states no square"
        raise PoseError(message)
    return PoseFile(side_text, side, tuple(squares))


def ceiling(value: Fraction, places: int) -> Fraction:
    """``value`` rounded up at ``places`` decimal places."""
    if places < 0:
        message = "places must be nonnegative"
        raise PoseError(message)
    scale = 10**places
    return Fraction(math.ceil(value * scale), scale)


def decimal_text(value: Fraction, places: int) -> str:
    """A fraction with a terminating ``places``-digit expansion, as that expansion."""
    scaled = value * 10**places
    if scaled.denominator != 1:
        message = f"{value} has no {places}-place decimal expansion"
        raise PoseError(message)
    digits = str(abs(scaled.numerator)).rjust(places + 1, "0")
    sign = "-" if scaled.numerator < 0 else ""
    if places == 0:
        return f"{sign}{digits}"
    return f"{sign}{digits[:-places]}.{digits[-places:]}"


# --------------------------------------------------------------------------- arithmetic


@contextmanager
def working_precision(digits: int) -> Iterator[None]:
    """Interval and float contexts at ``digits`` decimal digits, restored afterwards."""
    if digits < MIN_DIGITS:
        message = f"at least {MIN_DIGITS} working digits are needed, not {digits}"
        raise PoseError(message)
    previous = mp.iv.dps, mp.mp.dps
    mp.iv.dps = mp.mp.dps = digits
    try:
        yield
    finally:
        mp.iv.dps, mp.mp.dps = previous


def enclose(value: Fraction) -> Interval:
    """An outward-rounded enclosure of an exact rational."""
    numerator: Interval = interval(str(value.numerator))
    if value.denominator == 1:
        return numerator
    return numerator / interval(str(value.denominator))


def _maximum(values: Sequence[Interval]) -> Interval:
    """An enclosure of the largest of several values, deciding no order between them."""
    return from_endpoints(
        max(mp.mpf(value.a) for value in values), max(mp.mpf(value.b) for value in values)
    )


def _low(value: Interval) -> Any:
    return mp.mpf(value.a)


def _high(value: Interval) -> Any:
    return mp.mpf(value.b)


def _rendered(value: Interval) -> list[str]:
    return [
        decimal_string(_low(value), RENDER_DIGITS, upward=False),
        decimal_string(_high(value), RENDER_DIGITS, upward=True),
    ]


@dataclass(frozen=True)
class _Basis:
    cosine: Interval
    sine: Interval
    half_extent: Interval


def _bases(squares: Sequence[Pose]) -> list[_Basis]:
    bases: list[_Basis] = []
    for square in squares:
        degrees = enclose(square.degrees)
        cosine, sine = cos_degrees(degrees), sin_degrees(degrees)
        bases.append(_Basis(cosine, sine, (abs(cosine) + abs(sine)) / 2))
    return bases


def near_pairs(squares: Sequence[Pose]) -> list[tuple[int, int]]:
    """Index pairs whose centres are at most 2 apart, decided exactly on the centres.

    Buckets of side 2.5 on float centres only propose candidates: a pair within 2 lies
    in adjacent buckets even after rounding to floats, and the exact test decides.
    """
    cell = 2.5
    buckets: defaultdict[tuple[int, int], list[int]] = defaultdict(list)
    for index, square in enumerate(squares):
        buckets[math.floor(float(square.x) / cell), math.floor(float(square.y) / cell)].append(
            index
        )
    pairs: list[tuple[int, int]] = []
    for index, square in enumerate(squares):
        column = math.floor(float(square.x) / cell)
        row = math.floor(float(square.y) / cell)
        for other_column in (column - 1, column, column + 1):
            for other_row in (row - 1, row, row + 1):
                for other in buckets.get((other_column, other_row), []):
                    if other <= index:
                        continue
                    dx, dy = squares[other].x - square.x, squares[other].y - square.y
                    if dx * dx + dy * dy <= NEAR * NEAR:
                        pairs.append((index, other))
    return sorted(pairs)


def pair_separation(
    first: Pose, second: Pose, first_basis: _Basis, second_basis: _Basis, dilation: Fraction
) -> Interval:
    """The best separating-axis gap of two squares, centres dilated by ``dilation``."""
    dx = enclose(dilation * (second.x - first.x))
    dy = enclose(dilation * (second.y - first.y))
    projections = [
        abs(basis.cosine * dx + basis.sine * dy) for basis in (first_basis, second_basis)
    ] + [abs(basis.cosine * dy - basis.sine * dx) for basis in (first_basis, second_basis)]
    along = first_basis.cosine * second_basis.cosine + first_basis.sine * second_basis.sine
    across = first_basis.sine * second_basis.cosine - first_basis.cosine * second_basis.sine
    half_width = (abs(along) + abs(across)) / 2
    return _maximum(projections) - interval("0.5") - half_width


def wall_clearance(square: Pose, basis: _Basis, side: Fraction, dilation: Fraction) -> Interval:
    """The least clearance of the square's corners from the centred box of ``side``."""
    reach = max(abs(dilation * square.x), abs(dilation * square.y))
    return enclose(side / 2 - reach) - basis.half_extent


def _proved_nonnegative(value: Interval) -> bool:
    return _low(value) >= 0


def _proved_negative(value: Interval) -> bool:
    return _high(value) < 0


def measurement(
    pose: PoseFile, bases: Sequence[_Basis], pairs: Sequence[tuple[int, int]], side: Fraction
) -> dict[str, Any]:
    """Every wall and near pair of the pose at ``side``, centres scaled by ``side / s``."""
    dilation = side / pose.side
    squares = pose.squares
    walls = [
        (wall_clearance(square, basis, side, dilation), square.label)
        for square, basis in zip(squares, bases, strict=True)
    ]
    gaps = [
        (
            pair_separation(squares[i], squares[j], bases[i], bases[j], dilation),
            squares[i].label,
            squares[j].label,
        )
        for i, j in pairs
    ]
    least_wall = min(walls, key=lambda item: _low(item[0]))
    outside = sorted(
        (item for item in walls if _proved_negative(item[0])), key=lambda w: _low(w[0])
    )
    overlapping = sorted(
        (item for item in gaps if _proved_negative(item[0])), key=lambda g: _low(g[0])
    )
    undecided_walls = sum(
        1
        for value, _ in walls
        if not _proved_nonnegative(value) and not _proved_negative(value)
    )
    undecided_pairs = sum(
        1
        for value, _, _ in gaps
        if not _proved_nonnegative(value) and not _proved_negative(value)
    )
    touching = sum(1 for value, _, _ in gaps if _low(value) == 0 and _high(value) == 0)
    if outside or overlapping:
        verdict = "not-a-packing"
    elif undecided_walls or undecided_pairs:
        verdict = "undecided"
    else:
        verdict = "packing"
    result: dict[str, Any] = {
        "side": str(side),
        "verdict": verdict,
        "least_wall_clearance": _rendered(least_wall[0]),
        "least_wall_square": least_wall[1],
        "walls_outside": len(outside),
        "walls_undecided": undecided_walls,
        "worst_walls": [
            {"square": label, "clearance": _rendered(value)}
            for value, label in outside[:LISTED]
        ],
        "pairs_overlapping": len(overlapping),
        "pairs_undecided": undecided_pairs,
        "pairs_touching": touching,
        "deepest_overlaps": [
            {"squares": [first, second], "separation": _rendered(value)}
            for value, first, second in overlapping[:LISTED]
        ],
    }
    if gaps:
        least_gap = min(gaps, key=lambda item: _low(item[0]))
        result["least_pair_separation"] = _rendered(least_gap[0])
        result["least_pair"] = [least_gap[1], least_gap[2]]
    return result


# --------------------------------------------------------------------------- files


def _relative(root: Path, name: str) -> Path:
    relative = PurePosixPath(name)
    if relative.is_absolute() or ".." in relative.parts or relative.as_posix() != name:
        message = f"not a plain path under the root: {name}"
        raise PoseError(message)
    path = root / name
    if not path.is_file() or path.is_symlink():
        message = f"not a regular file under the root: {name}"
        raise PoseError(message)
    return path


def target_side(pose: PoseFile, places: int | None, explicit: str | None) -> Fraction:
    """The declared target: the printed side rounded up at ``places``, or ``explicit``."""
    if (places is None) == (explicit is None):
        message = "declare exactly one of a ceiling's places and an explicit target side"
        raise PoseError(message)
    target = ceiling(pose.side, places) if places is not None else Fraction(str(explicit))
    if target < pose.side:
        message = f"the target {target} is below the printed side {pose.side_text}"
        raise PoseError(message)
    return target


def measure_file(
    root: Path, name: str, *, digits: int, places: int | None, explicit: str | None
) -> dict[str, Any]:
    """One receipt row: the file's identity and its measurement at both sides."""
    data = _relative(root, name).read_bytes()
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as error:
        message = f"{name} is not UTF-8 text"
        raise PoseError(message) from error
    pose = parse_pose(text)
    target = target_side(pose, places, explicit)
    with working_precision(digits):
        bases = _bases(pose.squares)
        pairs = near_pairs(pose.squares)
        printed = measurement(pose, bases, pairs, pose.side)
        declared = measurement(pose, bases, pairs, target)
        dilation = target / pose.side
        excess = decimal_string(_high(enclose(dilation - 1)), RENDER_DIGITS, upward=True)
    return {
        "path": name,
        "sha256": hashlib.sha256(data).hexdigest(),
        "bytes": len(data),
        "n": len(pose.squares),
        "printed_side": pose.side_text,
        "target_side": decimal_text(target, places) if places is not None else str(explicit),
        "dilation": str(dilation),
        "dilation_minus_one": excess,
        "near_pairs": len(pairs),
        "at_printed_side": printed,
        "at_target_side": declared,
    }


def measure(
    root: Path,
    names: Sequence[str],
    *,
    digits: int = DEFAULT_DIGITS,
    places: int | None = None,
    explicit: str | None = None,
    source: str = "",
) -> dict[str, Any]:
    """A receipt over ``names``, read under ``root``, at one declared target rule."""
    if explicit is not None and len(names) != 1:
        message = "an explicit target side applies to one file"
        raise PoseError(message)
    rule: dict[str, Any] = (
        {"rule": "ceiling", "places": places}
        if places is not None
        else {"rule": "explicit", "side": explicit}
    )
    return {
        "format": FORMAT,
        "source": source,
        "working_digits": digits,
        "target": rule,
        "files": [
            measure_file(root, name, digits=digits, places=places, explicit=explicit)
            for name in names
        ],
    }


def check(receipt: dict[str, Any], root: Path) -> list[str]:
    """Every way a fresh measurement under ``root`` differs from ``receipt``."""
    if receipt.get("format") != FORMAT:
        return [f"the receipt's format is not {FORMAT}"]
    rule = receipt["target"]
    places = rule.get("places") if rule.get("rule") == "ceiling" else None
    explicit = rule.get("side") if rule.get("rule") == "explicit" else None
    problems: list[str] = []
    for row in receipt["files"]:
        name = row["path"]
        try:
            data = _relative(root, name).read_bytes()
        except PoseError as error:
            problems.append(str(error))
            continue
        if hashlib.sha256(data).hexdigest() != row["sha256"] or len(data) != row["bytes"]:
            problems.append(f"{name}: the bytes are not the measured file's")
            continue
        fresh = measure_file(
            root, name, digits=receipt["working_digits"], places=places, explicit=explicit
        )
        problems.extend(
            f"{name}: {key} is {row.get(key)!r} in the receipt and {value!r} measured"
            for key, value in fresh.items()
            if row.get(key) != value
        )
        problems.extend(
            f"{name}: the receipt has an unknown field {key}"
            for key in row.keys() - fresh.keys()
        )
    return problems


# --------------------------------------------------------------------------- command


def _summary(row: dict[str, Any]) -> str:
    printed, declared = row["at_printed_side"], row["at_target_side"]
    least = printed.get("least_pair_separation", ["-", "-"])
    return (
        f"n={row['n']:>4} s={row['printed_side']} T={row['target_side']} "
        f"lambda-1<={row['dilation_minus_one']}: at s {printed['verdict']} "
        f"(pair >= {least[0]}, wall >= {printed['least_wall_clearance'][0]}, "
        f"{printed['pairs_overlapping']} overlapping, {printed['walls_outside']} outside); "
        f"at T {declared['verdict']}"
    )


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        allow_abbrev=False,
    )
    commands = parser.add_subparsers(dest="command", required=True)
    run = commands.add_parser("measure", help="measure pose files and write a receipt")
    run.add_argument("files", nargs="+", help="pose files, as paths under --root")
    run.add_argument("--root", type=Path, required=True, help="directory the files are under")
    target = run.add_mutually_exclusive_group(required=True)
    target.add_argument("--target-places", type=int, help="target: printed side rounded up")
    target.add_argument("--target", help="target: an explicit side, for one file")
    run.add_argument("--digits", type=int, default=DEFAULT_DIGITS, help="working digits")
    run.add_argument("--source", default="", help="what the root is, recorded verbatim")
    run.add_argument("--output", type=Path, help="write the receipt here as JSON")
    admit = commands.add_parser("check", help="re-measure a receipt's files and compare")
    admit.add_argument("receipt", type=Path, help="a receipt written by measure")
    admit.add_argument("--root", type=Path, required=True, help="directory the files are under")
    args = parser.parse_args(argv)
    try:
        if args.command == "measure":
            receipt = measure(
                args.root,
                args.files,
                digits=args.digits,
                places=args.target_places,
                explicit=args.target,
                source=args.source,
            )
            for row in receipt["files"]:
                print(_summary(row))
            if args.output is not None:
                atomic_write_text(args.output, retained_json.dumps(receipt), encoding="utf-8")
            return 0
        problems = check(json.loads(args.receipt.read_text(encoding="utf-8")), args.root)
    except PoseError as error:
        print(f"REFUSED: {error}", file=sys.stderr)
        return 2
    for problem in problems:
        print(problem, file=sys.stderr)
    print("RECEIPT_DIFFERS_FROM_A_FRESH_MEASUREMENT" if problems else "RECEIPT_REPRODUCED")
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
