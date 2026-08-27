"""Exact controls for execution-scoped n=5 active-row reuse."""

from __future__ import annotations

import pytest

from cases.n5 import equal_side_face as face
from cases.n5 import minus_w_owner4, minus_w_row_jets, minus_w_scale, tangent_cones
from sqpack.field import NumberField


@pytest.mark.exhaustive_exact
def test_shared_row_inventory_is_exact_isolated_and_builds_once_per_stratum(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    field = face.make_field()
    original_builder = minus_w_row_jets.active_row_jets
    calls: list[str] = []

    def counted_builder(control_field: NumberField, stratum: str):
        calls.append(stratum)
        return original_builder(control_field, stratum)

    monkeypatch.setattr(minus_w_row_jets, "active_row_jets", counted_builder)
    inventory = minus_w_row_jets.RowJetInventory.build(field)
    assert calls == list(tangent_cones.STRATA)

    scale_records = minus_w_scale.positive_w_control_records(field, row_inventory=inventory)
    owner4_records = minus_w_owner4.positive_w_control_records(field, row_inventory=inventory)
    assert len(scale_records) == 15
    assert len(owner4_records) == 3
    assert calls == list(tangent_cones.STRATA)

    shared_a = inventory.active_rows(field, "A")
    monkeypatch.setattr(minus_w_row_jets, "active_row_jets", original_builder)
    assert shared_a == original_builder(field, "A")

    mutated_a = shared_a
    removed = "contact:3-4:owner4:a+:square3-feature+1"
    del mutated_a[removed]
    with pytest.raises(ValueError, match=r"generated owner-row keys drifted; missing=\["):
        minus_w_row_jets.owner_row_jets(
            field,
            "A",
            "owner4:a+",
            active_rows=mutated_a,
        )
    assert removed in inventory.active_rows(field, "A")
    assert removed in minus_w_row_jets.owner_row_jets(
        field,
        "A",
        "owner4:a+",
        active_rows=inventory.active_rows(field, "A"),
    )

    original_matrix = minus_w_row_jets.tangent_inventory.matrix

    def shortened_matrix(control_field: NumberField, stratum: str, owner: str):
        return original_matrix(control_field, stratum, owner)[:-1]

    with monkeypatch.context() as mutation:
        mutation.setattr(
            minus_w_row_jets.tangent_inventory,
            "matrix",
            shortened_matrix,
        )
        with pytest.raises(ValueError, match="generated owner-row keys drifted"):
            minus_w_row_jets.owner_row_jets(
                field,
                "A",
                "owner3:a+",
                active_rows=inventory.active_rows(field, "A"),
            )
    assert minus_w_row_jets.owner_row_jets(
        field,
        "A",
        "owner3:a+",
        active_rows=inventory.active_rows(field, "A"),
    )

    other_field = face.make_field()
    with pytest.raises(ValueError, match="row inventory belongs to a different number field"):
        inventory.active_rows(other_field, "A")
