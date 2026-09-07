"""Non-target BC-254 controls; no Trump support or target solve is constructed."""

from __future__ import annotations

from dataclasses import replace
from fractions import Fraction

import pytest

from cases.trump11.packing import U_INTERVAL, U_MIN_POLY
from devtools.check_full_size_density_support_ceiling import replay_upper
from sqpack.exact_lp import ExactLPError
from sqpack.field import NumberField
from sqpack.full_size_density.support_ceiling import (
    Support,
    SupportError,
    axis_square,
    build_control_support,
    necessary_row,
    solve_control_lp,
)


def test_overlapping_orbit_has_ceiling_one_and_exact_neighborhood() -> None:
    field = NumberField((1, 0), ("-1", "1"))
    side = field.rational(2)
    seed = axis_square(field.rational("3/4"), field.rational("3/4"))
    support = build_control_support((seed,), side)
    row = necessary_row(support, (field.one, field.one))
    assert support.sizes == (4,)
    assert row.coefficients == (4,)
    assert row.radius > 0
    solution = solve_control_lp((row.coefficients,), support.sizes)
    assert solution.point == (Fraction(1, 4),)
    assert solution.bound == 1
    assert replay_upper((seed,), support, (row,), solution.multipliers) == 1


def test_fractional_lp_uses_the_zero_basis_and_refuses_unbounded_columns() -> None:
    solution = solve_control_lp(((1, 2), (2, 1)), (4, 4))
    assert solution.point == (Fraction(1, 3), Fraction(1, 3))
    assert solution.multipliers == (Fraction(4, 3), Fraction(4, 3))
    assert solution.bound == Fraction(8, 3)
    with pytest.raises(SupportError, match="finite-bound"):
        solve_control_lp(((1, 0),), (4, 4))
    with pytest.raises(ExactLPError) as refusal:
        solve_control_lp(((1, 2), (2, 1)), (4, 4), pivot_budget=0)
    assert refusal.value.kind == "pivot-budget"


def test_algebraic_toy_has_eight_members_without_building_trump() -> None:
    field = NumberField(U_MIN_POLY, U_INTERVAL)
    side = field.rational(2)
    seed = axis_square(field.rational("3/4") + field.alpha / 100, field.rational("3/4"))
    support = build_control_support((seed,), side)
    row = necessary_row(support, (field.one, field.one))
    assert support.sizes == (8,)
    assert row.coefficients == (8,)
    assert replay_upper((seed,), support, (row,), (Fraction(1),)) == 1
    with pytest.raises(SupportError, match="target-disabled"):
        build_control_support((seed,), field.rational(4))


def test_source_permutations_preserve_geometry_and_replay_refuses_mutations() -> None:
    field = NumberField((1, 0), ("-1", "1"))
    side = field.rational(2)
    seed = axis_square(field.rational("3/4"), field.rational("3/4"))
    support = build_control_support((seed,), side)
    row = necessary_row(support, (field.one, field.one))
    variants = (seed[1:] + seed[:1], tuple(reversed(seed)), seed)
    permuted = build_control_support(variants, side)
    assert permuted.sizes == support.sizes
    assert replay_upper(variants, permuted, (row,), (Fraction(1),)) == 1
    with pytest.raises(SupportError, match="source"):
        replay_upper((seed,), Support(side, (support.orbits[0][:-1],)), (row,), (1,))
    with pytest.raises(SupportError, match="incidence"):
        replay_upper((seed,), support, (replace(row, coefficients=(1,)),), (1,))
    single_row = necessary_row(support, (field.rational("1/2"), field.rational("1/2")))
    with pytest.raises(SupportError, match="integers"):
        replay_upper((seed,), support, (replace(single_row, coefficients=(True,)),), (4,))
    with pytest.raises(SupportError, match="neighborhood"):
        replay_upper((seed,), support, (replace(row, radius=Fraction(1, 2)),), (1,))
    for weight in (-1, "1/2", 1.0, True, "1/0", "invalid"):
        with pytest.raises(SupportError):
            replay_upper((seed,), support, (row,), (weight,))
    with pytest.raises(SupportError, match="boundary"):
        necessary_row(support, (field.rational("1/4"), field.one))
    with pytest.raises(SupportError, match="containment"):
        build_control_support((axis_square(field.rational("7/4"), field.one),), side)
