"""Deterministic hue and shade assignment for packing squares."""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
from decimal import ROUND_CEILING, ROUND_FLOOR, ROUND_HALF_UP, Decimal, localcontext
from functools import cache
from math import atan2, cos, degrees, hypot, radians, sin

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
HALF_QUARTER_RADIANS = QUARTER_TURN_RADIANS / 2
RIGHT_ANGLE_HUE = 0
DIAGONAL_HUE = 1
RESERVED_HUES = 2
HUE_ORDER_CONTRACT = (
    "right angles pinned to hue 0; 45 degree tilts pinned to hue 1; "
    "remaining classes assigned from hue 2 by descending class size"
)

# Shade ramp. Lightness is compressed toward a mid band so no family is very dark
# or very pale, which matters because the four-contact shade carpets dense
# packings. Saturation CLIMBS with lightness (a negative drop): raising HSL
# lightness already costs chroma, so letting saturation fall too would grey the
# few-contact shades out.
SHADE_LIGHTNESS_CENTER = Decimal("0.52")
SHADE_LIGHTNESS_COMPRESSION = Decimal("0.85")
SHADE_SATURATION_FLOOR = Decimal("0.50")
SHADE_SATURATION_CAP = Decimal("0.85")
SHADE_SATURATION_DROP = Decimal("-0.12")
# The two darkest shades carry most of the atlas and are already where they want
# to be, so the ramp is widened only at the light end: shade i above the second
# is lifted by this much per step. Keeps the dark end fixed while opening a
# little more air between the lighter three.
SHADE_LIGHT_SPREAD = Decimal("0.015")


def _spread_light_end(lightnesses: tuple[Decimal, ...]) -> tuple[Decimal, ...]:
    """Push the shades above the second progressively lighter."""
    return tuple(
        lightness + SHADE_LIGHT_SPREAD * Decimal(max(0, index - 1))
        for index, lightness in enumerate(lightnesses)
    )


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
    reserved: int = RESERVED_HUES
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
        span = self.hue_count - self.reserved
        return tuple(
            self.reserved + registration % span
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


@dataclass(frozen=True)
class PerceptualRamp:
    """A shade ramp stated in OkLCh instead of HSL.

    Equal steps in HSL lightness are not equal steps in perceived lightness, and
    the error is worst for hues that already sit near the top of the luminance
    range. Slot 1's yellow-green travelled only 0.072 OkL across its five shades
    where slot 0's travelled 0.185, so its shades were nearly indistinguishable.
    Both pinned families therefore state their range perceptually. Chroma is
    clamped per shade to what the sRGB gamut holds at that lightness.
    """

    dark_end: Decimal
    light_end: Decimal
    chroma: Decimal


# Keyed by hue index. Only the two pinned families need this; every other family
# uses the HSL ramp, which is well behaved at their lightnesses.
PERCEPTUAL_SHADE_RAMPS = {
    0: PerceptualRamp(Decimal("0.50"), Decimal("0.70"), Decimal("0.080")),
    1: PerceptualRamp(Decimal("0.68"), Decimal("0.862"), Decimal("0.150")),
}


def _srgb_to_linear(channel: float) -> float:
    return channel / 12.92 if channel <= 0.04045 else ((channel + 0.055) / 1.055) ** 2.4


def _linear_to_srgb(channel: float) -> float:
    return 12.92 * channel if channel <= 0.0031308 else 1.055 * channel ** (1 / 2.4) - 0.055


def hex_oklch(fill: str) -> tuple[float, float, float]:
    """Convert an sRGB hex fill to OkLCh lightness, chroma and hue degrees."""
    red, green, blue = (
        _srgb_to_linear(int(fill[offset : offset + 2], 16) / 255) for offset in (1, 3, 5)
    )
    long = (0.4122214708 * red + 0.5363325363 * green + 0.0514459929 * blue) ** (1 / 3)
    medium = (0.2119034982 * red + 0.6806995451 * green + 0.1073969566 * blue) ** (1 / 3)
    short = (0.0883024619 * red + 0.2817188376 * green + 0.6299787005 * blue) ** (1 / 3)
    lightness = 0.2104542553 * long + 0.7936177850 * medium - 0.0040720468 * short
    green_red = 1.9779984951 * long - 2.4285922050 * medium + 0.4505937099 * short
    blue_yellow = 0.0259040371 * long + 0.7827717662 * medium - 0.8086757660 * short
    return (
        lightness,
        hypot(green_red, blue_yellow),
        degrees(atan2(blue_yellow, green_red)) % 360,
    )


def _oklch_linear_rgb(
    lightness: float, chroma: float, hue: float
) -> tuple[float, float, float]:
    green_red = chroma * cos(radians(hue))
    blue_yellow = chroma * sin(radians(hue))
    long = (lightness + 0.3963377774 * green_red + 0.2158037573 * blue_yellow) ** 3
    medium = (lightness - 0.1055613458 * green_red - 0.0638541728 * blue_yellow) ** 3
    short = (lightness - 0.0894841775 * green_red - 1.2914855480 * blue_yellow) ** 3
    return (
        4.0767416621 * long - 3.3077115913 * medium + 0.2309699292 * short,
        -1.2684380046 * long + 2.6097574011 * medium - 0.3413193965 * short,
        -0.0041960863 * long - 0.7034186147 * medium + 1.7076147010 * short,
    )


def _oklch_hex(lightness: float, chroma: float, hue: float) -> str:
    channels = []
    for value in _oklch_linear_rgb(lightness, chroma, hue):
        bounded = _linear_to_srgb(min(1.0, max(0.0, value)))
        channels.append(min(255, max(0, round(bounded * 255))))
    return f"#{channels[0]:02x}{channels[1]:02x}{channels[2]:02x}"


def _maximum_chroma(lightness: float, hue: float) -> float:
    """Largest chroma this hue holds at this lightness inside sRGB."""
    low, high = 0.0, 0.45
    for _step in range(48):
        middle = (low + high) / 2
        if all(-1e-4 <= c <= 1 + 1e-4 for c in _oklch_linear_rgb(lightness, middle, hue)):
            low = middle
        else:
            high = middle
    return low


def _perceptual_family(fill: str, ramp: PerceptualRamp, count: int) -> tuple[str, ...]:
    hue = hex_oklch(fill)[2]
    if count == 1:
        return (_oklch_hex(float(ramp.light_end), float(ramp.chroma), hue),)
    dark, light = float(ramp.dark_end), float(ramp.light_end)
    step = (light - dark) / (count - 1)
    lightnesses = _spread_light_end(
        tuple(Decimal(str(dark + step * index)) for index in range(count))
    )
    return tuple(
        _oklch_hex(
            float(lightness),
            min(float(ramp.chroma), 0.95 * _maximum_chroma(float(lightness), hue)),
            hue,
        )
        for lightness in lightnesses
    )


def _shade_lightnesses(count: int, *, base: Decimal, span: Decimal) -> tuple[Decimal, ...]:
    """Lightness ramp for one family, compressed toward the mid band."""
    if count <= 0:
        raise ValueError("shade count must be positive")
    centered = (
        SHADE_LIGHTNESS_CENTER + (base - SHADE_LIGHTNESS_CENTER) * SHADE_LIGHTNESS_COMPRESSION
    )
    if count == 1:
        return (centered,)
    step = span / Decimal(count - 1)
    minimum = centered - span / 4
    return _spread_light_end(tuple(minimum + step * index for index in range(count)))


def _shade_saturations(count: int, *, base: Decimal) -> tuple[Decimal, ...]:
    """Saturation across one family, climbing with lightness."""
    if count <= 0:
        raise ValueError("shade count must be positive")
    saturation = min(max(base, SHADE_SATURATION_FLOOR), SHADE_SATURATION_CAP)
    if count == 1:
        return (saturation,)
    return tuple(
        min(
            Decimal(1),
            max(
                Decimal("0.05"),
                saturation
                * (Decimal(1) - SHADE_SATURATION_DROP * (Decimal(index) / Decimal(count - 1))),
            ),
        )
        for index in range(count)
    )


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
    """Derive one shade family per hue from the fixed base palette."""
    if hue_count <= 0:
        raise ValueError("hue count must be positive")
    if shades_per_hue <= 0:
        raise ValueError("shade count must be positive")
    if not lightness_span.is_finite() or not Decimal(0) <= lightness_span <= Decimal("0.3"):
        raise ValueError("lightness span must be between 0 and 0.3")
    families: list[tuple[str, ...]] = []
    for index, (hue_sector, saturation, base_lightness) in enumerate(
        _base_hsl_palette(hue_count)
    ):
        ramp = PERCEPTUAL_SHADE_RAMPS.get(index)
        if ramp is not None:
            families.append(
                _perceptual_family(
                    _hsl_hex(
                        hue_sector=hue_sector,
                        saturation=saturation,
                        lightness=base_lightness,
                    ),
                    ramp,
                    shades_per_hue,
                )
            )
            continue
        families.append(
            tuple(
                _hsl_hex(
                    hue_sector=hue_sector, saturation=shade_saturation, lightness=lightness
                )
                for shade_saturation, lightness in zip(
                    _shade_saturations(shades_per_hue, base=saturation),
                    _shade_lightnesses(
                        shades_per_hue, base=base_lightness, span=lightness_span
                    ),
                    strict=True,
                )
            )
        )
    return tuple(families)


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


def _pinned_hue(representative: Decimal, *, tolerance: Decimal) -> int | None:
    """Pin the two orientations that recur across packings to fixed hues."""
    if _orientation_distance(representative, Decimal(0)) <= tolerance:
        return RIGHT_ANGLE_HUE
    if _orientation_distance(representative, HALF_QUARTER_RADIANS) <= tolerance:
        return DIAGONAL_HUE
    return None


def _angle_class_hues(
    classes: tuple[tuple[int, ...], ...],
    representatives: tuple[Decimal, ...],
    *,
    hue_count: int,
    tolerance: Decimal,
    registry: AngleHueRegistry | None,
) -> tuple[int, ...]:
    """Assign hues: pinned angles first, then the rest by descending size.

    Hues 0 and 1 stay reserved whether or not a packing contains those
    orientations, so a right angle is the same colour in every packing.
    Orientation is stored modulo a quarter turn, so a class sitting just under
    90 degrees is a right angle; ``_orientation_distance`` compares modulo that
    seam rather than against zero directly.
    """
    pins = [
        _pinned_hue(representative, tolerance=tolerance) for representative in representatives
    ]
    unpinned = sorted(
        (index for index, pin in enumerate(pins) if pin is None),
        key=lambda index: (-len(classes[index]), min(classes[index])),
    )
    hues = [pin if pin is not None else 0 for pin in pins]
    if registry is not None:
        shared = registry.hues_for(tuple(representatives[index] for index in unpinned))
        for position, index in enumerate(unpinned):
            hues[index] = shared[position]
    else:
        span = max(1, hue_count - RESERVED_HUES)
        for position, index in enumerate(unpinned):
            hues[index] = RESERVED_HUES + position % span
    return tuple(hues)


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
    # Written out rather than looped. This is the innermost comparison of an O(n^2)
    # edge sweep -- forty million calls over the prospective atlas alone -- and the two
    # index generators cost more than the eight subtractions they drive. The argument
    # order is the comprehensions': endpoint major, axis minor, so equal residuals still
    # resolve to the same Decimal instance and the same emitted text.
    (left_x0, left_y0), (left_x1, left_y1) = left
    (right_x0, right_y0), (right_x1, right_y1) = right
    direct = max(
        abs(left_x0 - right_x0),
        abs(left_y0 - right_y0),
        abs(left_x1 - right_x1),
        abs(left_y1 - right_y1),
    )
    reverse = max(
        abs(left_x0 - right_x1),
        abs(left_y0 - right_y1),
        abs(left_x1 - right_x0),
        abs(left_y1 - right_y0),
    )
    return min(direct, reverse)


def _contact_box(
    edges: tuple[tuple[tuple[Decimal, Decimal], tuple[Decimal, Decimal]], ...],
    *,
    tolerance: Decimal,
) -> tuple[Decimal, Decimal, Decimal, Decimal]:
    """One square's corner box, grown by the contact tolerance and never shrunk.

    A residual within tolerance puts every endpoint coordinate of the two edges within
    tolerance of each other, so two squares whose grown boxes are disjoint on either
    axis cannot hold a matching edge pair. Screening on that is what keeps the sweep
    from spending 254s on forty million residuals that a coordinate comparison refuses.

    The rounding modes are the soundness argument: coordinates carry more significant
    digits than the working precision, so the growth is rounded outward in both
    directions and the box is never smaller than the exact one.
    """
    xs = [point[0] for edge in edges for point in edge]
    ys = [point[1] for edge in edges for point in edge]
    with localcontext() as context:
        context.prec = ANGLE_WORKING_DIGITS
        context.rounding = ROUND_FLOOR
        low_x, low_y = min(xs) - tolerance, min(ys) - tolerance
        context.rounding = ROUND_CEILING
        high_x, high_y = max(xs) + tolerance, max(ys) + tolerance
    return low_x, high_x, low_y, high_y


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
    boxes = [_contact_box(edges, tolerance=contact_tolerance) for edges in square_edges]
    for left_index, left_edges in enumerate(square_edges):
        left_low_x, left_high_x, left_low_y, left_high_y = boxes[left_index]
        for right_index in range(left_index + 1, len(square_edges)):
            right_low_x, right_high_x, right_low_y, right_high_y = boxes[right_index]
            if (
                left_high_x < right_low_x
                or right_high_x < left_low_x
                or left_high_y < right_low_y
                or right_high_y < left_low_y
            ):
                continue
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
        angle_hue_registry.reserved != RESERVED_HUES
        or angle_hue_registry.hue_count != spec.hue_count
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
        class_hues = _angle_class_hues(
            angle_classes,
            representatives,
            hue_count=spec.hue_count,
            tolerance=spec.angle_tolerance_radians,
            registry=angle_hue_registry,
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
