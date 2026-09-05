"""Focused tests for target-free owner-4 proof data on the positive-W control."""

from __future__ import annotations

from dataclasses import replace

import pytest

from cases.n5 import equal_side_face as face
from cases.n5 import minus_w_owner4, tangent_cones
from sqpack.field import FieldElement, NumberField


@pytest.fixture(scope="module")
def owner4_control() -> tuple[NumberField, tuple[minus_w_owner4.Owner4Record, ...]]:
    field = face.make_field()
    return field, minus_w_owner4.positive_w_control_records(field)


@pytest.mark.exhaustive_exact
def test_positive_w_owner4_control_exhausts_three_strata_and_rejects_zero_w(
    owner4_control: tuple[NumberField, tuple[minus_w_owner4.Owner4Record, ...]],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    field, records = owner4_control

    assert len(records) == 3
    assert {record.stratum for record in records} == set(tangent_cones.STRATA)
    assert all(not hasattr(record, "outcome") for record in records)
    for record in records:
        assert record.stress.owner == "owner4:a+"
        assert {
            row.label for row in record.stress.rows if row.label.startswith("contact:3-4:")
        } == {
            "contact:3-4:owner4:a+:square3-feature+1",
            "contact:3-4:owner4:a+:square3-feature-1",
        }
        assert any(not value.is_zero() for value in record.correction)
        assert len(record.stress.rows) == 9
        assert all(row.weight.sign() > 0 for row in record.stress.rows)
        assert all(row.taylor.value.is_zero() for row in record.stress.rows)
        assert all(row.taylor.linear.is_zero() for row in record.stress.rows)
        assert record.correction_coefficients == record.stress.combined_jet.gradient
        assert len(record.correction_coefficients) == tangent_cones.VARIABLE_COUNT
        assert all(value.is_zero() for value in record.correction_coefficients)
        assert record.stress.combined_taylor.linear.is_zero()
        assert record.stress.combined_taylor.quadratic == record.stress.total_weighted_curvature
        assert record.constant == record.stress.total_weighted_curvature
        assert record.constant.sign() < 0

    baseline = records[0]
    non_tight_velocity = list(baseline.velocity)
    non_tight_velocity[tangent_cones.x(2)] += field.one
    mutated_rows = tuple(
        replace(
            row,
            taylor=row.jet.substitute(non_tight_velocity, baseline.correction),
        )
        for row in baseline.stress.rows
    )
    assert any(not row.taylor.linear.is_zero() for row in mutated_rows)
    with monkeypatch.context() as mutation:
        mutation.setattr(
            minus_w_owner4.minus_w_stress,
            "evaluate_stress",
            lambda *_args, **_kwargs: replace(baseline.stress, rows=mutated_rows),
        )
        with pytest.raises(
            ValueError,
            match="owner-4 source path is not first-order tight",
        ):
            minus_w_owner4.owner4_record(
                field,
                baseline.stratum,
                non_tight_velocity,
                baseline.correction,
            )

    with monkeypatch.context() as mutation:
        mutation.setattr(minus_w_owner4, "OWNER4", "owner3:a+")
        mutation.setattr(
            minus_w_owner4.minus_w_stress,
            "evaluate_stress",
            lambda *_args, **_kwargs: replace(baseline.stress, owner="owner3:a+"),
        )
        with pytest.raises(ValueError, match="owner-4 production branch drifted"):
            minus_w_owner4.owner4_record(
                field,
                baseline.stratum,
                baseline.velocity,
                baseline.correction,
            )

    missing_tied_stress = replace(
        baseline.stress,
        rows=tuple(
            row
            for row in baseline.stress.rows
            if row.label != "contact:3-4:owner4:a+:square3-feature+1"
        ),
    )
    with monkeypatch.context() as mutation:
        mutation.setattr(
            minus_w_owner4.minus_w_stress,
            "evaluate_stress",
            lambda *_args, **_kwargs: missing_tied_stress,
        )
        with pytest.raises(ValueError, match="owner-4 tied-row inventory drifted"):
            minus_w_owner4.owner4_record(
                field,
                baseline.stratum,
                baseline.velocity,
                baseline.correction,
            )

    original_vectors = minus_w_owner4.tangent_inventory.geometry_vectors
    calls: list[str] = []

    def zero_w(
        control_field: NumberField, stratum: str
    ) -> tuple[
        dict[str, list[FieldElement]],
        dict[str, list[FieldElement]],
        dict[str, list[FieldElement]],
        str,
    ]:
        calls.append(stratum)
        if len(calls) > 1:
            pytest.fail("later stratum fetched after first failed owner-4 control")
        lineality, sheet, transverse, kind = original_vectors(control_field, stratum)
        mutated = dict(lineality)
        mutated["W"] = [control_field.zero for _ in range(tangent_cones.VARIABLE_COUNT)]
        return mutated, sheet, transverse, kind

    monkeypatch.setattr(minus_w_owner4.tangent_inventory, "geometry_vectors", zero_w)
    with pytest.raises(
        ValueError,
        match="positive-W owner-4 control lost its strict production curvature",
    ):
        minus_w_owner4.positive_w_control_records(field)
    assert calls == [tangent_cones.STRATA[0]]
