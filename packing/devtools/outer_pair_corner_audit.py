"""Exact audit of the outer-pair and selected-corner ownership construction."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, replace
from fractions import Fraction
from itertools import combinations
from typing import Any

type Point = tuple[Fraction, Fraction]
type Polygon = tuple[Point, ...]

GEOMETRY = "rational-unit-square-family/v1"
CONTROL_NAMES = ("overlap", "broken-mark", "changed-target")


class GuardError(ValueError):
    """The input cannot support an exact geometric decision."""


@dataclass(frozen=True, slots=True)
class Square:
    name: str
    vertices: Polygon


@dataclass(frozen=True, slots=True)
class CoreMark:
    mark_id: str
    square: str
    point: Point


@dataclass(frozen=True, slots=True)
class SegmentOwnership:
    segment_id: str
    endpoints: tuple[Point, Point]
    owners: tuple[str, str]


@dataclass(frozen=True, slots=True)
class SquareFamily:
    geometry: str
    q: Fraction
    core_side: Fraction
    squares: tuple[Square, ...]
    core_marks: tuple[CoreMark, ...]
    segment: SegmentOwnership


def add(left: Point, right: Point) -> Point:
    return left[0] + right[0], left[1] + right[1]


def subtract(left: Point, right: Point) -> Point:
    return left[0] - right[0], left[1] - right[1]


def dot(left: Point, right: Point) -> Fraction:
    return left[0] * right[0] + left[1] * right[1]


def square(origin: Point, edge_u: Point, edge_v: Point) -> Polygon:
    return origin, add(origin, edge_u), add(add(origin, edge_u), edge_v), add(origin, edge_v)


def reference_family() -> SquareFamily:
    """Return the exact four-square construction at q=96/25."""
    q = Fraction(96, 25)
    c, s, g = Fraction(35, 37), Fraction(12, 37), Fraction(4, 5)
    unit_x, unit_y = (Fraction(1), Fraction(0)), (Fraction(0), Fraction(1))
    corner_lower = square((g, s), (c, -s), (s, c))
    a, b = Fraction(3152, 3175), Fraction(2336, 3175)
    return SquareFamily(
        GEOMETRY,
        q,
        Fraction(9977, 10000),
        (
            Square("A-minus", square((Fraction(0), Fraction(23, 25)), unit_x, unit_y)),
            Square("A-plus", square((Fraction(0), Fraction(48, 25)), unit_x, unit_y)),
            Square("C-minus", corner_lower),
            Square("C-plus", tuple((x, q - y) for x, y in corner_lower)),
        ),
        (
            CoreMark("bottom-left-a", "C-minus", (a, b)),
            CoreMark("top-left-a", "C-plus", (a, q - b)),
        ),
        SegmentOwnership(
            "left-outer-middle",
            ((Fraction(49, 100), Fraction(48, 25)), (Fraction(59, 100), Fraction(48, 25))),
            ("A-minus", "A-plus"),
        ),
    )


def _translate(item: Square, delta: Point) -> Square:
    return replace(item, vertices=tuple(add(vertex, delta) for vertex in item.vertices))


def control_family(name: str) -> SquareFamily:
    family = reference_family()
    if name == "overlap":
        return replace(
            family,
            squares=tuple(
                _translate(item, (Fraction(0), Fraction(-1, 100)))
                if item.name == "A-plus"
                else item
                for item in family.squares
            ),
        )
    if name == "broken-mark":
        b, a = Fraction(2336, 3175), Fraction(3152, 3175)
        return replace(
            family,
            core_marks=(replace(family.core_marks[0], point=(b, a)), family.core_marks[1]),
        )
    if name == "changed-target":
        return replace(family, q=Fraction(4))
    raise GuardError(f"unknown control {name!r}")


def _validate_point(point: object) -> bool:
    return (
        isinstance(point, tuple)
        and len(point) == 2
        and all(isinstance(value, Fraction) for value in point)
    )


def validate_unit_square(vertices: Polygon) -> None:
    """Require four cyclic vertices with exact unit edges and right angles."""
    if len(vertices) != 4 or any(not _validate_point(vertex) for vertex in vertices):
        raise GuardError("a unit square requires four exact rational vertices")
    edges = tuple(
        subtract(end, start)
        for start, end in zip(vertices, (*vertices[1:], vertices[0]), strict=True)
    )
    if any(dot(edge, edge) != 1 for edge in edges):
        raise GuardError("square edge length is not one")
    if any(dot(edges[index], edges[(index + 1) % 4]) != 0 for index in range(4)):
        raise GuardError("adjacent square edges are not orthogonal")
    if add(vertices[0], vertices[2]) != add(vertices[1], vertices[3]):
        raise GuardError("square diagonals do not share a midpoint")


def validate_family(family: SquareFamily) -> None:
    if family.geometry != GEOMETRY:
        raise GuardError(f"geometry must be {GEOMETRY!r}")
    if not isinstance(family.q, Fraction) or family.q <= 0:
        raise GuardError("q must be a positive Fraction")
    if not isinstance(family.core_side, Fraction) or not 0 < family.core_side <= 1:
        raise GuardError("core side must be a Fraction in (0,1]")
    names = [item.name for item in family.squares]
    if len(names) < 2 or any(not name for name in names) or len(names) != len(set(names)):
        raise GuardError("at least two uniquely named squares are required")
    for item in family.squares:
        validate_unit_square(item.vertices)
    mark_ids = [mark.mark_id for mark in family.core_marks]
    if (
        not mark_ids
        or any(not name for name in mark_ids)
        or len(mark_ids) != len(set(mark_ids))
    ):
        raise GuardError("at least one uniquely identified core mark is required")
    if any(
        mark.square not in names or not _validate_point(mark.point)
        for mark in family.core_marks
    ):
        raise GuardError("each core mark requires a known square and exact point")
    segment = family.segment
    if (
        not segment.segment_id
        or len(segment.endpoints) != 2
        or len(segment.owners) != 2
        or len(set(segment.owners)) != 2
        or any(owner not in names for owner in segment.owners)
        or any(not _validate_point(point) for point in segment.endpoints)
    ):
        raise GuardError("segment requires two exact endpoints and two distinct known owners")


def local_coordinates(vertices: Polygon, point: Point) -> Point:
    delta = subtract(point, vertices[0])
    return dot(delta, subtract(vertices[1], vertices[0])), dot(
        delta, subtract(vertices[3], vertices[0])
    )


def projection(vertices: Polygon, normal: Point) -> tuple[Fraction, Fraction]:
    values = tuple(dot(vertex, normal) for vertex in vertices)
    return min(values), max(values)


def separating_axis(left: Polygon, right: Polygon) -> tuple[Point, Fraction] | None:
    """Return the first nonnegative edge-normal gap; zero means boundary contact."""
    for polygon in (left, right):
        for start, end in zip(polygon, (*polygon[1:], polygon[0]), strict=True):
            edge = subtract(end, start)
            normal = (-edge[1], edge[0])
            left_low, left_high = projection(left, normal)
            right_low, right_high = projection(right, normal)
            gap = max(right_low - left_high, left_low - right_high)
            if gap >= 0:
                return normal, gap
    return None


def _square_receipts(family: SquareFamily) -> tuple[list[dict[str, Any]], bool]:
    rows = []
    for item in family.squares:
        contained = all(0 <= value <= family.q for vertex in item.vertices for value in vertex)
        center = tuple(sum(vertex[index] for vertex in item.vertices) / 4 for index in range(2))
        rows.append(
            {
                "name": item.name,
                "vertices": [[str(value) for value in vertex] for vertex in item.vertices],
                "center": tuple(str(value) for value in center),
                "unit_square": True,
                "contained": contained,
            }
        )
    return rows, all(row["contained"] for row in rows)


def _pair_receipts(family: SquareFamily) -> dict[str, Any]:
    rows = []
    for left, right in combinations(family.squares, 2):
        certificate = separating_axis(left.vertices, right.vertices)
        normal, gap = certificate if certificate is not None else (None, None)
        rows.append(
            {
                "squares": [left.name, right.name],
                "normal": None if normal is None else [str(value) for value in normal],
                "gap": None if gap is None else str(gap),
                "interiors_disjoint": certificate is not None,
                "strictly_separated": gap is not None and gap > 0,
            }
        )
    return {"holds": all(row["interiors_disjoint"] for row in rows), "pairs": rows}


def _core_receipts(family: SquareFamily) -> dict[str, Any]:
    squares = {item.name: item.vertices for item in family.squares}
    inset = (1 - family.core_side) / 2
    rows = []
    for mark in family.core_marks:
        coordinates = local_coordinates(squares[mark.square], mark.point)
        clearance = min(*coordinates, *(1 - value for value in coordinates)) - inset
        rows.append(
            {
                "mark_id": mark.mark_id,
                "square": mark.square,
                "point": [str(value) for value in mark.point],
                "local_coordinates": [str(value) for value in coordinates],
                "core_clearance": str(clearance),
                "strictly_inside_core": clearance > 0,
            }
        )
    clearances = [Fraction(row["core_clearance"]) for row in rows]
    return {
        "holds": all(row["strictly_inside_core"] for row in rows),
        "minimum_core_clearance": str(min(clearances)),
        "marks": rows,
    }


def _segment_receipt(family: SquareFamily) -> dict[str, Any]:
    squares = {item.name: item.vertices for item in family.squares}
    rows = []
    for owner in family.segment.owners:
        coordinates = tuple(
            local_coordinates(squares[owner], endpoint) for endpoint in family.segment.endpoints
        )
        rows.append(
            {
                "square": owner,
                "endpoint_local_coordinates": [
                    [str(value) for value in point] for point in coordinates
                ],
                "whole_segment_in_closed_square": all(
                    0 <= value <= 1 for point in coordinates for value in point
                ),
            }
        )
    return {
        "holds": all(row["whole_segment_in_closed_square"] for row in rows),
        "segment": [[str(value) for value in point] for point in family.segment.endpoints],
        "owners": rows,
    }


def audit_geometry(family: SquareFamily) -> dict[str, Any]:
    """Audit exact unit-square geometry without making the fixed target claim."""
    validate_family(family)
    squares, contained = _square_receipts(family)
    checks = {
        "container_containment": {"holds": contained},
        "pair_interior_disjointness": _pair_receipts(family),
        "core_membership": _core_receipts(family),
        "segment_membership": _segment_receipt(family),
    }
    return {
        "squares": squares,
        "checks": checks,
        "geometry_holds": all(check["holds"] for check in checks.values()),
    }


def _target_identity(family: SquareFamily) -> dict[str, bool]:
    target = reference_family()
    owners = (*family.segment.owners, *(mark.square for mark in family.core_marks))
    checks = {
        "fixed_q_and_core": (family.geometry, family.q, family.core_side)
        == (target.geometry, target.q, target.core_side),
        "exact_four_squares": set(family.squares) == set(target.squares),
        "specified_segment_M": family.segment == target.segment,
        "specified_corner_marks": set(family.core_marks) == set(target.core_marks),
        "four_distinct_owners": len(owners) == len(set(owners)) == 4,
    }
    return {**checks, "holds": all(checks.values())}


def audit_family(family: SquareFamily) -> dict[str, Any]:
    """Bind generic geometry to the fixed local-compatibility counterexample."""
    geometry, identity = audit_geometry(family), _target_identity(family)
    valid = geometry["geometry_holds"] and identity["holds"]
    return {
        "kind": "outer-pair-corner-audit/v1",
        "q": str(family.q),
        "core_side": str(family.core_side),
        **geometry,
        "target_identity": identity,
        "valid_target_counterexample": valid,
        "claim_refuted": valid,
        "refuted_claim": "the specified outer pair and selected corner owners are incompatible",
        "scope": "four-square local ownership compatibility",
        "eleven_square_packing_claimed": False,
    }


def _control_passed(name: str, report: dict[str, Any]) -> bool:
    checks = report["checks"]
    if name == "overlap":
        return not checks["pair_interior_disjointness"]["holds"] and all(
            checks[key]["holds"]
            for key in ("container_containment", "core_membership", "segment_membership")
        )
    if name == "broken-mark":
        return not checks["core_membership"]["holds"] and all(
            checks[key]["holds"]
            for key in (
                "container_containment",
                "pair_interior_disjointness",
                "segment_membership",
            )
        )
    return report["geometry_holds"] and not report["target_identity"]["holds"]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Audit the exact outer-pair construction.")
    parser.add_argument("--control", choices=CONTROL_NAMES)
    args = parser.parse_args(argv)
    try:
        family = reference_family() if args.control is None else control_family(args.control)
        report = audit_family(family)
    except GuardError as error:
        print(f"outer-pair corner audit refused input: {error}", file=sys.stderr)
        return 2
    passed = (
        report["valid_target_counterexample"]
        if args.control is None
        else _control_passed(args.control, report)
    )
    if args.control is not None:
        report.update(control=args.control, control_expectation_met=passed)
    report["status"] = (
        "verified_counterexample"
        if args.control is None and passed
        else "control_passed"
        if passed
        else "not_verified"
    )
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
