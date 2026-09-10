"""Exact vertical decomposition for several convex owner footprints.

This temporary implementation contains geometry only.  A residual centre is physical
when it lies in the open container-centre polygon and outside every closed Minkowski
collision polygon.  The returned positive-area polygon closures cover that strict
domain, but their boundaries may also contain forbidden tangencies.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from itertools import combinations, pairwise

from devtools.owner_footprints import (
    BOTTOM_LEFT_MARKS,
    OUTER_SIDE,
    OwnerBranchManifest,
    Point,
    Polygon,
    container_centre_polygon,
    convex_hull,
    forbidden_centre_polygon,
    full_owner_direction_manifest,
    owner_branch_manifest,
    owner_class_footprints,
    point_in_closed_convex_polygon,
    point_in_open_convex_polygon,
    polygon_area_twice,
)
from sqpack.fractional.model import Direction


@dataclass(frozen=True, slots=True)
class Affine:
    """One exact nonvertical boundary edge as ``v(u)``."""

    slope: Fraction
    intercept: Fraction

    def at(self, u: Fraction) -> Fraction:
        return self.slope * u + self.intercept


@dataclass(frozen=True, slots=True)
class Section:
    """Lower and upper affine boundaries of one convex polygon in an open slab."""

    lower: Affine
    upper: Affine


@dataclass(frozen=True, slots=True)
class Interval:
    """One closed vertical interval whose endpoints vary affinely through a slab."""

    lower: Affine
    upper: Affine


@dataclass(frozen=True, slots=True)
class VerticalDecomposition:
    """Positive-area closures of a container minus closed convex obstacles."""

    container_polygon: Polygon
    obstacle_polygons: tuple[Polygon, ...]
    cuts: tuple[Fraction, ...]
    components: tuple[Polygon, ...]
    physical_semantics: str = "interior(container) minus union(closed obstacles)"
    component_semantics: str = "positive-area closed cover of the strict physical domain"


@dataclass(frozen=True, slots=True)
class MultiFootprintDomain:
    """A residual-square domain outside several guaranteed owner footprints."""

    direction: Direction
    square_side: Fraction
    footprints: tuple[Polygon, ...]
    forbidden_polygons: tuple[Polygon, ...]
    container_polygon: Polygon
    cuts: tuple[Fraction, ...]
    components: tuple[Polygon, ...]
    physical_semantics: str = "interior(container) minus union(closed forbidden polygons)"
    component_semantics: str = "positive-area closed cover of the strict physical domain"


def _subtract(left: Point, right: Point) -> Point:
    return left[0] - right[0], left[1] - right[1]


def _cross(left: Point, right: Point) -> Fraction:
    return left[0] * right[1] - left[1] * right[0]


def _normalise_full_dimensional(polygon: Polygon) -> Polygon:
    result = convex_hull(polygon)
    if len(result) < 3 or polygon_area_twice(result) <= 0:
        raise ValueError("vertical decomposition requires full-dimensional convex polygons")
    return result


def _edges(polygon: Polygon) -> tuple[tuple[Point, Point], ...]:
    return tuple(zip(polygon, polygon[1:] + polygon[:1], strict=True))


def _segment_intersection_u(
    first_start: Point,
    first_end: Point,
    second_start: Point,
    second_end: Point,
) -> Fraction | None:
    """Return the u-coordinate of one isolated closed-segment intersection."""

    first_delta = _subtract(first_end, first_start)
    second_delta = _subtract(second_end, second_start)
    denominator = _cross(first_delta, second_delta)
    if denominator == 0:
        # Existing vertex cuts cover collinear-overlap endpoints.  Parallel disjoint
        # boundaries have no ordering event.
        return None
    offset = _subtract(second_start, first_start)
    first_parameter = _cross(offset, second_delta) / denominator
    second_parameter = _cross(offset, first_delta) / denominator
    if not (0 <= first_parameter <= 1 and 0 <= second_parameter <= 1):
        return None
    return first_start[0] + first_parameter * first_delta[0]


def _section(polygon: Polygon, u: Fraction) -> Section | None:
    functions: set[Affine] = set()
    for start, end in _edges(polygon):
        low, high = sorted((start[0], end[0]))
        if not low < u < high:
            continue
        slope = (end[1] - start[1]) / (end[0] - start[0])
        functions.add(Affine(slope, start[1] - slope * start[0]))
    if not functions:
        return None
    if len(functions) != 2:
        raise AssertionError(
            f"convex section at u={u} has {len(functions)} nonvertical boundaries"
        )
    ordered = sorted(functions, key=lambda function: function.at(u))
    if ordered[0].at(u) >= ordered[1].at(u):
        raise AssertionError("active convex section has no positive height")
    return Section(ordered[0], ordered[1])


def _choose_lower_max(first: Affine, second: Affine, u: Fraction) -> Affine:
    first_value, second_value = first.at(u), second.at(u)
    if first_value == second_value and first != second:
        raise AssertionError("isolated affine equality was not included as a slab cut")
    return first if first_value >= second_value else second


def _choose_upper_min(first: Affine, second: Affine, u: Fraction) -> Affine:
    first_value, second_value = first.at(u), second.at(u)
    if first_value == second_value and first != second:
        raise AssertionError("isolated affine equality was not included as a slab cut")
    return first if first_value <= second_value else second


def _choose_upper_max(first: Affine, second: Affine, u: Fraction) -> Affine:
    first_value, second_value = first.at(u), second.at(u)
    if first_value == second_value and first != second:
        raise AssertionError("isolated affine equality was not included as a slab cut")
    return first if first_value >= second_value else second


def _emit_strip(
    u0: Fraction,
    u1: Fraction,
    lower: Affine,
    upper: Affine,
) -> Polygon | None:
    lower0, lower1 = lower.at(u0), lower.at(u1)
    upper0, upper1 = upper.at(u0), upper.at(u1)
    if lower0 > upper0 or lower1 > upper1:
        raise AssertionError("free-strip boundaries cross within an event-free slab")
    polygon = convex_hull(((u0, lower0), (u1, lower1), (u1, upper1), (u0, upper0)))
    if len(polygon) < 3 or polygon_area_twice(polygon) <= 0:
        return None
    return polygon


def vertical_decompose(
    container_polygon: Polygon,
    obstacle_polygons: tuple[Polygon, ...],
) -> VerticalDecomposition:
    """Decompose a convex container minus a union of closed convex obstacles exactly."""

    container = _normalise_full_dimensional(container_polygon)
    obstacles = tuple(_normalise_full_dimensional(polygon) for polygon in obstacle_polygons)
    polygons = (container, *obstacles)
    container_low = min(u for u, _ in container)
    container_high = max(u for u, _ in container)
    cuts = {u for polygon in polygons for u, _ in polygon}
    for first, second in combinations(polygons, 2):
        for first_start, first_end in _edges(first):
            for second_start, second_end in _edges(second):
                u = _segment_intersection_u(first_start, first_end, second_start, second_end)
                if u is not None:
                    cuts.add(u)
    cuts = {u for u in cuts if container_low <= u <= container_high}
    cuts.update((container_low, container_high))
    ordered_cuts = tuple(sorted(cuts))

    components: list[Polygon] = []
    for u0, u1 in pairwise(ordered_cuts):
        if u0 == u1:
            continue
        midpoint = (u0 + u1) / 2
        container_section = _section(container, midpoint)
        if container_section is None:
            continue
        occupied: list[Interval] = []
        for obstacle in obstacles:
            obstacle_section = _section(obstacle, midpoint)
            if obstacle_section is None:
                continue
            lower = _choose_lower_max(obstacle_section.lower, container_section.lower, midpoint)
            upper = _choose_upper_min(obstacle_section.upper, container_section.upper, midpoint)
            if lower.at(midpoint) < upper.at(midpoint):
                occupied.append(Interval(lower, upper))

        occupied.sort(
            key=lambda interval: (
                interval.lower.at(midpoint),
                interval.upper.at(midpoint),
            )
        )
        merged: list[Interval] = []
        for interval in occupied:
            if not merged:
                merged.append(interval)
                continue
            previous = merged[-1]
            lower_value = interval.lower.at(midpoint)
            upper_value = previous.upper.at(midpoint)
            if lower_value == upper_value and interval.lower != previous.upper:
                raise AssertionError("isolated interval touch was not included as a slab cut")
            if lower_value <= upper_value:
                merged[-1] = Interval(
                    previous.lower,
                    _choose_upper_max(previous.upper, interval.upper, midpoint),
                )
            else:
                merged.append(interval)

        cursor = container_section.lower
        for interval in merged:
            if cursor.at(midpoint) < interval.lower.at(midpoint):
                component = _emit_strip(u0, u1, cursor, interval.lower)
                if component is not None:
                    components.append(component)
            cursor = _choose_upper_max(cursor, interval.upper, midpoint)
        if cursor.at(midpoint) < container_section.upper.at(midpoint):
            component = _emit_strip(u0, u1, cursor, container_section.upper)
            if component is not None:
                components.append(component)

    return VerticalDecomposition(container, obstacles, ordered_cuts, tuple(components))


def multi_footprint_domain(
    outer_side: Fraction,
    square_side: Fraction,
    direction: Direction,
    footprints: tuple[Polygon, ...],
) -> MultiFootprintDomain:
    """Build one rotated residual domain outside several closed owner footprints."""

    if not footprints:
        raise ValueError("multi-footprint domain requires at least one footprint")
    container = container_centre_polygon(outer_side, square_side, direction)
    forbidden = tuple(
        forbidden_centre_polygon(footprint, square_side, direction) for footprint in footprints
    )
    decomposition = vertical_decompose(container, forbidden)
    return MultiFootprintDomain(
        direction,
        square_side,
        footprints,
        forbidden,
        decomposition.container_polygon,
        decomposition.cuts,
        decomposition.components,
    )


def centre_in_strict_multi_footprint_domain(
    centre_uv: Point,
    domain: MultiFootprintDomain,
) -> bool:
    """Apply strict physical membership without trusting closure membership."""

    return point_in_open_convex_polygon(centre_uv, domain.container_polygon) and not any(
        point_in_closed_convex_polygon(centre_uv, forbidden)
        for forbidden in domain.forbidden_polygons
    )


def centre_in_decomposition_closures(
    centre_uv: Point,
    domain: VerticalDecomposition | MultiFootprintDomain,
) -> bool:
    """Test membership in the positive-area closure cover."""

    return any(
        point_in_closed_convex_polygon(centre_uv, component) for component in domain.components
    )


def reflect_to_four_corners(polygon: Polygon, outer_side: Fraction) -> tuple[Polygon, ...]:
    """Reflect one bottom-left footprint to all four physical container corners."""

    reflected = (
        polygon,
        tuple((outer_side - x, y) for x, y in polygon),
        tuple((x, outer_side - y) for x, y in polygon),
        tuple((outer_side - x, outer_side - y) for x, y in polygon),
    )
    return tuple(convex_hull(candidate) for candidate in reflected)


def compatible_m1_j0_footprints(
    kind: str,
    *,
    manifest: OwnerBranchManifest | None = None,
    outer_side: Fraction = OUTER_SIDE,
) -> tuple[Polygon, ...]:
    """Return the four reflected footprints of the compatible m1/j0 owner branch."""

    branch = manifest or owner_branch_manifest(full_owner_direction_manifest())
    owner_class = next(
        entry for entry in branch.classes if entry.class_id == "bottom-left:m1:j0"
    )
    footprints = owner_class_footprints(owner_class, branch.directions.directions)
    if kind not in footprints:
        raise ValueError(f"unknown owner footprint kind {kind!r}")
    return reflect_to_four_corners(footprints[kind], outer_side)


def compatible_axis_parent_centres(
    outer_side: Fraction = OUTER_SIDE,
) -> tuple[Point, ...]:
    """Return the exact compatible unit-parent centres for the four-corner branch."""

    return tuple(
        polygon[0]
        for polygon in reflect_to_four_corners((BOTTOM_LEFT_MARKS["m1"],), outer_side)
    )


def default_multi_owner_directions() -> tuple[Direction, ...]:
    """Retain the full 361 orientations for unrestricted singleton weights."""

    return full_owner_direction_manifest().directions


def guard_receipt(domain: MultiFootprintDomain) -> dict[str, object]:
    """Return geometry-only cardinalities before any covering target is run."""

    return {
        "scientific_target_run": False,
        "footprints": len(domain.footprints),
        "forbidden_edge_counts": [len(polygon) for polygon in domain.forbidden_polygons],
        "cuts": len(domain.cuts),
        "components": len(domain.components),
        "full_direction_count": len(default_multi_owner_directions()),
        "component_semantics": domain.component_semantics,
    }
