"""Exact geometry audit for the adjacent-corner ownership counterexample."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, replace
from fractions import Fraction
from itertools import combinations
from typing import Any

type Point = tuple[Fraction, Fraction]

GEOMETRY = "l1-diamond-family/v1"
PRIMARY_CHECK_NAMES = (
    "unit_containment",
    "core_ownership",
    "pair_interior_disjointness",
)
CONTROL_NAMES = ("overlap", "containment", "core-ownership")
CONTROL_FAILURE = {
    "overlap": "pair_interior_disjointness",
    "containment": "unit_containment",
    "core-ownership": "core_ownership",
}


class GuardError(ValueError):
    """The family is malformed or belongs to another geometric model."""


@dataclass(frozen=True, slots=True)
class Diamond:
    name: str
    center: Point


@dataclass(frozen=True, slots=True)
class OwnedMark:
    corner: str
    point: Point
    owner: str


@dataclass(frozen=True, slots=True)
class DiamondFamily:
    geometry: str
    container_side: Fraction
    diamond_side: Fraction
    core_side: Fraction
    diamonds: tuple[Diamond, ...]
    marks: tuple[OwnedMark, ...]
    adjacent_corners: tuple[str, str]


def reference_family() -> DiamondFamily:
    """The exact q=96/25 candidate, reflected across x=q/2."""
    q = Fraction(96, 25)
    a, b = Fraction(3152, 3175), Fraction(2336, 3175)
    return DiamondFamily(
        GEOMETRY,
        q,
        Fraction(1),
        Fraction(9977, 10000),
        (
            Diamond("A", (Fraction(6, 5), Fraction(71, 100))),
            Diamond("B", (Fraction(71, 100), Fraction(33, 20))),
            Diamond("A-prime", (Fraction(66, 25), Fraction(71, 100))),
            Diamond("B-prime", (Fraction(313, 100), Fraction(33, 20))),
        ),
        (
            OwnedMark("bottom-left", (a, b), "A"),
            OwnedMark("bottom-left", (b, a), "B"),
            OwnedMark("bottom-right", (q - a, b), "A-prime"),
            OwnedMark("bottom-right", (q - b, a), "B-prime"),
        ),
        ("bottom-left", "bottom-right"),
    )


def control_family(name: str) -> DiamondFamily:
    """Mutate one center so exactly one geometric obligation fails."""
    changes = {
        "overlap": ("A-prime", (Fraction(261, 100), Fraction(71, 100))),
        "containment": ("B", (Fraction(7, 10), Fraction(33, 20))),
        "core-ownership": ("B", (Fraction(71, 100), Fraction(7, 4))),
    }
    if name not in changes:
        raise GuardError(f"unknown control {name!r}")
    family, (target, center) = reference_family(), changes[name]
    return replace(
        family,
        diamonds=tuple(
            replace(diamond, center=center) if diamond.name == target else diamond
            for diamond in family.diamonds
        ),
    )


def validate_family(family: DiamondFamily) -> None:
    """Reject wrong geometry, nonpositive sides, and inconsistent identities."""
    if family.geometry != GEOMETRY:
        raise GuardError(f"geometry must be {GEOMETRY!r}")
    sides = (family.container_side, family.diamond_side, family.core_side)
    if any(not isinstance(side, Fraction) or side <= 0 for side in sides):
        raise GuardError("container, diamond, and core sides must be positive Fractions")
    if family.core_side > family.diamond_side:
        raise GuardError("core side cannot exceed diamond side")
    names = [diamond.name for diamond in family.diamonds]
    if len(names) < 2 or any(not name for name in names) or len(names) != len(set(names)):
        raise GuardError("at least two uniquely named diamonds are required")
    if len(family.adjacent_corners) != 2 or len(set(family.adjacent_corners)) != 2:
        raise GuardError("two distinct adjacent-corner labels are required")
    points = [diamond.center for diamond in family.diamonds] + [
        mark.point for mark in family.marks
    ]
    if any(
        not isinstance(point, tuple)
        or len(point) != 2
        or any(not isinstance(coordinate, Fraction) for coordinate in point)
        for point in points
    ):
        raise GuardError("centers and marks must be pairs of exact Fractions")
    if len({diamond.center for diamond in family.diamonds}) != len(family.diamonds):
        raise GuardError("diamond centers must be distinct")
    for mark in family.marks:
        if mark.corner not in family.adjacent_corners or mark.owner not in names:
            raise GuardError("each mark must name an adjacent corner and known owner")
    if any(
        not any(mark.corner == corner for mark in family.marks)
        for corner in family.adjacent_corners
    ):
        raise GuardError("each adjacent corner requires a mark")


def strictly_contained(margin_squared: Fraction, radius_squared: Fraction) -> bool:
    return margin_squared > radius_squared


def strictly_owned(twice_distance_squared: Fraction, core_side_squared: Fraction) -> bool:
    return twice_distance_squared < core_side_squared


def interiors_disjoint(distance_squared: Fraction, required_squared: Fraction) -> bool:
    return distance_squared >= required_squared


def _unit_containment(family: DiamondFamily) -> dict[str, Any]:
    required = family.diamond_side**2 / 2
    margins = {
        diamond.name: min(
            diamond.center[0],
            diamond.center[1],
            family.container_side - diamond.center[0],
            family.container_side - diamond.center[1],
        )
        for diamond in family.diamonds
    }
    contained = {
        name: margin > 0 and strictly_contained(margin * margin, required)
        for name, margin in margins.items()
    }
    return {
        "holds": all(contained.values()),
        "minimum_margin": str(min(margins.values())),
        "required_radius_squared": str(required),
        "margins": {name: str(value) for name, value in margins.items()},
        "strictly_contained": contained,
    }


def _core_ownership(family: DiamondFamily) -> dict[str, Any]:
    centers = {diamond.name: diamond.center for diamond in family.diamonds}
    distances = []
    for mark in family.marks:
        center = centers[mark.owner]
        distance = abs(mark.point[0] - center[0]) + abs(mark.point[1] - center[1])
        distances.append(distance)
    bridge = Fraction(7, 10)
    owned = [
        strictly_owned(2 * distance * distance, family.core_side**2) for distance in distances
    ]
    return {
        "holds": all(owned),
        "core_side_squared": str(family.core_side**2),
        "all_distances_below_7/10": all(distance < bridge for distance in distances),
        "7/10_inside_core_radius": strictly_owned(2 * bridge * bridge, family.core_side**2),
        "l1_distances": [str(value) for value in distances],
        "strictly_inside": owned,
    }


def _l1_reader(family: DiamondFamily) -> dict[tuple[str, str], tuple[Fraction, bool]]:
    required = 2 * family.diamond_side**2
    return {
        (left.name, right.name): (
            distance,
            interiors_disjoint(distance * distance, required),
        )
        for left, right in combinations(family.diamonds, 2)
        for distance in (
            abs(left.center[0] - right.center[0]) + abs(left.center[1] - right.center[1]),
        )
    }


def _sat_reader(
    family: DiamondFamily,
) -> dict[tuple[str, str], tuple[tuple[Fraction, ...], bool]]:
    """Apply SAT on (1,1),(1,-1) without calling the L1 formulation."""
    required = 2 * family.diamond_side**2
    result = {}
    for left, right in combinations(family.diamonds, 2):
        dx, dy = left.center[0] - right.center[0], left.center[1] - right.center[1]
        projections = (abs(dx + dy), abs(dx - dy))
        result[(left.name, right.name)] = (
            projections,
            any(interiors_disjoint(value * value, required) for value in projections),
        )
    return result


def _pair_disjointness(family: DiamondFamily) -> dict[str, Any]:
    l1, sat = _l1_reader(family), _sat_reader(family)
    agree = l1.keys() == sat.keys() and all(l1[pair][1] == sat[pair][1] for pair in l1)
    rows = [
        {
            "diamonds": list(pair),
            "l1_distance": str(distance),
            "l1_disjoint": disjoint,
            "sat_projection_distances": [str(value) for value in sat[pair][0]],
            "sat_disjoint": sat[pair][1],
        }
        for pair, (distance, disjoint) in l1.items()
    ]
    return {
        "holds": agree and all(row["l1_disjoint"] for row in rows),
        "l1_sat_agree": agree,
        "minimum_l1_distance": str(min(value[0] for value in l1.values())),
        "required_separation_squared": str(2 * family.diamond_side**2),
        "sat_normals": [[1, 1], [1, -1]],
        "pairs": rows,
    }


def audit_geometry(family: DiamondFamily) -> dict[str, Any]:
    """Audit any congruent rational L1-diamond family without a theorem claim."""
    validate_family(family)
    checks = {
        "unit_containment": _unit_containment(family),
        "core_ownership": _core_ownership(family),
        "pair_interior_disjointness": _pair_disjointness(family),
    }
    return {
        "checks": checks,
        "geometry_holds": all(check["holds"] for check in checks.values()),
    }


def _target_identity(family: DiamondFamily) -> dict[str, bool]:
    target = reference_family()
    owners = [mark.owner for mark in family.marks]
    checks = {
        "parameters": all(
            getattr(family, name) == getattr(target, name)
            for name in ("geometry", "container_side", "diamond_side", "core_side")
        ),
        "four_centers": set(family.diamonds) == set(target.diamonds),
        "four_mark_assignments": set(family.marks) == set(target.marks),
        "actual_adjacency": family.adjacent_corners == target.adjacent_corners,
        "all_four_owners_distinct": len(owners) == len(set(owners)) == 4,
    }
    return {**checks, "holds": all(checks.values())}


def audit_family(family: DiamondFamily) -> dict[str, Any]:
    """Bind the reusable geometry result to the exact n=11 target fixture."""
    geometry, identity = audit_geometry(family), _target_identity(family)
    valid = geometry["geometry_holds"] and identity["holds"]
    source_b = next((diamond for diamond in family.diamonds if diamond.name == "B"), None)
    reflection = None
    if source_b is not None:
        distance = abs(family.container_side - 2 * source_b.center[1])
        reflection = {
            "l1_distance": str(distance),
            "interiors_disjoint": interiors_disjoint(
                distance * distance, 2 * family.diamond_side**2
            ),
        }
    return {
        **geometry,
        "target_identity": identity,
        "valid_n11_counterexample": valid,
        "claim_refuted": valid,
        "horizontal_reflection_extension": reflection,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Audit the exact adjacent-corner fixture.")
    parser.add_argument("--control", choices=CONTROL_NAMES)
    args = parser.parse_args(argv)
    try:
        family = reference_family() if args.control is None else control_family(args.control)
        report = audit_family(family)
    except GuardError as error:
        print(f"corner ownership audit refused input: {error}", file=sys.stderr)
        return 2
    if args.control is None:
        passed = report["valid_n11_counterexample"]
        report["status"] = (
            "verified_n11_counterexample" if passed else "not_an_n11_counterexample"
        )
    else:
        failed = [name for name in PRIMARY_CHECK_NAMES if not report["checks"][name]["holds"]]
        passed = failed == [CONTROL_FAILURE[args.control]]
        report.update(
            control=args.control, observed_failed_checks=failed, control_expectation_met=passed
        )
        report["status"] = "control_passed" if passed else "control_failed"
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
