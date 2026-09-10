"""Independent exact controls for generic corner-owner footprint geometry."""

from __future__ import annotations

from fractions import Fraction

from devtools.owner_footprints import (
    ANGLE_LIMIT,
    BOTTOM_LEFT_MARKS,
    CORE_SIDE,
    DIRECTION_STEPS,
    ENDPOINT_FOOTPRINT_STATUS,
    HALF_CORE,
    OUTER_SIDE,
    Point,
    Polygon,
    anchored_quarter,
    centre_in_component_closures,
    centre_in_strict_residual_domain,
    cheap_guard_receipt,
    convex_polygon_contains_polygon,
    convex_polygon_intersection,
    endpoint_footprint,
    full_owner_direction_manifest,
    owner_branch_manifest,
    owner_class_footprints,
    point_footprint,
    point_in_closed_convex_polygon,
    polygon_area_twice,
    sector_endpoint_rays,
    signed_axis_rays,
    strict_residual_domain,
    triangle_footprint,
)
from sqpack.fractional.model import Direction, rotation_from_half_tangent


def _cross(left: Point, right: Point) -> Fraction:
    return left[0] * right[1] - left[1] * right[0]


def _subtract(left: Point, right: Point) -> Point:
    return left[0] - right[0], left[1] - right[1]


def _reflect(polygon: Polygon) -> set[Point]:
    return {(y, x) for x, y in polygon}


def _uv(direction: Direction, point: Point) -> Point:
    x, y = point
    return (
        direction.ux * x + direction.uy * y,
        direction.vx * x + direction.vy * y,
    )


def _core_polygon(direction: Direction, centre_xy: Point, side: Fraction) -> Polygon:
    half = side / 2
    u = direction.ux, direction.uy
    v = direction.vx, direction.vy
    offsets = (
        (-half * u[0] - half * v[0], -half * u[1] - half * v[1]),
        (half * u[0] - half * v[0], half * u[1] - half * v[1]),
        (half * u[0] + half * v[0], half * u[1] + half * v[1]),
        (-half * u[0] + half * v[0], -half * u[1] + half * v[1]),
    )
    return tuple((centre_xy[0] + x, centre_xy[1] + y) for x, y in offsets)


def _projection(polygon: Polygon, axis: Point) -> tuple[Fraction, Fraction]:
    values = tuple(axis[0] * x + axis[1] * y for x, y in polygon)
    return min(values), max(values)


def _direct_sat(first: Polygon, second: Polygon, *, positive_gap: bool) -> bool:
    """Independent SAT for closed disjointness or interior nonoverlap."""

    axes: list[Point] = []
    for polygon in (first, second):
        for start, end in zip(polygon, polygon[1:] + polygon[:1], strict=True):
            edge = _subtract(end, start)
            if edge != (0, 0):
                axes.append((-edge[1], edge[0]))
    for axis in axes:
        first_low, first_high = _projection(first, axis)
        second_low, second_high = _projection(second, axis)
        if positive_gap:
            separated = first_high < second_low or second_high < first_low
        else:
            separated = first_high <= second_low or second_high <= first_low
        if separated:
            return True
    return False


def _strictly_contained(core: Polygon, outer_side: Fraction) -> bool:
    return all(0 < x < outer_side and 0 < y < outer_side for x, y in core)


def test_full_orientation_and_branch_manifests_are_exact_and_exhaustive() -> None:
    directions = full_owner_direction_manifest()
    assert directions.angle_limit == ANGLE_LIMIT
    assert directions.direction_steps == DIRECTION_STEPS
    assert directions.folded_count == 181
    assert directions.full_count == 361
    assert sum(len(entry.sources) for entry in directions.orientations) == 362
    assert sorted(len(entry.sources) for entry in directions.orientations).count(2) == 1
    assert all(
        direction.ux > 0
        and direction.uy >= 0
        and direction.ux * direction.ux + direction.uy * direction.uy == 1
        for direction in directions.directions
    )
    assert len({(direction.ux, direction.uy) for direction in directions.directions}) == 361
    assert directions.directions[0].ux == 1
    assert directions.directions[0].uy == 0
    assert directions.directions[-1].uy > directions.directions[-1].ux

    branch = owner_branch_manifest(directions)
    assert len(branch.classes) == 16
    assert len(branch.representatives) == len(branch.reflection_pairs) == 8
    assert len({entry.class_id for entry in branch.classes}) == 16
    assert {entry.sector for entry in branch.classes if entry.mark_id == "m1"} == set(range(8))
    assert all(entry.class_id in branch.representatives for entry in branch.classes[:8])
    assert branch.endpoint_footprint_status == ENDPOINT_FOOTPRINT_STATUS

    by_id = {entry.class_id: entry for entry in branch.classes}
    for entry in branch.classes:
        reflected = by_id[entry.reflected_class_id]
        assert reflected.mark == (entry.mark[1], entry.mark[0])
        assert reflected.sector == (7 - entry.sector) % 8
        assert reflected.reflected_class_id == entry.class_id


def test_all_nested_footprints_and_reflections_match_exactly() -> None:
    manifest = owner_branch_manifest()
    by_id = {entry.class_id: entry for entry in manifest.classes}
    for entry in manifest.classes:
        footprints = owner_class_footprints(entry, manifest.directions.directions)
        assert footprints["point"] == point_footprint(entry.mark)
        assert convex_polygon_contains_polygon(footprints["triangle"], footprints["point"])
        assert convex_polygon_contains_polygon(footprints["endpoint"], footprints["triangle"])
        assert len(footprints["triangle"]) == 3
        assert len(footprints["endpoint"]) == 4
        assert polygon_area_twice(footprints["triangle"]) / 2 == CORE_SIDE * CORE_SIDE / 16

        reflected = by_id[entry.reflected_class_id]
        reflected_footprints = owner_class_footprints(reflected, manifest.directions.directions)
        for kind in footprints:
            assert _reflect(footprints[kind]) == set(reflected_footprints[kind])


def test_endpoint_formula_matches_clipping_and_every_retained_intermediate_square() -> None:
    directions = full_owner_direction_manifest().directions
    rays = signed_axis_rays(directions)
    mark = BOTTOM_LEFT_MARKS["m1"]
    for sector in range(8):
        first, last = sector_endpoint_rays(sector, directions)
        footprint = endpoint_footprint(mark, sector, directions)
        independently_clipped = convex_polygon_intersection(
            anchored_quarter(mark, first), anchored_quarter(mark, last)
        )
        assert set(footprint) == set(independently_clipped)

        determinant = _cross(first, last)
        dot = first[0] * last[0] + first[1] * last[1]
        assert polygon_area_twice(footprint) / 2 == HALF_CORE * HALF_CORE * dot / (
            1 + determinant
        )
        intermediate = tuple(
            ray for ray in rays if _cross(first, ray) >= 0 and _cross(ray, last) >= 0
        )
        assert first in intermediate
        assert last in intermediate
        assert all(
            convex_polygon_contains_polygon(anchored_quarter(mark, ray), footprint)
            for ray in intermediate
        )


def test_minkowski_piece_union_matches_independent_sat_in_rotated_frames() -> None:
    directions = (
        rotation_from_half_tangent("axis", Fraction(0)),
        rotation_from_half_tangent("three-four-five", Fraction(1, 3)),
        Direction(
            "reflected-three-four-five",
            Fraction(3, 5),
            Fraction(4, 5),
            Fraction(-4, 5),
            Fraction(3, 5),
        ),
    )
    footprint = triangle_footprint(BOTTOM_LEFT_MARKS["m1"], 0)
    coordinates = tuple(Fraction(value, 20) for value in range(10, 68, 3))
    for direction in directions:
        domain = strict_residual_domain(OUTER_SIDE, CORE_SIDE, direction, footprint)
        assert 4 <= len(domain.forbidden_polygon) <= 7
        assert all(polygon_area_twice(component) > 0 for component in domain.components)
        for x in coordinates:
            for y in coordinates:
                centre_xy = (x, y)
                centre_uv = _uv(direction, centre_xy)
                core = _core_polygon(direction, centre_xy, CORE_SIDE)
                strict_expected = _strictly_contained(core, OUTER_SIDE) and _direct_sat(
                    core, footprint, positive_gap=True
                )
                assert centre_in_strict_residual_domain(centre_uv, domain) == strict_expected
                if strict_expected:
                    assert centre_in_component_closures(centre_uv, domain)

                weak_expected = all(
                    0 <= px <= OUTER_SIDE and 0 <= py <= OUTER_SIDE for px, py in core
                ) and _direct_sat(core, footprint, positive_gap=False)
                if weak_expected and _strictly_contained(core, OUTER_SIDE):
                    assert centre_in_component_closures(centre_uv, domain)


def test_strict_domain_distinguishes_gap_tangency_overlap_and_container_boundary() -> None:
    axis = rotation_from_half_tangent("axis", Fraction(0))
    mark = (Fraction(2), Fraction(2))
    domain = strict_residual_domain(OUTER_SIDE, CORE_SIDE, axis, point_footprint(mark))
    assert len(domain.forbidden_polygon) == 4
    assert len(domain.components) == 4
    epsilon = Fraction(1, 1_000_000)
    positive_gap = (mark[0] + HALF_CORE + epsilon, mark[1])
    tangent = (mark[0] + HALF_CORE, mark[1])
    overlap = (mark[0] + HALF_CORE - epsilon, mark[1])
    assert centre_in_strict_residual_domain(positive_gap, domain)
    assert centre_in_component_closures(positive_gap, domain)
    assert not centre_in_strict_residual_domain(tangent, domain)
    assert centre_in_component_closures(tangent, domain)
    assert not centre_in_strict_residual_domain(overlap, domain)
    assert not centre_in_component_closures(overlap, domain)

    container_boundary = (HALF_CORE, OUTER_SIDE / 2)
    assert point_in_closed_convex_polygon(container_boundary, domain.container_polygon)
    assert not centre_in_strict_residual_domain(container_boundary, domain)


def test_positive_area_thin_piece_is_retained_and_zero_area_limit_is_removed() -> None:
    axis = rotation_from_half_tangent("axis", Fraction(0))
    epsilon = Fraction(1, 1_000_000)
    almost_covering: Polygon = (
        (Fraction(0), Fraction(0)),
        (OUTER_SIDE - CORE_SIDE - epsilon, Fraction(0)),
        (OUTER_SIDE - CORE_SIDE - epsilon, OUTER_SIDE),
        (Fraction(0), OUTER_SIDE),
    )
    thin = strict_residual_domain(OUTER_SIDE, CORE_SIDE, axis, almost_covering)
    assert len(thin.components) == 1
    xs = tuple(x for x, _ in thin.components[0])
    assert max(xs) - min(xs) == epsilon
    assert polygon_area_twice(thin.components[0]) > 0

    exactly_covering: Polygon = (
        (Fraction(0), Fraction(0)),
        (OUTER_SIDE - CORE_SIDE, Fraction(0)),
        (OUTER_SIDE - CORE_SIDE, OUTER_SIDE),
        (Fraction(0), OUTER_SIDE),
    )
    boundary_only = strict_residual_domain(OUTER_SIDE, CORE_SIDE, axis, exactly_covering)
    assert boundary_only.components == ()


def test_cheap_guard_receipt_reports_only_construction_cardinalities() -> None:
    receipt = cheap_guard_receipt()
    assert receipt["evidence_tier"] == "instrument construction controls only"
    assert receipt["scientific_target_run"] is False
    assert receipt["folded_direction_count"] == 181
    assert receipt["full_square_orientation_count"] == 361
    assert receipt["signed_axis_ray_count"] == 1444
    assert receipt["raw_owner_class_count"] == 16
    assert receipt["reflected_representative_count"] == 8
    assert receipt["reflection_pair_count"] == 8
    assert receipt["endpoint_footprint_status"] == ENDPOINT_FOOTPRINT_STATUS
