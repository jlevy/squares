"""Explicit H124 closed-cover source; importing this module constructs no target.

The scientific entry point is ``cover_source(frame)`` and has no default frame.
It implements H-124's continuous-cover contract, not an angle sample: the obstacle
is conv(D union K1), the kernel is the reviewed uniform inner square, and the three
marked-corner patches are clipped to the full center box. None of these polygons
alone establishes coverage or a packing bound. Source construction requires a
separately authorized invocation and subsequent independent source/cover checking.

Generic helpers below operate only on their supplied exact points. They share the
NumberField arithmetic, but no hull or Minkowski implementation with a reader.
"""

from __future__ import annotations

from collections.abc import Sequence
from fractions import Fraction
from typing import Any

from cases.stromquist.restricted_orientation import point_sets
from devtools.closed_polygon_cover import validate_source
from sqpack.field import FieldElement, NumberField

type Point = tuple[FieldElement, FieldElement]
type Polygon = tuple[Point, ...]

MAX_HULL_POINTS = 256
"""Bound generic point-cloud enumeration before exact hull work."""
SOURCE_FIELD_DEGREE = 2
"""Declared source degree, available without constructing the scientific field."""
SOURCE_VERTEX_BOUND = 60
"""At most 12 obstacle-sum vertices, nine quadrilaterals and three rectangles."""
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
)


class SourceError(ValueError):
    """Unsupported source selector or malformed exact generic geometry."""


def _frame(frame: str) -> None:
    if type(frame) is not str or frame not in ("axis", "diagonal"):
        raise SourceError("frame must be exactly axis or diagonal")


def _points(raw: Sequence[Point]) -> tuple[NumberField, tuple[Point, ...]]:
    if type(raw) not in (list, tuple) or not 1 <= len(raw) <= MAX_HULL_POINTS:
        raise SourceError("point cloud must be a nonempty bounded list or tuple")
    field: NumberField | None = None
    points: list[Point] = []
    for point in raw:
        if type(point) not in (list, tuple) or len(point) != 2:
            raise SourceError("point requires exactly two field coordinates")
        for coordinate in point:
            if type(coordinate) is not FieldElement:
                raise SourceError("geometry requires exact field elements")
            if field is None:
                field = coordinate.field
            elif coordinate.field is not field:
                raise SourceError("all points must use the same caller-bound field")
        points.append((point[0], point[1]))
    if field is None:
        raise SourceError("point cloud has no field")
    return field, tuple(points)


def _turn(origin: Point, first: Point, second: Point) -> FieldElement:
    return (first[0] - origin[0]) * (second[1] - origin[1]) - (first[1] - origin[1]) * (
        second[0] - origin[0]
    )


def convex_hull(points: Sequence[Point]) -> Polygon:
    """Strict CCW hull, starting at the exact lexicographic minimum.

    Duplicate, interior and collinear boundary points are removed. A point or
    segment cannot be represented as a positive-area cover polygon and is refused.
    """
    _, parsed = _points(points)
    ordered = sorted(set(parsed))
    lower: list[Point] = []
    upper: list[Point] = []
    for point in ordered:
        while len(lower) >= 2 and _turn(lower[-2], lower[-1], point) <= 0:
            lower.pop()
        lower.append(point)
    for point in reversed(ordered):
        while len(upper) >= 2 and _turn(upper[-2], upper[-1], point) <= 0:
            upper.pop()
        upper.append(point)
    result = tuple(lower[:-1] + upper[:-1])
    if len(result) < 3:
        raise SourceError("convex hull must have positive area")
    return result


def minkowski_sum(first: Sequence[Point], second: Sequence[Point]) -> Polygon:
    """Canonical Minkowski sum of two supplied positive-area convex hulls."""
    left, right = convex_hull(first), convex_hull(second)
    if left[0][0].field is not right[0][0].field:
        raise SourceError("Minkowski operands must have the same exact field")
    if len(left) * len(right) > MAX_HULL_POINTS:
        raise SourceError("Minkowski point inventory exceeds its cap")
    return convex_hull([(x + u, y + v) for x, y in left for u, v in right])


def translate(points: Sequence[Point], displacement: Point) -> Polygon:
    """Translate the supplied point-cloud hull and retain its canonical boundary."""
    field, parsed = _points(points)
    other, (vector,) = _points((displacement,))
    if field is not other:
        raise SourceError("translation must use the point cloud's exact field")
    return convex_hull([(x + vector[0], y + vector[1]) for x, y in parsed])


def _rectangle(bounds: Sequence[Point]) -> tuple[Point, Point]:
    if type(bounds) not in (list, tuple) or len(bounds) != 2:
        raise SourceError("rectangle requires lower and upper corners")
    _, (lower, upper) = _points(bounds)
    if lower[0] >= upper[0] or lower[1] >= upper[1]:
        raise SourceError("rectangle must have positive width and height")
    return lower, upper


def rectangle_polygon(bounds: Sequence[Point]) -> Polygon:
    """Canonical closed rectangle from lower-left and upper-right corners."""
    (left, bottom), (right, top) = _rectangle(bounds)
    return ((left, bottom), (right, bottom), (right, top), (left, top))


def intersect_rectangles(first: Sequence[Point], second: Sequence[Point]) -> Polygon:
    """Clip two closed rectangles; empty or boundary-only results are refused."""
    lower_a, upper_a = _rectangle(first)
    lower_b, upper_b = _rectangle(second)
    _points((lower_a, upper_a, lower_b, upper_b))
    return rectangle_polygon(
        (
            (max(lower_a[0], lower_b[0]), max(lower_a[1], lower_b[1])),
            (min(upper_a[0], upper_b[0]), min(upper_a[1], upper_b[1])),
        )
    )


def centered_square(field: NumberField, half_width: Fraction, frame: str) -> Polygon:
    """A supplied half-width square in the axis or positive sqrt2 diagonal frame."""
    _frame(frame)
    if type(field) is not NumberField or type(half_width) is not Fraction or half_width <= 0:
        raise SourceError("kernel requires a validated field and positive rational half-width")
    width = field.rational(half_width)
    corners = ((-width, -width), (width, -width), (width, width), (-width, width))
    if frame == "axis":
        return corners
    root = field.alpha
    if not (root * root - 2).is_zero() or root <= 0:
        raise SourceError("diagonal kernel requires the positive square root of two")
    rotation = root / 2
    return convex_hull([(rotation * (x - y), rotation * (x + y)) for x, y in corners])


def wire_point(point: Point) -> list[list[str]]:
    """Serialize a supplied point in full low-to-high field coefficient arrays."""
    _, (parsed,) = _points((point,))
    return [[str(coefficient) for coefficient in coordinate.coeffs] for coordinate in parsed]


def cover_source(frame: str) -> tuple[NumberField, list, list[dict[str, Any]]]:
    """Construct the fixed H124 source only on an explicitly authorized invocation.

    Source formulas: H-124's continuous-cover contract, its linked anchor-diamond
    proof, and original restricted_orientation.point_sets(q)[1][3:]. The point D
    and the diamond D have distinct roles; only the former labels a mark polygon.
    """
    _frame(frame)
    field = NumberField((1, 0, -2), (1, 2))
    q = field.rational("1939/500")
    one, zero = field.one, field.zero
    width, baseline = q / 2 - one, q - 3
    center_x, root_half = one + width / 2, field.alpha / 2
    diamond_height = Fraction(49, 50) * width / 2
    old_diamond = (
        (one, baseline),
        (center_x, baseline - diamond_height),
        (one + width, baseline),
        (center_x, baseline + diamond_height),
    )
    radius = field.rational("16/25")
    larger_diamond = (
        (center_x - radius, root_half),
        (center_x, root_half - radius),
        (center_x + radius, root_half),
        (center_x, root_half + radius),
    )
    obstacle = convex_hull((*old_diamond, *larger_diamond))
    tangent = Fraction(110880, 50803079)
    tangent_square = tangent * tangent
    half_width = (1 + tangent_square) / (2 * (1 + 2 * tangent - tangent_square))
    kernel = centered_square(field, half_width, frame)
    lower_extent = (
        field.rational("1/2")
        if frame == "axis"
        else root_half * (1 - tangent_square) / (1 + tangent_square)
    )
    bounds = ((lower_extent, lower_extent), (q - lower_extent, q - lower_extent))
    _, twelve = point_sets(q)
    marks = twelve[3:]
    if len(marks) != 9:
        raise SourceError("the original source must supply exactly nine unchanged B-J marks")
    polygons = [minkowski_sum(obstacle, kernel)]
    polygons.extend(translate(kernel, mark) for mark in marks)
    # Only bottom-right B, top-right D and top-left F are marked corners.
    corner_boxes = (
        ((q - one, zero), (q, one)),
        ((q - one, q - one), (q, q)),
        ((zero, q - one), (one, q)),
    )
    polygons.extend(intersect_rectangles(bounds, corner) for corner in corner_boxes)
    if len(polygons) != len(POLYGON_IDS) or sum(map(len, polygons)) > SOURCE_VERTEX_BOUND:
        raise SourceError("scientific polygon inventory exceeds its declared source bound")
    rectangle_wire = [wire_point(corner) for corner in bounds]
    polygon_wire = [
        {"id": identity, "vertices": [wire_point(point) for point in polygon]}
        for identity, polygon in zip(POLYGON_IDS, polygons, strict=True)
    ]
    validate_source(field, rectangle_wire, polygon_wire)
    return field, rectangle_wire, polygon_wire
