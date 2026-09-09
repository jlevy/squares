"""Uniform row implications, touching controls and exact proof replay on small cells."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import replace
from fractions import Fraction
from itertools import product
from typing import Any, cast

from sqpack.exact_lp import (
    ExactLP,
    ExactLPError,
    cell_lp_for_axes,
    check_infeasibility,
    prove_infeasible,
    rational_sign,
)
from sqpack.uniform_cell import (
    PairChoice,
    PoseBox,
    RationalInterval,
    UniformCellDescriptor,
    build_uniform_cell,
)


def _descriptor(radius: Fraction, side: Fraction) -> UniformCellDescriptor:
    centers = RationalInterval(Fraction(1, 2), side - Fraction(1, 2))
    pose = PoseBox(centers, centers, RationalInterval(-radius, radius))
    return UniformCellDescriptor(
        (pose, pose), RationalInterval(side, side), (PairChoice(0, 1, 1, -1),)
    )


def _row_values(lp: ExactLP, point: tuple[Fraction, ...]) -> tuple[Fraction, ...]:
    return tuple(
        sum(
            (
                coefficient * value
                for coefficient, value in zip(row.coefficients, point, strict=True)
            ),
            Fraction(0),
        )
        - bound
        for row, bound in zip(lp.rows, lp.rhs, strict=True)
    )


def _corners(t: Fraction) -> tuple[tuple[Fraction, Fraction], ...]:
    # Exact endpoint geometry is evaluated separately from the producer's midpoint.
    cosine, sine = (1 - t * t) / (1 + t * t), 2 * t / (1 + t * t)
    return tuple(
        ((a * cosine - b * sine) / 2, (a * sine + b * cosine) / 2)
        for a, b in ((-1, -1), (1, -1), (1, 1), (-1, 1))
    )


def _refuses(operation: Callable[[], object], kind: str | None = None) -> None:
    try:
        operation()
    except ExactLPError as error:
        if kind is not None:
            assert error.kind == kind
    else:
        raise AssertionError("an invalid descriptor or proof was accepted")


def test_zero_width_matches_exact_geometry_and_preserves_touching() -> None:
    descriptor = _descriptor(Fraction(0), Fraction(2))
    cell = build_uniform_cell(descriptor)
    square = (
        (Fraction(-1, 2), Fraction(-1, 2)),
        (Fraction(1, 2), Fraction(-1, 2)),
        (Fraction(1, 2), Fraction(1, 2)),
        (Fraction(-1, 2), Fraction(1, 2)),
    )
    exact = cell_lp_for_axes(
        (square, square), {(0, 1): (1, -1)}, zero=Fraction(0), one=Fraction(1)
    )
    assert cell.midpoint_lp == exact
    assert cell.lp.rows[: len(exact.rows)] == exact.rows
    assert cell.lp.rhs[: len(exact.rows)] == exact.rhs
    assert not any(cell.row_errors)
    touching = (Fraction(1, 2), Fraction(3, 2), Fraction(1, 2), Fraction(1, 2), Fraction(2))
    residuals = _row_values(cell.lp, touching)
    assert max(residuals) == 0
    _refuses(lambda: prove_infeasible(cell.lp, rational_sign), "feasible")


def test_positive_width_exclusion_has_a_replayable_exact_gap() -> None:
    cell = build_uniform_cell(_descriptor(Fraction(1, 100000), Fraction(19, 10)))
    certificate = prove_infeasible(cell.lp, rational_sign)
    assert certificate.gap > 0
    assert any(cell.row_errors)
    assert all(value >= 0 for value in certificate.multipliers)
    assert (
        check_infeasibility(cell.lp, certificate.multipliers, rational_sign) == certificate.gap
    )
    assert len(cell.row_errors) == len(cell.lp.rows)
    bound_rows = cell.lp.rows[len(cell.midpoint_lp.rows) :]
    assert len(bound_rows) == 2 * cell.lp.width
    assert all(value == 0 for value in cell.row_errors[len(cell.midpoint_lp.rows) :])


def test_widening_has_a_feasible_outer_witness_and_refuses_the_old_dual() -> None:
    small = build_uniform_cell(_descriptor(Fraction(1, 100000), Fraction(19, 10)))
    certificate = prove_infeasible(small.lp, rational_sign)
    wide = build_uniform_cell(_descriptor(Fraction(1, 10), Fraction(19, 10)))
    assert wide.lp.rows == small.lp.rows
    assert all(a <= b for a, b in zip(small.row_errors, wide.row_errors, strict=True))
    assert small.descriptor != wide.descriptor
    # Coincident centers are not a packing, but this exact point survives the wider LP.
    point = (Fraction(19, 20),) * 4 + (Fraction(19, 10),)
    assert max(_row_values(wide.lp, point)) <= 0
    _refuses(lambda: check_infeasibility(wide.lp, certificate.multipliers, rational_sign))


def test_uniform_errors_bound_endpoint_geometry_for_all_directed_axis_owners() -> None:
    first = PoseBox(
        RationalInterval(Fraction(1, 2), 1),
        RationalInterval(1, 2),
        RationalInterval(Fraction(-1, 3), Fraction(1, 4)),
    )
    second = PoseBox(
        RationalInterval(2, 3),
        RationalInterval(Fraction(1, 2), Fraction(3, 2)),
        RationalInterval(Fraction(1, 5), Fraction(2, 5)),
    )
    points = (
        (first.x.lower, second.x.upper, first.y.upper, second.y.lower, Fraction(4)),
        (first.x.upper, second.x.lower, first.y.lower, second.y.upper, Fraction(3)),
    )
    for axis, orientation in product(range(4), (-1, 1)):
        descriptor = UniformCellDescriptor(
            (first, second), RationalInterval(3, 4), (PairChoice(0, 1, axis, orientation),)
        )
        cell = build_uniform_cell(descriptor)
        for first_t, second_t in product(
            (first.half_angle.lower, first.half_angle.upper),
            (second.half_angle.lower, second.half_angle.upper),
        ):
            actual = cell_lp_for_axes(
                (_corners(first_t), _corners(second_t)),
                {(0, 1): (axis, orientation)},
                zero=Fraction(0),
                one=Fraction(1),
            )
            assert tuple(row.label for row in actual.rows) == tuple(
                row.label for row in cell.midpoint_lp.rows
            )
            for point in points:
                exact_residual = _row_values(actual, point)
                reference = _row_values(cell.midpoint_lp, point)
                assert all(
                    abs(actual_value - midpoint_value) <= error
                    for actual_value, midpoint_value, error in zip(
                        exact_residual,
                        reference,
                        cell.row_errors[: len(actual.rows)],
                        strict=True,
                    )
                )


def test_descriptor_refuses_lossy_numbers_and_incomplete_pair_domains() -> None:
    descriptor = _descriptor(Fraction(0), Fraction(2))
    pose = descriptor.poses[0]
    invalid_axis: Any = True
    for invalid in (True, False, 0.25, float("inf"), "1/4"):
        _refuses(lambda value=invalid: RationalInterval(cast(Any, value), 1), "bad-descriptor")
        _refuses(lambda value=invalid: RationalInterval(0, cast(Any, value)), "bad-descriptor")
    operations: tuple[Callable[[], object], ...] = (
        lambda: RationalInterval(1, 0),
        lambda: PairChoice(0, 1, invalid_axis, 1),
        lambda: PairChoice(0, 1, 0, cast(Any, 1.0)),
        lambda: PairChoice(1, 0, 0, 1),
        lambda: PairChoice(0, 1, 4, 1),
        lambda: PairChoice(0, 1, 0, 0),
        lambda: PoseBox(cast(Any, (0, 1)), pose.y, pose.half_angle),
        lambda: replace(descriptor, side=RationalInterval(0, 2)),
        lambda: replace(descriptor, choices=()),
        lambda: replace(descriptor, choices=descriptor.choices * 2),
        lambda: replace(descriptor, poses=(pose, pose, pose)),
        lambda: replace(descriptor, poses=cast(Any, list(descriptor.poses))),
        lambda: replace(descriptor, poses=(replace(pose, x=RationalInterval(-1, 1)), pose)),
        lambda: replace(descriptor, poses=(replace(pose, y=RationalInterval(0, 3)), pose)),
        lambda: build_uniform_cell(cast(Any, {})),
    )
    for operation in operations:
        _refuses(operation, "bad-descriptor")
