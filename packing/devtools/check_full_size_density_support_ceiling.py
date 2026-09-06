"""Solver-independent BC-254 replay using oriented edge determinants.

The file checker reconstructs the named source instead of trusting a serialized support
or incidence matrix. It checks finite-row certificates, never global depth feasibility.
"""

from __future__ import annotations

import argparse
import json
import os
import signal
import stat
import sys
from collections.abc import Sequence
from fractions import Fraction
from pathlib import Path
from typing import Any

from cases.trump11.packing import U_INTERVAL, U_MIN_POLY, build
from sqpack.field import FieldElement, NumberField
from sqpack.full_size_density.support_ceiling import (
    NecessaryRow,
    Square,
    Support,
    SupportError,
    axis_square,
    check_upper,
    checked_rational,
)
from sqpack.full_size_density.support_screen import extend_rows, initial_rows, primal_value
from sqpack.verify import exact_sign, verify_packing

PACKET_BYTES = 2 * 1024 * 1024


def load_source(source: str) -> tuple[tuple[Square, ...], FieldElement]:
    """Load a fixed construction; importing this module never constructs the target."""
    if source == "trump11-v1":
        squares, side, _ = build()
        return tuple(tuple(square) for square in squares), side
    if source == "toy-rational-v1":
        field = NumberField((1, 0), ("-1", "1"))
        x = field.rational("3/4")
    elif source == "toy-algebraic-v1":
        field = NumberField(U_MIN_POLY, U_INTERVAL)
        x = field.rational("3/4") + field.alpha / 100
    else:
        raise SupportError("unknown frozen source identifier")
    return (axis_square(x, field.rational("3/4")),), field.rational(2)


def _key(square: Square):
    return tuple(sorted((tuple(x.coeffs), tuple(y.coeffs)) for x, y in square))


def _direct_images(seed: Square, side: FieldElement) -> tuple[Square, ...]:
    # Explicit coordinate maps are separate from the producer's iterative rotations.
    transforms = (
        lambda x, y: (x, y),
        lambda x, y: (side - y, x),
        lambda x, y: (side - x, side - y),
        lambda x, y: (y, side - x),
        lambda x, y: (side - x, y),
        lambda x, y: (side - y, side - x),
        lambda x, y: (x, side - y),
        lambda x, y: (y, x),
    )
    return tuple(tuple(transform(x, y) for x, y in seed) for transform in transforms)


def _orbit(seed: Square, side: FieldElement):
    return {_key(square) for square in _direct_images(seed, side)}


def replay_upper(
    seeds: Sequence[Square],
    support: Support,
    rows: Sequence[NecessaryRow],
    multipliers: Sequence[object],
) -> Fraction:
    """Regenerate support identity, strict neighborhoods, and the upper inequality."""
    side = support.side
    if side != 2:
        raise SupportError("target-disabled: replay is commissioned only for side-two toys")
    return _replay_upper(seeds, support, rows, multipliers)


def _replay_upper(
    seeds: Sequence[Square],
    support: Support,
    rows: Sequence[NecessaryRow],
    multipliers: Sequence[object],
) -> Fraction:
    side = support.side
    expected = sorted(
        {_key_orbit for seed in seeds for _key_orbit in (tuple(sorted(_orbit(seed, side))),)}
    )
    actual = [tuple(_key(square) for square in orbit) for orbit in support.orbits]
    if actual != expected:
        raise SupportError("support or orbit multiplicities disagree with declared source")
    if not expected:
        raise SupportError("empty source support")
    matrix: list[tuple[int, ...]] = []
    for row in rows:
        if any(type(value) is not int for value in row.coefficients):
            raise SupportError("incidence coefficients require exact integers")
        radius = checked_rational(row.radius)
        if radius <= 0:
            raise SupportError("neighborhood radius must be positive")
        px, py = row.point
        margins = [px, side - px, py, side - py]
        if any((value - 2 * radius).sign() <= 0 for value in margins):
            raise SupportError("neighborhood crosses the container boundary")
        counts: list[int] = []
        for orbit in support.orbits:
            count = 0
            for square in orbit:
                if len(square) != 4:
                    raise SupportError("square has wrong corner count")
                edges = []
                for index, (x, y) in enumerate(square):
                    if x.field is not side.field or y.field is not side.field:
                        raise SupportError("geometry field mismatch")
                    if any(value.sign() < 0 or (side - value).sign() < 0 for value in (x, y)):
                        raise SupportError("square fails containment")
                    nx, ny = square[(index + 1) % 4]
                    dx, dy = nx - x, ny - y
                    if dx * dx + dy * dy != 1:
                        raise SupportError("square edge is not unit length")
                    edges.append((dx, dy))
                ex, ey = edges[0]
                fx, fy = edges[1]
                if (
                    not (ex * fx + ey * fy).is_zero()
                    or edges[2] != (-ex, -ey)
                    or edges[3] != (-fx, -fy)
                ):
                    raise SupportError("corners are not a cyclic unit square")
                orientation = (ex * fy - ey * fx).sign()
                if orientation == 0:
                    raise SupportError("degenerate square")
                signs = []
                for (x, y), (dx, dy) in zip(square, edges, strict=True):
                    value = orientation * (dx * (py - y) - dy * (px - x))
                    sign = value.sign()
                    absolute = value if sign > 0 else -value
                    if sign == 0 or (absolute - 2 * radius).sign() <= 0:
                        raise SupportError("boundary or uncertified neighborhood")
                    signs.append(sign)
                count += int(all(sign > 0 for sign in signs))
            counts.append(count)
        if tuple(counts) != row.coefficients:
            raise SupportError("claimed incidence disagrees with determinant replay")
        matrix.append(tuple(counts))
    return check_upper(matrix, support.sizes, multipliers)


def reconstruct_source(source: str) -> tuple[tuple[Square, ...], Support, dict[str, Any]]:
    """Independent direct-map support/preimage enumeration; no producer constructor."""
    seeds, side = load_source(source)
    if not verify_packing(seeds, side, sign=exact_sign).valid:
        raise SupportError("source is not an exact packing")
    placements: dict[Any, Square] = {}
    labels: dict[Any, list[list[int]]] = {}
    for source_index, seed in enumerate(seeds):
        for map_index, square in enumerate(_direct_images(seed, side)):
            key = _key(square)
            placements.setdefault(key, square)
            labels.setdefault(key, []).append([source_index, map_index // 4, map_index % 4])
    orbit_keys = sorted({tuple(sorted(_orbit(seed, side))) for seed in seeds})
    if any(
        not verify_packing((square,), side, sign=exact_sign).valid
        for square in placements.values()
    ):
        raise SupportError(
            "an independently reconstructed image is not a contained unit square"
        )
    support = Support(
        side, tuple(tuple(placements[key] for key in keys) for keys in orbit_keys)
    )
    counts = [sum(_key(seed) in keys for seed in seeds) for keys in orbit_keys]
    weights = [
        Fraction(count, len(keys)) for count, keys in zip(counts, orbit_keys, strict=True)
    ]
    for keys, weight in zip(orbit_keys, weights, strict=True):
        if any(Fraction(len(labels[key]), 8) != weight for key in keys):
            raise SupportError("independent uniform preimage count mismatch")
    if sum(weight * size for weight, size in zip(weights, support.sizes, strict=True)) != len(
        seeds
    ):
        raise SupportError("independent source mass mismatch")

    def encode_key(key):
        return [
            [[str(coefficient) for coefficient in coordinate] for coordinate in corner]
            for corner in key
        ]

    metadata = {
        "side": [str(coefficient) for coefficient in side.coeffs],
        "orbits": [[encode_key(key) for key in keys] for keys in orbit_keys],
        "preimages": [
            {"square": encode_key(key), "labels": labels[key]} for key in sorted(labels)
        ],
        "sizes": list(support.sizes),
        "original_counts": counts,
        "uniform_weights": [str(weight) for weight in weights],
    }
    return seeds, support, metadata


def _keys(value: Any, expected: set[str]) -> dict[str, Any]:
    if type(value) is not dict or set(value) != expected:
        raise SupportError("packet object has missing or unexpected keys")
    return value


def _rational(value: Any) -> Fraction:
    if type(value) is not str or len(value) > 4096:
        raise SupportError("packet rational must be a bounded canonical string")
    result = checked_rational(value)
    if str(result) != value:
        raise SupportError("packet rational is not canonical")
    return result


def _element(value: Any, field: NumberField) -> FieldElement:
    if type(value) is not list or len(value) != field.degree:
        raise SupportError("field element has wrong coefficient count")
    return field.element([_rational(coefficient) for coefficient in value])


def _exact_equal(actual: Any, expected: Any, label: str) -> None:
    # JSON equality distinguishes Boolean true from integer 1; Python dict equality does not.
    if json.dumps(actual, sort_keys=True) != json.dumps(expected, sort_keys=True):
        raise SupportError(f"{label} disagrees with exact source replay")


def replay_packet(packet: Any) -> Fraction:
    """Check a strict, source-bound finite-row upper/optimality packet without solving."""
    data = _keys(
        packet,
        {
            "version",
            "source",
            "support",
            "rows",
            "dispositions",
            "primal",
            "multipliers",
            "bound",
            "solve_pivots",
        },
    )
    if (
        type(data["version"]) is not int
        or data["version"] != 1
        or type(data["source"]) is not str
    ):
        raise SupportError("unsupported packet version or source type")
    seeds, support, metadata = reconstruct_source(data["source"])
    _exact_equal(data["support"], metadata, "support/preimage metadata")
    raw_rows = data["rows"]
    if type(raw_rows) is not list or not 1 <= len(raw_rows) <= 47:
        raise SupportError("packet row cap or shape violated")
    rows = []
    for raw in raw_rows:
        entry = _keys(raw, {"point", "radius", "coefficients"})
        point = entry["point"]
        if type(point) is not list or len(point) != 2:
            raise SupportError("row point requires two exact coordinates")
        coefficients = entry["coefficients"]
        if (
            type(coefficients) is not list
            or len(coefficients) != len(support.sizes)
            or any(type(value) is not int for value in coefficients)
        ):
            raise SupportError("row incidence requires integer orbit counts")
        rows.append(
            NecessaryRow(
                (
                    _element(point[0], support.side.field),
                    _element(point[1], support.side.field),
                ),
                _rational(entry["radius"]),
                tuple(coefficients),
            )
        )
    if type(data["multipliers"]) is not list or type(data["primal"]) is not list:
        raise SupportError("certificate weights require arrays")
    multipliers = tuple(_rational(weight) for weight in data["multipliers"])
    point = tuple(_rational(weight) for weight in data["primal"])
    upper = _replay_upper(seeds, support, rows, multipliers)
    if upper != _rational(data["bound"]):
        raise SupportError("claimed bound differs from upper witness sum")
    baseline = tuple(_rational(weight) for weight in metadata["uniform_weights"])
    if primal_value(rows, support.sizes, baseline) != len(seeds) or upper < len(seeds):
        raise SupportError("finite-row packet contradicts the retained uniform control")
    if primal_value(rows, support.sizes, point) != upper:
        raise SupportError("primal and upper witness values do not agree")
    pivots = data["solve_pivots"]
    if (
        type(pivots) is not list
        or not 1 <= len(pivots) <= 2
        or any(type(value) is not int or not 0 <= value <= 64 for value in pivots)
    ):
        raise SupportError("solve count or pivot cap violated")
    # Regenerate the frozen point protocol, then independently check its geometry above.
    expected_rows, expected_dispositions = initial_rows(support)
    raw_dispositions = data["dispositions"]
    if type(raw_dispositions) is not list:
        raise SupportError("row dispositions must be an array")
    if len(raw_dispositions) != len(expected_dispositions):
        expected_rows, extension = extend_rows(support, expected_rows)
        expected_dispositions += extension
    expected_receipt = [
        {
            "phase": item.phase,
            "source": list(item.source),
            "trial": item.trial,
            "skipped": list(item.skipped),
            "row_index": item.row_index,
        }
        for item in expected_dispositions
    ]
    _exact_equal(raw_dispositions, expected_receipt, "deterministic row dispositions")
    if len(rows) != len(expected_rows) or any(
        row.point != expected.point or row.coefficients != expected.coefficients
        for row, expected in zip(rows, expected_rows, strict=True)
    ):
        raise SupportError("row order differs from the frozen point protocol")
    return upper


def load_packet(path: Path) -> Any:
    """Read one bounded UTF-8 JSON file; refuse links, floats, and duplicate keys."""
    if not stat.S_ISREG(path.lstat().st_mode):
        raise SupportError("certificate path must be a regular file, not a symlink")
    descriptor = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    with os.fdopen(descriptor, "rb") as stream:
        if not stat.S_ISREG(os.fstat(stream.fileno()).st_mode):
            raise SupportError("certificate path changed to a non-regular file")
        payload = stream.read(PACKET_BYTES + 1)
    if len(payload) > PACKET_BYTES:
        raise SupportError("certificate file exceeds the size cap")

    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise SupportError("duplicate JSON object key")
            result[key] = value
        return result

    def refuse_float(value):
        raise SupportError(f"floating or non-finite JSON number is forbidden: {value}")

    try:
        return json.loads(
            payload.decode("utf-8"),
            object_pairs_hook=pairs,
            parse_float=refuse_float,
            parse_constant=refuse_float,
        )
    except (UnicodeError, ValueError, RecursionError) as error:
        raise SupportError(f"malformed certificate JSON: {error}") from error


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("certificate", type=Path)
    parser.add_argument("--timeout-seconds", type=int, default=60)
    args = parser.parse_args(argv)
    if not 1 <= args.timeout_seconds <= 60:
        parser.error("timeout must be an integer from 1 to 60 seconds")

    def expired(_signal, _frame):
        raise TimeoutError("certificate replay reached its process wall cap")

    previous_handler = signal.signal(signal.SIGALRM, expired)
    signal.alarm(args.timeout_seconds)
    try:
        value = replay_packet(load_packet(args.certificate))
    except TimeoutError as error:
        print(f"unresolved: {error}", file=sys.stderr)
        return 1
    except (SupportError, OSError) as error:
        print(f"refused: {error}", file=sys.stderr)
        return 2
    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, previous_handler)
    print(
        json.dumps(
            {
                "finite_row_optimum": str(value),
                "scope": "specified finite support only; no almost-everywhere depth claim",
            }
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
