#!/usr/bin/env python3
"""Independent exact checker for rational-corner Witness/v2 files.

This intentionally shares no geometry or verification code with ``sqpack.witness`` or
``sqpack.verify``. It exists because a promotion generator accepting its own output
would not catch a shared sign, axis, or corner-order defect.
"""

from __future__ import annotations

import argparse
import itertools
from fractions import Fraction
from pathlib import Path
from typing import Any

from sqpack.yamlio import safe_load

Point = tuple[Fraction, Fraction]
Square = list[Point]


def parse(path: Path) -> tuple[list[Square], Fraction]:
    document = safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(document, dict) or not isinstance(document.get("witness"), dict):
        raise TypeError("expected a Witness/v2 envelope")
    witness: dict[str, Any] = document["witness"]
    if witness.get("representation") != "corners" or witness.get("scalar") != {
        "kind": "rational"
    }:
        raise ValueError("independent checker accepts rational corner witnesses only")
    raw_squares = witness.get("squares")
    if not isinstance(raw_squares, list) or len(raw_squares) != witness.get("n"):
        raise ValueError("declared n does not match the complete square list")
    ids = [square.get("id") for square in raw_squares]
    if len(ids) != len(set(ids)):
        raise ValueError("square ids are not unique")
    squares = [
        [(Fraction(point[0]), Fraction(point[1])) for point in square["corners"]]
        for square in raw_squares
    ]
    if any(len(square) != 4 for square in squares):
        raise ValueError("every square must have four corners")
    return squares, Fraction(witness["side"])


def dot(left: Point, right: Point) -> Fraction:
    return left[0] * right[0] + left[1] * right[1]


def subtract(left: Point, right: Point) -> Point:
    return left[0] - right[0], left[1] - right[1]


def square_failures(square: Square, index: int) -> list[str]:
    failures: list[str] = []
    edges = [subtract(square[(corner + 1) % 4], square[corner]) for corner in range(4)]
    for edge_index, edge in enumerate(edges):
        if dot(edge, edge) != 1:
            failures.append(f"square {index} edge {edge_index} is not unit length")
        if dot(edge, edges[(edge_index + 1) % 4]) != 0:
            failures.append(
                f"square {index} edges {edge_index}/{(edge_index + 1) % 4} not orthogonal"
            )
    if edges[0] != (-edges[2][0], -edges[2][1]) or edges[1] != (
        -edges[3][0],
        -edges[3][1],
    ):
        failures.append(f"square {index} corner order does not close a parallelogram")
    return failures


def axes(square: Square) -> tuple[Point, Point]:
    first = subtract(square[1], square[0])
    second = subtract(square[2], square[1])
    return (-first[1], first[0]), (-second[1], second[0])


def interval(square: Square, axis: Point) -> tuple[Fraction, Fraction]:
    values = [dot(point, axis) for point in square]
    return min(values), max(values)


def pair_gap(left: Square, right: Square) -> Fraction:
    gaps: list[Fraction] = []
    for axis in (*axes(left), *axes(right)):
        left_min, left_max = interval(left, axis)
        right_min, right_max = interval(right, axis)
        gaps.extend((right_min - left_max, left_min - right_max))
    return max(gaps)


def check(path: Path) -> dict[str, Any]:
    squares, side = parse(path)
    failures = [
        failure
        for index, square in enumerate(squares, start=1)
        for failure in square_failures(square, index)
    ]
    containment = [
        clearance
        for square in squares
        for x, y in square
        for clearance in (x, y, side - x, side - y)
    ]
    if min(containment) < 0:
        failures.append(f"container penetration {min(containment)}")
    pair_gaps = [
        pair_gap(squares[left], squares[right])
        for left, right in itertools.combinations(range(len(squares)), 2)
    ]
    overlaps = [gap for gap in pair_gaps if gap < 0]
    if overlaps:
        failures.append(f"{len(overlaps)} overlapping pairs; worst exact gap {min(overlaps)}")
    return {
        "verification_passed": not failures,
        "coordinate_provenance": "verified" if not failures else "not-established",
        "method": "exact-algebraic",
        "field": "Q",
        "n": len(squares),
        "side": str(side),
        "pairs_tested": len(pair_gaps),
        "minimum_containment_clearance": str(min(containment)),
        "minimum_best_pair_gap": str(min(pair_gaps)) if pair_gaps else str(side),
        "failures": failures,
        "limitations": "Verifies witness feasibility and its upper bound, not optimality.",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("witness", type=Path)
    args = parser.parse_args()
    result = check(args.witness)
    print(
        ("VERIFIED" if result["verification_passed"] else "VERIFICATION FAILED")
        + f": {result['n']} squares, {result['pairs_tested']} pairs"
    )
    print(f"  exact side: {result['side']}")
    print(f"  minimum pair gap: {result['minimum_best_pair_gap']}")
    for failure in result["failures"]:
        print(f"  FAILURE: {failure}")
    return 0 if result["verification_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
