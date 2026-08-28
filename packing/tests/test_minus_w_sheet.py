"""Focused tests for the exact exp-034 positive sheet-path evaluator."""

from __future__ import annotations

from fractions import Fraction

import pytest

from cases.n5 import (
    angle_sheet,
    equal_side_face,
    minus_w_sheet,
    tangent_cones,
    tangent_inventory,
)
from sqpack.research.exact_jets import Taylor2


def test_sheet_path_vectors_and_base_bind_exact_exp034_source() -> None:
    field = equal_side_face.make_field()
    q = field.rational
    source = minus_w_sheet.source_binding(field)
    path = minus_w_sheet.positive_left_boundary_path(field)
    expected_side, expected_centers, expected_cosine, expected_sine = (
        angle_sheet.parameter_values(field, sign=1, endpoint="left", q_abs=Fraction(0))
    )

    assert source.side == expected_side
    assert source.centers == tuple(expected_centers)
    assert source.centers == tuple(tangent_cones.centres_for_stratum(field, "A"))
    assert (source.cosine, source.sine) == (expected_cosine, expected_sine) == (q(1), q(0))
    assert len(path.velocity) == len(path.correction) == tangent_cones.VARIABLE_COUNT
    assert {
        index: value for index, value in enumerate(path.velocity) if not value.is_zero()
    } == {
        tangent_cones.x(0): q(1) / 2,
        tangent_cones.y(0): q(1) / 2,
        tangent_cones.theta(0): q(1),
    }
    assert {
        index: value for index, value in enumerate(path.correction) if not value.is_zero()
    } == {
        tangent_cones.x(0): -q(1) / 4,
        tangent_cones.y(0): -q(1) / 4,
    }


def test_wrong_half_angle_normalization_fails_formula_validator() -> None:
    field = equal_side_face.make_field()

    with pytest.raises(
        ValueError,
        match="half-angle rate does not normalize the physical angle",
    ):
        minus_w_sheet.derive_positive_left_boundary_path(
            field, half_angle_rate=field.rational(1)
        )


def test_lexicographic_compatibility_does_not_require_positive_quadratic_after_release() -> (
    None
):
    field = equal_side_face.make_field()
    q = field.rational

    assert minus_w_sheet.row_is_lexicographically_compatible(Taylor2(q(0), q(1), q(-7)))
    assert minus_w_sheet.row_is_lexicographically_compatible(Taylor2(q(0), q(0), q(0)))
    assert minus_w_sheet.row_is_lexicographically_compatible(Taylor2(q(0), q(0), q(3)))
    assert not minus_w_sheet.row_is_lexicographically_compatible(Taylor2(q(0), q(0), q(-1)))
    assert not minus_w_sheet.row_is_lexicographically_compatible(Taylor2(q(0), q(-1), q(7)))


@pytest.mark.exhaustive_exact
def test_positive_sheet_path_checks_all_seventeen_rows_for_both_owners() -> None:
    field = equal_side_face.make_field()
    result = minus_w_sheet.evaluate_path(
        field, minus_w_sheet.positive_left_boundary_path(field)
    )

    assert result.compatible
    assert (
        tuple(owner.owner for owner in result.owners) == tangent_cones.EXPECTED_CONTACT_BRANCHES
    )
    for owner_result in result.owners:
        expected_labels = tuple(
            row.label for row in tangent_inventory.matrix(field, "A", owner_result.owner)
        )
        assert len(owner_result.rows) == 17
        assert tuple(owner_result.rows) == expected_labels
        assert all(isinstance(value, Taylor2) for value in owner_result.rows.values())
        assert owner_result.compatible
        assert all(
            minus_w_sheet.row_is_lexicographically_compatible(value)
            for value in owner_result.rows.values()
        )


@pytest.mark.exhaustive_exact
def test_bad_center_correction_is_rejected_by_same_row_evaluator() -> None:
    field = equal_side_face.make_field()
    q = field.rational
    bad_path = minus_w_sheet.bad_left_boundary_path(field)
    result = minus_w_sheet.evaluate_path(field, bad_path)

    assert bad_path.velocity == minus_w_sheet.positive_left_boundary_path(field).velocity
    assert bad_path.correction[tangent_cones.x(0)] == -q(1) / 2
    assert bad_path.correction[tangent_cones.y(0)] == -q(1) / 2
    assert not result.compatible
    for owner_result in result.owners:
        bad_row = owner_result.rows["wall:0:x-lower:-"]
        assert bad_row.linear.is_zero()
        assert bad_row.quadratic == -q(1) / 4
        assert not owner_result.compatible
