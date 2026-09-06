"""Controls for `sqpack.fractional.ceiling`, the dual that bounds the method.

A ceiling certificate claims that no covering measure of mass below ``n``
exists, by weak duality against a family of placements whose depth never
exceeds 1. The only way that claim can overreach is a depth above 1 that goes
unseen, an inadmissible placement, or a placement that leaves the container,
so each of those is refused here on a hand-checked instance. The positive
control is the simplest ceiling there is: four disjoint corner squares in side
2, which say what is true, that the method cannot separate ``s(4)`` from 2.
"""

from __future__ import annotations

from fractions import Fraction

import pytest

from sqpack.fractional.ceiling import (
    CeilingCertificate,
    Placement,
    arrangement_lines,
    container_vertices,
    depth_screening_is_safe,
    maximum_depth,
    scaled_to_unit_depth,
    verify_ceiling,
)

B = Fraction(9977, 10000)
LIMIT = Fraction(207107, 500000)
NET = tuple(LIMIT * k / 180 for k in range(181))
COARSE = (Fraction(0), LIMIT)
TWO = Fraction(2)


def upright(x: Fraction, y: Fraction, weight: Fraction, side: Fraction = B) -> Placement:
    return Placement(Fraction(0), x, y, weight, side)


def corners(side: Fraction, weight: Fraction = Fraction(1)) -> tuple[Placement, ...]:
    """Four axis-aligned ``side``-squares in the corners of ``[0, 2]^2``."""
    low, high = side / 2, TWO - side / 2
    return tuple(upright(x, y, weight, side) for x in (low, high) for y in (low, high))


def test_four_disjoint_corner_squares_prove_the_ceiling_at_four() -> None:
    certificate = CeilingCertificate(4, TWO, B, NET, corners(B))
    verdict = verify_ceiling(certificate)
    assert verdict.proved, verdict.failures
    assert verdict.total_weight == 4
    assert verdict.max_depth == 1
    assert verdict.regime == "net"
    assert not verdict.symmetric_only
    # The corner squares meet nothing: the deepest vertex is inside one square.
    assert verdict.decided_exactly > 0
    assert "cannot certify" in verdict.statement


def test_two_overlapping_unit_weight_squares_are_refused() -> None:
    """The negative control the module exists to pass: depth 2 is not depth 1."""
    overlapping = (
        upright(Fraction(1, 2), Fraction(1, 2), Fraction(1), Fraction(1)),
        upright(Fraction(1), Fraction(1), Fraction(1), Fraction(1)),
    )
    certificate = CeilingCertificate(2, TWO, Fraction(1), COARSE, overlapping)
    verdict = verify_ceiling(certificate)
    assert not verdict.proved
    assert verdict.failures == ("K2 depth at most 1 at every arrangement vertex",)
    assert verdict.max_depth == 2
    assert verdict.total_weight == 2


def test_large_coordinates_cannot_hide_a_false_ceiling_behind_float_screening() -> None:
    """The half-integer grid is a covering certificate below this alleged ceiling.

    A B-square contains an axis-aligned square of side at least B/sqrt(2) > 1/2,
    hence a grid point. The two coincident dual placements have depth n, not zero.
    """
    side, shrink, n = Fraction(10000000010), Fraction(9, 10), 2 * 10**21
    net = tuple(map(Fraction, ("0", "1/10", "1/5", "3/10", "2/5", "21/50")))
    square = Placement(
        Fraction(1, 5), Fraction(10**10), Fraction(70000000004, 7), Fraction(n, 2), Fraction(1)
    )
    certificate = CeilingCertificate(n, side, shrink, net, (square, square))
    assert (2 * side + 1) ** 2 < n
    assert shrink**2 > 2 * Fraction(1, 2) ** 2
    verdict = verify_ceiling(certificate)
    assert verdict.failures == ("K2 depth at most 1 at every arrangement vertex",)
    assert verdict.max_depth == n
    scaled, factor = scaled_to_unit_depth(certificate)
    assert factor == n
    assert scaled.total_weight == 1
    assert verify_ceiling(scaled).max_depth == 1


def test_coordinates_beyond_float_range_still_receive_an_exact_decision() -> None:
    large = Fraction(10**400)
    square = upright(large, large, Fraction(1), Fraction(1))
    certificate = CeilingCertificate(2, large + 1, B, NET, (square, square))
    verdict = verify_ceiling(certificate)
    assert verdict.failures == ("K2 depth at most 1 at every arrangement vertex",)
    assert verdict.max_depth == 2
    # The public intersection helper must also handle out-of-range line inputs.
    lines = [(large, Fraction(0), large), (Fraction(0), large, large)]
    assert container_vertices(certificate, lines) == [(Fraction(1), Fraction(1))]


def test_the_reported_maximum_is_exact_even_below_one() -> None:
    certificate = CeilingCertificate(1, TWO, B, NET, corners(B, Fraction(1, 4)))
    verdict = verify_ceiling(certificate)
    assert verdict.proved
    assert verdict.max_depth == Fraction(1, 4)


def test_weights_beyond_float_range_are_refused_by_the_exact_depth() -> None:
    large = Fraction(10**400)
    square = upright(Fraction(1), Fraction(1), large, Fraction(1))
    verdict = verify_ceiling(CeilingCertificate(1, TWO, B, NET, (square,)))
    assert verdict.failures == ("K2 depth at most 1 at every arrangement vertex",)
    assert verdict.max_depth == large


def test_a_large_family_uses_exact_sums_even_at_small_coordinates() -> None:
    """The family-size limit is the guard's edge: 4096 screens, 4097 goes exact."""
    vertex = (Fraction(1), Fraction(1))
    square = upright(Fraction(1), Fraction(1), Fraction(1, 4097))
    bounded = CeilingCertificate(1, TWO, B, NET, (square,) * 4096)
    assert depth_screening_is_safe(bounded, [vertex])
    certificate = CeilingCertificate(1, TWO, B, NET, (square,) * 4097)
    assert not depth_screening_is_safe(certificate, [vertex])
    worst, decided, where = maximum_depth(certificate, [vertex])
    assert worst == 1
    assert decided == 1
    assert where == vertex


def test_scaling_by_the_maximum_depth_restores_feasibility_and_halves_the_total() -> None:
    overlapping = (
        upright(Fraction(1, 2), Fraction(1, 2), Fraction(1), Fraction(1)),
        upright(Fraction(1), Fraction(1), Fraction(1), Fraction(1)),
    )
    certificate = CeilingCertificate(1, TWO, Fraction(1), COARSE, overlapping)
    scaled, factor = scaled_to_unit_depth(certificate)
    assert factor == 2
    assert scaled.total_weight == 1
    assert verify_ceiling(scaled).proved


def test_a_slight_overlap_is_found_at_the_vertex_where_two_edges_cross() -> None:
    """Weights 3/5 and 1/2 overlap on a small square; the depth there is 11/10.

    No test point grid would be trusted to land in a region this small, which
    is why the decision is at arrangement vertices and not on a grid.
    """
    family = (
        upright(Fraction(1, 2), Fraction(1, 2), Fraction(3, 5), Fraction(1)),
        upright(Fraction(29, 20), Fraction(29, 20), Fraction(1, 2), Fraction(1)),
    )
    certificate = CeilingCertificate(1, TWO, Fraction(1), COARSE, family)
    verdict = verify_ceiling(certificate)
    assert verdict.max_depth == Fraction(11, 10)
    assert not verdict.proved


def test_touching_squares_have_depth_one_along_the_shared_edge() -> None:
    """Closed squares that share an edge have depth 2 there: touching is overlap."""
    touching = (
        upright(Fraction(1, 2), Fraction(1, 2), Fraction(1), Fraction(1)),
        upright(Fraction(3, 2), Fraction(1, 2), Fraction(1), Fraction(1)),
    )
    certificate = CeilingCertificate(2, TWO, Fraction(1), COARSE, touching)
    assert verify_ceiling(certificate).max_depth == 2


def test_a_placement_outside_the_container_is_refused() -> None:
    outside = (*corners(B)[:3], upright(TWO, Fraction(1), Fraction(1)))
    verdict = verify_ceiling(CeilingCertificate(4, TWO, B, NET, outside))
    assert "K1 every placement lies in the container" in verdict.failures


def test_total_weight_below_n_is_refused_even_when_feasible() -> None:
    verdict = verify_ceiling(CeilingCertificate(5, TWO, B, NET, corners(B)))
    assert verdict.failures == ("K3 total weight at least n",)


def test_a_b_square_off_the_net_is_inadmissible() -> None:
    tilted = Placement(Fraction(1, 10), Fraction(1), Fraction(1), Fraction(1), B)
    verdict = verify_ceiling(CeilingCertificate(1, TWO, B, COARSE, (tilted,)))
    assert "K0 every placement is admissible" in verdict.failures
    assert verdict.regime == "none"


def test_a_mirrored_net_angle_is_admissible_only_against_symmetric_measures() -> None:
    tangent = NET[60]
    mirrored = (1 - tangent) / (1 + tangent)
    assert mirrored not in NET
    square = Placement(mirrored, Fraction(1), Fraction(1), Fraction(1), B)
    verdict = verify_ceiling(CeilingCertificate(1, TWO, B, NET, (square,)))
    assert verdict.proved, verdict.failures
    assert verdict.symmetric_only
    assert "D4-symmetric measure" in verdict.statement


def test_a_unit_square_at_any_angle_within_pi_over_4_bounds_every_valid_net() -> None:
    """The unit regime needs Condition 3 and Condition 4 of the net it bounds,
    and refuses otherwise."""
    square = Placement(Fraction(1, 5), Fraction(1), Fraction(1), Fraction(1), Fraction(1))
    fine = verify_ceiling(CeilingCertificate(1, TWO, B, NET, (square,)))
    assert fine.proved, fine.failures
    assert fine.regime == "unit"
    assert "every shrunken side B" in fine.statement
    coarse = verify_ceiling(CeilingCertificate(1, TWO, B, COARSE, (square,)))
    assert "K0 every placement is admissible" in coarse.failures


def test_a_three_four_five_rotation_is_decided_with_exact_corners() -> None:
    """Half-tangent 1/3 rotates by the 3-4-5 angle; corners are exact rationals.

    Two such unit squares placed so their corners coincide at (1, 3/2) overlap
    at that single closed point, which is a vertex of the arrangement and
    carries depth 2 -- so a claim of two disjoint squares is refused, and the
    same pair with the second moved by 1/100 along its own axis is accepted.
    """
    net = (Fraction(0), Fraction(1, 3), LIMIT)
    # With a = (4/5, 3/5) and b = (-3/5, 4/5), (1/2)(a + b) = (1/10, 7/10): the
    # square centred at (9/10, 4/5) has a corner at (1, 3/2), as does the one
    # centred at (11/10, 11/5), from the opposite side.
    shared = (Fraction(1), Fraction(3, 2))
    first = Placement(Fraction(1, 3), Fraction(9, 10), Fraction(4, 5), Fraction(1), Fraction(1))
    assert shared in first.corners()
    second = Placement(
        Fraction(1, 3), Fraction(11, 10), Fraction(11, 5), Fraction(1), Fraction(1)
    )
    assert shared in second.corners()
    side = Fraction(3)
    touching = verify_ceiling(CeilingCertificate(2, side, Fraction(1), net, (first, second)))
    assert touching.failures == ("K2 depth at most 1 at every arrangement vertex",)
    assert touching.max_depth == 2
    nudged = Placement(
        Fraction(1, 3),
        second.centre_x + Fraction(1, 100) * Fraction(4, 5),
        second.centre_y + Fraction(1, 100) * Fraction(3, 5),
        Fraction(1),
        Fraction(1),
    )
    apart = verify_ceiling(CeilingCertificate(2, side, Fraction(1), net, (first, nudged)))
    assert apart.proved, apart.failures
    assert apart.max_depth == 1


def test_the_maximum_depth_is_taken_at_an_arrangement_vertex() -> None:
    """Every vertex the walls and edges make is listed, and the deepest is exact."""
    certificate = CeilingCertificate(2, TWO, Fraction(1), COARSE, corners(Fraction(1)))
    lines = arrangement_lines(certificate)
    vertices = container_vertices(certificate, lines)
    # Four unit squares tile [0, 2]^2: the lines x, y in {0, 1, 2} meet at 9 points.
    assert len(lines) == 6
    assert len(vertices) == 9
    worst, decided, where = maximum_depth(certificate, vertices)
    assert worst == 4
    assert where == (Fraction(1), Fraction(1))
    # Vertices arrive in lexicographic order with depths 1, 2, 1, 2, 4, 2, 1, 2, 1;
    # the screen decides exactly each vertex that could still raise the record.
    assert decided == 4


def test_records_round_trip_exactly() -> None:
    certificate = CeilingCertificate(4, TWO, B, NET, corners(B, Fraction(999, 1000)))
    assert CeilingCertificate.from_record(certificate.to_record()) == certificate


def test_malformed_certificates_are_refused_at_construction() -> None:
    with pytest.raises(ValueError, match="non-negative"):
        upright(Fraction(1), Fraction(1), Fraction(-1))
    with pytest.raises(ValueError, match="at least one placement"):
        CeilingCertificate(1, TWO, B, NET, ())
    with pytest.raises(ValueError, match="strictly increasing"):
        CeilingCertificate(1, TWO, B, (Fraction(0), Fraction(0)), corners(B))
