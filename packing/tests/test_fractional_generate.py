"""Controls for site column generation on the fractional covering LP.

The instrument under test is `sqpack.fractional.colgen`, which moves the
candidate sites instead of fixing them to a grid. Three things have to hold or
the loop is reporting a number about nothing: the price it puts on a new orbit
has to be the reduced cost it claims to be, adding an orbit must never make the
optimum worse on the rows already held, and the ceiling by-product must refuse
a dual that covers some point of the container twice -- which is the only way
that by-product could ever claim more than weak duality allows.
"""

from __future__ import annotations

from fractions import Fraction

import numpy as np

from sqpack.fractional import colgen
from sqpack.fractional.certificate import verify
from sqpack.fractional.generate import direction_net, net_half_tangents
from sqpack.fractional.model import Atom, rotation_from_half_tangent
from sqpack.fractional.sweep import minimum_covered_mass

UPRIGHT = rotation_from_half_tangent("0", Fraction(0))


def axis_aligned(
    centre: tuple[Fraction, Fraction], outer_side: Fraction, side: Fraction
) -> colgen.Square:
    return colgen.square_at(UPRIGHT, centre, outer_side, side)


def test_reduced_cost_counts_the_orbit_members_one_placement_covers() -> None:
    """A hand-counted instance: four of eight images sit in the square.

    Container side 4, so the centre is (2, 2). The square has side 1 and centre
    (13/5, 2), covering ``x`` in [21/10, 31/10] and ``y`` in [3/2, 5/2]. The
    orbit of (5/2, 11/5) is the eight points (2 +- 1/2, 2 +- 1/5) and
    (2 +- 1/5, 2 +- 1/2); the four with ``x = 5/2`` or ``x = 11/5`` are inside,
    two of them on the edge, which counts because coverage is by closed squares.
    """
    outer = Fraction(4)
    square = axis_aligned((Fraction(13, 5), Fraction(2)), outer, Fraction(1))
    orbit = colgen.d4_orbit(Fraction(5, 2), Fraction(11, 5), outer)
    assert len(orbit) == 8

    covered = [point for point in orbit if square.covers(*_centred(point, outer))]
    assert len(covered) == 4
    assert colgen.reduced_cost(orbit, ((square, Fraction(3)),), outer) == 8 - 3 * 4


def test_orbit_averaged_depth_is_the_symmetrised_pointwise_depth() -> None:
    """The identity the column generation rests on, on a two-square dual.

    Reduced cost is defined by orbit-averaged depth, but the candidate search
    ranks points by the pointwise depth of the symmetrised dual. Those are the
    same function, and if they ever came apart the search would be maximising
    something the LP does not price.
    """
    outer = Fraction(4)
    weighted = (
        (axis_aligned((Fraction(13, 5), Fraction(2)), outer, Fraction(1)), Fraction(3)),
        (axis_aligned((Fraction(2), Fraction(9, 4)), outer, Fraction(3, 2)), Fraction(1)),
    )
    point = (Fraction(5, 2), Fraction(11, 5))
    orbit = colgen.d4_orbit(point[0], point[1], outer)
    averaged = 1 - colgen.reduced_cost(orbit, weighted, outer) / len(orbit)
    pointwise = sum(
        (
            weight
            for square, weight in colgen.symmetrise(weighted)
            if square.covers(*_centred(point, outer))
        ),
        start=Fraction(0),
    )
    assert averaged == pointwise


def test_symmetrising_preserves_the_total_dual_weight() -> None:
    outer = Fraction(4)
    square = axis_aligned((Fraction(13, 5), Fraction(2)), outer, Fraction(1))
    weighted = ((square, Fraction(3)),)
    assert sum(weight for _, weight in colgen.symmetrise(weighted)) == Fraction(3)


def test_adding_a_site_orbit_never_raises_the_optimum_on_the_rows_held() -> None:
    """Monotonicity, which is what makes the column loop safe to iterate.

    The comparison is on one fixed row set: adding a column only widens the
    feasible region, so the optimum cannot rise. Re-generating rows afterwards
    can raise it, and that is a different statement -- one about the placements
    the new sites expose, not about the sites.
    """
    outer, side = Fraction(11, 5), Fraction(24, 25)
    tangents = net_half_tangents(Fraction(207107, 500000), 12)
    sites = colgen.site_set_from_grids(outer, (7,), Fraction(1, 2))
    rows = colgen.Rows()
    solution = colgen.solve_rows(sites, side, tangents, rows, rows_per_direction=2)
    assert solution.converged, solution.stopped

    weighted = colgen.dual_squares(rows, solution.duals, tangents, outer, side, support_cap=16)
    candidate = colgen.best_candidate(sites, weighted)
    orbit = (
        candidate.orbit
        if candidate is not None
        else colgen.d4_orbit(Fraction(3, 4), Fraction(9, 10), outer)
    )
    rows.add_column(colgen.orbit_column(rows, orbit, tangents, side))
    widened = colgen.SiteSet(outer, (*sites.orbits, orbit))

    solved = colgen.solve_lp(widened, rows)
    assert solved is not None
    assert solved[2] <= solution.objective + 1e-9


def test_the_float_oracle_never_reports_less_than_the_exact_sweep() -> None:
    """One-sided, because the two do not agree, and the gap is the instrument's.

    `placement_cells` calls a cell reachable when its centre lies in the centre
    domain, which is what `generate._worst_cells` has always done.
    `sweep.reduce_to_cells` calls it reachable when its v-range meets the
    domain's v-extent within the u-slab, which is a strictly larger set. So the
    oracle can miss a cell the verifier weighs -- here it reports 2.125 where
    the sweep finds 2.0 -- and it never invents one, which is the direction
    that matters: a row it generates is a real placement's constraint. The
    consequence is not academic. A solve that converges by this oracle can
    still be refused by C4, and at L = 39/10 for n = 12 it was, by 1.6%.
    """
    outer, side = Fraction(11, 5), Fraction(24, 25)
    tangents = net_half_tangents(Fraction(207107, 500000), 12)
    sites = colgen.site_set_from_grids(outer, (9,), Fraction(1, 2))
    positions = sites.positions()
    pattern = [Fraction((index * 5) % 4, 8) for index in range(len(positions))]
    atoms = tuple(
        Atom(str(index), x, y, pattern[index])
        for index, (x, y) in enumerate(positions)
        if pattern[index] > 0
    )
    weights = np.array([float(weight) for weight in pattern])
    points = sites.points()
    gaps = []
    for direction in direction_net(tangents):
        exact, _ = minimum_covered_mass(atoms, direction, outer, side)
        cells = colgen.placement_cells(
            points, weights, direction, float(outer), float(side), keep=3
        )
        least = min(mass for mass, _, _, _ in cells)
        assert least >= float(exact) - 1e-9
        gaps.append(least - float(exact))
    assert max(gaps) > 0, "the gap this test documents has closed; tighten it"


def test_the_ceiling_refuses_a_dual_that_covers_a_point_twice() -> None:
    """Pointwise, not orbit-averaged: overlap is what invalidates a ceiling."""
    outer = Fraction(4)
    overlapping = (
        (axis_aligned((Fraction(19, 10), Fraction(2)), outer, Fraction(1)), Fraction(1)),
        (axis_aligned((Fraction(21, 10), Fraction(2)), outer, Fraction(1)), Fraction(1)),
    )
    result = colgen.check_ceiling(2, overlapping, outer)
    assert result.max_pointwise_depth == 2
    assert result.total_weight == 2
    assert result.feasible_total == 1
    assert not result.proved


def test_the_ceiling_accepts_a_dual_of_disjoint_placements() -> None:
    """The positive control: weight 2 spread over squares that never overlap."""
    outer = Fraction(4)
    disjoint = (
        (axis_aligned((Fraction(1), Fraction(1)), outer, Fraction(1)), Fraction(1)),
        (axis_aligned((Fraction(3), Fraction(3)), outer, Fraction(1)), Fraction(1)),
    )
    result = colgen.check_ceiling(2, disjoint, outer)
    assert result.max_pointwise_depth == 1
    assert result.feasible_total == 2
    assert result.proved


def test_the_dual_of_a_converged_solve_matches_its_objective() -> None:
    """Strong duality on the generated rows, which is what prices the columns."""
    outer, side = Fraction(11, 5), Fraction(24, 25)
    tangents = net_half_tangents(Fraction(207107, 500000), 12)
    sites = colgen.site_set_from_grids(outer, (7,), Fraction(1, 2))
    rows = colgen.Rows()
    solution = colgen.solve_rows(sites, side, tangents, rows, rows_per_direction=2)
    assert solution.converged, solution.stopped
    assert float(solution.duals.sum()) == np.float64(solution.objective).astype(float)


def test_a_union_of_grids_is_closed_under_d4_and_holds_both_grids() -> None:
    outer = Fraction(11, 5)
    union = colgen.site_set_from_grids(outer, (5, 7), Fraction(1, 2))
    held = set(union.positions())
    for x, y in held:
        assert set(colgen.d4_orbit(x, y, outer)) <= held
    assert len(held) == len(union.positions())
    assert union.size == sum(len(orbit) for orbit in union.orbits)


def test_generate_adaptive_produces_a_certificate_the_exact_verifier_accepts() -> None:
    """End to end on a bound nobody doubts: s(5) >= 11/5, well under 2.7071."""
    certificate, log = colgen.generate_adaptive(
        5,
        Fraction(11, 5),
        Fraction(24, 25),
        grid_counts=(9,),
        inset=Fraction(1, 2),
        angle_limit=Fraction(207107, 500000),
        direction_steps=12,
        scale=2000,
        column_rounds=2,
        rows_per_direction=2,
    )
    assert certificate is not None, log.stopped
    assert log.ceiling is not None
    verdict = verify(certificate)
    assert verdict.accepted, verdict.failures
    assert certificate.total_mass < 5


def _centred(
    point: tuple[Fraction, Fraction], outer_side: Fraction
) -> tuple[Fraction, Fraction]:
    return point[0] - outer_side / 2, point[1] - outer_side / 2
