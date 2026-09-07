"""Exact Farkas receipts and selected SAT cells independent of a feasible seed."""

from __future__ import annotations

from collections.abc import Callable, Mapping
from dataclasses import replace
from fractions import Fraction
from typing import cast

from sqpack.exact_lp import (
    ExactLP,
    ExactLPError,
    LinearRow,
    cell_lp_for_axes,
    check_infeasibility,
    feasible_basis,
    fixed_cell_lp,
    prove_infeasible,
    rational_sign,
    solve,
    solve_from_scratch,
    translated_squares,
)
from sqpack.field import NumberField
from sqpack.verify import edge_axes, exact_sign, project, verify_packing


def refusal(action: Callable[[], object]) -> str:
    try:
        action()
    except ExactLPError as error:
        return error.kind
    return "none"


def contradiction() -> ExactLP:
    return ExactLP(
        objective=(Fraction(1),),
        rows=(LinearRow("upper", (Fraction(1),)), LinearRow("lower", (Fraction(-1),))),
        rhs=(Fraction(0), Fraction(-1)),
        zero=Fraction(0),
        one=Fraction(1),
    )


def unit(x: int = 0) -> list[tuple[Fraction, Fraction]]:
    return [(Fraction(x + dx), Fraction(dy)) for dx, dy in ((0, 0), (1, 0), (1, 1), (0, 1))]


def cap_side(lp: ExactLP, side: int) -> ExactLP:
    return replace(
        lp,
        rows=(*lp.rows, LinearRow("side-cap", (*([lp.zero] * (lp.width - 1)), lp.one))),
        rhs=(*lp.rhs, Fraction(side)),
    )


def test_phase1_exports_a_dense_original_row_certificate() -> None:
    lp = contradiction()
    certificate = prove_infeasible(lp, rational_sign)
    assert len(certificate.multipliers) == len(lp.rows)
    assert certificate.gap > 0
    assert check_infeasibility(lp, certificate.multipliers, rational_sign) == certificate.gap
    assert sum(certificate.multipliers, Fraction(0)) > 0
    assert refusal(lambda: feasible_basis(lp, rational_sign)) == "infeasible"


def test_bland_choice_is_independent_of_starting_basis_order() -> None:
    # The optimal edge has two endpoints. The lowest original row must leave first,
    # regardless of where that row happens to sit in the supplied basis.
    lp = ExactLP(
        objective=(Fraction(-1), Fraction(-1)),
        rows=(
            LinearRow("x-lower", (Fraction(-1), Fraction(0))),
            LinearRow("y-lower", (Fraction(0), Fraction(-1))),
            LinearRow("sum-upper", (Fraction(1), Fraction(1))),
        ),
        rhs=(Fraction(0), Fraction(0), Fraction(1)),
        zero=Fraction(0),
        one=Fraction(1),
    )
    for start in ((0, 1), (1, 0)):
        result = solve(lp, start, rational_sign, pivot_budget=1)
        assert result.vertex.point == (Fraction(1), Fraction(0))
        assert result.vertex.objective_value == -1
        assert result.pivots == 1


def test_reader_rejects_changed_dual_rhs_and_missing_rows() -> None:
    lp = contradiction()
    assert check_infeasibility(lp, (Fraction(1), Fraction(1)), rational_sign) == 1
    for multipliers in ((1,), (-1, -1), (1, 2), (0, 0)):
        assert refusal(lambda m=multipliers: check_infeasibility(lp, m, rational_sign)) in {
            "bad-request",
            "invalid-certificate",
        }
    touching = replace(lp, rhs=(Fraction(0), Fraction(0)))
    assert refusal(lambda: check_infeasibility(touching, (1, 1), rational_sign)) == (
        "invalid-certificate"
    )
    shortened = replace(lp, rows=lp.rows[:1], rhs=lp.rhs[:1])
    assert (
        refusal(lambda: check_infeasibility(shortened, (1, 1), rational_sign)) == "bad-request"
    )
    changed = replace(lp, rows=(LinearRow("changed-upper", (Fraction(2),)), lp.rows[1]))
    assert refusal(lambda: check_infeasibility(changed, (1, 1), rational_sign)) == (
        "invalid-certificate"
    )


def test_feasible_touching_and_exhausted_budget_are_not_certificates() -> None:
    touching = replace(contradiction(), rhs=(Fraction(0), Fraction(0)))
    assert feasible_basis(touching, rational_sign).point == (Fraction(0),)
    assert refusal(lambda: prove_infeasible(touching, rational_sign)) == "feasible"
    lp = ExactLP(
        objective=(Fraction(0), Fraction(0)),
        rows=tuple(
            LinearRow(label, tuple(Fraction(value) for value in row))
            for label, row in (
                ("x-upper", (1, 0)),
                ("y-upper", (0, 1)),
                ("x-lower", (-1, 0)),
                ("y-stricter", (0, 1)),
            )
        ),
        rhs=tuple(Fraction(value) for value in (0, 0, -1, -5)),
        zero=Fraction(0),
        one=Fraction(1),
    )
    assert (
        refusal(lambda: prove_infeasible(lp, rational_sign, pivot_budget=0)) == "pivot-budget"
    )
    certificate = prove_infeasible(lp, rational_sign)
    assert certificate.pivots > 0
    assert check_infeasibility(lp, certificate.multipliers, rational_sign) > 0


def test_algebraic_coefficients_keep_exact_cancellation() -> None:
    field = NumberField((1, 0, -2), ("1", "2"))
    lp = ExactLP(
        objective=(field.one,),
        rows=(LinearRow("upper", (field.alpha,)), LinearRow("lower", (-field.one,))),
        rhs=(field.zero, -field.one),
        zero=field.zero,
        one=field.one,
    )
    assert exact_sign(check_infeasibility(lp, (field.one, field.alpha), exact_sign)) > 0
    certificate = prove_infeasible(lp, exact_sign)
    assert exact_sign(certificate.gap) > 0
    assert (
        exact_sign(
            check_infeasibility(lp, certificate.multipliers, exact_sign) - certificate.gap
        )
        == 0
    )


def test_rank_deficient_program_can_be_checked_without_a_vertex() -> None:
    lp = replace(
        contradiction(),
        objective=(Fraction(1), Fraction(0)),
        rows=(
            LinearRow("upper", (Fraction(1), Fraction(0))),
            LinearRow("lower", (Fraction(-1), Fraction(0))),
        ),
    )
    assert check_infeasibility(lp, (1, 1), rational_sign) == 1
    assert refusal(lambda: prove_infeasible(lp, rational_sign)) == "no-vertex-basis"


def test_selected_cells_need_no_feasible_seed_and_preserve_every_axis_choice() -> None:
    squares = [unit(), unit()]
    assert refusal(lambda: fixed_cell_lp(squares, rational_sign, zero=0, one=1)) == (
        "no-separating-axis"
    )
    for position in range(4):
        for orientation in (-1, 1):
            lp = cell_lp_for_axes(
                squares,
                {(0, 1): (position, orientation)},
                zero=Fraction(0),
                one=Fraction(1),
            )
            solution = solve_from_scratch(lp, rational_sign)
            assert solution.vertex.objective_value == 2
            translated = translated_squares(squares, solution.vertex.point)
            report = verify_packing(translated, Fraction(2), rational_sign)
            assert report.valid
            assert report.touching_pairs == 1
            certificate = prove_infeasible(cap_side(lp, 1), rational_sign)
            assert (
                check_infeasibility(cap_side(lp, 1), certificate.multipliers, rational_sign) > 0
            )
            assert refusal(lambda p=lp: prove_infeasible(cap_side(p, 2), rational_sign)) == (
                "feasible"
            )


def test_distinct_square_axes_and_both_orders_match_independent_projections() -> None:
    tilted = [(Fraction(x, 5), Fraction(y, 5)) for x, y in ((0, 0), (3, 4), (-1, 7), (-4, 3))]
    squares = [unit(), tilted]
    axes = edge_axes(squares[0]) + edge_axes(squares[1])
    for position, axis in enumerate(axes):
        for orientation in (-1, 1):
            lp = cell_lp_for_axes(
                squares,
                {(0, 1): (position, orientation)},
                zero=Fraction(0),
                one=Fraction(1),
            )
            solution = solve_from_scratch(lp, rational_sign)
            translated = translated_squares(squares, solution.vertex.point)
            first_lo, first_hi = project(translated[0], axis, rational_sign)
            second_lo, second_hi = project(translated[1], axis, rational_sign)
            gap = second_lo - first_hi if orientation > 0 else first_lo - second_hi
            assert gap >= 0
            assert verify_packing(
                translated, solution.vertex.objective_value, rational_sign
            ).valid


def test_fixed_cell_keeps_its_feasible_pose_interface() -> None:
    squares = [unit(), unit(1)]
    lp = fixed_cell_lp(squares, rational_sign, zero=Fraction(0), one=Fraction(1))
    solution = solve_from_scratch(lp, rational_sign)
    assert solution.vertex.objective_value == 2
    report = verify_packing(
        translated_squares(squares, solution.vertex.point), Fraction(2), rational_sign
    )
    assert report.valid
    assert report.touching_pairs == 1


def test_choice_inventory_and_integer_labels_fail_closed() -> None:
    malformed = (
        {},
        {(1, 0): (0, 1)},
        {(0, 2): (0, 1)},
        {(0, 1): (4, 1)},
        {(0, 1): (-1, 1)},
        {(0, 1): (0, 0)},
        {(0, 1): (0, 2)},
        {(0, 1): (True, 1)},
        {(0, 1): (0, True)},
        {(False, 1): (0, 1)},
        {(0.0, 1): (0, 1)},
        {(0, 1): (0.0, 1)},
        {(0, 1): (0, 1.0)},
        {(0, 1): (0,)},
        {(0, 1, 2): (0, 1)},
        {(0, 1): (0, 1), (1, 0): (0, 1)},
    )
    for choices in malformed:
        typed = cast(Mapping[tuple[int, int], tuple[int, int]], choices)
        assert refusal(
            lambda c=typed: cell_lp_for_axes([unit(), unit()], c, zero=0, one=1)
        ) == ("bad-request")
    partial = {(0, 1): (0, 1), (0, 2): (0, 1)}
    assert (
        refusal(lambda: cell_lp_for_axes([unit(), unit(), unit()], partial, zero=0, one=1))
        == "bad-request"
    )
