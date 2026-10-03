"""`induction.minkowski_sum` is the hull of the pairwise sums, vertex for vertex.

`forbidden_regions` once built each `K_j - Q_i` as the hull of every pairwise
difference; it now merges the two hulls' edges and hands the visited points to the same
`hull`. The checker's events and regions depend on those polygons being the same list
in the same order, so the comparison here is `==` on the lists, over random polygons
in general and degenerate position and over the explicit cases the merge treats apart.
"""

from __future__ import annotations

import random
from collections.abc import Callable

from sqpack.hull_kernel.geometry import Point, Polygon
from sqpack.hull_kernel.induction import forbidden_regions, hull, minkowski_sum
from sqpack.hull_kernel.rational import Q


def pairwise_hull(left: Polygon, right: Polygon) -> Polygon:
    """The form `forbidden_regions` used before the edge merge."""
    return hull([(p[0] + q[0], p[1] + q[1]) for p in left for q in right])


def random_points(rng: random.Random, count: int) -> Polygon:
    return [
        (Q(rng.randint(-24, 24), rng.randint(1, 5)), Q(rng.randint(-24, 24), rng.randint(1, 5)))
        for _ in range(count)
    ]


def random_collinear(rng: random.Random, count: int) -> Polygon:
    origin = random_points(rng, 1)[0]
    dx, dy = Q(rng.randint(-5, 5)), Q(rng.randint(-5, 5))
    return [
        (origin[0] + k * dx, origin[1] + k * dy)
        for k in (rng.randint(-6, 6) for _ in range(count))
    ]


GENERATORS: tuple[Callable[[random.Random, int], Polygon], ...] = (
    random_points,
    random_collinear,
)


def random_polygon(rng: random.Random) -> Polygon:
    """Mostly points in general position, so the merge path is the one mostly taken;
    one in four is collinear or tiny, so the pairwise fallback is taken too."""
    if rng.random() < 0.25:
        return rng.choice(GENERATORS)(rng, rng.randint(1, 6))
    return random_points(rng, rng.randint(3, 9))


def test_the_merge_matches_the_pairwise_hull_on_random_polygons() -> None:
    rng = random.Random(20261003)
    merged_paths = 0
    for _ in range(600):
        left, right = random_polygon(rng), random_polygon(rng)
        if rng.random() < 0.2:
            left = [*left, rng.choice(left)]  # a repeated point
        expected = pairwise_hull(left, right)
        assert minkowski_sum(left, right) == expected
        assert minkowski_sum(right, left) == expected
        merged_paths += len(hull(left)) >= 3 and len(hull(right)) >= 3
    assert 250 <= merged_paths <= 550, merged_paths


def test_the_explicit_cases_the_merge_treats_apart() -> None:
    square: Polygon = [(Q(0), Q(0)), (Q(2), Q(0)), (Q(2), Q(2)), (Q(0), Q(2))]
    diamond: Polygon = [(Q(1), Q(0)), (Q(2), Q(1)), (Q(1), Q(2)), (Q(0), Q(1))]
    point: Polygon = [(Q(3, 7), Q(-5, 3))]
    segment: Polygon = [(Q(0), Q(0)), (Q(3), Q(1))]
    collinear: Polygon = [(Q(0), Q(0)), (Q(1), Q(1)), (Q(2), Q(2)), (Q(1), Q(1))]
    triangle: Polygon = [(Q(0), Q(0)), (Q(4), Q(0)), (Q(0), Q(1))]
    for left, right in [
        (square, square),  # every edge parallel to one of the other's: the cross == 0 path
        (square, diamond),
        (diamond, triangle),
        (point, square),
        (segment, square),
        (collinear, square),
        (point, point),
        (segment, segment),
        (segment, [(Q(0), Q(0)), (Q(-3), Q(-1))]),
        (triangle, [(Q(0), Q(0)), (Q(0), Q(-4)), (Q(-1), Q(0))]),  # a summand reflected
    ]:
        assert minkowski_sum(left, right) == pairwise_hull(left, right)
        assert minkowski_sum(right, left) == pairwise_hull(right, left)


def test_forbidden_regions_are_the_pairwise_differences_in_owner_order() -> None:
    rng = random.Random(7)
    for _ in range(40):
        prior = {
            owner: rng.choice(GENERATORS)(rng, rng.randint(1, 8)) for owner in (3, 1, 2, 5)
        }
        core = random_points(rng, rng.randint(3, 7))
        owner = rng.choice(list(prior))
        expected = [
            hull([(p[0] - q[0], p[1] - q[1]) for p in group for q in core])
            for other, group in prior.items()
            if other != owner
        ]
        assert forbidden_regions(prior, owner, core) == expected


def test_a_sum_is_a_polygon_of_the_same_type() -> None:
    result = minkowski_sum([(Q(1, 2), Q(1, 3))], [(Q(1, 2), Q(2, 3))])
    expected: list[Point] = [(Q(1), Q(1))]
    assert result == expected
    assert all(type(x) is type(Q(1)) for point in result for x in point)
