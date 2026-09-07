"""Independent exact vertical-slab enumeration of fixed-weight a.e. depth.

Between consecutive x-events, each square's vertical section has fixed endpoint
formulas and ordering. A change requires a vertical supporting line or a crossing
of two supporting lines, all of which this reader enumerates. Every positive-area
face meets an open slab, so sweeping all open y-bands gives the complete maximum.
Exceptional x-lines and section endpoints have area zero and are never scored.

The shared foundations are NumberField arithmetic and make_family's unit-geometry,
containment, and duplicate-alias validation. No facet enumeration is imported.
This control kernel has no source binding, target dispatch, or portable packet format.
"""

from __future__ import annotations

import argparse
import json
from collections.abc import Sequence
from dataclasses import dataclass
from fractions import Fraction
from itertools import combinations, pairwise

from sqpack.field import FieldElement, NumberField
from sqpack.full_size_density.pair_separator import PairFamily, make_family
from sqpack.full_size_density.support_ceiling import Point, Square, SupportError, axis_square


@dataclass(frozen=True)
class Boundary:
    """An affine supporting line a*x + b*y + c = 0, normalized exactly."""

    a: FieldElement
    b: FieldElement
    c: FieldElement


@dataclass(frozen=True)
class Section:
    member: int
    lower: FieldElement
    upper: FieldElement


@dataclass(frozen=True)
class Slab:
    left: FieldElement
    right: FieldElement
    bands: int
    maximum: Fraction
    point: Point
    members: tuple[int, ...]


@dataclass(frozen=True)
class SlabWitness:
    point: Point
    radius: Fraction
    members: tuple[int, ...]
    excess: Fraction


@dataclass(frozen=True)
class SlabResult:
    family: PairFamily
    x_events: tuple[FieldElement, ...]
    slabs: tuple[Slab, ...]
    maximum: Fraction
    witness: SlabWitness | None


def _edge_forms(square: Square) -> tuple[Boundary, ...]:
    """Interior-positive determinant forms, independent of orthogonal coordinates."""
    origin, next_corner, _, previous = square
    ex, ey = next_corner[0] - origin[0], next_corner[1] - origin[1]
    fx, fy = previous[0] - origin[0], previous[1] - origin[1]
    orientation = (ex * fy - ey * fx).sign()
    if orientation == 0:
        raise SupportError("square has zero orientation")
    forms = []
    for index, (x, y) in enumerate(square):
        nx, ny = square[(index + 1) % 4]
        dx, dy = nx - x, ny - y
        forms.append(
            Boundary(-orientation * dy, orientation * dx, orientation * (dy * x - dx * y))
        )
    return tuple(forms)


def supporting_boundaries(family: PairFamily) -> tuple[Boundary, ...]:
    """Reconstruct positive-weight supporting lines and all four container walls."""
    zero, one = family.side.field.zero, family.side.field.one
    forms = [
        Boundary(one, zero, zero),
        Boundary(one, zero, -family.side),
        Boundary(zero, one, zero),
        Boundary(zero, one, -family.side),
    ]
    for entry in family.placements:
        if entry.weight:
            forms.extend(_edge_forms(entry.square))
    unique: dict[tuple[FieldElement, ...], Boundary] = {}
    for form in forms:
        divisor = form.a if not form.a.is_zero() else form.b
        if divisor.is_zero():
            raise SupportError("supporting boundary has a zero normal")
        key = form.a / divisor, form.b / divisor, form.c / divisor
        unique[key] = Boundary(*key)
    # This is only a deterministic line enumeration. Event sorting below is algebraic.
    return tuple(
        unique[key] for key in sorted(unique, key=lambda key: tuple(v.coeffs for v in key))
    )


def slab_events(family: PairFamily) -> tuple[FieldElement, ...]:
    """Include crossings even when their y-coordinate is outside the container."""
    lines = supporting_boundaries(family)
    events = {family.side.field.zero, family.side}
    for line in lines:
        if line.b.is_zero():
            x = -line.c / line.a
            if 0 <= x <= family.side:
                events.add(x)
    for first, second in combinations(lines, 2):
        determinant = first.a * second.b - second.a * first.b
        if not determinant.is_zero():
            x = (first.b * second.c - second.b * first.c) / determinant
            if 0 <= x <= family.side:
                events.add(x)
    return tuple(sorted(events))


def vertical_section(
    square: Square, x: FieldElement, side: FieldElement
) -> tuple[FieldElement, FieldElement] | None:
    """Intersect four strict edge half-planes and the open container with x fixed.

    The square and field must already be validated by make_family. A vertical edge
    contact or a singleton section is empty under these interior semantics.
    """
    lower, upper = side.field.zero, side
    for form in _edge_forms(square):
        constant = form.a * x + form.c
        direction = form.b.sign()
        if direction == 0:
            if constant.sign() <= 0:
                return None
        elif direction > 0:
            lower = max(lower, -constant / form.b)
        else:
            upper = min(upper, -constant / form.b)
    return (lower, upper) if lower < upper else None


def _scan_slab(family: PairFamily, left: FieldElement, right: FieldElement) -> Slab:
    if not 0 <= left < right <= family.side:
        raise SupportError("slab endpoints do not define a nonempty interior interval")
    x = (left + right) / 2
    sections = []
    for index, entry in enumerate(family.placements):
        if entry.weight:
            interval = vertical_section(entry.square, x, family.side)
            if interval is not None:
                sections.append(Section(index, *interval))
    zero = family.side.field.zero
    events: dict[FieldElement, tuple[list[int], list[int]]] = {
        zero: ([], []),
        family.side: ([], []),
    }
    for section in sections:
        events.setdefault(section.lower, ([], []))[0].append(section.member)
        events.setdefault(section.upper, ([], []))[1].append(section.member)
    ordered = sorted(events)
    active: set[int] = set()
    depth, maximum = Fraction(), Fraction(-1)
    point: Point = x, family.side / 2
    members: tuple[int, ...] = ()
    bands = 0
    for index, y in enumerate(ordered):
        entering, leaving = events[y]
        # Apply the entire endpoint group before scoring the next OPEN band.
        for member in leaving:
            if member not in active:
                raise SupportError("section closes before it opens")
            active.remove(member)
            depth -= family.placements[member].weight
        for member in entering:
            if member in active:
                raise SupportError("section opens twice")
            active.add(member)
            depth += family.placements[member].weight
        if index + 1 < len(ordered):
            bands += 1
            if depth > maximum:
                maximum = depth
                point = x, (y + ordered[index + 1]) / 2
                members = tuple(sorted(active))
    if active or depth != 0 or bands == 0:
        raise SupportError("open-band sweep did not close completely")
    return Slab(left, right, bands, maximum, point, members)


def _excess_box(family: PairFamily, slab: Slab) -> SlabWitness:
    """Choose a rational radius below every strict affine margin/L1 normal bound."""
    x, y = slab.point
    bounds = [x / 2, y / 2, (family.side - x) / 2, (family.side - y) / 2]
    for member in slab.members:
        for form in _edge_forms(family.placements[member].square):
            normal = form.a * form.a.sign() + form.b * form.b.sign()
            bounds.append((form.a * x + form.b * y + form.c) / (2 * normal))
    lower_bounds = []
    for bound in bounds:
        if bound.sign() <= 0:
            raise SupportError("maximum band did not give a strict interior margin")
        lower, _ = family.side.field.enclose(bound)
        if lower <= 0:
            raise SupportError("strict margin lacks a positive rational enclosure")
        lower_bounds.append(lower)
    return SlabWitness(slab.point, min(lower_bounds), slab.members, slab.maximum - 1)


def check_witness(
    squares: Sequence[Square],
    side: FieldElement,
    weights: Sequence[Fraction],
    witness: SlabWitness,
) -> None:
    """Check all box corners by dot products, independently of the slab edge forms.

    Convexity then puts the whole closed box strictly inside every listed unit
    square and the container. The checked subset alone has weight above one.
    This is a typed-kernel check, not a serialized packet parser.
    """
    family = make_family(squares, side, weights)
    if not isinstance(witness, SlabWitness) or (
        type(witness.radius) is not Fraction
        or witness.radius <= 0
        or type(witness.excess) is not Fraction
        or witness.excess <= 0
        or type(witness.point) is not tuple
        or len(witness.point) != 2
        or any(
            not isinstance(coordinate, FieldElement) or coordinate.field is not side.field
            for coordinate in witness.point
        )
        or type(witness.members) is not tuple
        or not witness.members
        or any(type(member) is not int for member in witness.members)
        or tuple(sorted(set(witness.members))) != witness.members
        or any(not 0 <= member < len(family.placements) for member in witness.members)
    ):
        raise SupportError("malformed strict excess-box witness")
    total = sum((family.placements[member].weight for member in witness.members), Fraction())
    if total - 1 != witness.excess:
        raise SupportError("witness subset does not have the declared strict excess")
    for sx, sy in ((-1, -1), (-1, 1), (1, -1), (1, 1)):
        x = witness.point[0] + sx * witness.radius
        y = witness.point[1] + sy * witness.radius
        if not 0 < x < side or not 0 < y < side:
            raise SupportError("witness box leaves the strict container interior")
        for member in witness.members:
            square = family.placements[member].square
            dx, dy = x - square[0][0], y - square[0][1]
            for corner in (square[1], square[3]):
                ex, ey = corner[0] - square[0][0], corner[1] - square[0][1]
                if not 0 < dx * ex + dy * ey < 1:
                    raise SupportError("witness box is not strictly inside its square subset")


def verify_density_slabs(
    squares: Sequence[Square], side: FieldElement, weights: Sequence[Fraction]
) -> SlabResult:
    """Recompute every open slab; supplied events or partial receipts are not accepted.

    The shared family contract requires 1--60 squares. Duplicate geometries are
    aliases carrying the same weight, not additive copies. All-zero weights are
    allowed; an empty or malformed family is refused before enumeration.
    """
    family = make_family(squares, side, weights)
    events = slab_events(family)
    slabs = tuple(_scan_slab(family, left, right) for left, right in pairwise(events))
    if not slabs:
        raise SupportError("no complete interior slabs were enumerated")
    largest = max(slabs, key=lambda slab: slab.maximum)
    witness = _excess_box(family, largest) if largest.maximum > 1 else None
    if witness is not None:
        check_witness(squares, side, weights, witness)
    return SlabResult(family, events, slabs, largest.maximum, witness)


def main(argv: Sequence[str] | None = None) -> int:
    """Run a hand-set control; source/target inputs deliberately have no CLI entry."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--control", required=True, choices=("contacts", "triple"))
    args = parser.parse_args(argv)
    field = NumberField((1, 0), ("-1", "1"))
    q = field.rational
    if args.control == "contacts":
        centers = (("1/2", "1/2"), ("3/2", "1/2"), ("3/2", "3/2"))
        side, weights, expected = q(2), (Fraction(1),) * 3, Fraction(1)
    else:
        centers = (("1", "1"), ("3/2", "1"), ("5/4", "5/4"))
        side, weights, expected = q(3), (Fraction(2, 5),) * 3, Fraction(6, 5)
    squares = tuple(axis_square(q(x), q(y)) for x, y in centers)
    result = verify_density_slabs(squares, side, weights)
    if result.maximum != expected:
        raise SupportError("slab control disagrees with its hand-derived open depth")
    print(
        json.dumps(
            {
                "scope": "toy-only-ae-depth",
                "control": args.control,
                "maximum": str(result.maximum),
                "x_events": len(result.x_events),
                "slabs": len(result.slabs),
                "bands": sum(slab.bands for slab in result.slabs),
                "excess_witness": result.witness is not None,
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
