"""Byte replay and schema/firewall controls for ContactFullCellControl/v1."""

from __future__ import annotations

import json
from copy import deepcopy

import pytest

import devtools.generate_contact_full_cell_control as generator


def _keys(value: object) -> set[str]:
    if isinstance(value, dict):
        return set(value) | {key for child in value.values() for key in _keys(child)}
    if isinstance(value, list):
        return {key for child in value for key in _keys(child)}
    return set()


def test_retained_control_replays_byte_for_byte_with_separate_work_counts() -> None:
    expected = generator.expected_document()
    retained = json.loads(generator.OUTPUT.read_text(encoding="utf-8"))
    assert retained == expected
    control = retained["control"]
    canonical = control["canonical"]
    price = control["price"]
    assert canonical["unique_image_count"] == 48
    assert canonical["duplicate_image_count"] == 0
    assert price["candidate_domains"]["nonedge_axis_assignments"] == 8
    assert price["executed_work"]["raw_cells_built"] == 1
    assert price["executed_work"]["orbit_images_examined"] == 48
    assert price["executed_work"]["lp_solves"] == 0
    assert control["controls"]["d4-negative-polarity"] == {
        "status": "passing",
        "cases_checked": 16,
        "negative_cases_checked": 8,
        "reversed_relabel_checked": True,
    }


def test_schema_refuses_an_extra_geometry_channel() -> None:
    mutation = deepcopy(generator.expected_document())
    mutation["control"]["coordinates"] = [[0, 0]]
    with pytest.raises(ValueError, match="Additional properties"):
        generator.validate_document(mutation)

    promotion = deepcopy(generator.expected_document())
    promotion["control"]["promotion_boundary"] = (
        "passing authorizes BC-021 and target-sized execution"
    )
    with pytest.raises(ValueError, match="was expected"):
        generator.validate_document(promotion)

    refusal = deepcopy(generator.expected_document())
    refusal["control"]["controls"]["omitted-wall"]["observed_kind"] = "packing-feasible"
    with pytest.raises(ValueError, match="was expected"):
        generator.validate_document(refusal)


def test_control_has_no_geometry_solver_target_or_corpus_payload() -> None:
    control = generator.expected_document()["control"]
    keys = _keys(control)
    assert {
        "centres",
        "centers",
        "coordinates",
        "side",
        "row_matrix",
        "solver_outcome",
        "container_fit",
        "packing_feasible",
        "optimal",
        "target_n",
        "atlas_identity",
        "corpus_provenance",
    }.isdisjoint(keys)
    assert control["evidence_role"].endswith(
        "no geometry, container fit, packing feasibility, or optimality claim"
    )
    assert control["promotion_boundary"] == generator.PROMOTION_BOUNDARY
