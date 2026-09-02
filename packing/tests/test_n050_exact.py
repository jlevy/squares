"""Target-blind controls for the n = 50 source-semantics intake."""

from __future__ import annotations

import copy
from pathlib import Path
from typing import Any

import pytest

from cases.n050_exact.n19_control import (
    CONTROL_INPUTS,
    EXPECTED_MUTATION_PAIR_COUNT,
    EXPECTED_PAIR_COUNT,
    EXPECTED_SIDE_TEXT,
    ControlError,
    run_control,
    write_new_receipt,
)
from cases.n050_exact.source_semantics import (
    IntakeDecision,
    canonical_json,
    evaluate_receipt,
    load_receipt,
)
from cases.n050_exact.source_semantics_runner import (
    INPUT_PATHS,
    SourceApplicationError,
    atomic_publish_new,
    build_result,
)

FIXTURE = Path("cases/n050_exact/w1_source_fixture.json")


def _valid_receipt(kind: str = "exact") -> dict[str, Any]:
    receipt = load_receipt(FIXTURE)
    receipt["role_map"]["source_author"]["name"] = "Synthetic Source Author"
    receipt["role_map"]["file_publisher"]["name"] = "Synthetic File Publisher"
    receipt["semantics_context"] = {
        "coordinate_units": "synthetic-unit",
        "coordinate_frame": "synthetic-origin-right-up",
        "rotation_convention": "synthetic-counterclockwise-turns",
        "exporter_version": "synthetic-1",
    }
    tokens = (
        ("cx", "center_x", "1/3"),
        ("cy", "center_y", "5/4"),
        ("rot", "rotation", "-1/2"),
    )
    receipt["token_inventory"] = [
        {"token_id": token_id, "scalar_class": scalar_class, "serialized_value": value}
        for token_id, scalar_class, value in tokens
    ]
    declarations = []
    for token_id, _, value in tokens:
        if kind == "interval":
            lower, upper = value, value
        else:
            lower = upper = None
        declarations.append(
            {
                "token_id": token_id,
                "kind": kind,
                "precision_digits": 3 if kind in {"nearest", "truncate"} else None,
                "lower": lower,
                "upper": upper,
            }
        )
    receipt["declarations"] = declarations
    return receipt


def _refusal(receipt: dict[str, Any], reason: str) -> None:
    decision = evaluate_receipt(receipt)
    assert not decision.accepted
    assert decision.reason == reason
    assert decision.cells == ()


def test_sanitized_w1_fixture_stops_at_attribution_fallback() -> None:
    receipt = load_receipt(FIXTURE)
    assert len(receipt["resources"]) == 2
    assert receipt["attribution_artifact_sha256"] == receipt["resources"][0]["sha256"]
    assert set(receipt["role_map"]) == {
        "packing_finder",
        "later_optimizer",
        "source_author",
        "file_publisher",
        "compilation_basis",
    }
    _refusal(receipt, "attribution-unbound")


@pytest.mark.parametrize("kind", ["exact", "nearest", "truncate", "interval"])
def test_complete_declaration_kinds_emit_deterministic_cells(kind: str) -> None:
    receipt = _valid_receipt(kind)
    first = evaluate_receipt(receipt)
    second = evaluate_receipt(copy.deepcopy(receipt))
    assert first.accepted
    assert first.reason is None
    assert len(first.cells) == 3
    assert canonical_json(first) == canonical_json(second)


def test_strict_refusal_order_and_zero_cell_output() -> None:
    mutations: list[tuple[str, dict[str, Any]]] = []

    unavailable = _valid_receipt()
    unavailable["resources"][0]["available"] = False
    mutations.append(("source-unavailable", unavailable))

    unbound_hash = _valid_receipt()
    unbound_hash["resources"][0]["sha256"] = "bad"
    mutations.append(("source-hash-or-version-unbound", unbound_hash))

    unbound_attribution = _valid_receipt()
    unbound_attribution["role_map"]["file_publisher"]["name"] = None
    mutations.append(("attribution-unbound", unbound_attribution))

    undefined_frame = _valid_receipt()
    undefined_frame["semantics_context"]["coordinate_frame"] = None
    mutations.append(("units-frame-or-rotation-undefined", undefined_frame))

    uncovered = _valid_receipt()
    uncovered["declarations"].pop()
    mutations.append(("scalar-class-uncovered", uncovered))

    contradictory = _valid_receipt()
    contradictory["declarations"][0]["lower"] = "0"
    mutations.append(("serialization-rule-undefined", contradictory))

    missing_precision = _valid_receipt("nearest")
    missing_precision["declarations"][0]["precision_digits"] = None
    mutations.append(("precision-or-error-bound-undefined", missing_precision))

    empty_cell = _valid_receipt("interval")
    empty_cell["declarations"][0]["lower"] = "2"
    empty_cell["declarations"][0]["upper"] = "1"
    mutations.append(("cell-empty-or-nondeterministic", empty_cell))

    retention = _valid_receipt()
    retention["retention"]["raw_asset_retained"] = True
    mutations.append(("retention-boundary-violated", retention))

    for reason, receipt in mutations:
        _refusal(receipt, reason)


def test_reason_three_precedes_missing_semantics_and_coverage() -> None:
    receipt = _valid_receipt()
    receipt["role_map"]["source_author"]["name"] = None
    receipt["semantics_context"]["coordinate_units"] = None
    receipt["declarations"] = []
    _refusal(receipt, "attribution-unbound")


def test_canonical_serialization_ignores_mapping_insertion_order() -> None:
    decision = evaluate_receipt(_valid_receipt("nearest"))
    reordered = IntakeDecision(
        cells=decision.cells,
        reason=decision.reason,
        accepted=decision.accepted,
    )
    assert canonical_json(decision) == canonical_json(reordered)


def test_loader_rejects_markdown_receipts() -> None:
    with pytest.raises(ValueError, match="must be JSON"):
        load_receipt(Path("campaign/agent-sessions/session-070.md"))


def test_n19_exact_control_matches_durable_receipt() -> None:
    observed = run_control()
    retained = load_receipt(Path("cases/n050_exact/n19_control_receipt.json"))

    assert observed == retained
    assert retained["control_inputs"] == [
        {"path": path, "sha256": digest} for path, digest in CONTROL_INPUTS
    ]
    assert retained["build_call"] == "build(19)"
    assert retained["expected_side"]["serialized"] == EXPECTED_SIDE_TEXT
    assert retained["observed_side"]["serialized"] == EXPECTED_SIDE_TEXT
    assert retained["observed_side"]["equals_expected"] is True
    assert retained["verification"] == {
        "assurance": "exact-sign",
        "valid": True,
        "observed_n": 19,
        "pair_semantics": "all-unordered-pairs",
        "expected_pairs": EXPECTED_PAIR_COUNT,
        "observed_pairs": EXPECTED_PAIR_COUNT,
    }
    assert retained["mutation"]["kind"] == "append-duplicate-of-square-1"
    assert retained["mutation"]["observed_valid"] is False
    assert retained["mutation"]["observed_pairs"] == EXPECTED_MUTATION_PAIR_COUNT
    assert "overlap" in retained["mutation"]["failure_kinds"]
    assert retained["skip_count"] == 0


def test_n19_receipt_writer_refuses_overwrite(tmp_path: Path) -> None:
    path = tmp_path / "control.json"
    receipt = {"control": "synthetic"}
    write_new_receipt(path, receipt)
    with pytest.raises(ControlError, match="already exists"):
        write_new_receipt(path, receipt)
    assert load_receipt(path) == receipt


def test_source_application_builds_only_reason_three_zero_cell_result() -> None:
    receipt = load_receipt(FIXTURE)
    control = load_receipt(Path("cases/n050_exact/n19_control_receipt.json"))
    bindings = {name: f"synthetic-{name}" for name in INPUT_PATHS}

    result = build_result(receipt, bindings, control)

    assert result["executed"] is True
    assert result["outcome"] == "e1-refusal"
    assert result["reason_index"] == 3
    assert result["reason"] == "attribution-unbound"
    assert result["cells"] == []
    assert result["cell_count"] == 0
    assert result["needs_review"] is True
    assert "not an n = 50 geometry" in str(result["claim_boundary"])


def test_source_application_refuses_other_outcome() -> None:
    receipt = _valid_receipt()
    control = load_receipt(Path("cases/n050_exact/n19_control_receipt.json"))
    bindings = {name: f"synthetic-{name}" for name in INPUT_PATHS}

    with pytest.raises(SourceApplicationError, match="reason 3"):
        build_result(receipt, bindings, control)


def test_source_application_atomic_writer_refuses_overwrite(tmp_path: Path) -> None:
    target = tmp_path / "result.json"
    atomic_publish_new(target, b"one\n")
    with pytest.raises(SourceApplicationError, match="already exists"):
        atomic_publish_new(target, b"two\n")
    assert target.read_bytes() == b"one\n"
