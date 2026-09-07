"""Exact facet probes for almost-everywhere weighted-square depth.

The public kernel rebuilds the whole arrangement; it does not accept a claimed list
of faces. Every bounded open arrangement face has a nondegenerate boundary segment.
Splitting every line at every crossing and stepping to both adjacent sides therefore
visits every positive-area face. Boundary-only depth is deliberately not measured.

This is the BC-243 control instrument, not the independent complete slab reader or a
target receipt interface. See the complete-face successor in
campaign/series/series-000-smoke-and-calibration/results/agenda-026/
bc-254-post-screen-next-discriminator.md. No source or target runs at import time.
"""

from __future__ import annotations

import argparse
import json
from collections.abc import Sequence
from dataclasses import dataclass, field
from fractions import Fraction
from itertools import pairwise

from sqpack.field import FieldElement, NumberField
from sqpack.full_size_density.pair_separator import PairFamily, make_family
from sqpack.full_size_density.support_ceiling import Point, Square, SupportError, axis_square


@dataclass(frozen=True)
class Line:
    """Canonical a*x + b*y = c; labels identify edges, with -1 for a wall."""

    a: FieldElement
    b: FieldElement
    c: FieldElement
    labels: tuple[tuple[int, int], ...] = ()

    def at(self, point: Point) -> FieldElement:
        return self.a * point[0] + self.b * point[1] - self.c


@dataclass(frozen=True)
class Facet:
    line: int
    start: Point
    end: Point


@dataclass(frozen=True)
class Arrangement:
    lines: tuple[Line, ...]
    facets: tuple[Facet, ...]
    point_contacts: tuple[tuple[int, Point], ...]
    _clearance_reciprocals: dict[frozenset[Point], FieldElement] = field(
        default_factory=dict, init=False, compare=False, repr=False
    )

    def clearance_reciprocal(
        self, first: Line, second: Line, derivative: FieldElement
    ) -> FieldElement:
        """Invert each nonzero unordered canonical-normal pair at most once.

        Offsets and facets do not affect 4*abs(n_first dot n_second). Fill lazily
        after the gap sign check: eager sign checks could refine the shared root
        interval earlier and change the rational clearance selected downstream.
        """
        key = frozenset(((first.a, first.b), (second.a, second.b)))
        reciprocal = self._clearance_reciprocals.get(key)
        if reciprocal is None:
            reciprocal = (4 * _absolute(derivative)).inverse()
            self._clearance_reciprocals[key] = reciprocal
        return reciprocal


@dataclass(frozen=True)
class FaceProbe:
    facet: int
    direction: int
    point: Point
    members: tuple[int, ...]
    depth: Fraction


@dataclass(frozen=True)
class ExcessBox:
    """An open L-infinity box contained in every listed square and the container."""

    point: Point
    radius: Fraction
    members: tuple[int, ...]
    excess: Fraction


@dataclass(frozen=True)
class FaceResult:
    family: PairFamily
    arrangement: Arrangement
    probes: tuple[FaceProbe, ...]
    maximum: Fraction
    witness: ExcessBox | None


def normalized_line(
    a: FieldElement,
    b: FieldElement,
    c: FieldElement,
    *,
    labels: tuple[tuple[int, int], ...] = (),
) -> Line:
    """Normalize by exact field division, never by a numeric approximation."""
    if any(value.field is not a.field for value in (b, c)):
        raise SupportError("line coefficients use different fields")
    divisor = a if not a.is_zero() else b
    if divisor.is_zero():
        raise SupportError("line normal must be nonzero")
    return Line(a / divisor, b / divisor, c / divisor, labels)


def _intersection(first: Line, second: Line) -> Point | None:
    determinant = first.a * second.b - second.a * first.b
    if determinant.is_zero():
        return None
    return (
        (first.c * second.b - second.c * first.b) / determinant,
        (first.a * second.c - second.a * first.c) / determinant,
    )


def _walls(side: FieldElement) -> tuple[Line, ...]:
    zero, one = side.field.zero, side.field.one
    return tuple(
        Line(a, b, c, ((-1, index),))
        for index, (a, b, c) in enumerate(
            ((one, zero, zero), (one, zero, side), (zero, one, zero), (zero, one, side))
        )
    )


def _in_container(point: Point, side: FieldElement, *, strict: bool) -> bool:
    lower = 1 if strict else 0
    return all(value.sign() >= lower for value in (*point, side - point[0], side - point[1]))


def clip_line(line: Line, side: FieldElement) -> tuple[Point, ...]:
    """Return zero, one, or two exact endpoints; a tangent is not a segment."""
    if side.sign() <= 0 or any(
        value.field is not side.field for value in (line.a, line.b, line.c)
    ):
        raise SupportError("clipping needs one exact field and a positive side")
    if line.a.is_zero() and line.b.is_zero():
        raise SupportError("line normal must be nonzero")
    zero = side.field.zero
    points = {
        point
        for point in ((zero, zero), (zero, side), (side, zero), (side, side))
        if line.at(point).is_zero()
    }
    for wall in _walls(side):
        point = _intersection(line, wall)
        if point is not None and _in_container(point, side, strict=False):
            points.add(point)
    coordinate = 0 if not line.b.is_zero() else 1
    ordered = sorted(points, key=lambda point: point[coordinate])
    if len(ordered) > 2:
        raise SupportError("clipping produced more than two distinct extreme points")
    return tuple(ordered)


def _supporting_lines(family: PairFamily) -> tuple[Line, ...]:
    groups: dict[tuple[FieldElement, ...], list[tuple[int, int]]] = {}
    for index, entry in enumerate(family.placements):
        if not entry.weight:
            continue
        for edge, (x, y) in enumerate(entry.square):
            nx, ny = entry.square[(edge + 1) % 4]
            a, b = ny - y, x - nx
            line = normalized_line(a, b, a * x + b * y)
            groups.setdefault((line.a, line.b, line.c), []).append((index, edge))
    for wall in _walls(family.side):
        groups.setdefault((wall.a, wall.b, wall.c), []).extend(wall.labels)
    # Coefficient tuples provide a reproducible enumeration, not geometric ordering.
    keys = sorted(groups, key=lambda key: tuple(value.coeffs for value in key))
    return tuple(Line(key[0], key[1], key[2], tuple(groups[key])) for key in keys)


def build_arrangement(family: PairFamily) -> Arrangement:
    """Split all positive-weight supporting lines and walls at all exact crossings."""
    lines = _supporting_lines(family)
    facets: list[Facet] = []
    contacts: list[tuple[int, Point]] = []
    for index, line in enumerate(lines):
        clipped = clip_line(line, family.side)
        if len(clipped) < 2:
            contacts.extend((index, point) for point in clipped)
            continue
        cuts = set(clipped)
        for other in lines:
            point = _intersection(line, other)
            if point is not None and _in_container(point, family.side, strict=False):
                cuts.add(point)
        coordinate = 0 if not line.b.is_zero() else 1
        ordered = sorted(cuts, key=lambda point: point[coordinate])
        facets.extend(Facet(index, start, end) for start, end in pairwise(ordered))
    return Arrangement(lines, tuple(facets), tuple(contacts))


def _positive_lower(value: FieldElement) -> Fraction:
    if value.sign() <= 0:
        raise SupportError("positive rational margin was not established")
    lower, _ = value.field.enclose(value)
    if lower <= 0:
        raise SupportError("positive rational enclosure was not established")
    return lower


def _absolute(value: FieldElement) -> FieldElement:
    return value if value.sign() >= 0 else -value


def facet_probes(
    arrangement: Arrangement,
    facet: Facet,
    side: FieldElement,
) -> tuple[tuple[int, Point], ...]:
    """Visit each contained side without crossing any other supporting line."""
    if not 0 <= facet.line < len(arrangement.lines) or facet.start == facet.end:
        raise SupportError("invalid facet or zero-length segment")
    line = arrangement.lines[facet.line]
    if not line.at(facet.start).is_zero() or not line.at(facet.end).is_zero():
        raise SupportError("facet endpoints are not on their line")
    midpoint = tuple(
        (first + second) / 2 for first, second in zip(facet.start, facet.end, strict=True)
    )
    center: Point = midpoint[0], midpoint[1]
    delta = Fraction(1, 4)
    for index, other in enumerate(arrangement.lines):
        if index == facet.line:
            continue
        gap = other.at(center)
        if gap.is_zero():
            raise SupportError("facet midpoint meets an unsplit crossing or duplicate line")
        derivative = other.a * line.a + other.b * line.b
        if not derivative.is_zero():
            clearance = _absolute(gap) * arrangement.clearance_reciprocal(
                line, other, derivative
            )
            delta = min(delta, _positive_lower(clearance))
    probes: list[tuple[int, Point]] = []
    for direction in (-1, 1):
        point = (center[0] + direction * delta * line.a, center[1] + direction * delta * line.b)
        if not _in_container(point, side, strict=True):
            continue
        if any(other.at(point).is_zero() for other in arrangement.lines):
            raise SupportError("facet probe lies on a supporting line")
        for index, other in enumerate(arrangement.lines):
            if index != facet.line and other.at(point).sign() != other.at(center).sign():
                raise SupportError("facet probe crossed another supporting line")
        probes.append((direction, point))
    expected = 1 if any(index == -1 for index, _ in line.labels) else 2
    if len(probes) != expected:
        raise SupportError("facet did not visit every contained adjacent side")
    return tuple(probes)


def _membership_forms(square: Square, point: Point) -> tuple[FieldElement, ...]:
    x, y = square[0]
    ex, ey = square[1][0] - x, square[1][1] - y
    fx, fy = square[3][0] - x, square[3][1] - y
    u, v = ex * (point[0] - x) + ey * (point[1] - y), fx * (point[0] - x) + fy * (point[1] - y)
    return u, 1 - u, v, 1 - v


def _excess_box(family: PairFamily, probe: FaceProbe) -> ExcessBox:
    forms = [*probe.point, family.side - probe.point[0], family.side - probe.point[1]]
    for index in probe.members:
        forms.extend(_membership_forms(family.placements[index].square, probe.point))
    # Unit-edge normals have L1 norm <= sqrt(2) < 2, including reflected ordering.
    radius = min(_positive_lower(value) for value in forms) / 4
    return ExcessBox(probe.point, radius, probe.members, probe.depth - 1)


def check_excess_box(family: PairFamily, witness: ExcessBox) -> None:
    """Recheck a positive-area excess using oriented edges, not facet incidences."""
    if (
        type(witness.radius) is not Fraction
        or witness.radius <= 0
        or type(witness.excess) is not Fraction
        or witness.excess <= 0
        or not witness.members
        or any(type(index) is not int for index in witness.members)
        or tuple(sorted(set(witness.members))) != witness.members
        or any(not 0 <= index < len(family.placements) for index in witness.members)
    ):
        raise SupportError("invalid excess-box radius, members, or excess")
    if any(value.field is not family.side.field for value in witness.point):
        raise SupportError("excess-box point uses another field")
    if (
        sum((family.placements[index].weight for index in witness.members), Fraction())
        != 1 + witness.excess
    ):
        raise SupportError("excess-box weights do not establish its claimed excess")
    px, py = witness.point
    radius = witness.radius
    if any(
        (margin - radius).sign() <= 0 for margin in (px, py, family.side - px, family.side - py)
    ):
        raise SupportError("excess box is not strictly inside the container")
    for index in witness.members:
        square = family.placements[index].square
        ex, ey = square[1][0] - square[0][0], square[1][1] - square[0][1]
        fx, fy = square[3][0] - square[0][0], square[3][1] - square[0][1]
        orientation = (ex * fy - ey * fx).sign()
        for edge, (x, y) in enumerate(square):
            nx, ny = square[(edge + 1) % 4]
            dx, dy = nx - x, ny - y
            margin = orientation * (dx * (py - y) - dy * (px - x))
            if (margin - radius * (_absolute(dx) + _absolute(dy))).sign() <= 0:
                raise SupportError("excess box is not in every listed square interior")


def verify_density(
    squares: Sequence[Square],
    side: FieldElement,
    weights: Sequence[Fraction],
) -> FaceResult:
    """Compute a complete a.e. maximum for validated, deduplicated fixed weights.

    Zero-weight edges are omitted only for this fixed candidate. Returned probes are
    not admissible necessary LP rows without checking all support boundaries again.
    No supplied arrangement, partial prefix, or point list can authorize completion.
    """
    family = make_family(squares, side, weights)
    arrangement = build_arrangement(family)
    probes: list[FaceProbe] = []
    for facet_index, facet in enumerate(arrangement.facets):
        for direction, point in facet_probes(arrangement, facet, side):
            members = tuple(
                index
                for index, entry in enumerate(family.placements)
                if entry.weight
                and all(value.sign() > 0 for value in _membership_forms(entry.square, point))
            )
            depth = sum((family.placements[index].weight for index in members), Fraction())
            probes.append(FaceProbe(facet_index, direction, point, members, depth))
    if not probes:
        raise SupportError("complete arrangement produced no interior face probes")
    largest = max(probes, key=lambda probe: probe.depth)
    witness = _excess_box(family, largest) if largest.depth > 1 else None
    if witness is not None:
        check_excess_box(family, witness)
    return FaceResult(family, arrangement, tuple(probes), largest.depth, witness)


def main(argv: Sequence[str] | None = None) -> int:
    """Run a named rational control; there is no target or file-input mode."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("control", choices=("contacts", "triple"))
    args = parser.parse_args(argv)
    field = NumberField((1, 0), ("-1", "1"))
    q = field.rational
    centers = (("1/2", "1/2"), ("3/2", "1/2"), ("3/2", "3/2"))
    weight, side = Fraction(1), q(2)
    if args.control == "triple":
        centers = (("1", "1"), ("3/2", "1"), ("5/4", "5/4"))
        weight, side = Fraction(2, 5), q(3)
    result = verify_density(
        tuple(axis_square(q(x), q(y)) for x, y in centers), side, (weight,) * 3
    )
    print(
        json.dumps(
            {
                "control": args.control,
                "scope": "complete-a.e.-control",
                "maximum": str(result.maximum),
                "facets": len(result.arrangement.facets),
                "probes": len(result.probes),
            }
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
