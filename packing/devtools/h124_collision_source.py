"""Append the reviewed center-correlated collision region to the old H124 axis source.

Only an explicitly authorized ``cover_source()`` call constructs scientific data.
Importing this module neither loads the old source nor creates a field. The old
rectangle and thirteen regions are preserved; the new region is already a set of
second-square centers, so it is NOT Minkowski-expanded again. Its support bounds
implement bc-255-center-correlated-collision.md with the fixed epsilon 1/500.

Generic helpers use exact closed half-plane clipping from caller-supplied axis
bounds. Empty, point and segment intersections refuse rather than disappearing
from the source. No cover or packing conclusion follows from source construction.
"""

from __future__ import annotations

from collections.abc import Sequence
from fractions import Fraction
from typing import Any

from devtools.closed_polygon_cover import parse_rational, validate_source
from sqpack.field import FieldElement, NumberField

type Point = tuple[FieldElement, FieldElement]
type Polygon = tuple[Point, ...]
type HalfPlane = tuple[FieldElement, FieldElement, FieldElement]

SOURCE_FIELD_DEGREE = 2
SOURCE_VERTEX_BOUND = 68
COLLISION_VERTEX_BOUND = 8
MAX_HALFPLANES = 8
MAX_NOMINAL_POINTS = 16
MAX_INPUT_BITS = 128
MAX_DERIVED_BITS = 4096
NORMALS = ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1))
POLYGON_IDS = (
    "obstacle",
    "B",
    "C0",
    "D",
    "E",
    "F",
    "G",
    "H",
    "I",
    "J",
    "corner-B",
    "corner-D",
    "corner-F",
    "collision",
)


class SourceError(ValueError):
    """Malformed generic geometry or an unproved scientific source admission."""


def _admit_field(field: NumberField) -> None:
    certificate = field.precondition_certificate()
    polynomial = certificate["normalized_minimal_polynomial"]
    interval = certificate["declared_isolating_interval"]
    if (
        type(polynomial) is not list
        or len(polynomial) != field.degree + 1
        or type(interval) is not list
        or len(interval) != 2
        or certificate["irreducible_over_q"] is not True
        or certificate["root_count_in_open_interval"] != 1
        or certificate["endpoints_are_not_roots"] is not True
    ):
        raise SourceError("field requires its complete validated real embedding")
    # The public cover admission parser applies lexical/length guards before Fraction.
    for coefficient in [*polynomial, *interval]:
        parse_rational(coefficient)


def _bounded(value: FieldElement, bits: int = MAX_DERIVED_BITS) -> FieldElement:
    if any(
        max(c.numerator.bit_length(), c.denominator.bit_length()) > bits for c in value.coeffs
    ):
        raise SourceError("exact coefficient exceeds its arithmetic bit cap")
    return value


def _exact(value: Any, field: NumberField | None = None) -> FieldElement:
    if type(value) is not FieldElement:
        raise SourceError("coordinates and half-planes require exact field elements")
    if type(value.field) is not NumberField or not 1 <= value.field.degree <= 4:
        raise SourceError(
            "generic geometry requires a validated field of degree one through four"
        )
    if field is None:
        _admit_field(value.field)
    if field is not None and value.field is not field:
        raise SourceError("every coordinate must use the same caller-bound field")
    if len(value.coeffs) != value.field.degree or any(
        type(c) is not Fraction for c in value.coeffs
    ):
        raise SourceError("field coordinates require full exact coefficient vectors")
    return _bounded(value, MAX_INPUT_BITS)


def _points(raw: Sequence[Point]) -> tuple[NumberField, tuple[Point, ...]]:
    if type(raw) not in (list, tuple) or not 1 <= len(raw) <= MAX_NOMINAL_POINTS:
        raise SourceError("nominal points must form a nonempty bounded list or tuple")
    field: NumberField | None = None
    points: list[Point] = []
    for point in raw:
        if type(point) not in (list, tuple) or len(point) != 2:
            raise SourceError("point must have exactly two coordinates")
        x = _exact(point[0], field)
        field = x.field
        points.append((x, _exact(point[1], field)))
    assert field is not None
    return field, tuple(points)


def support_halfplanes(
    nominal: Sequence[Point],
    supports: Sequence[FieldElement],
    margin: Fraction,
) -> tuple[HalfPlane, ...]:
    """Shift eight supplied support bounds by every nominal point and an L1 penalty.

    This helper has no scientific constants or kernel assumption: its caller must
    justify the support values and the uniform coordinate-displacement margin.
    """
    if type(supports) not in (list, tuple) or len(supports) != len(NORMALS):
        raise SourceError("exactly eight support values are required")
    if (
        type(margin) is not Fraction
        or margin < 0
        or max(margin.numerator.bit_length(), margin.denominator.bit_length()) > MAX_INPUT_BITS
    ):
        raise SourceError("margin must be a bounded nonnegative exact Fraction")
    field, points = _points(nominal)
    heights = tuple(_exact(value, field) for value in supports)
    result: list[HalfPlane] = []
    for (nx, ny), height in zip(NORMALS, heights, strict=True):
        offsets = [_bounded(nx * x + ny * y) for x, y in points]
        bound = _bounded(height + min(offsets) - margin * (abs(nx) + abs(ny)))
        result.append((field.rational(nx), field.rational(ny), bound))
    return tuple(result)


def _value(plane: HalfPlane, point: Point) -> FieldElement:
    a, b, c = plane
    return _bounded(a * point[0] + b * point[1] - c)


def _turn(origin: Point, first: Point, second: Point) -> FieldElement:
    return _bounded(
        (first[0] - origin[0]) * (second[1] - origin[1])
        - (first[1] - origin[1]) * (second[0] - origin[0])
    )


def _canonical(points: Sequence[Point]) -> Polygon:
    """Clean a clipped convex cycle without replacing it by a larger hull."""
    cleaned: list[Point] = []
    for point in points:
        if not cleaned or point != cleaned[-1]:
            cleaned.append(point)
    if len(cleaned) > 1 and cleaned[0] == cleaned[-1]:
        cleaned.pop()
    while len(cleaned) >= 3:
        redundant = next(
            (
                index
                for index in range(len(cleaned))
                if _turn(
                    cleaned[index - 1], cleaned[index], cleaned[(index + 1) % len(cleaned)]
                ).is_zero()
            ),
            None,
        )
        if redundant is None:
            break
        cleaned.pop(redundant)
    if len(cleaned) < 3:
        raise SourceError("half-plane intersection must have positive area")
    if len(cleaned) > MAX_HALFPLANES or len(set(cleaned)) != len(cleaned):
        raise SourceError("clipped vertex inventory is invalid")
    for index, current in enumerate(cleaned):
        following = cleaned[(index + 1) % len(cleaned)]
        if any(_turn(current, following, point).sign() < 0 for point in cleaned):
            raise SourceError("clipping did not retain a positive-area convex CCW cycle")
    first = min(range(len(cleaned)), key=cleaned.__getitem__)
    return tuple(cleaned[first:] + cleaned[:first])


def _clip(polygon: Polygon, plane: HalfPlane) -> Polygon:
    result: list[Point] = []
    previous = polygon[-1]
    previous_value = _value(plane, previous)
    previous_inside = previous_value.sign() <= 0
    for current in polygon:
        current_value = _value(plane, current)
        current_inside = current_value.sign() <= 0
        if previous_inside != current_inside:
            denominator = _bounded(previous_value - current_value)
            # Opposite closed-membership states imply distinct signed values.
            if denominator.is_zero():
                raise SourceError("crossing has a zero exact denominator")
            fraction = _bounded(previous_value / denominator)
            crossing = (
                _bounded(previous[0] + fraction * (current[0] - previous[0])),
                _bounded(previous[1] + fraction * (current[1] - previous[1])),
            )
            result.append(crossing)
        if current_inside:
            result.append(current)
        previous, previous_value, previous_inside = current, current_value, current_inside
    return _canonical(result)


def axis_bounded_intersection(halfplanes: Sequence[HalfPlane]) -> Polygon:
    """Intersect four declared axis bounds and at most four other closed half-planes.

    The first normals must be +x, -x, +y, -y, in that order, each unnormalized
    coefficient exactly one or minus one. All inputs are admitted before clipping.
    No arbitrary bounding box, line-pair enumeration or floating tolerance is used.
    """
    if type(halfplanes) not in (list, tuple) or not 4 <= len(halfplanes) <= MAX_HALFPLANES:
        raise SourceError("half-plane inventory must contain four through eight entries")
    field: NumberField | None = None
    planes: list[HalfPlane] = []
    for raw in halfplanes:
        if type(raw) not in (list, tuple) or len(raw) != 3:
            raise SourceError("half-plane must have exactly three coefficients")
        a = _exact(raw[0], field)
        field = a.field
        b, c = _exact(raw[1], field), _exact(raw[2], field)
        if a.is_zero() and b.is_zero():
            raise SourceError("half-plane normal must be nonzero")
        planes.append((a, b, c))
    assert field is not None
    if any(
        (a, b) != (field.rational(nx), field.rational(ny))
        for (a, b, _), (nx, ny) in zip(planes[:4], NORMALS[:4], strict=True)
    ):
        raise SourceError("the first four entries must be the declared axis bounds")
    left, right = -planes[1][2], planes[0][2]
    bottom, top = -planes[3][2], planes[2][2]
    if left >= right or bottom >= top:
        raise SourceError("axis intersection must have positive area")
    polygon = ((left, bottom), (right, bottom), (right, top), (left, top))
    for plane in planes[4:]:
        polygon = _clip(polygon, plane)
    # Final exact replay prevents a clipping defect from weakening any input plane.
    if any(_value(plane, point).sign() > 0 for plane in planes for point in polygon):
        raise SourceError("a clipped vertex violates an original closed half-plane")
    return _canonical(polygon)


def wire_point(point: Point) -> list[list[str]]:
    """Emit every low-to-high coefficient, under the existing source input cap."""
    _, (parsed,) = _points((point,))
    return [[str(coefficient) for coefficient in coordinate.coeffs] for coordinate in parsed]


def append_collision_region(
    field: NumberField,
    rectangle: Any,
    regions: Any,
    polygon: Sequence[Point],
) -> list[dict[str, Any]]:
    """Validate and preserve the supplied thirteen regions before adding one polygon.

    This assembly helper constructs no scientific source. Its caller supplies all
    geometry; the unchanged prefix and complete augmented source are both checked.
    """
    validated = validate_source(field, rectangle, regions)
    if tuple(item.identifier for item in validated.polygons) != POLYGON_IDS[:-1]:
        raise SourceError("the complete unchanged thirteen-region inventory is required")
    if (
        sum(len(item.vertices) for item in validated.polygons)
        > SOURCE_VERTEX_BOUND - COLLISION_VERTEX_BOUND
    ):
        raise SourceError("old source exceeds its sixty-vertex declaration")
    if type(polygon) not in (list, tuple) or not 3 <= len(polygon) <= COLLISION_VERTEX_BOUND:
        raise SourceError("collision source requires three through eight vertices")
    polygon_field, points = _points(polygon)
    if polygon_field is not field:
        raise SourceError("collision polygon must use the old source's exact field")
    canonical = _canonical(points)
    result = [*regions, {"id": "collision", "vertices": [wire_point(p) for p in canonical]}]
    if (
        len(result) != len(POLYGON_IDS)
        or sum(len(p["vertices"]) for p in result) > SOURCE_VERTEX_BOUND
    ):
        raise SourceError("augmented source exceeds its complete fourteen-region inventory")
    validate_source(field, rectangle, result)
    return result


def cover_source() -> tuple[NumberField, list, list[dict[str, Any]]]:
    """Explicit scientific factory, requiring a separate committed prospective protocol."""
    # Keep the scientific source dependency behind the explicit factory boundary.
    from devtools import h124_cover_source  # noqa: PLC0415

    field, rectangle, regions = h124_cover_source.cover_source("axis")
    certificate = field.precondition_certificate()
    if (
        field.degree != SOURCE_FIELD_DEGREE
        or certificate["normalized_minimal_polynomial"] != ["1", "0", "-2"]
        or certificate["declared_isolating_interval"] != ["1", "2"]
        or field.alpha <= 0
        or not (field.alpha * field.alpha - 2).is_zero()
    ):
        raise SourceError("old source must use the declared positive square root of two")
    q = field.rational("1939/500")
    m, r = q / 2, field.alpha / 2
    k = (1 + m) / 2
    nominal = ((k, k - r), (2 * r, r), (m + 1 - 2 * r, r))
    tangent = Fraction(110880, 50803079)
    half_width = (1 + tangent * tangent) / (2 * (1 + 2 * tangent - tangent * tangent))
    supports = tuple(
        half_width * (abs(nx) + abs(ny)) + half_width * field.alpha * max(abs(nx), abs(ny))
        for nx, ny in NORMALS
    )
    planes = support_halfplanes(nominal, supports, Fraction(1, 500))
    polygon = axis_bounded_intersection(planes)
    result = append_collision_region(field, rectangle, regions, polygon)
    return field, rectangle, result
