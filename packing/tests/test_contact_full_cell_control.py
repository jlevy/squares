"""Byte replay and schema/firewall controls for ContactFullCellControl/v1."""

from __future__ import annotations

import json
from copy import deepcopy

import pytest

import devtools.generate_contact_full_cell_control as generator

EXPECTED_EXECUTION_ROWS = (
    ("wall/0/left", "open-wall-inequality"),
    ("wall/0/right", "seated-wall-equality"),
    ("wall/0/bottom", "open-wall-inequality"),
    ("wall/0/top", "seated-wall-equality"),
    ("wall/1/left", "open-wall-inequality"),
    ("wall/1/right", "open-wall-inequality"),
    ("wall/1/bottom", "open-wall-inequality"),
    ("wall/1/top", "seated-wall-equality"),
    ("wall/2/left", "open-wall-inequality"),
    ("wall/2/right", "seated-wall-equality"),
    ("wall/2/bottom", "open-wall-inequality"),
    ("wall/2/top", "open-wall-inequality"),
    ("pair/0/1/0/u/0", "contact-equality"),
    ("pair/0/2/0/v/0", "contact-equality"),
    ("pair/1/2/1/u/2", "nonedge-inequality"),
)
EXPECTED_EXECUTION_WORK = {
    "raw_cell_domain_size": 8,
    "raw_cells_built": 1,
    "axis_order_branches_examined": 1,
    "orbit_images_examined": 48,
    "unique_orbit_images": 48,
    "duplicate_orbit_images": 0,
    "canonical_cells_admitted": 1,
    "wall_rows_compiled": 12,
    "contact_equalities": 2,
    "nonedge_inequalities": 1,
    "pair_constraints_compiled": 3,
    "pair_tests": 0,
    "lp_solver_attempts": 0,
}
EXPECTED_EXECUTION_CONTROLS = {
    "execution-plan-replay": {"status": "passing"},
    "execution-plan-omitted-row": {
        "status": "passing",
        "observed_kind": "full-cell-row-plan",
    },
    "execution-plan-role-swap": {
        "status": "passing",
        "observed_kind": "full-cell-row-plan",
    },
    "execution-plan-forged-count": {
        "status": "passing",
        "observed_kind": "full-cell-work-count",
    },
}


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
    execution_plan = control["execution_plan"]
    assert execution_plan["contract"] == "packing.squares:FullCellExecutionPlan/v1"
    assert execution_plan["promotion_boundary"] == (
        "passing advances only BC-017 instrumentation readiness; actual LP execution, "
        "BC-017 completion, BC-018, think-u97a, BC-021, and target-sized execution "
        "remain closed"
    )
    assert execution_plan["canonical_label"] == canonical["label"]
    assert (
        tuple((row["row_id"], row["mode"]) for row in execution_plan["rows"])
        == EXPECTED_EXECUTION_ROWS
    )
    assert execution_plan["work"] == EXPECTED_EXECUTION_WORK
    execution_controls = {
        key: value
        for key, value in control["controls"].items()
        if key.startswith("execution-plan-")
    }
    assert execution_controls == EXPECTED_EXECUTION_CONTROLS
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

    forged_work = deepcopy(generator.expected_document())
    forged_work["control"]["execution_plan"]["work"]["pair_tests"] = 1
    with pytest.raises(ValueError, match="was expected"):
        generator.validate_document(forged_work)

    extra_coordinates = deepcopy(generator.expected_document())
    extra_coordinates["control"]["execution_plan"]["coordinates"] = [[0, 0]]
    with pytest.raises(ValueError, match="Additional properties"):
        generator.validate_document(extra_coordinates)

    extra_solver = deepcopy(generator.expected_document())
    extra_solver["control"]["execution_plan"]["solver_status"] = "feasible"
    with pytest.raises(ValueError, match="Additional properties"):
        generator.validate_document(extra_solver)

    widened_plan = deepcopy(generator.expected_document())
    widened_plan["control"]["execution_plan"]["promotion_boundary"] = (
        "passing also advances BC-016 readiness"
    )
    with pytest.raises(ValueError, match="was expected"):
        generator.validate_document(widened_plan)

    missing_plan_boundary = deepcopy(generator.expected_document())
    del missing_plan_boundary["control"]["execution_plan"]["promotion_boundary"]
    with pytest.raises(ValueError, match="required property"):
        generator.validate_document(missing_plan_boundary)


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
