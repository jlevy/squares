"""Focused tests for exact weighted evaluation of the n=5 stress rows."""

from __future__ import annotations

import pytest

from cases.n5 import equal_side_face as face
from cases.n5 import minus_w_stress, tangent_cones, tangent_inventory


@pytest.mark.parametrize("stratum", tangent_cones.STRATA)
@pytest.mark.parametrize("owner", tangent_cones.EXPECTED_CONTACT_BRANCHES)
def test_w_curvature_is_even_nonzero_and_quadratically_scaled(stratum: str, owner: str) -> None:
    field = face.make_field()
    q = field.rational
    positive_w = tuple(tangent_inventory.geometry_vectors(field, stratum)[0]["W"])
    negative_w = tuple(-value for value in positive_w)
    double_w = tuple(q(2) * value for value in positive_w)
    correction = tuple(q(index - 7) for index in range(tangent_cones.VARIABLE_COUNT))

    results = tuple(
        minus_w_stress.evaluate_stress(
            field,
            stratum,
            owner,
            velocity,
            correction,
        )
        for velocity in (positive_w, negative_w, double_w)
    )
    for result in results:
        assert len(result.rows) == 9
        assert all(row.weight.sign() > 0 for row in result.rows)
        assert all(value.is_zero() for value in result.combined_jet.gradient)
        assert result.combined_taylor.linear.is_zero()
        assert result.combined_taylor.quadratic == result.total_weighted_curvature
        assert sum((row.weighted_curvature for row in result.rows), q(0)) == (
            result.total_weighted_curvature
        )
        assert all(row.correction_coefficients == row.jet.gradient for row in result.rows)
        assert all(
            row.taylor.quadratic
            == sum(
                (
                    coefficient * value
                    for coefficient, value in zip(
                        row.correction_coefficients, correction, strict=True
                    )
                ),
                q(0),
            )
            + row.velocity_curvature
            for row in result.rows
        )

    positive, negative, doubled = (result.total_weighted_curvature for result in results)
    assert positive.sign() < 0
    assert negative == positive
    assert doubled == q(4) * positive


def test_real_production_weight_perturbation_breaks_cancellation() -> None:
    field = face.make_field()
    q = field.rational
    velocity = tuple(tangent_inventory.geometry_vectors(field, "A")[0]["W"])
    correction = tuple(q(0) for _ in range(tangent_cones.VARIABLE_COUNT))

    with pytest.raises(ValueError, match="combined stress gradient does not cancel"):
        minus_w_stress.evaluate_stress(
            field,
            "A",
            "owner4:a+",
            velocity,
            correction,
            weight_adjustments={"wall:2:x-lower:+": q(1)},
        )


def test_uniform_weight_rescaling_fails_exact_normalization() -> None:
    field = face.make_field()
    q = field.rational
    velocity = tuple(tangent_inventory.geometry_vectors(field, "A")[0]["W"])
    correction = tuple(q(0) for _ in range(tangent_cones.VARIABLE_COUNT))
    baseline = minus_w_stress.evaluate_stress(
        field,
        "A",
        "owner4:a+",
        velocity,
        correction,
    )

    with pytest.raises(ValueError, match="weight normalization or source identity"):
        minus_w_stress.evaluate_stress(
            field,
            "A",
            "owner4:a+",
            velocity,
            correction,
            weight_adjustments={row.label: row.weight for row in baseline.rows},
        )
