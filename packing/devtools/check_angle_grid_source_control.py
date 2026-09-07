"""Independent rectangle-corner replay of the original theta-zero ten-point cover.

This reader imports neither the tile producer nor its membership/mesh routines.
It shares only exact NumberField arithmetic and generic file-I/O foundations.
For each of all 18 closed rectangles, four world-coordinate corners satisfy
the assigned point's four closed axis inequalities. Affinity and convexity then
cover that entire rectangle; the fixed 6-by-3 grid covers the whole center box.
This proves only the original source's axis-ten-cover clause, never H-036/H-102
or a nonzero angle interval. Original source construction requires explicit CLI
dispatch; tests use only toys or a mocked source constructor.
"""

from __future__ import annotations

import argparse
import json
import signal
import sys
import time
from collections.abc import Sequence
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

from devtools.check_full_size_density_support_ceiling import load_packet
from sqpack.cover import write_text_atomic
from sqpack.field import FieldElement, NumberField

type Point = tuple[FieldElement, FieldElement]
type Assignment = tuple[tuple[int, ...], ...]
type Failure = tuple[int, int, int, int]

COLUMNS = 6
ROWS = 3
POINT_CAP = 10
HALF = Fraction(1, 2)
PRODUCER_INEQUALITIES = ROWS * COLUMNS * 2 * 3 * 4
PACKET_KEYS = {
    "version",
    "kind",
    "grid",
    "angle_slab",
    "assignments",
    "status",
    "inequalities_checked",
    "unresolved",
}
SCOPE = "original Theorem 3 axis-ten-cover at theta=0 only"
PACKET_BYTE_CAP = 262144
WALL_CAP_SECONDS = 10


@dataclass(frozen=True)
class GridResult:
    corners_checked: int
    inequalities_checked: int
    failures: tuple[Failure, ...]

    @property
    def proved(self) -> bool:
        return not self.failures


def _assignment(value: Any, point_count: int) -> Assignment:
    if type(value) not in (tuple, list) or len(value) != ROWS:
        raise ValueError("assignments require exactly three rows")
    result = []
    for row in value:
        if type(row) not in (tuple, list) or len(row) != COLUMNS:
            raise ValueError("each assignment row requires exactly six labels")
        if any(type(label) is not int or not 0 <= label < point_count for label in row):
            raise ValueError("assignment contains an invalid point label")
        result.append(tuple(row))
    return tuple(result)


def original_source() -> tuple[FieldElement, tuple[Point, ...]]:
    """Rebuild paper Theorem 3's four seeds and coordinate reflections directly.

    Original source: Stromquist, paper pages 10--11; the retained transcription
    and source-control assessment name these formulas. No fixed-side target or
    repaired Theorem 2 coordinates enter this constructor.
    """
    field = NumberField((1, 0, -2), ("1", "2"))
    side = 2 + Fraction(4, 3) * field.alpha
    one = field.one
    seeds = (
        (one, one),
        (side / 2, one),
        (Fraction(3, 2) - side / 4, side / 2),
        (HALF + side / 4, side / 2),
    )
    points = {
        (side - x if reflect_x else x, side - y if reflect_y else y)
        for x, y in seeds
        for reflect_x in (False, True)
        for reflect_y in (False, True)
    }
    if len(points) != POINT_CAP:
        raise ValueError("original source did not reconstruct ten distinct points")
    # FieldElement ordering compares real values, not polynomial coefficient tuples.
    return side, tuple(sorted(points))


def check_rectangles(
    side: FieldElement, points: Sequence[Point], assignments: object
) -> GridResult:
    """Check every closed rectangle corner by direct theta-zero coordinate bounds."""
    if not isinstance(side, FieldElement) or side <= 1:
        raise ValueError("source replay needs a positive-width exact center box")
    if not 1 <= len(points) <= POINT_CAP:
        raise ValueError("point inventory must be nonempty and bounded")
    for point in points:
        if len(point) != 2 or any(
            not isinstance(coordinate, FieldElement) or coordinate.field is not side.field
            for coordinate in point
        ):
            raise ValueError("point coordinates must share the side's exact field")
        if any(not 0 <= coordinate <= side for coordinate in point):
            raise ValueError("marked point is outside the container")
    if len(set(points)) != len(points) or tuple(sorted(points)) != tuple(points):
        raise ValueError("points must be distinct and in real lexicographic order")
    labels = _assignment(assignments, len(points))
    failures: list[Failure] = []
    corners = checked = 0
    width = side - 1
    for row in range(ROWS):
        for column in range(COLUMNS):
            px, py = points[labels[row][column]]
            for corner, (ix, iy) in enumerate(((0, 0), (1, 0), (1, 1), (0, 1))):
                cx = HALF + width * Fraction(column + ix, COLUMNS)
                cy = HALF + width * Fraction(row + iy, ROWS)
                dx, dy = px - cx, py - cy
                corners += 1
                for axis, margin in enumerate((HALF - dx, HALF + dx, HALF - dy, HALF + dy)):
                    checked += 1
                    if margin.sign() < 0:
                        failures.append((row, column, corner, axis))
    return GridResult(corners, checked, tuple(failures))


def validate_packet(packet: Any) -> Assignment:
    """Validate the exact fixed-grid envelope, including a stopped producer prefix."""
    if type(packet) is not dict or set(packet) != PACKET_KEYS:
        raise ValueError("proof packet has missing or unexpected keys")
    if type(packet["version"]) is not int or packet["version"] != 1:
        raise ValueError("unsupported proof packet version")
    if packet["kind"] != "original-source-axis-ten-cover-grid":
        raise ValueError("proof packet is not the fixed original-source clause")
    if (
        type(packet["grid"]) is not list
        or packet["grid"] != [COLUMNS, ROWS]
        or any(type(value) is not int for value in packet["grid"])
        or type(packet["angle_slab"]) is not list
        or packet["angle_slab"] != ["0", "0"]
    ):
        raise ValueError("proof packet changes the grid or singleton angle slab")
    if type(packet["assignments"]) is not list or any(
        type(row) is not list for row in packet["assignments"]
    ):
        raise ValueError("proof assignments must be JSON row arrays")
    labels = _assignment(packet["assignments"], POINT_CAP)
    status = packet["status"]
    count = packet["inequalities_checked"]
    if status not in ("proved", "unresolved") or (
        type(count) is not int or not 0 <= count <= PRODUCER_INEQUALITIES
    ):
        raise ValueError("invalid producer status or completed-prefix count")
    failures = packet["unresolved"]
    if type(failures) is not list or len(failures) > count:
        raise ValueError("invalid unresolved-inequality inventory")
    last = -1
    for failure in failures:
        if (
            type(failure) is not list
            or len(failure) != 5
            or any(
                type(value) is not int or not 0 <= value < limit
                for value, limit in zip(failure, (ROWS, COLUMNS, 2, 3, 4), strict=True)
            )
        ):
            raise ValueError("invalid unresolved inequality coordinates")
        row, column, triangle, vertex, axis = failure
        ordinal = ((((row * COLUMNS + column) * 2 + triangle) * 3 + vertex) * 4) + axis
        if not last < ordinal < count:
            raise ValueError("unresolved entries must be unique ordered members of the prefix")
        last = ordinal
    complete_pass = count == PRODUCER_INEQUALITIES and not failures
    if (status == "proved") != complete_pass:
        raise ValueError("producer status contradicts its completed-prefix evidence")
    return labels


def check_packet(packet: Any) -> dict[str, Any]:
    """Rebuild source and all rectangles only after admission of a complete proof."""
    labels = validate_packet(packet)
    if packet["status"] != "proved":
        return {
            "decision": "unresolved",
            "reason": "producer did not complete its assigned-grid proof",
            "scope": SCOPE,
            "h036_outcome": "unresolved",
            "h102_outcome": "unresolved",
        }
    side, points = original_source()
    result = check_rectangles(side, points, labels)
    if not result.proved:
        raise ValueError(
            f"assigned cover failed direct rectangle-corner replay: {result.failures}"
        )
    return {
        "decision": "proved",
        "scope": SCOPE,
        "rectangles_checked": ROWS * COLUMNS,
        "corners_checked": result.corners_checked,
        "inequalities_checked": result.inequalities_checked,
        "producer_inequalities_checked": packet["inequalities_checked"],
        "h036_outcome": "unresolved",
        "h102_outcome": "unresolved",
    }


def _expired(_signal: int, _frame: Any) -> None:
    raise TimeoutError("source-grid replay reached its fixed ten-second wall cap")


def main(argv: Sequence[str] | None = None) -> int:
    """Fixed source-only replay; publish each requested output atomically.

    Explicit output paths permit replacement. No crash durability or transaction
    across receipt/log files is promised; a publication failure exits nonzero.
    The alarm covers input parsing, source construction, and exact verification.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("packet", type=Path)
    parser.add_argument("--source-control", action="store_true", required=True)
    parser.add_argument("--output", type=Path, help="atomically replace this replay receipt")
    parser.add_argument("--log", type=Path, help="atomically replace this cost/exit log")
    args = parser.parse_args(argv)
    paths = [
        path.resolve() for path in (args.packet, args.output, args.log) if path is not None
    ]
    if len(set(paths)) != len(paths):
        parser.error("input, receipt, and log paths must differ")
    started, cpu_started = time.monotonic(), time.process_time()
    previous = signal.signal(signal.SIGALRM, _expired)
    signal.alarm(WALL_CAP_SECONDS)
    try:
        packet = load_packet(args.packet, max_bytes=PACKET_BYTE_CAP)
        result = check_packet(packet)
        code = 0 if result["decision"] == "proved" else 1
    except TimeoutError as error:
        result = {
            "decision": "unresolved",
            "scope": SCOPE,
            "reason": str(error),
            "h036_outcome": "unresolved",
            "h102_outcome": "unresolved",
        }
        code = 1
    except (OSError, ValueError, TypeError, KeyError, RecursionError) as error:
        result = {
            "decision": "refused",
            "scope": SCOPE,
            "reason": str(error),
            "h036_outcome": "unresolved",
            "h102_outcome": "unresolved",
        }
        code = 2
    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, previous)
    log = {
        "input": str(args.packet),
        "exit_code": code,
        "wall_cap_seconds": WALL_CAP_SECONDS,
        "wall_seconds": time.monotonic() - started,
        "cpu_seconds": time.process_time() - cpu_started,
    }
    try:
        if args.output is not None:
            write_text_atomic(args.output, json.dumps(result, indent=2, sort_keys=True) + "\n")
        if args.log is not None:
            write_text_atomic(args.log, json.dumps(log, indent=2, sort_keys=True) + "\n")
    except OSError as error:
        print(f"replay output publication failed: {error}", file=sys.stderr)
        return 2
    print(json.dumps(result, sort_keys=True))
    return code


if __name__ == "__main__":
    raise SystemExit(main())
