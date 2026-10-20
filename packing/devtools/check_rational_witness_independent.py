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
    metadata = document.get("softschema")
    if (
        not isinstance(metadata, dict)
        or metadata.get("contract") != "packing.squares:Witness/v2"
    ):
        raise ValueError("expected the Witness/v2 contract")
    witness: dict[str, Any] = document["witness"]
    if witness.get("representation") != "corners" or witness.get("scalar") != {
        "kind": "rational"
    }:
        raise ValueError("independent checker accepts rational corner witnesses only")
    if witness.get("square_size") != "1":
        raise ValueError("independent checker accepts unit squares only")
    if witness.get("coordinates") != {
        "origin": "lower-left",
        "axes": "x-right-y-up",
        "angle_unit": "not-applicable",
    }:
        raise ValueError("independent checker requires lower-left x-right-y-up coordinates")
    raw_squares = witness.get("squares")
    n = witness.get("n")
    if (
        type(n) is not int
        or n < 1
        or not isinstance(raw_squares, list)
        or len(raw_squares) != n
    ):
        raise ValueError("declared n does not match the complete square list")
    if any(not isinstance(square, dict) for square in raw_squares):
        raise ValueError("every square must be an object")
    ids = [square.get("id") for square in raw_squares]
    if len(ids) != len(set(ids)):
        raise ValueError("square ids are not unique")
    squares: list[Square] = []
    for square in raw_squares:
        points = square.get("corners")
        if not isinstance(points, list) or len(points) != 4:
            raise ValueError("every square must have four corners")
        if any(
            not isinstance(point, list)
            or len(point) != 2
            or any(type(coordinate) is not str for coordinate in point)
            for point in points
        ):
            raise ValueError("every corner must contain two rational strings")
        squares.append([(Fraction(point[0]), Fraction(point[1])) for point in points])
    raw_side = witness.get("side")
    if type(raw_side) is not str:
        raise ValueError("container side must be a rational string")
    return squares, Fraction(raw_side)


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


Projection = tuple[Point, tuple[Fraction, Fraction]]


def own_intervals(square: Square) -> list[Projection]:
    """Each of a square's two edge normals, with the square's own interval on it.

    Half of every pair's projections depend on one square alone, so `check_squares`
    computes them once per square rather than once per pair (think-uomm): over large
    rationals the dot products are nearly all of the decision's cost.
    """
    return [(axis, interval(square, axis)) for axis in axes(square)]


def _separation(
    left: Square, right: Square, left_own: list[Projection], right_own: list[Projection]
) -> Fraction:
    """`pair_gap` from the two squares' `own_intervals`: the same eight gaps, so the
    same exact maximum."""
    gaps: list[Fraction] = []
    for axis, (left_min, left_max) in left_own:
        right_min, right_max = interval(right, axis)
        gaps.extend((right_min - left_max, left_min - right_max))
    for axis, (right_min, right_max) in right_own:
        left_min, left_max = interval(left, axis)
        gaps.extend((right_min - left_max, left_min - right_max))
    return max(gaps)


def pair_gap(left: Square, right: Square) -> Fraction:
    return _separation(left, right, own_intervals(left), own_intervals(right))


def check(path: Path) -> dict[str, Any]:
    squares, side = parse(path)
    return check_squares(squares, side)


def check_squares(squares: list[Square], side: Fraction) -> dict[str, Any]:
    """Decide exact unit squares, given as four rational corners each, in ``[0, side]^2``.

    The geometry `check` applies to a parsed witness, for a caller that holds its squares
    in another exact form and converts them itself: the conversion is then the caller's
    to state, and this decision is still this module's alone.
    """
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
    own = [own_intervals(square) for square in squares]
    pair_gaps = [
        _separation(squares[left], squares[right], own[left], own[right])
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
