"""Exact geometry for generic corner-owner footprint branches.

This module constructs geometry and branch metadata only.  In particular, it does
not filter a target family, solve a covering program, or issue a packing
certificate.  The enlarged endpoint footprint is provisional pending the campaign's
authoritative proof review; callers can inspect ``ENDPOINT_FOOTPRINT_STATUS`` and the
manifest's matching field rather than inferring a certification claim from geometry.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from functools import cmp_to_key
from typing import Any

from sqpack.fractional.generate import direction_net, net_half_tangents
from sqpack.fractional.model import Direction

type Point = tuple[Fraction, Fraction]
type Polygon = tuple[Point, ...]

OUTER_SIDE = Fraction(96, 25)
CORE_SIDE = Fraction(9977, 10000)
HALF_CORE = CORE_SIDE / 2
ANGLE_LIMIT = Fraction(207107, 500000)
DIRECTION_STEPS = 180

BOTTOM_LEFT_MARKS: dict[str, Point] = {
    "m1": (Fraction(3152, 3175), Fraction(2336, 3175)),
    "m2": (Fraction(2336, 3175), Fraction(3152, 3175)),
}

ENDPOINT_FOOTPRINT_STATUS = (
    "provisional exact geometry; no authoritative endpoint-footprint certificate"
)

SOURCE_CONTRACTS = (
    (
        "packing/campaign/series/series-000-smoke-and-calibration/results/agenda-031/"
        "proofs/corner-owner-sector-footprints.md"
    ),
    "/private/tmp/n11-sector-sprint-contract.md",
    "/private/tmp/n11-dual-salvage-contract.md",
)


@dataclass(frozen=True, slots=True)
class DirectionSource:
    """One folded-net source of a canonical square orientation."""

    folded_index: int
    reflected: bool


@dataclass(frozen=True, slots=True)
class OwnerOrientation:
    """A square orientation modulo quarter turns, with exact source provenance."""

    index: int
    direction: Direction
    sources: tuple[DirectionSource, ...]


@dataclass(frozen=True, slots=True)
class OwnerDirectionManifest:
    """The exact full direction family used to construct owner footprints."""

    angle_limit: Fraction
    direction_steps: int
    folded_count: int
    orientations: tuple[OwnerOrientation, ...]

    @property
    def full_count(self) -> int:
        return len(self.orientations)

    @property
    def directions(self) -> tuple[Direction, ...]:
        return tuple(entry.direction for entry in self.orientations)


@dataclass(frozen=True, slots=True)
class OwnerClass:
    """One raw bottom-left mark/sector class."""

    class_id: str
    mark_id: str
    mark: Point
    sector: int
    reflected_class_id: str
    representative: bool


@dataclass(frozen=True, slots=True)
class OwnerBranchManifest:
    """The exhaustive one-corner class partition and its sound reflection pairs."""

    directions: OwnerDirectionManifest
    classes: tuple[OwnerClass, ...]
    representatives: tuple[str, ...]
    reflection_pairs: tuple[tuple[str, str], ...]
    endpoint_footprint_status: str
    source_contracts: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class StrictResidualDomain:
    """A strict residual family represented by positive-area closed covers.

    ``forbidden_polygon`` is ``rot(footprint) + [-side/2, side/2]^2``.  The physical
    centres are in the interior of ``container_polygon`` and outside the closed
    forbidden polygon.  ``components`` are separate closed exterior-half-plane
    intersections with positive area.  Their union covers every physical centre and
    also contains some tangencies on its boundary; membership in that union alone is
    therefore not a claim of strict disjointness.
    """

    direction: Direction
    square_side: Fraction
    footprint: Polygon
    forbidden_polygon: Polygon
    container_polygon: Polygon
    components: tuple[Polygon, ...]
    physical_semantics: str = "interior(container) minus closed(forbidden)"
    component_semantics: str = "positive-area closed cover of the strict physical domain"


def _proper_rotation(direction: Direction) -> None:
    if (direction.vx, direction.vy) != (-direction.uy, direction.ux):
        raise ValueError("direction must use the counterclockwise orthogonal second axis")


def _canonical_square_axis(direction: Direction) -> Point:
    """Return the unique first-quadrant axis representing a square orientation."""

    _proper_rotation(direction)
    candidates = (
        (direction.ux, direction.uy),
        (direction.vx, direction.vy),
        (-direction.ux, -direction.uy),
        (-direction.vx, -direction.vy),
    )
    matches = tuple((x, y) for x, y in candidates if x > 0 and y >= 0)
    if len(matches) != 1:
        raise ValueError("could not canonicalize square orientation modulo quarter turns")
    return matches[0]


def full_owner_direction_manifest(
    *,
    angle_limit: Fraction = ANGLE_LIMIT,
    direction_steps: int = DIRECTION_STEPS,
) -> OwnerDirectionManifest:
    """Build the full exact net before any numerical direction subset is chosen."""

    if direction_steps < 1:
        raise ValueError("direction_steps must be positive")
    folded = direction_net(net_half_tangents(angle_limit, direction_steps))
    sources_by_axis: dict[Point, list[DirectionSource]] = {}
    for index, direction in enumerate(folded):
        reflected = Direction(
            f"{index}-reflected",
            direction.uy,
            direction.ux,
            -direction.ux,
            direction.uy,
        )
        for candidate, is_reflected in ((direction, False), (reflected, True)):
            axis = _canonical_square_axis(candidate)
            sources_by_axis.setdefault(axis, []).append(DirectionSource(index, is_reflected))

    axes = sorted(sources_by_axis, key=cmp_to_key(_compare_first_quadrant_rays))
    orientations = tuple(
        OwnerOrientation(
            index,
            Direction(f"owner-{index:03d}", cosine, sine, -sine, cosine),
            tuple(sources_by_axis[(cosine, sine)]),
        )
        for index, (cosine, sine) in enumerate(axes)
    )
    return OwnerDirectionManifest(angle_limit, direction_steps, len(folded), orientations)


def owner_branch_manifest(
    directions: OwnerDirectionManifest | None = None,
) -> OwnerBranchManifest:
    """Return all sixteen raw classes and the eight diagonal-reflection pairs."""

    direction_manifest = directions or full_owner_direction_manifest()
    classes: list[OwnerClass] = []
    for mark_id, mark in BOTTOM_LEFT_MARKS.items():
        other = "m2" if mark_id == "m1" else "m1"
        for sector in range(8):
            reflected_sector = (7 - sector) % 8
            classes.append(
                OwnerClass(
                    f"bottom-left:{mark_id}:j{sector}",
                    mark_id,
                    mark,
                    sector,
                    f"bottom-left:{other}:j{reflected_sector}",
                    mark_id == "m1",
                )
            )
    representatives = tuple(entry.class_id for entry in classes if entry.representative)
    reflection_pairs = tuple(
        (entry.class_id, entry.reflected_class_id) for entry in classes if entry.representative
    )
    return OwnerBranchManifest(
        direction_manifest,
        tuple(classes),
        representatives,
        reflection_pairs,
        ENDPOINT_FOOTPRINT_STATUS,
        SOURCE_CONTRACTS,
    )


def _compare_first_quadrant_rays(left: Point, right: Point) -> int:
    cross = _cross(left, right)
    if cross > 0:
        return -1
    if cross < 0:
        return 1
    return (left > right) - (left < right)


def _cross(left: Point, right: Point) -> Fraction:
    return left[0] * right[1] - left[1] * right[0]


def _subtract(left: Point, right: Point) -> Point:
    return left[0] - right[0], left[1] - right[1]


def _add(left: Point, right: Point) -> Point:
    return left[0] + right[0], left[1] + right[1]


def _scale(factor: Fraction, point: Point) -> Point:
    return factor * point[0], factor * point[1]


def _quarter_turn(point: Point) -> Point:
    return -point[1], point[0]


def _sector_contains(sector: int, ray: Point) -> bool:
    if not 0 <= sector < 8:
        raise ValueError("sector must lie in 0..7")
    x, y = ray
    return (
        (x >= 0 and y >= 0 and x >= y),
        (x >= 0 and y >= 0 and y >= x),
        (x <= 0 and y >= 0 and y >= -x),
        (x <= 0 and y >= 0 and -x >= y),
        (x <= 0 and y <= 0 and -x >= -y),
        (x <= 0 and y <= 0 and -y >= -x),
        (x >= 0 and y <= 0 and -y >= x),
        (x >= 0 and y <= 0 and x >= -y),
    )[sector]


def signed_axis_rays(directions: tuple[Direction, ...]) -> tuple[Point, ...]:
    """Deduplicate all four signed axes of every exact square orientation."""

    rays: set[Point] = set()
    for direction in directions:
        _proper_rotation(direction)
        rays.update(
            {
                (direction.ux, direction.uy),
                (direction.vx, direction.vy),
                (-direction.ux, -direction.uy),
                (-direction.vx, -direction.vy),
            }
        )
    return tuple(sorted(rays))


def sector_endpoint_rays(sector: int, directions: tuple[Direction, ...]) -> tuple[Point, Point]:
    """Select the angularly first and last retained signed rays in one closed sector."""

    candidates = [ray for ray in signed_axis_rays(directions) if _sector_contains(sector, ray)]
    if not candidates:
        raise ValueError(f"sector {sector} has no retained signed-axis ray")
    candidates.sort(key=cmp_to_key(_compare_sector_rays))
    return candidates[0], candidates[-1]


def _compare_sector_rays(left: Point, right: Point) -> int:
    if left == right:
        return 0
    cross = _cross(left, right)
    if cross > 0:
        return -1
    if cross < 0:
        return 1
    return (left > right) - (left < right)


def triangle_footprint(mark: Point, sector: int, *, half: Fraction = HALF_CORE) -> Polygon:
    """Construct the reviewed rational triangle guaranteed by one owner class."""

    rays = (
        (half, Fraction(0)),
        (half / 2, half / 2),
        (Fraction(0), half),
        (-half / 2, half / 2),
        (-half, Fraction(0)),
        (-half / 2, -half / 2),
        (Fraction(0), -half),
        (half / 2, -half / 2),
    )
    if not 0 <= sector < 8:
        raise ValueError("sector must lie in 0..7")
    return _normalise_polygon(
        (mark, _add(mark, rays[(sector + 1) % 8]), _add(mark, rays[(sector + 2) % 8]))
    )


def point_footprint(mark: Point) -> Polygon:
    """Represent bare mark ownership as a one-vertex convex footprint."""

    return (mark,)


def anchored_quarter(mark: Point, ray: Point, *, half: Fraction = HALF_CORE) -> Polygon:
    """Construct the anchored quarter-core square ``Q_ray(mark)``."""

    if ray[0] * ray[0] + ray[1] * ray[1] != 1:
        raise ValueError("anchored-quarter ray must have exact unit length")
    turned = _quarter_turn(ray)
    return (
        mark,
        _add(mark, _scale(half, ray)),
        _add(mark, _scale(half, _add(ray, turned))),
        _add(mark, _scale(half, turned)),
    )


def endpoint_footprint(
    mark: Point,
    sector: int,
    directions: tuple[Direction, ...] | None = None,
    *,
    half: Fraction = HALF_CORE,
) -> Polygon:
    """Construct the provisional exact endpoint-intersection quadrilateral."""

    full_directions = directions or full_owner_direction_manifest().directions
    first, last = sector_endpoint_rays(sector, full_directions)
    dot = first[0] * last[0] + first[1] * last[1]
    determinant = _cross(first, last)
    if determinant < 0 or determinant > 1 or dot <= 0:
        raise ValueError("sector endpoint rays do not span an acute counterclockwise wedge")
    turned = _quarter_turn(first)
    middle_vector = _add(_scale(dot / (1 + determinant), first), turned)
    return _normalise_polygon(
        (
            mark,
            _add(mark, _scale(half, last)),
            _add(mark, _scale(half, middle_vector)),
            _add(mark, _scale(half, turned)),
        )
    )


def owner_class_footprints(
    owner_class: OwnerClass,
    directions: tuple[Direction, ...] | None = None,
) -> dict[str, Polygon]:
    """Return the nested point, reviewed triangle, and provisional enlarged arms."""

    return {
        "point": point_footprint(owner_class.mark),
        "triangle": triangle_footprint(owner_class.mark, owner_class.sector),
        "endpoint": endpoint_footprint(
            owner_class.mark, owner_class.sector, directions=directions
        ),
    }


def polygon_area_twice(polygon: Polygon) -> Fraction:
    """Return the signed doubled area of a polygon."""

    return sum(
        (
            first[0] * second[1] - first[1] * second[0]
            for first, second in zip(polygon, polygon[1:] + polygon[:1], strict=True)
        ),
        start=Fraction(0),
    )


def _normalise_polygon(polygon: Polygon) -> Polygon:
    cleaned: list[Point] = []
    for point in polygon:
        if not cleaned or point != cleaned[-1]:
            cleaned.append(point)
    if len(cleaned) > 1 and cleaned[0] == cleaned[-1]:
        cleaned.pop()
    changed = True
    while changed and len(cleaned) >= 3:
        changed = False
        for index in range(len(cleaned)):
            previous = cleaned[index - 1]
            current = cleaned[index]
            following = cleaned[(index + 1) % len(cleaned)]
            if _cross(_subtract(current, previous), _subtract(following, current)) == 0:
                cleaned.pop(index)
                changed = True
                break
    result = tuple(cleaned)
    if polygon_area_twice(result) < 0:
        result = tuple(reversed(result))
    return result


def convex_hull(points: tuple[Point, ...]) -> Polygon:
    """Return the exact counterclockwise convex hull without collinear vertices."""

    ordered = sorted(set(points))
    if len(ordered) <= 1:
        return tuple(ordered)

    def half(sequence: list[Point]) -> list[Point]:
        result: list[Point] = []
        for point in sequence:
            while (
                len(result) >= 2
                and _cross(_subtract(result[-1], result[-2]), _subtract(point, result[-1])) <= 0
            ):
                result.pop()
            result.append(point)
        return result

    return tuple(half(ordered)[:-1] + half(list(reversed(ordered)))[:-1])


def point_in_closed_convex_polygon(point: Point, polygon: Polygon) -> bool:
    """Test exact membership in a convex polygon, including its boundary."""

    if not polygon:
        return False
    if len(polygon) == 1:
        return point == polygon[0]
    if len(polygon) == 2:
        delta = _subtract(polygon[1], polygon[0])
        offset = _subtract(point, polygon[0])
        return _cross(delta, offset) == 0 and all(
            min(first, second) <= value <= max(first, second)
            for first, second, value in zip(polygon[0], polygon[1], point, strict=True)
        )
    orientation = 1 if polygon_area_twice(polygon) > 0 else -1
    return all(
        orientation * _cross(_subtract(second, first), _subtract(point, first)) >= 0
        for first, second in zip(polygon, polygon[1:] + polygon[:1], strict=True)
    )


def convex_polygon_contains_polygon(container: Polygon, contained: Polygon) -> bool:
    """Test exact closed containment using convexity."""

    return bool(contained) and all(
        point_in_closed_convex_polygon(point, container) for point in contained
    )


def _clip_half_plane(polygon: Polygon, a: Fraction, b: Fraction, bound: Fraction) -> Polygon:
    if not polygon:
        return ()
    output: list[Point] = []

    def signed(point: Point) -> Fraction:
        return a * point[0] + b * point[1] - bound

    previous = polygon[-1]
    previous_value = signed(previous)
    previous_inside = previous_value <= 0
    for current in polygon:
        current_value = signed(current)
        current_inside = current_value <= 0
        if current_inside != previous_inside:
            factor = previous_value / (previous_value - current_value)
            output.append(
                (
                    previous[0] + factor * (current[0] - previous[0]),
                    previous[1] + factor * (current[1] - previous[1]),
                )
            )
        if current_inside:
            output.append(current)
        previous = current
        previous_value = current_value
        previous_inside = current_inside
    return _normalise_polygon(tuple(output))


def convex_polygon_intersection(first: Polygon, second: Polygon) -> Polygon:
    """Intersect two counterclockwise convex rational polygons exactly."""

    if not first or not second:
        return ()
    if len(second) < 3 or polygon_area_twice(second) <= 0:
        raise ValueError("clipping polygon must be nondegenerate and counterclockwise")
    result = first
    for start, end in zip(second, second[1:] + second[:1], strict=True):
        delta = _subtract(end, start)
        # Interior of a counterclockwise edge is to its left.
        result = _clip_half_plane(
            result,
            delta[1],
            -delta[0],
            delta[1] * start[0] - delta[0] * start[1],
        )
        if not result:
            break
    return result


def _rotated_point(point: Point, direction: Direction) -> Point:
    return (
        direction.ux * point[0] + direction.uy * point[1],
        direction.vx * point[0] + direction.vy * point[1],
    )


def forbidden_centre_polygon(
    footprint: Polygon, square_side: Fraction, direction: Direction
) -> Polygon:
    """Build ``rot(footprint) + [-side/2, side/2]^2`` as an exact hull."""

    if not footprint:
        raise ValueError("footprint must be nonempty")
    _proper_rotation(direction)
    half = square_side / 2
    square = ((-half, -half), (half, -half), (half, half), (-half, half))
    rotated = tuple(_rotated_point(point, direction) for point in footprint)
    return convex_hull(tuple(_add(point, corner) for point in rotated for corner in square))


def container_centre_polygon(
    outer_side: Fraction, square_side: Fraction, direction: Direction
) -> Polygon:
    """Build the exact centre polygon for strict containment in its interior."""

    _proper_rotation(direction)
    extent = square_side * (abs(direction.ux) + abs(direction.uy)) / 2
    low, high = extent, outer_side - extent
    if low >= high:
        raise ValueError("square has no full-dimensional centre domain in the container")
    physical = ((low, low), (high, low), (high, high), (low, high))
    return tuple(_rotated_point(point, direction) for point in physical)


def strict_residual_domain(
    outer_side: Fraction,
    square_side: Fraction,
    direction: Direction,
    footprint: Polygon,
) -> StrictResidualDomain:
    """Build separate positive-area closures covering the strict residual domain."""

    container = container_centre_polygon(outer_side, square_side, direction)
    forbidden = forbidden_centre_polygon(footprint, square_side, direction)
    components: list[Polygon] = []
    seen: set[Polygon] = set()
    for start, end in zip(forbidden, forbidden[1:] + forbidden[:1], strict=True):
        delta = _subtract(end, start)
        a, b = -delta[1], delta[0]
        bound = a * start[0] + b * start[1]
        piece = _clip_half_plane(container, a, b, bound)
        if len(piece) < 3 or polygon_area_twice(piece) <= 0:
            continue
        canonical = _canonical_polygon_cycle(piece)
        if canonical not in seen:
            seen.add(canonical)
            components.append(piece)
    return StrictResidualDomain(
        direction, square_side, footprint, forbidden, container, tuple(components)
    )


def _canonical_polygon_cycle(polygon: Polygon) -> Polygon:
    index = min(range(len(polygon)), key=polygon.__getitem__)
    return polygon[index:] + polygon[:index]


def point_in_open_convex_polygon(point: Point, polygon: Polygon) -> bool:
    """Test exact membership in the interior of a nondegenerate convex polygon."""

    if len(polygon) < 3 or polygon_area_twice(polygon) == 0:
        return False
    orientation = 1 if polygon_area_twice(polygon) > 0 else -1
    return all(
        orientation * _cross(_subtract(second, first), _subtract(point, first)) > 0
        for first, second in zip(polygon, polygon[1:] + polygon[:1], strict=True)
    )


def centre_in_component_closures(centre_uv: Point, domain: StrictResidualDomain) -> bool:
    """Test membership in the domain's closed positive-area component cover."""

    return any(
        point_in_closed_convex_polygon(centre_uv, component) for component in domain.components
    )


def convex_polygons_strictly_disjoint(first: Polygon, second: Polygon) -> bool:
    """Use exact SAT to require a positive gap between two closed convex polygons."""

    if not first or not second:
        raise ValueError("strict-disjointness operands must be nonempty")
    axes = []
    for polygon in (first, second):
        for start, end in zip(polygon, polygon[1:] + polygon[:1], strict=True):
            delta = _subtract(end, start)
            if delta != (0, 0):
                axes.append((-delta[1], delta[0]))
    for axis in axes:
        first_projection = tuple(axis[0] * x + axis[1] * y for x, y in first)
        second_projection = tuple(axis[0] * x + axis[1] * y for x, y in second)
        if max(first_projection) < min(second_projection) or max(second_projection) < min(
            first_projection
        ):
            return True
    return False


def centre_in_strict_residual_domain(centre_uv: Point, domain: StrictResidualDomain) -> bool:
    """Apply the physical strict semantics, independent of component membership."""

    if not point_in_open_convex_polygon(centre_uv, domain.container_polygon):
        return False
    half = domain.square_side / 2
    core = tuple(
        _add(centre_uv, offset)
        for offset in ((-half, -half), (half, -half), (half, half), (-half, half))
    )
    rotated_footprint = tuple(
        _rotated_point(point, domain.direction) for point in domain.footprint
    )
    return convex_polygons_strictly_disjoint(core, rotated_footprint)


def cheap_guard_receipt() -> dict[str, Any]:
    """Report construction-only cardinalities without running a scientific target."""

    manifest = owner_branch_manifest()
    signed_rays = signed_axis_rays(manifest.directions.directions)
    endpoints = tuple(
        sector_endpoint_rays(sector, manifest.directions.directions) for sector in range(8)
    )
    return {
        "evidence_tier": "instrument construction controls only",
        "scientific_target_run": False,
        "folded_direction_count": manifest.directions.folded_count,
        "full_square_orientation_count": manifest.directions.full_count,
        "signed_axis_ray_count": len(signed_rays),
        "raw_owner_class_count": len(manifest.classes),
        "reflected_representative_count": len(manifest.representatives),
        "reflection_pair_count": len(manifest.reflection_pairs),
        "sector_endpoint_pairs": endpoints,
        "endpoint_footprint_status": ENDPOINT_FOOTPRINT_STATUS,
        "source_contracts": SOURCE_CONTRACTS,
    }
