"""Deterministic hue and shade assignment for packing squares."""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from decimal import ROUND_HALF_UP, Decimal, localcontext
from functools import cache

import mpmath as mp

from sqpack.render.model import (
    HueScheme,
    PackingFrame,
    RenderSpec,
    ShadeScheme,
    SquareGeometry,
)
from sqpack.render.style import SQUARE_HUE_PALETTE

SHADE_ADJACENCY_TOLERANCE = Decimal("0.002")
FULL_SIDE_CONTACT_TOLERANCE = Decimal("0.002")
ANGLE_WORKING_DIGITS = 60
QUARTER_TURN_RADIANS = Decimal("1.57079632679489661923132169163975144209858469968755291048747")


@dataclass(frozen=True)
class SquareColor:
    fill: str
    hue_index: int
    shade_index: int
    angle_class: int | None
    contact_sides: int | None


def _hue_slots(count: int) -> tuple[int, ...]:
    """Order even hue-wheel slots by farthest-point separation."""
    if count <= 0:
        raise ValueError("hue count must be positive")
    selected = [(count + 1) // 3 % count]
    remaining = set(range(count)) - set(selected)
    while remaining:
        slot = max(
            remaining,
            key=lambda candidate: (
                min(
                    min(abs(candidate - existing), count - abs(candidate - existing))
                    for existing in selected
                ),
                -candidate,
            ),
        )
        selected.append(slot)
        remaining.remove(slot)
    return tuple(selected)


def _shade_lightnesses(count: int, *, base: Decimal, span: Decimal) -> tuple[Decimal, ...]:
    if count <= 0:
        raise ValueError("shade count must be positive")
    if count == 1:
        return (base,)
    step = span / Decimal(count - 1)
    minimum = base - span / 2
    return tuple(minimum + step * index for index in range(count))


def _channel(value: Decimal) -> int:
    bounded = min(Decimal(1), max(Decimal(0), value))
    return int((bounded * 255).quantize(Decimal(1), rounding=ROUND_HALF_UP))


def _hsl_hex(*, hue_sector: Decimal, saturation: Decimal, lightness: Decimal) -> str:
    sector = int(hue_sector) % 6
    chroma = (Decimal(1) - abs(Decimal(2) * lightness - Decimal(1))) * saturation
    x = chroma * (Decimal(1) - abs((hue_sector % Decimal(2)) - Decimal(1)))
    red, green, blue = {
        0: (chroma, x, Decimal(0)),
        1: (x, chroma, Decimal(0)),
        2: (Decimal(0), chroma, x),
        3: (Decimal(0), x, chroma),
        4: (x, Decimal(0), chroma),
        5: (chroma, Decimal(0), x),
    }[sector]
    match = lightness - chroma / Decimal(2)
    channels = (_channel(red + match), _channel(green + match), _channel(blue + match))
    return f"#{channels[0]:02x}{channels[1]:02x}{channels[2]:02x}"


def _hex_hsl(fill: str) -> tuple[Decimal, Decimal, Decimal]:
    red, green, blue = (
        Decimal(int(fill[offset : offset + 2], 16)) / 255 for offset in (1, 3, 5)
    )
    maximum = max(red, green, blue)
    minimum = min(red, green, blue)
    lightness = (maximum + minimum) / 2
    difference = maximum - minimum
    if difference.is_zero():
        return Decimal(0), Decimal(0), lightness
    saturation = difference / (Decimal(1) - abs(Decimal(2) * lightness - Decimal(1)))
    if maximum == red:
        hue_sector = ((green - blue) / difference) % Decimal(6)
    elif maximum == green:
        hue_sector = (blue - red) / difference + 2
    else:
        hue_sector = (red - green) / difference + 4
    return hue_sector, saturation, lightness


LEGACY_HSL_PALETTE = tuple(_hex_hsl(fill) for fill in SQUARE_HUE_PALETTE)


def _base_hsl_palette(hue_count: int) -> tuple[tuple[Decimal, Decimal, Decimal], ...]:
    if hue_count <= len(LEGACY_HSL_PALETTE):
        return LEGACY_HSL_PALETTE[:hue_count]
    slots = _hue_slots(hue_count)
    return tuple(
        (
            Decimal(6 * slot) / Decimal(hue_count),
            LEGACY_HSL_PALETTE[index % len(LEGACY_HSL_PALETTE)][1],
            LEGACY_HSL_PALETTE[index % len(LEGACY_HSL_PALETTE)][2],
        )
        for index, slot in enumerate(slots)
    )


@cache
def square_fill_palette(
    *,
    hue_count: int,
    shades_per_hue: int,
    lightness_span: Decimal = Decimal("0.2"),
) -> tuple[tuple[str, ...], ...]:
    """Derive stable, narrow shade families from the original fill palette."""
    if hue_count <= 0:
        raise ValueError("hue count must be positive")
    if not lightness_span.is_finite() or not Decimal(0) <= lightness_span <= Decimal("0.3"):
        raise ValueError("lightness span must be between 0 and 0.3")
    return tuple(
        tuple(
            _hsl_hex(
                hue_sector=hue_sector,
                saturation=saturation,
                lightness=lightness,
            )
            for lightness in _shade_lightnesses(
                shades_per_hue,
                base=base_lightness,
                span=lightness_span,
            )
        )
        for hue_sector, saturation, base_lightness in _base_hsl_palette(hue_count)
    )


def _square_orientation(square: SquareGeometry) -> Decimal:
    with mp.workdps(ANGLE_WORKING_DIGITS):
        if square.pose is not None:
            angle = mp.mpf(str(square.pose.angle.projected))
        else:
            first, second = square.corners[:2]
            edge_x = mp.mpf(str(second.x.projected - first.x.projected))
            edge_y = mp.mpf(str(second.y.projected - first.y.projected))
            angle = mp.atan2(edge_y, edge_x)
        quarter = mp.pi / 2
        orientation = mp.fmod(angle, quarter)
        if orientation < 0:
            orientation += quarter
        return Decimal(str(mp.nstr(orientation, ANGLE_WORKING_DIGITS - 5)))


def _orientation_distance(left: Decimal, right: Decimal) -> Decimal:
    difference = abs(left - right)
    return min(difference, QUARTER_TURN_RADIANS - difference)


def _angle_classes(
    frame: PackingFrame, *, tolerance: Decimal
) -> tuple[tuple[tuple[int, ...], ...], tuple[Decimal, ...]]:
    classes: list[list[int]] = []
    representatives: list[Decimal] = []
    orientations: list[Decimal] = []
    for index, square in enumerate(frame.squares):
        orientation = _square_orientation(square)
        orientations.append(orientation)
        matching = next(
            (
                class_index
                for class_index, representative in enumerate(representatives)
                if _orientation_distance(orientation, representative) <= tolerance
            ),
            None,
        )
        if matching is None:
            representatives.append(orientation)
            classes.append([index])
        else:
            classes[matching].append(index)
    return tuple(tuple(members) for members in classes), tuple(orientations)


def _center(square: SquareGeometry) -> tuple[Decimal, Decimal]:
    return (
        sum((point.x.projected for point in square.corners), Decimal(0)) / 4,
        sum((point.y.projected for point in square.corners), Decimal(0)) / 4,
    )


def _basis(square: SquareGeometry) -> tuple[Decimal, Decimal]:
    first, second = square.corners[:2]
    edge_x = second.x.projected - first.x.projected
    edge_y = second.y.projected - first.y.projected
    with localcontext() as context:
        context.prec = max(
            40,
            first.x.precision,
            first.y.precision,
            second.x.precision,
            second.y.precision,
        )
        length = (edge_x * edge_x + edge_y * edge_y).sqrt()
        if length.is_zero():
            raise ValueError("square edge must be nondegenerate")
        return edge_x / length, edge_y / length


def _edges(
    square: SquareGeometry,
) -> tuple[
    tuple[tuple[Decimal, Decimal], tuple[Decimal, Decimal]],
    ...,
]:
    points = tuple((point.x.projected, point.y.projected) for point in square.corners)
    return tuple((points[index], points[(index + 1) % 4]) for index in range(4))


def _points_close(left: tuple[Decimal, Decimal], right: tuple[Decimal, Decimal]) -> bool:
    return all(
        abs(left_coordinate - right_coordinate) <= FULL_SIDE_CONTACT_TOLERANCE
        for left_coordinate, right_coordinate in zip(left, right, strict=True)
    )


def _edges_fully_flush(
    left: tuple[tuple[Decimal, Decimal], tuple[Decimal, Decimal]],
    right: tuple[tuple[Decimal, Decimal], tuple[Decimal, Decimal]],
) -> bool:
    return (_points_close(left[0], right[0]) and _points_close(left[1], right[1])) or (
        _points_close(left[0], right[1]) and _points_close(left[1], right[0])
    )


def _edge_on_container_wall(
    edge: tuple[tuple[Decimal, Decimal], tuple[Decimal, Decimal]],
    *,
    container_side: Decimal,
) -> bool:
    return any(
        all(abs(point[axis] - boundary) <= FULL_SIDE_CONTACT_TOLERANCE for point in edge)
        for axis in (0, 1)
        for boundary in (Decimal(0), container_side)
    )


def _full_side_contact_counts(frame: PackingFrame) -> dict[int, int]:
    square_edges = tuple(_edges(square) for square in frame.squares)
    counts: dict[int, int] = {}
    for square_index, edges in enumerate(square_edges):
        count = 0
        for edge in edges:
            if _edge_on_container_wall(edge, container_side=frame.container_side.projected):
                count += 1
                continue
            if any(
                _edges_fully_flush(edge, other_edge)
                for other_index, other_edges in enumerate(square_edges)
                if other_index != square_index
                for other_edge in other_edges
            ):
                count += 1
        counts[square_index] = count
    return counts


def _positive_edge_neighbors(
    left_center: tuple[Decimal, Decimal],
    right_center: tuple[Decimal, Decimal],
    left_basis: tuple[Decimal, Decimal],
    left_orientation: Decimal,
    right_orientation: Decimal,
    *,
    angle_tolerance: Decimal,
) -> bool:
    if _orientation_distance(left_orientation, right_orientation) > angle_tolerance:
        return False
    left_x, left_y = left_center
    right_x, right_y = right_center
    axis_x, axis_y = left_basis
    delta_x, delta_y = right_x - left_x, right_y - left_y
    along = abs(delta_x * axis_x + delta_y * axis_y)
    across = abs(-delta_x * axis_y + delta_y * axis_x)
    tolerance = SHADE_ADJACENCY_TOLERANCE
    return (abs(along - Decimal(1)) <= tolerance and across < Decimal(1) - tolerance) or (
        abs(across - Decimal(1)) <= tolerance and along < Decimal(1) - tolerance
    )


def _shade_order(count: int) -> tuple[int, ...]:
    result: list[int] = []
    low, high = 0, count - 1
    while low <= high:
        result.append(low)
        if low != high:
            result.append(high)
        low += 1
        high -= 1
    return tuple(result)


def _shade_score(
    shade: int,
    *,
    neighbor_shades: tuple[int, ...],
    usage: list[int],
    shades_per_hue: int,
    rank: dict[int, int],
) -> tuple[int, int, int, int, int]:
    distances = [abs(shade - neighbor) for neighbor in neighbor_shades]
    return (
        -sum(shade == neighbor for neighbor in neighbor_shades),
        -usage[shade],
        min(distances, default=shades_per_hue),
        sum(distances),
        -rank[shade],
    )


def _contrast_shades(
    frame: PackingFrame,
    groups: dict[int, list[int]],
    *,
    shades_per_hue: int,
    angle_tolerance: Decimal,
    orientations: tuple[Decimal, ...],
) -> dict[int, int]:
    assignments: dict[int, int] = {}
    order = _shade_order(shades_per_hue)
    rank = {shade: index for index, shade in enumerate(order)}
    centers = tuple(_center(square) for square in frame.squares)
    bases = tuple(_basis(square) for square in frame.squares)
    for members in groups.values():
        neighbors = {index: set() for index in members}
        for position, left in enumerate(members):
            for right in members[position + 1 :]:
                if _positive_edge_neighbors(
                    centers[left],
                    centers[right],
                    bases[left],
                    orientations[left],
                    orientations[right],
                    angle_tolerance=angle_tolerance,
                ):
                    neighbors[left].add(right)
                    neighbors[right].add(left)
        usage = [0] * shades_per_hue
        remaining = set(members)
        while remaining:
            square_index = max(
                remaining,
                key=lambda index: (
                    len(
                        {
                            assignments[neighbor]
                            for neighbor in neighbors[index]
                            if neighbor in assignments
                        }
                    ),
                    len(neighbors[index]),
                    -index,
                ),
            )
            neighbor_shades = tuple(
                assignments[neighbor]
                for neighbor in neighbors[square_index]
                if neighbor in assignments
            )
            shade = max(
                range(shades_per_hue),
                key=lambda candidate: _shade_score(
                    candidate,
                    neighbor_shades=neighbor_shades,
                    usage=usage,
                    shades_per_hue=shades_per_hue,
                    rank=rank,
                ),
            )
            assignments[square_index] = shade
            usage[shade] += 1
            remaining.remove(square_index)
    return assignments


def _contact_shade(contact_sides: int, *, shades_per_hue: int) -> int:
    if not 0 <= contact_sides <= 4:
        raise ValueError("full-side contact count must be between zero and four")
    if shades_per_hue == 1:
        return 0
    scaled = Decimal(4 - contact_sides) * Decimal(shades_per_hue - 1) / Decimal(4)
    return int(scaled.quantize(Decimal(1), rounding=ROUND_HALF_UP))


def assign_square_colors(frame: PackingFrame, spec: RenderSpec) -> dict[str, SquareColor]:
    """Assign one deterministic color to every square in stable frame order."""
    if spec.hue_count <= 0 or spec.shades_per_hue <= 0:
        raise ValueError("color hue and shade counts must be positive")
    if not spec.angle_tolerance_radians.is_finite() or spec.angle_tolerance_radians <= 0:
        raise ValueError("color angle tolerance must be finite and positive")
    if (
        not spec.shade_lightness_span.is_finite()
        or spec.shade_lightness_span < 0
        or spec.shade_lightness_span > Decimal("0.3")
    ):
        raise ValueError("color shade lightness span must be between 0 and 0.3")

    angle_classes: tuple[tuple[int, ...], ...] = ()
    class_by_square: dict[int, int] = {}
    if spec.hue_scheme is HueScheme.ANGLE:
        angle_classes, orientations = _angle_classes(
            frame, tolerance=spec.angle_tolerance_radians
        )
        class_by_square = {
            square_index: class_index
            for class_index, members in enumerate(angle_classes)
            for square_index in members
        }
        hue_by_square = {
            index: class_by_square[index] % spec.hue_count
            for index in range(len(frame.squares))
        }
        shade_groups = {index: list(members) for index, members in enumerate(angle_classes)}
    else:
        orientations = tuple(_square_orientation(square) for square in frame.squares)
        hue_by_square = {index: index % spec.hue_count for index in range(len(frame.squares))}
        shade_groups = defaultdict(list)
        for index, hue in hue_by_square.items():
            shade_groups[hue].append(index)

    contact_sides_by_square: dict[int, int] = {}
    if spec.shade_scheme is ShadeScheme.CONTACTS:
        contact_sides_by_square = _full_side_contact_counts(frame)
        shade_by_square = {
            index: _contact_shade(contact_sides, shades_per_hue=spec.shades_per_hue)
            for index, contact_sides in contact_sides_by_square.items()
        }
    elif spec.shade_scheme is ShadeScheme.CONTRAST:
        shade_by_square = _contrast_shades(
            frame,
            dict(shade_groups),
            shades_per_hue=spec.shades_per_hue,
            angle_tolerance=spec.angle_tolerance_radians,
            orientations=orientations,
        )
    else:
        shade_by_square = {}
        for members in shade_groups.values():
            for occurrence, square_index in enumerate(members):
                shade_by_square[square_index] = occurrence % spec.shades_per_hue

    palette = square_fill_palette(
        hue_count=spec.hue_count,
        shades_per_hue=spec.shades_per_hue,
        lightness_span=spec.shade_lightness_span,
    )
    return {
        square.square_id: SquareColor(
            fill=palette[hue_by_square[index]][shade_by_square[index]],
            hue_index=hue_by_square[index],
            shade_index=shade_by_square[index],
            angle_class=(
                class_by_square[index] if spec.hue_scheme is HueScheme.ANGLE else None
            ),
            contact_sides=contact_sides_by_square.get(index),
        )
        for index, square in enumerate(frame.squares)
    }
