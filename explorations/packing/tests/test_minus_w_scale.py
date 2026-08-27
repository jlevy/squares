"""Focused tests for exact owner-3 scale routing on the positive-W control."""

from __future__ import annotations

from collections.abc import Iterator

import pytest

from cases.n5 import equal_side_face as face
from cases.n5 import minus_w_scale, tangent_cones
from sqpack.field import FieldElement, NumberField


@pytest.fixture(scope="module")
def scale_control() -> Iterator[tuple[NumberField, tuple[minus_w_scale.ScaleRecord, ...]]]:
    field = face.make_field()
    yield field, minus_w_scale.positive_w_control_records(field)


@pytest.mark.exhaustive_exact
def test_positive_w_control_has_exact_three_by_five_inventory(
    scale_control: tuple[NumberField, tuple[minus_w_scale.ScaleRecord, ...]],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    field, records = scale_control

    assert len(records) == 15
    assert {(record.stratum, record.key) for record in records} == {
        (stratum, key)
        for stratum in tangent_cones.STRATA
        for key in minus_w_scale.EXPECTED_SCALE_KEYS
    }
    assert all(not hasattr(record, "outcome") for record in records)
    for record in records:
        affine = record.bounded_affine
        assert affine.beta_symbol == "beta"
        assert len(affine.correction_coefficients) == tangent_cones.VARIABLE_COUNT
        assert all(value.is_zero() for value in affine.correction_coefficients)
        assert affine.beta_coefficient.is_zero()
        assert sum(not value.is_zero() for value in affine.beta_direction) == 1
        assert not isinstance(affine.beta_symbol, type(affine.constant))
        assert affine.beta_direction[tangent_cones.theta(3)] == affine.constant.field.one
        assert all(
            value.is_zero()
            for index, value in enumerate(affine.beta_direction)
            if index != tangent_cones.theta(3)
        )
        assert affine.constant.sign() < 0
        tied = {
            row.label: row for row in record.stress.rows if row.label.startswith("contact:3-4:")
        }
        cusp = record.unbounded_cusp
        assert set(tied) == {
            minus_w_scale.TIED_PLUS_LABEL,
            minus_w_scale.TIED_MINUS_LABEL,
        }
        assert all(row.weight.sign() > 0 for row in tied.values())
        assert cusp.tied_gradients == (
            tied[minus_w_scale.TIED_PLUS_LABEL].jet.gradient,
            tied[minus_w_scale.TIED_MINUS_LABEL].jet.gradient,
        )
        assert cusp.b_plus == -(cusp.h + cusp.transverse_projection)
        assert -cusp.b_minus == -(cusp.h - cusp.transverse_projection)
        assert cusp.kappa_positive == cusp.b_plus
        assert cusp.kappa_negative == -cusp.b_minus
        assert cusp.kappa_positive.sign() < 0
        assert cusp.kappa_negative.sign() < 0
        assert all(value.is_zero() for value in cusp.nuisance_coefficients)
        assert cusp.normalized_remainder_limits == minus_w_scale.NORMALIZED_REMAINDER_LIMITS
    routes = {record.key: record.route for record in records if record.stratum == "A"}

    assert routes[minus_w_scale.BOUNDED_BETA_NEGATIVE].beta_sign == -1
    assert routes[minus_w_scale.BOUNDED_BETA_ZERO].beta_sign == 0
    assert routes[minus_w_scale.BOUNDED_BETA_POSITIVE].beta_sign == 1
    assert routes[minus_w_scale.UNBOUNDED_DELTA_NEGATIVE].delta_sign == -1
    assert routes[minus_w_scale.UNBOUNDED_DELTA_POSITIVE].delta_sign == 1
    assert all(
        route.family == "bounded" and route.delta_sign is None
        for key, route in routes.items()
        if key.startswith("bounded_")
    )
    assert all(
        route.family == "unbounded" and route.beta_sign is None
        for key, route in routes.items()
        if key.startswith("unbounded_")
    )
    assert routes[minus_w_scale.BOUNDED_BETA_NEGATIVE].decisive_tied_labels == (
        minus_w_scale.TIED_MINUS_LABEL,
    )
    assert routes[minus_w_scale.BOUNDED_BETA_POSITIVE].decisive_tied_labels == (
        minus_w_scale.TIED_PLUS_LABEL,
    )
    assert set(routes[minus_w_scale.BOUNDED_BETA_ZERO].decisive_tied_labels) == {
        minus_w_scale.TIED_PLUS_LABEL,
        minus_w_scale.TIED_MINUS_LABEL,
    }
    assert routes[minus_w_scale.UNBOUNDED_DELTA_NEGATIVE].decisive_tied_labels == (
        minus_w_scale.TIED_MINUS_LABEL,
    )
    assert routes[minus_w_scale.UNBOUNDED_DELTA_POSITIVE].decisive_tied_labels == (
        minus_w_scale.TIED_PLUS_LABEL,
    )

    original_vectors = minus_w_scale.tangent_inventory.geometry_vectors

    def zero_w(
        control_field: NumberField, stratum: str
    ) -> tuple[
        dict[str, list[FieldElement]],
        dict[str, list[FieldElement]],
        dict[str, list[FieldElement]],
        str,
    ]:
        lineality, sheet, transverse, kind = original_vectors(control_field, stratum)
        mutated = dict(lineality)
        mutated["W"] = [control_field.zero for _ in range(tangent_cones.VARIABLE_COUNT)]
        return mutated, sheet, transverse, kind

    monkeypatch.setattr(minus_w_scale.tangent_inventory, "geometry_vectors", zero_w)
    with pytest.raises(
        ValueError, match="positive-W control lost its strict production curvature"
    ):
        minus_w_scale.positive_w_control_records(field)


def test_missing_real_scale_handler_is_rejected_before_evaluation(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    field = face.make_field()
    handlers = dict(minus_w_scale.SCALE_HANDLERS)
    del handlers[minus_w_scale.UNBOUNDED_DELTA_POSITIVE]

    def unexpected_stress(*_args: object, **_kwargs: object) -> None:
        pytest.fail("stress evaluation ran before scale exhaustion rejected")

    monkeypatch.setattr(minus_w_scale.minus_w_stress, "evaluate_stress", unexpected_stress)
    exact_error = (
        r"scale handler inventory drifted; "
        r"missing=\['unbounded_delta_positive'\], extra=\[\]"
    )
    with pytest.raises(
        ValueError,
        match=exact_error,
    ):
        minus_w_scale.positive_w_control_records(field, handlers=handlers)
