"""Exact controls for the information lost by removing a square container's walls.

The cyclic examples are axis-parallel unit-square packings on a square flat torus.
They are not packings in an ordinary square container. Two independent predicates
check every pair: wrapped coordinate distances and explicit neighboring translates.

An empty straight seam perpendicular to an axis exists exactly when a cyclic gap
between projected centers is at least one. Between consecutive lifted centers a,b,
the permissible seam interval is [a+1/2,b-1/2], including its endpoints. The final
gap ends at the first center plus the period; a singleton therefore has gap S.
This criterion concerns axis-parallel straight cuts, not arbitrary torus cuts or
unrestricted finite-container bounds.
"""

from __future__ import annotations

import json
from fractions import Fraction
from itertools import combinations, product
from math import isqrt
from typing import TypedDict

type Point = tuple[Fraction, Fraction]


class AxisSeam(TypedDict):
    """An exact projected gap and, when possible, a straight seam coordinate."""

    maximum_cyclic_gap: str
    gap_start: str
    gap_end_unwrapped: str
    exists: bool
    seam_coordinate: str | None
    boundary_candidates_checked: int


class StraightSeams(TypedDict):
    """Both axis tests; a rectangular cut requires one seam in each direction."""

    x: AxisSeam
    y: AxisSeam
    axis_parallel_rectangular_cut_exists: bool


def _validated_inputs(side: object, points: object) -> tuple[Fraction, list[Point]]:
    if not isinstance(side, Fraction):
        raise TypeError("the torus side must be a Fraction")
    if side < 1:
        raise ValueError("the torus side must be at least one")
    if not isinstance(points, list):
        raise TypeError("centers must be a list")
    if not points:
        raise ValueError("the center list must be nonempty")
    checked: list[Point] = []
    for point in points:
        if not isinstance(point, tuple):
            raise TypeError("each center must be a tuple")
        if len(point) != 2:
            raise ValueError("each center must have two coordinates")
        x, y = point
        if not isinstance(x, Fraction) or not isinstance(y, Fraction):
            raise TypeError("center coordinates must be exact Fractions")
        if not (0 <= x < side and 0 <= y < side):
            raise ValueError("center coordinates must lie in the half-open fundamental domain")
        checked.append((x, y))
    return side, checked


def _axis_seam(side: Fraction, coordinates: list[Fraction]) -> AxisSeam:
    coordinates = sorted(coordinates)
    successors = [*coordinates[1:], coordinates[0] + side]
    left, right = max(
        zip(coordinates, successors, strict=True), key=lambda pair: pair[1] - pair[0]
    )
    gap = right - left
    exists = gap >= 1
    seam = ((left + right) / 2) % side if exists else None
    half = Fraction(1, 2)

    def clears(candidate: Fraction) -> bool:
        return all(
            min(abs(center - candidate), side - abs(center - candidate)) >= half
            for center in coordinates
        )

    # Independently enumerate interval boundaries. A nonempty complement of the
    # finitely many open unit arcs contains one of their endpoints, so this
    # cross-check also covers an isolated seam where the maximum gap equals one.
    candidates = {
        (center + direction * half) % side for center in coordinates for direction in (-1, 1)
    }
    clear_boundaries = [candidate for candidate in sorted(candidates) if clears(candidate)]
    if bool(clear_boundaries) != exists:
        raise ArithmeticError("cyclic-gap and projected-boundary seam tests disagree")
    if seam is not None and not clears(seam):
        raise ArithmeticError("the constructed seam enters a square interior")
    return {
        "maximum_cyclic_gap": str(gap),
        "gap_start": str(left),
        "gap_end_unwrapped": str(right),
        "exists": exists,
        "seam_coordinate": str(seam) if seam is not None else None,
        "boundary_candidates_checked": len(candidates),
    }


def straight_seams(side: object, points: object) -> StraightSeams:
    """Decide whether straight x/y seams can avoid all unit-square interiors.

    Require S>=1 as a Fraction and a nonempty list of two-tuples of Fraction
    coordinates in [0,S). Repeated coordinates and even repeated centers are
    allowed: this tests seams, while ``check_witness`` separately checks packing.
    Floats, integer substitutes, empty lists and malformed or out-of-domain
    centers are refused. Boundary contact with a seam is allowed.
    """
    period, centers = _validated_inputs(side, points)
    x = _axis_seam(period, [point[0] for point in centers])
    y = _axis_seam(period, [point[1] for point in centers])
    return {"x": x, "y": y, "axis_parallel_rectangular_cut_exists": x["exists"] and y["exists"]}


def wrapped_disjoint(first: Point, second: Point, side: Fraction) -> bool:
    """Check disjoint interiors of axis-parallel unit squares modulo the period."""
    distances = [abs(a - b) % side for a, b in zip(first, second, strict=True)]
    return any(min(distance, side - distance) >= 1 for distance in distances)


def translated_disjoint(first: Point, second: Point, side: Fraction) -> bool:
    """Check every neighboring lift, with equality allowed at a touching edge."""
    return all(
        abs(first[0] - second[0] - dx * side) >= 1 or abs(first[1] - second[1] - dy * side) >= 1
        for dx, dy in product((-1, 0, 1), repeat=2)
    )


def cyclic_witness(n: int) -> tuple[Fraction, list[Point]]:
    """Return the classical cyclic torus candidate; validity is checked separately."""
    if n < 4:
        raise ValueError("the retained controls require n >= 4")
    m = isqrt(n)
    side = Fraction(n, m)
    return side, [(Fraction(j, m), Fraction(j) % side) for j in range(n)]


def check_witness(side: Fraction, points: list[Point]) -> tuple[int, int]:
    """Return pair count and overlaps, refusing a malformed fundamental-domain list."""
    side, points = _validated_inputs(side, points)
    pairs = 0
    overlaps = 0
    for first, second in combinations(points, 2):
        wrapped = wrapped_disjoint(first, second, side)
        translated = translated_disjoint(first, second, side)
        if wrapped != translated:
            raise ArithmeticError("wrapped-distance and neighboring-lift checks disagree")
        pairs += 1
        overlaps += not wrapped
    return pairs, overlaps


def _seam_controls() -> dict[str, object]:
    origin = (Fraction(0), Fraction(0))
    diagonal = [origin, (Fraction(1), Fraction(1))]
    covered_side, covered_points = cyclic_witness(5)
    controls: list[tuple[str, Fraction, list[Point], Fraction, Fraction | None]] = [
        ("touching_boundary", Fraction(2), diagonal, Fraction(1), Fraction(1, 2)),
        ("wide_wrapped_gap", Fraction(3), diagonal, Fraction(2), Fraction(2)),
        ("covered_axes", covered_side, covered_points, Fraction(1, 2), None),
        (
            "singleton_unit_period",
            Fraction(1),
            [(Fraction(3, 4), Fraction(3, 4))],
            Fraction(1),
            Fraction(1, 4),
        ),
    ]
    passed: list[dict[str, object]] = []
    for name, side, points, expected_gap, expected_seam in controls:
        if check_witness(side, points)[1]:
            raise ArithmeticError("a seam control was not a valid torus packing")
        result = straight_seams(side, points)
        for axis in (result["x"], result["y"]):
            if axis["maximum_cyclic_gap"] != str(expected_gap):
                raise ArithmeticError("a seam control returned the wrong cyclic gap")
            expected = str(expected_seam) if expected_seam is not None else None
            if axis["seam_coordinate"] != expected or axis["exists"] != (
                expected_seam is not None
            ):
                raise ArithmeticError("a seam control returned the wrong seam")
        passed.append({"name": name, "side": str(side), "diagnostic": result})

    # Distinct axis verdicts detect accidentally reusing one projection for both.
    asymmetric = [
        origin,
        (Fraction(3, 2), Fraction(3, 4)),
        (Fraction(0), Fraction(3, 2)),
        (Fraction(3, 2), Fraction(9, 4)),
    ]
    for name, points, expected_gaps, expected_seams in (
        ("only_x_seam", asymmetric, ("3/2", "3/4"), ("3/4", None)),
        ("only_y_seam", [(y, x) for x, y in asymmetric], ("3/4", "3/2"), (None, "3/4")),
    ):
        side = Fraction(3)
        if check_witness(side, points)[1]:
            raise ArithmeticError("an asymmetric seam control was not a valid torus packing")
        result = straight_seams(side, points)
        for axis, expected_gap, expected_seam in zip(
            (result["x"], result["y"]), expected_gaps, expected_seams, strict=True
        ):
            if (
                axis["maximum_cyclic_gap"] != expected_gap
                or axis["seam_coordinate"] != expected_seam
                or axis["exists"] != (expected_seam is not None)
            ):
                raise ArithmeticError("an asymmetric seam control mixed the two axes")
        if result["axis_parallel_rectangular_cut_exists"]:
            raise ArithmeticError("a single-axis seam was accepted as a rectangular cut")
        passed.append({"name": name, "side": str(side), "diagnostic": result})

    malformed: list[tuple[str, object, object]] = [
        ("short_period", Fraction(1, 2), [origin]),
        ("inexact_period", 2.0, [origin]),
        ("integer_period", 2, [origin]),
        ("empty_centers", Fraction(2), []),
        ("tuple_instead_of_list", Fraction(2), (origin,)),
        ("list_instead_of_point_tuple", Fraction(2), [list(origin)]),
        ("short_point", Fraction(2), [(Fraction(0),)]),
        ("missing_point", Fraction(2), [None]),
        ("negative_coordinate", Fraction(2), [(Fraction(-1), Fraction(0))]),
        ("coordinate_at_period", Fraction(2), [(Fraction(2), Fraction(0))]),
        ("inexact_coordinate", Fraction(2), [(0.0, Fraction(0))]),
        ("integer_coordinate", Fraction(2), [(0, Fraction(0))]),
    ]
    for name, side, points in malformed:
        try:
            straight_seams(side, points)
        except TypeError, ValueError:
            continue
        raise ArithmeticError(f"malformed seam input was accepted: {name}")
    return {
        "geometric_controls": passed,
        "malformed_inputs_refused": [row[0] for row in malformed],
    }


def audit() -> dict[str, object]:
    """Replay the two counterexamples to a useful wall-free torus lower bound."""
    cases: list[dict[str, object]] = []
    for n in (11, 17):
        side, points = cyclic_witness(n)
        pair_count, overlap_count = check_witness(side, points)
        seams = straight_seams(side, points)
        for axis in (seams["x"], seams["y"]):
            if axis["maximum_cyclic_gap"] != str(Fraction(1, isqrt(n))) or axis["exists"]:
                raise ArithmeticError(
                    "the cyclic control unexpectedly has an empty straight seam"
                )
        if overlap_count:
            raise ArithmeticError("the retained cyclic candidate overlaps")
        # Duplicating a square must fail both deciding predicates, including wrap.
        mutant = points.copy()
        mutant[-1] = mutant[0]
        if check_witness(side, mutant)[1] == 0:
            raise ArithmeticError("the duplicate-square negative control was accepted")
        cases.append(
            {
                "n": n,
                "side": str(side),
                "centres": [[str(x), str(y)] for x, y in points],
                "pairs_checked_by_each_method": pair_count,
                "overlaps": overlap_count,
                "duplicate_square_refused": True,
                "straight_seams": seams,
            }
        )
    origin = (Fraction(0), Fraction(0))
    for point, expected in (
        ((Fraction(1), Fraction(0)), True),
        ((Fraction(3), Fraction(0)), True),
        ((Fraction(7, 2), Fraction(0)), False),
    ):
        if wrapped_disjoint(origin, point, Fraction(4)) != expected:
            raise ArithmeticError("a contact or wrapped-overlap control failed")
        if translated_disjoint(origin, point, Fraction(4)) != expected:
            raise ArithmeticError("a lifted contact or overlap control failed")
    return {
        "schema": "fibonacci-torus-periodic-audit/v1",
        "arithmetic": "fractions.Fraction; exact rational",
        "scope": "square flat torus; axis-parallel unit squares; boundary contact allowed",
        "cases": cases,
        "contact_and_wrap_controls_passed": True,
        "seam_criterion": (
            "An empty straight seam exists iff the maximum cyclic projected-center gap "
            "is at least one."
        ),
        "seam_inputs": (
            "Fraction side >= 1; nonempty list of two-tuples of Fraction coordinates "
            "in [0,side); repeated coordinates allowed."
        ),
        "seam_controls": _seam_controls(),
        "finite_container_claim": False,
    }


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2, sort_keys=True))
