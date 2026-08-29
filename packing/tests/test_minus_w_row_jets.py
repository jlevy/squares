"""Focused tests for the production n=5 row-jet inventory builder."""

from __future__ import annotations

import pytest

from cases.n5 import equal_side_face as face
from cases.n5 import minus_w_row_jets, tangent_cones, tangent_inventory


@pytest.mark.parametrize(
    ("stratum", "expected_count"),
    (("A", 17), ("interior", 15), ("B", 17)),
)
@pytest.mark.parametrize("owner", tangent_cones.EXPECTED_CONTACT_BRANCHES)
@pytest.mark.exhaustive_exact
def test_owner_rows_match_complete_authoritative_inventory(
    stratum: str, expected_count: int, owner: str
) -> None:
    field = face.make_field()
    actual = minus_w_row_jets.owner_row_jets(field, stratum, owner)
    source_rows = tangent_inventory.matrix(field, stratum, owner)

    assert len(actual) == expected_count
    assert tuple(actual) == tuple(row.label for row in source_rows)
    assert {label: jet.gradient for label, jet in actual.items()} == {
        row.label: row.coefficients for row in source_rows
    }
    assert all(jet.value.is_zero() for jet in actual.values())
    assert all(jet.dimension == tangent_cones.VARIABLE_COUNT for jet in actual.values())
    assert sum(label.startswith("contact:3-4:") for label in actual) == 2
    assert all(
        not label.startswith("contact:3-4:") or label.startswith(f"contact:3-4:{owner}:")
        for label in actual
    )


@pytest.mark.parametrize(
    ("stratum", "expected_count"),
    (("A", 19), ("interior", 17), ("B", 19)),
)
@pytest.mark.exhaustive_exact
def test_active_rows_expose_both_owner_alternatives(stratum: str, expected_count: int) -> None:
    field = face.make_field()
    rows = minus_w_row_jets.active_row_jets(field, stratum)

    assert len(rows) == expected_count
    tied = {label for label in rows if label.startswith("contact:3-4:")}
    assert len(tied) == 4
    assert {label.split(":square", maxsplit=1)[0] for label in tied} == {
        "contact:3-4:owner3:a+",
        "contact:3-4:owner4:a+",
    }


@pytest.mark.exhaustive_exact
def test_sat_row_retains_exact_center_angle_cross_curvature() -> None:
    field = face.make_field()
    row = minus_w_row_jets.owner_row_jets(field, "A", "owner4:a+")["contact:2-4:owner4:a+"]
    center = tangent_cones.x(4)
    angle = tangent_cones.theta(4)

    assert row.hessian[center][angle] == -field.alpha / 2
    assert row.hessian[angle][center] == row.hessian[center][angle]


def test_builder_rejects_unregistered_strata_and_owners() -> None:
    field = face.make_field()
    with pytest.raises(ValueError, match="unknown source stratum"):
        minus_w_row_jets.active_row_jets(field, "midpoint")
    with pytest.raises(ValueError, match="unknown source owner"):
        minus_w_row_jets.owner_row_jets(field, "A", "owner2:a+")
