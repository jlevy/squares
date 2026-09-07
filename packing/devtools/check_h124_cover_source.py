"""Independent source reconstruction for the H124 whole-band polygon cover.

``cover_source`` is a scientific constructor: it must not be invoked before a
separately committed protocol authorizes the source. Importing this module does not
construct a field or evaluate the scientific geometry. Generic helpers and mocked
source binding are the only pre-authorization controls.

The source contains E+B_phi, the nine unchanged Stromquist marks plus B_phi, and
the three marked-corner windows clipped to Z_phi. E is the convex hull of the old
two-anchor diamond and the reviewed larger common diamond. The two central frame
names stand for whole-band inner kernels, not sampled-angle cover claims. A failed
sufficient cover does not refute H124, and one frame cannot establish both bands.

This implementation shares only exact field arithmetic and the accepted generic
endpoint-chain reader. It does not import a source producer or source point factory.
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any

from devtools.check_closed_polygon_cover import check_packet as check_closed_cover
from sqpack.field import FieldElement, NumberField

type Point = tuple[FieldElement, FieldElement]
type Polygon = tuple[Point, ...]
type Rectangle = tuple[Point, Point]
type Plane = tuple[FieldElement, FieldElement, FieldElement]

MARK_IDS = ("B", "C0", "D", "E", "F", "G", "H", "I", "J")
CORNER_IDS = ("corner-B", "corner-D", "corner-F")
MAX_GENERIC_POINTS = 256


class SourceError(ValueError):
    """Invalid generic geometry or failure to reconstruct the exact source contract."""


def _points(raw: Any) -> Polygon:
    if not isinstance(raw, (tuple, list)) or len(raw) > MAX_GENERIC_POINTS:
        raise SourceError("point inventory must be a bounded exact sequence")
    field: NumberField | None = None
    result: list[Point] = []
    for point in raw:
        if (
            not isinstance(point, (tuple, list))
            or len(point) != 2
            or any(not isinstance(value, FieldElement) for value in point)
        ):
            raise SourceError("points must have two exact field coordinates")
        if field is None:
            field = point[0].field
        if any(value.field is not field for value in point):
            raise SourceError("every coordinate must belong to the same exact field")
        result.append((point[0], point[1]))
    return tuple(result)


def _turn(origin: Point, first: Point, second: Point) -> FieldElement:
    return (first[0] - origin[0]) * (second[1] - origin[1]) - (first[1] - origin[1]) * (
        second[0] - origin[0]
    )


def _distance_squared(first: Point, second: Point) -> FieldElement:
    return (first[0] - second[0]) ** 2 + (first[1] - second[1]) ** 2


def convex_hull(points: Sequence[Point]) -> Polygon:
    """Gift-wrap the exact hull, lexicographic start and CCW, without collinear points.

    Empty sets, singletons and segments retain their dimension. At a collinear
    support edge the farthest endpoint is selected, so redundant boundary points
    do not enter the canonical wire. Sorting uses the real field order.
    """
    vertices = sorted(set(_points(points)))
    if len(vertices) < 2:
        return tuple(vertices)
    start = current = vertices[0]
    hull: list[Point] = []
    for _ in range(len(vertices) + 1):
        hull.append(current)
        candidate = vertices[1] if current == vertices[0] else vertices[0]
        for point in vertices:
            if point == current:
                continue
            direction = _turn(current, candidate, point).sign()
            if direction < 0 or (
                direction == 0
                and _distance_squared(current, point) > _distance_squared(current, candidate)
            ):
                candidate = point
        if candidate == start:
            return tuple(hull)
        current = candidate
    raise SourceError("convex hull did not close within its finite vertex inventory")


def minkowski_sum(first: Sequence[Point], second: Sequence[Point]) -> Polygon:
    """Return conv(first)+conv(second) using the exact pairwise vertex sums."""
    left, right = _points(first), _points(second)
    _points((*left, *right))
    if not left or not right:
        return ()
    if len(left) * len(right) > MAX_GENERIC_POINTS:
        raise SourceError("Minkowski vertex-pair inventory exceeds its cap")
    return convex_hull(tuple((x + u, y + v) for x, y in left for u, v in right))


def centered_parallelogram(u: Point, v: Point) -> Polygon:
    """The canonical convex hull of the four half-vector combinations ±u±v."""
    _points((u, v))
    return convex_hull(
        tuple(
            (sx * u[0] + sy * v[0], sx * u[1] + sy * v[1])
            for sx, sy in ((-1, -1), (1, -1), (1, 1), (-1, 1))
        )
    )


def clip_halfplane(polygon: Sequence[Point], plane: Plane) -> Polygon:
    """Intersect a convex hull with a*x+b*y<=c, preserving all closed contacts."""
    vertices = convex_hull(polygon)
    if (
        not isinstance(plane, (tuple, list))
        or len(plane) != 3
        or any(not isinstance(value, FieldElement) for value in plane)
        or any(value.field is not plane[0].field for value in plane)
    ):
        raise SourceError("half-plane requires three coordinates in one exact field")
    if not vertices:
        return ()
    if vertices[0][0].field is not plane[0].field:
        raise SourceError("half-plane and polygon must share their field")
    a, b, bound = plane
    clipped: list[Point] = []
    previous = vertices[-1]
    previous_value = a * previous[0] + b * previous[1] - bound
    for current in vertices:
        current_value = a * current[0] + b * current[1] - bound
        before_inside, now_inside = previous_value <= 0, current_value <= 0
        if before_inside != now_inside:
            fraction = previous_value / (previous_value - current_value)
            clipped.append(
                (
                    previous[0] + fraction * (current[0] - previous[0]),
                    previous[1] + fraction * (current[1] - previous[1]),
                )
            )
        if now_inside:
            clipped.append(current)
        previous, previous_value = current, current_value
    return convex_hull(tuple(clipped))


def _rectangle(raw: Any, *, positive: bool) -> Rectangle:
    points = _points(raw)
    if len(points) != 2:
        raise SourceError("rectangle requires lower and upper corners")
    lower, upper = points
    if any(
        lower[axis] > upper[axis] or (positive and lower[axis] == upper[axis])
        for axis in (0, 1)
    ):
        raise SourceError("rectangle bounds do not have the required positive area")
    return lower, upper


def _rectangle_vertices(rectangle: Rectangle) -> Polygon:
    (left, bottom), (right, top) = rectangle
    return (left, bottom), (right, bottom), (right, top), (left, top)


def clip_rectangle(polygon: Sequence[Point], rectangle: Rectangle) -> Polygon:
    """Clip to a closed box; a zero-width box may retain a point or segment."""
    (left, bottom), (right, top) = _rectangle(rectangle, positive=False)
    zero, one = left.field.zero, left.field.one
    result = convex_hull(polygon)
    for plane in (
        (-one, zero, -left),
        (one, zero, right),
        (zero, -one, -bottom),
        (zero, one, top),
    ):
        result = clip_halfplane(result, plane)
    return result


def _wire_point(point: Point) -> list[list[str]]:
    return [[str(coefficient) for coefficient in value.coeffs] for value in point]


def _region(identity: str, vertices: Sequence[Point]) -> dict[str, Any]:
    hull = convex_hull(vertices)
    if len(hull) < 3:
        raise SourceError(f"source region {identity} must have positive area")
    return {"id": identity, "vertices": [_wire_point(point) for point in hull]}


def assemble_source(
    rectangle: Rectangle,
    obstacle: Sequence[Point],
    kernel: Sequence[Point],
    marks: Sequence[tuple[str, Point]],
    corner_windows: Sequence[tuple[str, Rectangle]],
) -> tuple[list[list[list[str]]], list[dict[str, Any]]]:
    """Assemble the full named cover from generic inputs, clipping only corner patches."""
    lower, upper = _rectangle(rectangle, positive=True)
    if (
        tuple(identity for identity, _ in marks) != MARK_IDS
        or tuple(identity for identity, _ in corner_windows) != CORNER_IDS
    ):
        raise SourceError("mark or marked-corner inventory is missing, reordered or foreign")
    obstacle_hull, kernel_hull = convex_hull(obstacle), convex_hull(kernel)
    if len(obstacle_hull) < 3 or len(kernel_hull) < 3:
        raise SourceError("obstacle and inner kernel must have positive area")
    _points((lower, upper, *obstacle_hull, *kernel_hull, *(point for _, point in marks)))
    regions = [_region("obstacle", minkowski_sum(obstacle_hull, kernel_hull))]
    regions.extend(
        _region(identity, minkowski_sum((point,), kernel_hull)) for identity, point in marks
    )
    for identity, window in corner_windows:
        region = clip_rectangle(
            _rectangle_vertices(_rectangle(window, positive=False)), (lower, upper)
        )
        regions.append(_region(identity, region))
    return [_wire_point(lower), _wire_point(upper)], regions


def _frame(frame: str) -> None:
    if type(frame) is not str or frame not in {"axis", "diagonal"}:
        raise SourceError("frame must be exactly axis or diagonal")


def cover_source(frame: str) -> tuple[NumberField, list, list]:
    """SCIENTIFIC: reconstruct the complete fixed H124 source for one whole angle band.

    This function is deliberately uncalled by source-free controls. All field and
    target arithmetic is lazy here. The field polynomial API is high-to-low;
    coordinate coefficients in the returned wire remain low-to-high.
    """
    _frame(frame)
    field = NumberField((1, 0, -2), (1, 2))
    zero, one = field.zero, field.one
    q = field.rational("1939/500")
    endpoint = field.rational("110880/50803079")
    r = field.alpha / 2
    m = q / 2
    midpoint = (one + m) / 2
    anchor_y = q - 3
    diamond_height = field.rational("49/50") * (m - one) / 2
    old_diamond = (
        (one, anchor_y),
        (midpoint, anchor_y - diamond_height),
        (m, anchor_y),
        (midpoint, anchor_y + diamond_height),
    )
    radius = field.rational("16/25")
    new_diamond = (
        (midpoint - radius, r),
        (midpoint, r - radius),
        (midpoint + radius, r),
        (midpoint, r + radius),
    )
    obstacle = convex_hull((*old_diamond, *new_diamond))

    half_side = (one + endpoint * endpoint) / (2 + 4 * endpoint - 2 * endpoint * endpoint)
    if frame == "axis":
        lower_distance = one / 2
        kernel = centered_parallelogram((half_side, zero), (zero, half_side))
    else:
        lower_distance = r * (one - endpoint * endpoint) / (one + endpoint * endpoint)
        kernel = centered_parallelogram(
            (half_side * r, half_side * r), (-half_side * r, half_side * r)
        )
    rectangle = ((lower_distance, lower_distance), (q - lower_distance, q - lower_distance))

    # Original point_sets(q), entries B through J; no fixed-side calibration factory.
    marks = (
        ("B", (q - one, one)),
        ("C0", (q - field.rational("4/5"), q / 2)),
        ("D", (q - one, q - one)),
        ("E", (q / 2, q - field.rational("4/5"))),
        ("F", (one, q - one)),
        ("G", (field.rational("4/5"), q - 2)),
        ("H", (field.rational("17/10"), field.rational("11/5"))),
        ("I", (field.rational("11/5"), field.rational("11/5"))),
        ("J", (field.rational("11/5"), field.rational("17/10"))),
    )
    # B is bottom-right, D top-right, F top-left. There is no bottom-left patch.
    windows = (
        ("corner-B", ((q - one, zero), (q, one))),
        ("corner-D", ((q - one, q - one), (q, q))),
        ("corner-F", ((zero, q - one), (one, q))),
    )
    rectangle_wire, polygons_wire = assemble_source(rectangle, obstacle, kernel, marks, windows)
    return field, rectangle_wire, polygons_wire


def check_packet(raw: Any, *, frame: str) -> dict[str, Any]:
    """SCIENTIFIC: bind one frame's independently reconstructed source and replay it."""
    _frame(frame)
    field, rectangle, polygons = cover_source(frame)
    return check_closed_cover(raw, field=field, rectangle=rectangle, polygons=polygons)
