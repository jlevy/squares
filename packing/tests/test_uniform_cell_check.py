"""Independent descriptor-bound geometry replay and hostile receipt controls."""

from __future__ import annotations

from collections.abc import Callable
from copy import copy
from dataclasses import replace
from fractions import Fraction
from typing import cast

from sqpack.exact_lp import ExactLPError, prove_infeasible, rational_sign
from sqpack.uniform_cell import (
    PairChoice,
    PoseBox,
    RationalInterval,
    UniformCell,
    UniformCellDescriptor,
    build_uniform_cell,
)
from sqpack.uniform_cell_check import check_uniform_cell


def _refuses(operation: Callable[[], object], kind: str) -> None:
    try:
        operation()
    except ExactLPError as error:
        assert error.kind == kind
    else:
        raise AssertionError("mutated uniform-cell receipt was accepted")


def _mutated[T](value: T, attribute: str, replacement: object) -> T:
    # Bypass producer constructors to exercise the reader's own hostile-input boundary.
    altered = copy(value)
    object.__setattr__(altered, attribute, replacement)
    return altered


def _descriptor(side: Fraction = Fraction(19, 10)) -> UniformCellDescriptor:
    centers = RationalInterval(Fraction(1, 2), side - Fraction(1, 2))
    first = PoseBox(centers, centers, RationalInterval(Fraction(-1, 10000), Fraction(2, 10000)))
    second = PoseBox(
        centers, centers, RationalInterval(Fraction(-3, 10000), Fraction(-1, 10000))
    )
    return UniformCellDescriptor(
        (first, second), RationalInterval(side, side), (PairChoice(0, 1, 1, -1),)
    )


def _case() -> tuple[UniformCell, tuple[Fraction, ...]]:
    cell = build_uniform_cell(_descriptor())
    return cell, prove_infeasible(cell.lp, rational_sign).multipliers


def test_independent_reader_accepts_both_normal_owners_and_all_directions() -> None:
    descriptor = _descriptor()
    for position in range(4):
        for orientation in (-1, 1):
            cell = build_uniform_cell(
                replace(descriptor, choices=(PairChoice(0, 1, position, orientation),))
            )
            certificate = prove_infeasible(cell.lp, rational_sign)
            assert check_uniform_cell(cell, certificate.multipliers) == certificate.gap
            assert certificate.gap > 0


def test_geometry_reader_rejects_omitted_corrupted_and_flipped_rows() -> None:
    cell, dual = _case()
    first_row = cell.lp.rows[0]
    changed_coefficient = replace(
        first_row, coefficients=tuple(-value for value in first_row.coefficients)
    )
    variants = (
        replace(cell, lp=_mutated(cell.lp, "rows", cell.lp.rows[1:])),
        replace(cell, lp=replace(cell.lp, rows=(changed_coefficient, *cell.lp.rows[1:]))),
        replace(
            cell,
            descriptor=replace(
                cell.descriptor,
                choices=(replace(cell.descriptor.choices[0], orientation=1),),
            ),
        ),
        replace(
            cell,
            midpoint_lp=replace(
                cell.midpoint_lp,
                rows=(replace(first_row, label="unbound-label"), *cell.midpoint_lp.rows[1:]),
            ),
        ),
    )
    for variant in variants:
        _refuses(lambda value=variant: check_uniform_cell(value, dual), "bad-cell")
    pair_row = 16 * len(cell.descriptor.poses)
    rows = list(cell.lp.rows)
    rows[pair_row] = replace(
        rows[pair_row], coefficients=tuple(-value for value in rows[pair_row].coefficients)
    )
    _refuses(
        lambda: check_uniform_cell(replace(cell, lp=replace(cell.lp, rows=tuple(rows))), dual),
        "bad-cell",
    )


def test_angle_loss_or_widening_cannot_reuse_a_narrow_receipt() -> None:
    cell, dual = _case()
    first, second = cell.descriptor.poses
    for angle in (
        RationalInterval(first.half_angle.midpoint, first.half_angle.midpoint),
        RationalInterval(Fraction(-1, 10), Fraction(1, 10)),
    ):
        descriptor = replace(cell.descriptor, poses=(replace(first, half_angle=angle), second))
        _refuses(
            lambda d=descriptor: check_uniform_cell(replace(cell, descriptor=d), dual),
            "bad-cell",
        )
    wide_pose = replace(first, half_angle=RationalInterval(Fraction(-1, 10), Fraction(1, 10)))
    wide = build_uniform_cell(replace(cell.descriptor, poses=(wide_pose, wide_pose)))
    _refuses(lambda: check_uniform_cell(wide, dual), "invalid-certificate")


def test_bounds_rhs_and_error_metadata_are_reconstructed() -> None:
    cell, dual = _case()
    rhs = list(cell.lp.rhs)
    rhs[-1] += 1
    errors = list(cell.row_errors)
    errors[0] += Fraction(1, 100)
    center = RationalInterval(Fraction(3, 5), Fraction(7, 5))
    first, second = cell.descriptor.poses
    variants = (
        replace(cell, lp=replace(cell.lp, rhs=tuple(rhs))),
        replace(cell, row_errors=tuple(errors)),
        replace(cell, row_errors=cell.row_errors[:-1]),
        replace(
            cell,
            descriptor=replace(cell.descriptor, poses=(replace(first, x=center), second)),
        ),
        replace(
            cell, midpoint_lp=replace(cell.midpoint_lp, rhs=(-1, *cell.midpoint_lp.rhs[1:]))
        ),
    )
    for variant in variants:
        _refuses(lambda value=variant: check_uniform_cell(value, dual), "bad-cell")


def test_reader_revalidates_frozen_descriptor_types_and_pair_inventory() -> None:
    cell, dual = _case()
    descriptor = cell.descriptor
    first, second = descriptor.poses
    choice = descriptor.choices[0]
    variants = (
        _mutated(descriptor, "poses", list(descriptor.poses)),
        _mutated(descriptor, "choices", ()),
        _mutated(descriptor, "choices", descriptor.choices * 2),
        _mutated(descriptor, "choices", (_mutated(choice, "orientation", replacement=True),)),
        _mutated(descriptor, "choices", (_mutated(choice, "axis_position", 4),)),
        _mutated(descriptor, "choices", (_mutated(choice, "first", 1),)),
        _mutated(descriptor, "poses", (first, second, first)),
        _mutated(descriptor, "side", _mutated(descriptor.side, "lower", Fraction(0))),
        _mutated(
            descriptor,
            "poses",
            (_mutated(first, "x", _mutated(first.x, "lower", 0.5)), second),
        ),
        _mutated(
            descriptor,
            "poses",
            (
                _mutated(
                    first, "half_angle", _mutated(first.half_angle, "upper", replacement=True)
                ),
                second,
            ),
        ),
        _mutated(
            descriptor,
            "poses",
            (_mutated(first, "y", RationalInterval(-1, 1)), second),
        ),
    )
    for variant in variants:
        _refuses(
            lambda value=variant: check_uniform_cell(replace(cell, descriptor=value), dual),
            "bad-descriptor",
        )


def test_dense_dual_and_cell_scalars_must_be_exact_rationals() -> None:
    cell, dual = _case()
    invalid_duals = (
        dual[:-1],
        tuple(-value for value in dual),
        (dual[0] + 1, *dual[1:]),
        (Fraction(0),) * len(dual),
    )
    for invalid in invalid_duals:
        _refuses(lambda value=invalid: check_uniform_cell(cell, value), "invalid-certificate")
    for lossy in (0.0, float("nan"), float("inf"), False, "0", 0):
        bad_dual = _mutated(cell, "row_errors", (lossy, *cell.row_errors[1:]))
        _refuses(lambda value=bad_dual: check_uniform_cell(value, dual), "bad-cell")
        changed = cast(tuple[Fraction, ...], (lossy, *dual[1:]))
        _refuses(lambda value=changed: check_uniform_cell(cell, value), "invalid-certificate")
    bad_lp = _mutated(cell.lp, "zero", replacement=False)
    _refuses(lambda: check_uniform_cell(replace(cell, lp=bad_lp), dual), "bad-cell")
    for lp_name in ("lp", "midpoint_lp"):
        program = getattr(cell, lp_name)
        changed_row = _mutated(
            program.rows[0], "coefficients", (float("nan"), *program.rows[0].coefficients[1:])
        )
        bad_programs = (
            _mutated(program, "rhs", (0.0, *program.rhs[1:])),
            _mutated(program, "objective", (False, *program.objective[1:])),
            _mutated(program, "one", Fraction(2)),
            _mutated(program, "rows", (changed_row, *program.rows[1:])),
        )
        for bad_program in bad_programs:
            altered = _mutated(cell, lp_name, bad_program)
            _refuses(lambda value=altered: check_uniform_cell(value, dual), "bad-cell")


def test_feasible_touching_has_no_strict_farkas_gap() -> None:
    cell, dual = _case()
    centers = RationalInterval(Fraction(1, 2), Fraction(3, 2))
    pose = PoseBox(centers, centers, RationalInterval(0, 0))
    touching = build_uniform_cell(
        UniformCellDescriptor((pose, pose), RationalInterval(2, 2), cell.descriptor.choices)
    )
    _refuses(lambda: check_uniform_cell(touching, dual), "invalid-certificate")
    _refuses(
        lambda: check_uniform_cell(touching, (Fraction(0),) * len(touching.lp.rows)),
        "invalid-certificate",
    )
