"""Independent exact controls for the multiple-owner vertical decomposition."""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations

import pytest

from devtools.multi_owner_domains import (
    centre_in_decomposition_closures,
    centre_in_strict_multi_footprint_domain,
    compatible_axis_parent_centres,
    compatible_m1_j0_footprints,
    default_multi_owner_directions,
    guard_receipt,
    multi_footprint_domain,
    vertical_decompose,
)
from devtools.owner_footprints import (
    CORE_SIDE,
    OUTER_SIDE,
    Point,
    Polygon,
    centre_in_component_closures,
    convex_polygon_intersection,
    convex_polygons_strictly_disjoint,
    point_in_closed_convex_polygon,
    point_in_open_convex_polygon,
    polygon_area_twice,
    strict_residual_domain,
)
from sqpack.fractional.model import Direction, rotation_from_half_tangent

F = Fraction


def _rectangle(
    x0: int | Fraction, y0: int | Fraction, x1: int | Fraction, y1: int | Fraction
) -> Polygon:
    return ((F(x0), F(y0)), (F(x1), F(y0)), (F(x1), F(y1)), (F(x0), F(y1)))


def _direct(point: Point, container: Polygon, obstacles: tuple[Polygon, ...]) -> bool:
    return point_in_open_convex_polygon(point, container) and not any(
        point_in_closed_convex_polygon(point, obstacle) for obstacle in obstacles
    )


def _area(polygon: Polygon) -> Fraction:
    return abs(polygon_area_twice(polygon)) / 2


def _independent_free_area(container: Polygon, obstacles: tuple[Polygon, ...]) -> Fraction:
    """Use 15-term inclusion-exclusion, independently of vertical decomposition."""

    occupied = F(0)
    for count in range(1, len(obstacles) + 1):
        sign = 1 if count % 2 else -1
        for selected in combinations(obstacles, count):
            intersection = container
            for obstacle in selected:
                intersection = convex_polygon_intersection(intersection, obstacle)
                if len(intersection) < 3 or polygon_area_twice(intersection) == 0:
                    intersection = ()
                    break
            occupied += sign * _area(intersection)
    return _area(container) - occupied


def _assert_samples(
    container: Polygon,
    obstacles: tuple[Polygon, ...],
    coordinates: tuple[Fraction, ...],
) -> None:
    domain = vertical_decompose(container, obstacles)
    for u in coordinates:
        for v in coordinates:
            point = (u, v)
            strict = _direct(point, domain.container_polygon, domain.obstacle_polygons)
            if strict:
                assert centre_in_decomposition_closures(point, domain)
            if any(point_in_open_convex_polygon(point, piece) for piece in domain.components):
                assert strict


def test_zero_and_one_obstacle_match_direct_membership_and_existing_one_owner_cover() -> None:
    container = _rectangle(0, 0, 4, 4)
    empty = vertical_decompose(container, ())
    assert empty.components == (container,)

    obstacle = _rectangle(1, 1, 3, 3)
    _assert_samples(container, (obstacle,), tuple(F(i, 4) for i in range(-1, 18)))

    axis = rotation_from_half_tangent("axis", F(0))
    footprint = compatible_m1_j0_footprints("endpoint")[0]
    old = strict_residual_domain(OUTER_SIDE, CORE_SIDE, axis, footprint)
    new = multi_footprint_domain(OUTER_SIDE, CORE_SIDE, axis, (footprint,))
    samples = tuple(F(i, 20) for i in range(9, 70, 3))
    for u in samples:
        for v in samples:
            point = (u, v)
            old_strict = point_in_open_convex_polygon(
                point, old.container_polygon
            ) and not point_in_closed_convex_polygon(point, old.forbidden_polygon)
            assert centre_in_strict_multi_footprint_domain(point, new) == old_strict
            assert centre_in_component_closures(point, old) == centre_in_decomposition_closures(
                point, new
            )


@pytest.mark.parametrize(
    "obstacles",
    [
        (_rectangle(1, 1, 2, 2), _rectangle(1, 1, 2, 2)),
        (_rectangle(F(1, 2), 1, F(3, 2), 3), _rectangle(F(5, 2), 1, F(7, 2), 3)),
        (_rectangle(1, 1, 3, 3), _rectangle(2, 2, F(7, 2), F(7, 2))),
        (_rectangle(1, 1, 3, 3), _rectangle(F(3, 2), F(3, 2), F(5, 2), F(5, 2))),
        (_rectangle(1, 1, 2, 3), _rectangle(2, 1, 3, 3)),
        (_rectangle(1, 1, 2, 2), _rectangle(2, 2, 3, 3)),
        (_rectangle(-1, 1, 2, 3),),
    ],
)
def test_duplicate_disjoint_overlap_containment_shared_edge_tangent_and_crossing(
    obstacles: tuple[Polygon, ...],
) -> None:
    coordinates = tuple(F(i, 8) for i in range(-9, 42))
    _assert_samples(_rectangle(0, 0, 4, 4), obstacles, coordinates)


def test_closing_gap_is_retained_as_a_positive_area_triangle() -> None:
    container = _rectangle(0, 0, 4, 4)
    obstacle: Polygon = ((F(0), F(0)), (F(4), F(0)), (F(4), F(4)))
    domain = vertical_decompose(container, (obstacle,))
    assert len(domain.components) == 1
    assert len(domain.components[0]) == 3
    assert polygon_area_twice(domain.components[0]) == 16
    assert _direct((F(1), F(3)), container, (obstacle,))
    assert not _direct((F(3), F(1)), container, (obstacle,))


def test_obstacle_covering_the_full_container_has_no_positive_area_component() -> None:
    container = _rectangle(0, 0, 4, 4)
    domain = vertical_decompose(container, (_rectangle(-1, -1, 5, 5),))
    assert domain.components == ()


def test_rational_samples_on_both_sides_of_every_new_event_match_direct_semantics() -> None:
    container: Polygon = ((F(0), F(2)), (F(2), F(0)), (F(5), F(2)), (F(2), F(5)))
    obstacles = (
        ((F(0), F(1)), (F(4), F(3)), (F(3), F(4)), (F(1), F(4))),
        _rectangle(1, F(3, 2), 4, F(5, 2)),
    )
    domain = vertical_decompose(container, obstacles)
    for cut in domain.cuts[1:-1]:
        for delta in (F(-1, 10_000), F(1, 10_000)):
            u = cut + delta
            if not domain.cuts[0] < u < domain.cuts[-1]:
                continue
            for v in tuple(F(i, 17) for i in range(-2, 90)):
                point = (u, v)
                strict = _direct(point, domain.container_polygon, domain.obstacle_polygons)
                if strict:
                    assert centre_in_decomposition_closures(point, domain)
                if any(
                    point_in_open_convex_polygon(point, piece) for piece in domain.components
                ):
                    assert strict


def _core_uv(centre: Point, side: Fraction) -> Polygon:
    half = side / 2
    u, v = centre
    return (
        (u - half, v - half),
        (u + half, v - half),
        (u + half, v + half),
        (u - half, v + half),
    )


def _rotate_footprint(footprint: Polygon, direction: Direction) -> Polygon:
    return tuple(
        (
            direction.ux * x + direction.uy * y,
            direction.vx * x + direction.vy * y,
        )
        for x, y in footprint
    )


def test_four_owner_membership_matches_independent_exact_sat() -> None:
    directions = (
        rotation_from_half_tangent("axis", F(0)),
        rotation_from_half_tangent("three-four-five", F(1, 3)),
        Direction("reflected", F(3, 5), F(4, 5), F(-4, 5), F(3, 5)),
    )
    footprints = compatible_m1_j0_footprints("endpoint")
    coordinates = tuple(F(i, 20) for i in range(8, 69, 3))
    for direction in directions:
        domain = multi_footprint_domain(OUTER_SIDE, CORE_SIDE, direction, footprints)
        rotated = tuple(_rotate_footprint(footprint, direction) for footprint in footprints)
        for u in coordinates:
            for v in coordinates:
                centre = (u, v)
                expected = point_in_open_convex_polygon(
                    centre, domain.container_polygon
                ) and all(
                    convex_polygons_strictly_disjoint(_core_uv(centre, CORE_SIDE), footprint)
                    for footprint in rotated
                )
                assert centre_in_strict_multi_footprint_domain(centre, domain) == expected
                if expected:
                    assert centre_in_decomposition_closures(centre, domain)


def test_four_reflected_m1_j0_owners_are_compatible_and_scope_is_full_net() -> None:
    centres = compatible_axis_parent_centres()
    a, b = centres[0]
    assert min(a, b, OUTER_SIDE - a, OUTER_SIDE - b) > F(1, 2)
    assert OUTER_SIDE - 2 * a == F(5888, 3175) > 1
    assert OUTER_SIDE - 2 * b == F(7520, 3175) > 1
    assert len(set(centres)) == 4
    for first, second in combinations(centres, 2):
        assert abs(first[0] - second[0]) > 1 or abs(first[1] - second[1]) > 1
    assert len(default_multi_owner_directions()) == 361


def test_endpoint_domain_obeys_polynomial_raw_piece_bound_and_guard_is_non_target() -> None:
    axis = rotation_from_half_tangent("axis", F(0))
    domain = multi_footprint_domain(
        OUTER_SIDE, CORE_SIDE, axis, compatible_m1_j0_footprints("endpoint")
    )
    assert len(domain.cuts) <= 164
    assert len(domain.components) <= 815
    assert all(polygon_area_twice(component) > 0 for component in domain.components)
    receipt = guard_receipt(domain)
    assert receipt["scientific_target_run"] is False
    assert receipt["footprints"] == 4
    assert receipt["full_direction_count"] == 361


@pytest.mark.parametrize(
    "direction",
    [
        rotation_from_half_tangent("axis", F(0)),
        rotation_from_half_tangent("three-four-five", F(1, 3)),
        Direction("reflected", F(3, 5), F(4, 5), F(-4, 5), F(3, 5)),
    ],
)
def test_exact_component_area_matches_independent_obstacle_union_area(
    direction: Direction,
) -> None:
    domain = multi_footprint_domain(
        OUTER_SIDE, CORE_SIDE, direction, compatible_m1_j0_footprints("endpoint")
    )
    decomposed_area = sum((_area(component) for component in domain.components), F(0))
    expected_area = _independent_free_area(domain.container_polygon, domain.forbidden_polygons)
    assert decomposed_area == expected_area
