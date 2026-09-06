"""Exact one-square Stromquist Theorem 3 controls, including all event strata.

The source uses open squares of side greater than one. These controls check
sufficient closed-unit-square statements, without perturbing either orientation.
"""

from __future__ import annotations

import argparse
import json
from collections.abc import Callable, Iterator, Sequence
from dataclasses import dataclass
from fractions import Fraction
from itertools import pairwise

from sqpack.field import FieldElement, NumberField

type Point = tuple[FieldElement, FieldElement]
type Polygon = tuple[Point, ...]
type Plane = tuple[FieldElement, FieldElement, FieldElement]

HALF = Fraction(1, 2)
OBLIGATIONS = (
    "axis_ten_cover",
    "localization",
    "forced_A1",
    "forced_A2",
    "forced_A3",
    "twelve_cover_0",
    "twelve_cover_45",
)
ANGLE_OBLIGATIONS = {
    0: ("axis_ten_cover", "twelve_cover_0"),
    45: ("localization", "forced_A1", "forced_A2", "forced_A3", "twelve_cover_45"),
}


@dataclass(frozen=True)
class Stratum:
    low: FieldElement
    high: FieldElement

    @property
    def dimension(self) -> int:
        return int(self.low != self.high)

    def contains(self, value: FieldElement) -> bool:
        return value == self.low if self.dimension == 0 else self.low < value < self.high


@dataclass(frozen=True)
class Cell:
    u: Stratum
    v: Stratum
    polygon: Polygon
    witness: Point
    covered: int

    @property
    def dimension(self) -> int:
        return self.u.dimension + self.v.dimension


@dataclass(frozen=True)
class CoverResult:
    reachable_by_dimension: tuple[int, int, int]
    escape: Point | None


def source_field() -> NumberField:
    """The positive square root of two, with an exact isolating interval."""
    return NumberField((1, 0, -2), ("1", "2"))


def direction(side: FieldElement, angle: int) -> Point:
    """Only the two source orientations are admitted, modulo square quarter turns."""
    if type(angle) is not int or angle not in (0, 45):
        raise ValueError("source control requires exactly 0 or 45 degrees")
    if angle == 0:
        return side.field.one, side.field.zero
    root = side.field.alpha
    if root * root != 2 or root.sign() <= 0:
        raise ValueError("45-degree control requires the positive square root of two")
    return root / 2, root / 2


def project(point: Point, frame: Point) -> Point:
    x, y = point
    cosine, sine = frame
    return cosine * x + sine * y, -sine * x + cosine * y


def unproject(point: Point, frame: Point) -> Point:
    u, v = point
    cosine, sine = frame
    return cosine * u - sine * v, sine * u + cosine * v


def clip_polygon(polygon: Polygon, plane: Plane) -> Polygon:
    """Intersect with a closed half-plane, preserving points and segments."""
    if not polygon:
        return ()
    a, b, bound = plane
    output: list[Point] = []
    previous = polygon[-1]
    old = a * previous[0] + b * previous[1] - bound
    for current in polygon:
        new = a * current[0] + b * current[1] - bound
        if (old.sign() <= 0) != (new.sign() <= 0):
            fraction = old / (old - new)
            output.append(
                (
                    previous[0] + fraction * (current[0] - previous[0]),
                    previous[1] + fraction * (current[1] - previous[1]),
                )
            )
        if new.sign() <= 0:
            output.append(current)
        previous, old = current, new
    return tuple(dict.fromkeys(output))


def cell_witness(polygon: Polygon, u: Stratum, v: Stratum) -> Point | None:
    """A vertex average meets every non-identically-tight strict cell inequality."""
    if not polygon:
        return None
    zero = u.low.field.zero
    center = (
        sum((point[0] for point in polygon), zero) / len(polygon),
        sum((point[1] for point in polygon), zero) / len(polygon),
    )
    return center if u.contains(center[0]) and v.contains(center[1]) else None


def _strata(values: Sequence[FieldElement]) -> tuple[Stratum, ...]:
    events = sorted(set(values))
    result = [Stratum(value, value) for value in events]
    result.extend(Stratum(left, right) for left, right in pairwise(events))
    return tuple(sorted(result, key=lambda value: (value.low, value.high)))


def event_cells(side: FieldElement, angle: int, points: Sequence[Point]) -> Iterator[Cell]:
    """Partition the entire contained closed-unit-square center domain exactly."""
    frame = direction(side, angle)
    half_extent = sum(frame, side.field.zero) / 2
    if side < 2 * half_extent:
        raise ValueError("the contained-center domain is empty")
    if any(value.field is not side.field for point in points for value in point):
        raise ValueError("points and container require one exact field")
    low, high = half_extent, side - half_extent
    domain = tuple(
        dict.fromkeys(
            project(point, frame)
            for point in ((low, low), (high, low), (high, high), (low, high))
        )
    )
    projected = tuple(project(point, frame) for point in points)
    axes: list[tuple[Stratum, ...]] = []
    masks: list[list[int]] = []
    for axis in (0, 1):
        lower, upper = (
            min(point[axis] for point in domain),
            max(point[axis] for point in domain),
        )
        events = [lower, upper]
        events.extend(
            value
            for point in projected
            for value in (point[axis] - HALF, point[axis] + HALF)
            if lower <= value <= upper
        )
        strata = _strata(events)
        axes.append(strata)
        masks.append(
            [
                sum(
                    1 << index
                    for index, point in enumerate(projected)
                    if point[axis] - HALF <= (item.low + item.high) / 2 <= point[axis] + HALF
                )
                for item in strata
            ]
        )
    zero, one = side.field.zero, side.field.one
    for i, u in enumerate(axes[0]):
        column = clip_polygon(clip_polygon(domain, (-one, zero, -u.low)), (one, zero, u.high))
        for j, v in enumerate(axes[1]):
            polygon = clip_polygon(
                clip_polygon(column, (zero, -one, -v.low)), (zero, one, v.high)
            )
            witness = cell_witness(polygon, u, v)
            if witness is not None:
                yield Cell(u, v, polygon, witness, masks[0][i] & masks[1][j])


def direct_membership(
    side: FieldElement,
    angle: int,
    center: Point,
    points: Sequence[Point],
    *,
    square_side: Fraction = Fraction(1),
    closed: bool = True,
) -> int:
    """Check containment and point membership by oriented corner determinants.

    This witness check does not use clipping, event ownership, or projection masks.
    An open square is a source box only when its side is strictly greater than one.
    """
    if type(square_side) is not Fraction or square_side <= 0:
        raise ValueError("witness side must be a positive exact Fraction")
    cosine, sine = direction(side, angle)
    x, y = center
    half = square_side / 2
    corners = tuple(
        (x + half * (a * cosine - b * sine), y + half * (a * sine + b * cosine))
        for a, b in ((-1, -1), (1, -1), (1, 1), (-1, 1))
    )
    if any(value < 0 or value > side for corner in corners for value in corner):
        raise ValueError("witness square fails exact corner containment")
    mask = 0
    for index, (px, py) in enumerate(points):
        determinants = []
        for (ax, ay), (bx, by) in pairwise((*corners, corners[0])):
            determinants.append((bx - ax) * (py - ay) - (by - ay) * (px - ax))
        if all(value.sign() >= (0 if closed else 1) for value in determinants):
            mask |= 1 << index
    return mask


def cover_replay(side: FieldElement, angle: int, points: Sequence[Point]) -> CoverResult:
    """Return a complete closed point-cover check or a directly checked escape."""
    counts = [0, 0, 0]
    escape = None
    frame = direction(side, angle)
    for cell in event_cells(side, angle, points):
        counts[cell.dimension] += 1
        if not cell.covered and escape is None:
            escape = unproject(cell.witness, frame)
            if direct_membership(side, angle, escape, points):
                raise ValueError("escape disagrees with independent determinant check")
    return CoverResult((counts[0], counts[1], counts[2]), escape)


def source_points(
    field: NumberField,
) -> tuple[FieldElement, tuple[Point, ...], tuple[Point, ...]]:
    """Original Theorem 3 coordinates, paper pages 10-11; no Theorem 2 repair."""
    side = 2 + Fraction(4, 3) * field.alpha
    ten, twelve = point_sets(side)
    return side, ten, twelve


def point_sets(side: FieldElement) -> tuple[tuple[Point, ...], tuple[Point, ...]]:
    """The unchanged coordinate formulas; another side is a separate auxiliary claim."""
    field = side.field
    one = field.one
    seeds = (
        (one, one),
        (side / 2, one),
        (Fraction(3, 2) - side / 4, side / 2),
        (HALF + side / 4, side / 2),
    )
    ten = tuple(
        sorted(
            {
                (side - x if flip_x else x, side - y if flip_y else y)
                for x, y in seeds
                for flip_x in (False, True)
                for flip_y in (False, True)
            }
        )
    )
    twelve = (
        (one, side - 3),
        (side / 2, side - 3),
        (field.rational("3/2"), field.rational("13/10")),
        (side - 1, one),
        (side - Fraction(4, 5), side / 2),
        (side - 1, side - 1),
        (side / 2, side - Fraction(4, 5)),
        (one, side - 1),
        (field.rational("4/5"), side - 2),
        (field.rational("17/10"), field.rational("11/5")),
        (field.rational("11/5"), field.rational("11/5")),
        (field.rational("11/5"), field.rational("17/10")),
    )
    if len(ten) != 10 or len(set(twelve)) != 12:
        raise ValueError("source point inventory is not ten and twelve distinct points")
    return ten, twelve


def region_witness(cell: Cell, constraints: Sequence[tuple[Plane, bool]]) -> Point | None:
    """Intersect with closed half-planes, then enforce any strict region edges."""
    polygon = cell.polygon
    for plane, _ in constraints:
        polygon = clip_polygon(polygon, plane)
    witness = cell_witness(polygon, cell.u, cell.v)
    if witness is None:
        return None
    for (a, b, bound), strict in constraints:
        if strict and (a * witness[0] + b * witness[1] - bound).sign() >= 0:
            return None
    return witness


def _checked_obstruction(
    name: str,
    side: FieldElement,
    angle: int,
    center: Point,
    *,
    ten: tuple[Point, ...],
    twelve: tuple[Point, ...],
) -> dict[str, object]:
    ten_mask = direct_membership(side, angle, center, ten)
    twelve_mask = direct_membership(side, angle, center, twelve)
    x, y = center
    if name.startswith("twelve"):
        valid = twelve_mask == 0
    elif name == "axis_ten_cover":
        valid = angle == 0 and ten_mask == 0
    elif name == "localization":
        localized = 1 <= x <= side - 1 and (y <= 1 or y >= side - 1)
        valid = angle == 45 and ten_mask == 0 and not localized
    else:
        index = int(name.removeprefix("forced_A")) - 1
        canonical = 1 <= x <= side / 2 and 0 <= y <= 1
        valid = angle == 45 and ten_mask == 0 and canonical and not twelve_mask & (1 << index)
    if not valid:
        raise ValueError(f"{name} witness disagrees with independent direct geometry")
    return {
        "obligation": name,
        "angle_degrees": angle,
        "center_power_basis": [x.text(), y.text()],
        "square_side": "1",
        "square_semantics": "closed",
        "ten_membership_mask": ten_mask,
        "twelve_membership_mask": twelve_mask,
        "direct_corner_and_determinant_check": True,
        "strict_box_counterexample_established": False,
    }


def replay_point_sets(
    side: FieldElement,
    ten: tuple[Point, ...],
    twelve: tuple[Point, ...],
    *,
    on_angle_complete: Callable[[dict[str, object]], None] | None = None,
) -> dict[str, object]:
    """Check all seven exact-angle auxiliary clauses; report only completed angles."""
    if len(ten) != 10 or len(twelve) != 12 or len(set(ten)) != 10 or len(set(twelve)) != 12:
        raise ValueError("point inventory must be ten and twelve distinct points")
    points = ten + twelve
    ten_mask = (1 << len(ten)) - 1
    twelve_mask = ((1 << len(twelve)) - 1) << len(ten)
    failures: dict[str, dict[str, object]] = {}
    cases: list[dict[str, object]] = []
    for angle in (0, 45):
        cosine, sine = frame = direction(side, angle)
        counts = [0, 0, 0]
        avoiders = canonical_avoiders = 0
        canonical = (
            ((-cosine, sine, -side.field.one), False),
            ((cosine, -sine, side / 2), False),
            ((sine, cosine, side.field.one), False),
        )
        outside_regions = (
            (((cosine, -sine, side.field.one), True),),
            (((-cosine, sine, 1 - side), True),),
            (((-sine, -cosine, -side.field.one), True), ((sine, cosine, side - 1), True)),
        )
        for cell in event_cells(side, angle, points):
            counts[cell.dimension] += 1
            cover_name = f"twelve_cover_{angle}"
            if not cell.covered & twelve_mask and cover_name not in failures:
                failures[cover_name] = _checked_obstruction(
                    cover_name,
                    side,
                    angle,
                    unproject(cell.witness, frame),
                    ten=ten,
                    twelve=twelve,
                )
            if cell.covered & ten_mask:
                continue
            avoiders += 1
            if angle == 0:
                if "axis_ten_cover" not in failures:
                    failures["axis_ten_cover"] = _checked_obstruction(
                        "axis_ten_cover",
                        side,
                        angle,
                        unproject(cell.witness, frame),
                        ten=ten,
                        twelve=twelve,
                    )
                continue
            if "localization" not in failures:
                for region in outside_regions:
                    witness = region_witness(cell, region)
                    if witness is not None:
                        failures["localization"] = _checked_obstruction(
                            "localization",
                            side,
                            angle,
                            unproject(witness, frame),
                            ten=ten,
                            twelve=twelve,
                        )
                        break
            witness = region_witness(cell, canonical)
            if witness is None:
                continue
            canonical_avoiders += 1
            for index in range(3):
                name = f"forced_A{index + 1}"
                if not cell.covered & (1 << (len(ten) + index)) and name not in failures:
                    failures[name] = _checked_obstruction(
                        name, side, angle, unproject(witness, frame), ten=ten, twelve=twelve
                    )
        if not sum(counts):
            raise ValueError("source replay reached no center stratum")
        case: dict[str, object] = {
            "angle_degrees": angle,
            "reachable_event_strata_by_dimension": counts,
            "ten_avoiding_strata": avoiders,
            "canonical_ten_avoiding_strata": canonical_avoiders,
        }
        cases.append(case)
        if on_angle_complete is not None:
            names = ANGLE_OBLIGATIONS[angle]
            on_angle_complete(
                {
                    "angle_degrees": angle,
                    "case": case,
                    "obligations": {name: name not in failures for name in names},
                    "obstructions": [failures[name] for name in names if name in failures],
                }
            )
    return {
        "complete": True,
        "status": "obstruction_retained" if failures else "pending_independent_review",
        "scope": "fixed-side exact-angle auxiliary clauses only",
        "field": "Q(sqrt(2)), positive root in (1,2)",
        "container_side_power_basis": side.text(),
        "point_counts": [len(ten), len(twelve)],
        "cases": cases,
        "obligations": {name: name not in failures for name in OBLIGATIONS},
        "obstructions": list(failures.values()),
        "strict_box_transfer": "a larger open box contains its concentric closed unit square",
        "theorem_acceptance": False,
    }


def source_replay() -> dict[str, object]:
    """Check the complete two-angle source control, retaining first obstructions."""
    result = replay_point_sets(*source_points(source_field()))
    result["scope"] = "Theorem 3 source control only; no H-036 target"
    return result


def main() -> None:
    """Print the fixed source replay; there are no target-side or angle arguments."""
    argparse.ArgumentParser(description=__doc__).parse_args()
    print(json.dumps(source_replay(), indent=2))


if __name__ == "__main__":
    main()
