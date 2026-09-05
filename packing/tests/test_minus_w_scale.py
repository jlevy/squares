"""Focused tests for exact owner-3 scale routing on the positive-W control."""

from __future__ import annotations

from dataclasses import replace

import pytest

from cases.n5 import equal_side_face as face
from cases.n5 import minus_w_scale, tangent_cones
from sqpack.field import FieldElement, NumberField
from sqpack.research.exact_jets import SecondOrderJet


@pytest.fixture(scope="module")
def scale_control() -> tuple[NumberField, tuple[minus_w_scale.ScaleRecord, ...]]:
    field = face.make_field()
    return field, minus_w_scale.positive_w_control_records(field)


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
        sign_evidence = record.route_sign_evidence
        assert sign_evidence.projection.value.is_zero()
        assert sign_evidence.delta_coefficient.sign() > 0
        assert sign_evidence.projection.gradient[tangent_cones.theta(3)] == field.one
        assert sign_evidence.projection.gradient[tangent_cones.theta(4)] == -field.one
        assert sign_evidence.positive_delta_tied_label == minus_w_scale.TIED_PLUS_LABEL
        assert sign_evidence.negative_delta_tied_label == minus_w_scale.TIED_MINUS_LABEL
        if record.route.family == "bounded":
            assert record.route.unbounded_premises is None
            assert record.normalized_remainder_limits == ()
        else:
            premises = record.route.unbounded_premises
            assert premises is not None
            assert premises.delta_sign == record.route.delta_sign
            witnesses = record.normalized_remainder_limits
            assert (
                tuple(witness.expression for witness in witnesses)
                == minus_w_scale.NORMALIZED_REMAINDER_EXPRESSIONS
            )
            assert tuple(witness.rule for witness in witnesses) == (
                minus_w_scale.RemainderRule.RECIPROCAL_DIVERGENT_RATIO,
                minus_w_scale.RemainderRule.CANCEL_EVENTUALLY_NONZERO_ABS_DELTA,
                minus_w_scale.RemainderRule.ABS_DELTA_FROM_LITTLE_O,
            )
            assert tuple(witness.premises for witness in witnesses) == (
                frozenset(
                    {
                        minus_w_scale.ScalePremise.T_EVENTUALLY_POSITIVE,
                        minus_w_scale.ScalePremise.DELTA_EVENTUALLY_NONZERO,
                        minus_w_scale.ScalePremise.DELTA_SIGN_STABLE,
                        minus_w_scale.ScalePremise.ABS_DELTA_OVER_T_SQUARED_TO_POSITIVE_INFINITY,
                    }
                ),
                frozenset(
                    {
                        minus_w_scale.ScalePremise.T_EVENTUALLY_POSITIVE,
                        minus_w_scale.ScalePremise.DELTA_EVENTUALLY_NONZERO,
                        minus_w_scale.ScalePremise.DELTA_SIGN_STABLE,
                        minus_w_scale.ScalePremise.T_TO_ZERO,
                    }
                ),
                frozenset(
                    {
                        minus_w_scale.ScalePremise.T_EVENTUALLY_POSITIVE,
                        minus_w_scale.ScalePremise.DELTA_EVENTUALLY_NONZERO,
                        minus_w_scale.ScalePremise.DELTA_SIGN_STABLE,
                        minus_w_scale.ScalePremise.DELTA_LITTLE_O_T,
                        minus_w_scale.ScalePremise.T_TO_ZERO,
                    }
                ),
            )
            assert all(witness.delta_sign == record.route.delta_sign for witness in witnesses)
            for witness in witnesses:
                assert minus_w_scale.ScalePremise.T_EVENTUALLY_POSITIVE in witness.premises
                assert minus_w_scale.ScalePremise.DELTA_EVENTUALLY_NONZERO in witness.premises
                assert minus_w_scale.ScalePremise.DELTA_SIGN_STABLE in witness.premises
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

    swapped_handlers = dict(minus_w_scale.SCALE_HANDLERS)
    swapped_handlers[minus_w_scale.UNBOUNDED_DELTA_POSITIVE] = swapped_handlers[
        minus_w_scale.UNBOUNDED_DELTA_NEGATIVE
    ]
    with pytest.raises(
        ValueError,
        match="scale handler semantics drifted; key=unbounded_delta_positive",
    ):
        minus_w_scale.validated_route_specs(swapped_handlers, records[0].route_sign_evidence)

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

    monkeypatch.setattr(minus_w_scale.tangent_inventory, "geometry_vectors", original_vectors)
    monkeypatch.setattr(
        minus_w_scale.minus_w_row_jets,
        "owner3_tied_feature_projection",
        lambda _field, _stratum: SecondOrderJet.constant(
            field.zero, tangent_cones.VARIABLE_COUNT
        ),
    )
    with pytest.raises(ValueError, match="owner-3 tied projection has no strict delta sign"):
        minus_w_scale.route_sign_evidence(field, "A", records[0].stress)

    projection = records[0].route_sign_evidence.projection
    malformed_gradient = list(projection.gradient)
    malformed_gradient[tangent_cones.x(0)] = field.one
    malformed = SecondOrderJet(projection.value, tuple(malformed_gradient), projection.hessian)
    monkeypatch.setattr(
        minus_w_scale.minus_w_row_jets,
        "owner3_tied_feature_projection",
        lambda _field, _stratum: malformed,
    )
    with pytest.raises(
        ValueError, match="owner-3 tied projection is not a pure delta covector"
    ):
        minus_w_scale.route_sign_evidence(field, "A", records[0].stress)


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


@pytest.mark.parametrize(
    "premise_name",
    [
        "t_to_zero",
        "t_eventually_positive",
        "delta_little_o_t",
        "abs_delta_over_t_squared_to_positive_infinity",
        "delta_eventually_nonzero",
        "delta_sign_stable",
    ],
)
def test_unbounded_remainder_witnesses_require_every_declared_premise(
    premise_name: str,
) -> None:
    premises = minus_w_scale.unbounded_route_premises(1)
    mutated = replace(premises, **{premise_name: False})
    with pytest.raises(
        ValueError,
        match=rf"unbounded scale assumption missing; premises=\['{premise_name}'\]",
    ):
        minus_w_scale.unbounded_remainder_witnesses(mutated)


def test_unbounded_remainder_witness_inventory_is_closed() -> None:
    premises = minus_w_scale.unbounded_route_premises(-1)
    baseline = minus_w_scale.unbounded_remainder_witnesses(premises)
    mutated = replace(
        baseline[0],
        rule=minus_w_scale.RemainderRule.ABS_DELTA_FROM_LITTLE_O,
    )

    with pytest.raises(
        ValueError,
        match=r"unbounded remainder witness drifted; expression=t\^2/abs\(delta\)->0",
    ):
        minus_w_scale.unbounded_remainder_witnesses(
            premises,
            witness_overrides={mutated.expression: mutated},
        )


def test_unbounded_route_rejects_invalid_delta_sign() -> None:
    with pytest.raises(ValueError, match="unbounded scale route has invalid delta sign 0"):
        minus_w_scale.unbounded_route_premises(0)
