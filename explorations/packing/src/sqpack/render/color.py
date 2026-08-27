"""Deterministic hue and shade assignment for packing squares."""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
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
ANGLE_WORKING_DIGITS = 60
QUARTER_TURN_RADIANS = Decimal("1.57079632679489661923132169163975144209858469968755291048747")
ANGLE_CLASS_CONTRACT = "tolerance-seeded; strict-full-side contacts merged"


@dataclass(frozen=True)
class SideContact:
    contact_id: str
    residual: Decimal


@dataclass(frozen=True)
class SquareColor:
    fill: str
    hue_index: int
    shade_index: int
    orientation_radians: Decimal
    angle_class: int | None
    angle_class_residual_radians: Decimal | None
    contact_sides: int | None
    full_side_contacts: tuple[str, ...]
    maximum_contact_residual: Decimal | None


@dataclass
class AngleHueRegistry:
    """Share angle-class hue identities across panels in one render."""

    hue_count: int
    angle_tolerance_radians: Decimal
    _representatives: list[Decimal] = field(default_factory=list)

    def hues_for(self, representatives: tuple[Decimal, ...]) -> tuple[int, ...]:
        """Return stable hues, preferring the closest earlier class match."""
        registrations: list[int | None] = [None] * len(representatives)
        used_registrations: set[int] = set()
        candidates = sorted(
            (
                (_orientation_distance(representative, registered), current, previous)
                for current, representative in enumerate(representatives)
                for previous, registered in enumerate(self._representatives)
                if _orientation_distance(representative, registered)
                <= self.angle_tolerance_radians
            )
        )
        for _distance, current, previous in candidates:
            if registrations[current] is None and previous not in used_registrations:
                registrations[current] = previous
                used_registrations.add(previous)
        for current, representative in enumerate(representatives):
            if registrations[current] is None:
                registrations[current] = len(self._representatives)
                self._representatives.append(representative)
        return tuple(
            registration % self.hue_count
            for registration in registrations
            if registration is not None
        )


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
        hue_sector = (green - blue) / difference
        if hue_sector < 0:
            hue_sector += Decimal(6)
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


def _orientation_representative(
    orientations: tuple[Decimal, ...], members: tuple[int, ...] | list[int]
) -> Decimal:
    """Return a seam-safe mean orientation modulo one quarter turn."""
    with localcontext() as context:
        context.prec = ANGLE_WORKING_DIGITS
        anchor = orientations[members[0]]
        half_turn = QUARTER_TURN_RADIANS / 2
        offsets: list[Decimal] = []
        for member in members:
            offset = orientations[member] - anchor
            if offset > half_turn:
                offset -= QUARTER_TURN_RADIANS
            elif offset < -half_turn:
                offset += QUARTER_TURN_RADIANS
            offsets.append(offset)
        representative = anchor + sum(offsets, Decimal(0)) / Decimal(len(offsets))
        representative %= QUARTER_TURN_RADIANS
        if representative < 0:
            representative += QUARTER_TURN_RADIANS
        return representative


def _angle_classes(
    orientations: tuple[Decimal, ...], *, tolerance: Decimal
) -> tuple[
    tuple[tuple[int, ...], ...],
    tuple[Decimal, ...],
    tuple[Decimal, ...],
]:
    classes: list[list[int]] = []
    seed_representatives: list[Decimal] = []
    for index, orientation in enumerate(orientations):
        matching = next(
            (
                class_index
                for class_index, representative in enumerate(seed_representatives)
                if _orientation_distance(orientation, representative) <= tolerance
            ),
            None,
        )
        if matching is None:
            seed_representatives.append(orientation)
            classes.append([index])
        else:
            classes[matching].append(index)
    frozen_classes = tuple(tuple(members) for members in classes)
    return (
        frozen_classes,
        orientations,
        tuple(_orientation_representative(orientations, members) for members in frozen_classes),
    )


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


def _edge_match_residual(
    left: tuple[tuple[Decimal, Decimal], tuple[Decimal, Decimal]],
    right: tuple[tuple[Decimal, Decimal], tuple[Decimal, Decimal]],
) -> Decimal:
    direct = max(
        abs(left[endpoint][axis] - right[endpoint][axis])
        for endpoint in range(2)
        for axis in range(2)
    )
    reverse = max(
        abs(left[endpoint][axis] - right[1 - endpoint][axis])
        for endpoint in range(2)
        for axis in range(2)
    )
    return min(direct, reverse)


def _edge_wall_candidates(
    edge: tuple[tuple[Decimal, Decimal], tuple[Decimal, Decimal]],
    *,
    container_side: Decimal,
) -> tuple[SideContact, ...]:
    return tuple(
        SideContact(
            contact_id=f"wall-{name}",
            residual=max(abs(point[axis] - boundary) for point in edge),
        )
        for name, axis, boundary in (
            ("left", 0, Decimal(0)),
            ("right", 0, container_side),
            ("bottom", 1, Decimal(0)),
            ("top", 1, container_side),
        )
    )


def _full_side_contacts(
    frame: PackingFrame,
    *,
    orientations: tuple[Decimal, ...],
    angle_tolerance: Decimal,
    contact_tolerance: Decimal,
) -> dict[int, tuple[SideContact, ...]]:
    square_edges = tuple(_edges(square) for square in frame.squares)
    candidates: dict[int, list[list[SideContact]]] = {
        index: [[] for _edge in edges] for index, edges in enumerate(square_edges)
    }
    for square_index, edges in enumerate(square_edges):
        if _orientation_distance(orientations[square_index], Decimal(0)) > angle_tolerance:
            continue
        for edge_index, edge in enumerate(edges):
            candidates[square_index][edge_index].extend(
                contact
                for contact in _edge_wall_candidates(
                    edge, container_side=frame.container_side.projected
                )
                if contact.residual <= contact_tolerance
            )
    for left_index, left_edges in enumerate(square_edges):
        for right_index in range(left_index + 1, len(square_edges)):
            if (
                _orientation_distance(orientations[left_index], orientations[right_index])
                > angle_tolerance
            ):
                continue
            for left_edge_index, left_edge in enumerate(left_edges):
                for right_edge_index, right_edge in enumerate(square_edges[right_index]):
                    residual = _edge_match_residual(left_edge, right_edge)
                    if residual > contact_tolerance:
                        continue
                    candidates[left_index][left_edge_index].append(
                        SideContact(frame.squares[right_index].square_id, residual)
                    )
                    candidates[right_index][right_edge_index].append(
                        SideContact(frame.squares[left_index].square_id, residual)
                    )
    return {
        square_index: tuple(
            min(edge_candidates, key=lambda contact: (contact.residual, contact.contact_id))
            for edge_candidates in edge_candidate_groups
            if edge_candidates
        )
        for square_index, edge_candidate_groups in candidates.items()
    }


def _merge_contact_angle_classes(
    classes: tuple[tuple[int, ...], ...],
    *,
    orientations: tuple[Decimal, ...],
    contacts_by_square: dict[int, tuple[SideContact, ...]],
    square_ids: tuple[str, ...],
) -> tuple[tuple[tuple[int, ...], ...], tuple[Decimal, ...]]:
    """Merge tolerance-seeded classes when full-side geometry proves alignment."""
    class_by_square = {
        square_index: class_index
        for class_index, members in enumerate(classes)
        for square_index in members
    }
    square_by_id = {square_id: index for index, square_id in enumerate(square_ids)}
    parents = list(range(len(classes)))

    def find(class_index: int) -> int:
        while parents[class_index] != class_index:
            parents[class_index] = parents[parents[class_index]]
            class_index = parents[class_index]
        return class_index

    def union(left: int, right: int) -> None:
        left_root = find(left)
        right_root = find(right)
        if left_root != right_root:
            parents[max(left_root, right_root)] = min(left_root, right_root)

    wall_class: int | None = None
    for square_index, contacts in contacts_by_square.items():
        square_class = class_by_square[square_index]
        for contact in contacts:
            if contact.contact_id.startswith("wall-"):
                if wall_class is None:
                    wall_class = square_class
                else:
                    union(wall_class, square_class)
                continue
            union(square_class, class_by_square[square_by_id[contact.contact_id]])

    merged_by_root: dict[int, list[int]] = defaultdict(list)
    for class_index, members in enumerate(classes):
        merged_by_root[find(class_index)].extend(members)
    merged_classes = tuple(
        tuple(sorted(members))
        for _root, members in sorted(merged_by_root.items(), key=lambda item: min(item[1]))
    )
    return (
        merged_classes,
        tuple(_orientation_representative(orientations, members) for members in merged_classes),
    )


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


def assign_square_colors(
    frame: PackingFrame,
    spec: RenderSpec,
    *,
    angle_hue_registry: AngleHueRegistry | None = None,
) -> dict[str, SquareColor]:
    """Assign one deterministic color to every square in stable frame order."""
    if spec.hue_count <= 0 or spec.shades_per_hue <= 0:
        raise ValueError("color hue and shade counts must be positive")
    if not spec.angle_tolerance_radians.is_finite() or spec.angle_tolerance_radians <= 0:
        raise ValueError("color angle tolerance must be finite and positive")
    if (
        not spec.full_side_contact_tolerance.is_finite()
        or spec.full_side_contact_tolerance <= 0
    ):
        raise ValueError("full-side contact tolerance must be finite and positive")
    if (
        not spec.shade_lightness_span.is_finite()
        or spec.shade_lightness_span < 0
        or spec.shade_lightness_span > Decimal("0.3")
    ):
        raise ValueError("color shade lightness span must be between 0 and 0.3")
    if angle_hue_registry is not None and (
        angle_hue_registry.hue_count != spec.hue_count
        or angle_hue_registry.angle_tolerance_radians != spec.angle_tolerance_radians
    ):
        raise ValueError("angle hue registry must match the render color contract")

    orientations = tuple(_square_orientation(square) for square in frame.squares)
    contacts_by_square = _full_side_contacts(
        frame,
        orientations=orientations,
        angle_tolerance=spec.angle_tolerance_radians,
        contact_tolerance=spec.full_side_contact_tolerance,
    )

    angle_classes: tuple[tuple[int, ...], ...] = ()
    class_by_square: dict[int, int] = {}
    representatives: tuple[Decimal, ...] = ()
    if spec.hue_scheme is HueScheme.ANGLE:
        angle_classes, _, _ = _angle_classes(
            orientations, tolerance=spec.angle_tolerance_radians
        )
        angle_classes, representatives = _merge_contact_angle_classes(
            angle_classes,
            orientations=orientations,
            contacts_by_square=contacts_by_square,
            square_ids=tuple(square.square_id for square in frame.squares),
        )
        class_by_square = {
            square_index: class_index
            for class_index, members in enumerate(angle_classes)
            for square_index in members
        }
        class_hues = (
            angle_hue_registry.hues_for(representatives)
            if angle_hue_registry is not None
            else tuple(index % spec.hue_count for index in range(len(angle_classes)))
        )
        hue_by_square = {
            index: class_hues[class_by_square[index]] for index in range(len(frame.squares))
        }
        shade_groups = {index: list(members) for index, members in enumerate(angle_classes)}
    else:
        hue_by_square = {index: index % spec.hue_count for index in range(len(frame.squares))}
        shade_groups = defaultdict(list)
        for index, hue in hue_by_square.items():
            shade_groups[hue].append(index)

    contact_sides_by_square = {
        index: len(contacts) for index, contacts in contacts_by_square.items()
    }
    if spec.shade_scheme is ShadeScheme.CONTACTS:
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
            orientation_radians=orientations[index],
            angle_class=(
                class_by_square[index] if spec.hue_scheme is HueScheme.ANGLE else None
            ),
            angle_class_residual_radians=(
                _orientation_distance(
                    orientations[index], representatives[class_by_square[index]]
                )
                if spec.hue_scheme is HueScheme.ANGLE
                else None
            ),
            contact_sides=contact_sides_by_square[index],
            full_side_contacts=tuple(
                contact.contact_id for contact in contacts_by_square.get(index, ())
            ),
            maximum_contact_residual=(
                max(contact.residual for contact in contacts_by_square[index])
                if contacts_by_square.get(index)
                else None
            ),
        )
        for index, square in enumerate(frame.squares)
    }
