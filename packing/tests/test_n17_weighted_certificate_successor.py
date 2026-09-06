"""Target-blind controls for the fresh H-052 successor chain and its two schemas."""

from __future__ import annotations

import json
import subprocess
import sys
from dataclasses import replace
from fractions import Fraction
from pathlib import Path
from typing import Any

import pytest

from cases.n17_weighted_certificate.model import Atom, Direction, canonical_json
from cases.n17_weighted_certificate.target_independent import (
    accumulate_target_independent,
)
from cases.n17_weighted_certificate_successor.run import (
    CHAIN_GENESIS_CHECKPOINT,
    DISAGREEMENT_ABSENCES,
    FROZEN_MUTATIONS,
    IMMEDIATE_PARENT_CHECKPOINT,
    IMMEDIATE_PARENT_LAST_ROW_HASH,
    IMMEDIATE_PARENT_PROGRESS,
    IMMEDIATE_PARENT_ROW_COUNT,
    PRODUCTION_EXPECTATIONS,
    TERMINAL_COMPLETE_AGREEMENT,
    TERMINAL_EARLY_DISAGREEMENT,
    SuccessorChainDriver,
    SuccessorCheckpoint,
    SuccessorDisagreementStopError,
    SuccessorError,
    ancestry_report,
    assemble_synthetic_result,
    chain_status,
    derive_decision,
    require_writable,
    run_selftest,
    synthetic_inputs,
    synthetic_receipt,
    synthetic_successor_store,
    validate_result,
    verify_chain_genesis,
    verify_immediate_parent,
)


def _as_json(value: object) -> dict[str, Any]:
    """Round-trip a record through its canonical bytes, as a reviewer would read it."""

    loaded: dict[str, Any] = json.loads(canonical_json(value))
    return loaded


def _completed(tmp_path: Path, name: str = "case"):
    receipt, genesis, immediate = synthetic_receipt(tmp_path, name)
    store = synthetic_successor_store(tmp_path, name, receipt)
    atoms, _, outer_side, square_side = synthetic_inputs()
    completed = SuccessorChainDriver(store).run(
        atoms=atoms, outer_side=outer_side, square_side=square_side
    )
    return receipt, genesis, immediate, store, completed


def test_successor_recomputes_the_interrupted_ordinal(tmp_path: Path) -> None:
    receipt, _, _, store, completed = _completed(tmp_path)
    first_new = store.binding.first_new_ordinal
    assert first_new == len(receipt.carried_rows)
    assert completed.rows[:first_new] == receipt.carried_rows
    assert completed.rows[first_new].ordinal == first_new
    assert completed.rows[first_new].previous_row_hash == receipt.immediate_parent.last_row_hash
    assert len(completed.rows) == len(store.directions)
    assert all(row.agreement for row in completed.rows)
    assert not store.progress_path.exists()


def test_the_two_ancestries_are_separately_bound(tmp_path: Path) -> None:
    receipt, _, _, store, _ = _completed(tmp_path)
    parent = store.binding.immediate_parent
    genesis = store.binding.chain_genesis
    assert parent.role != genesis.role
    assert parent.experiment_id != genesis.experiment_id
    assert genesis.row_count < parent.row_count
    assert receipt.carried_rows[0].previous_row_hash == genesis.binding_hash
    assert receipt.carried_rows[-1].row_hash == parent.last_row_hash
    assert receipt.carried_rows[: genesis.row_count] == receipt.genesis_rows


def test_swapped_ancestry_is_refused(tmp_path: Path) -> None:
    _, genesis, immediate = synthetic_receipt(tmp_path, "swap")
    _, directions, _, _ = synthetic_inputs()
    with pytest.raises(SuccessorError):
        verify_immediate_parent(
            replace(
                immediate,
                checkpoint_path=genesis.checkpoint_path,
                progress_path=genesis.progress_path,
                checkpoint_sha256=immediate.checkpoint_sha256,
            ),
            directions,
        )
    with pytest.raises(SuccessorError):
        verify_chain_genesis(
            replace(genesis, checkpoint_path=immediate.checkpoint_path),
            directions,
            resume_stage="source_started",
        )
    with pytest.raises(SuccessorError):
        verify_immediate_parent(
            replace(immediate, experiment_id="exp-052", genesis_experiment_id="exp-056"),
            directions,
        )


def test_frozen_ancestor_paths_are_never_writable(tmp_path: Path) -> None:
    """BC-147 caveat 1: the exp-056 paths the child driver's guard set allowed."""

    _, _, _, store, _ = _completed(tmp_path)
    for candidate in (
        IMMEDIATE_PARENT_CHECKPOINT,
        IMMEDIATE_PARENT_PROGRESS,
        CHAIN_GENESIS_CHECKPOINT,
        Path("cases/n17_weighted_certificate_resume/stolen.json"),
        Path("cases/n17_weighted_certificate_child/stolen.json"),
        store.output_root / ".." / "escaped.json",
        tmp_path / "outside.json",
    ):
        with pytest.raises(SuccessorError):
            require_writable(candidate, store.output_root, "checkpoint path")


def test_agreement_schema_carries_both_complete_manifests(tmp_path: Path) -> None:
    _, _, _, store, completed = _completed(tmp_path)
    record = _as_json(assemble_synthetic_result(completed, store))
    assert record["terminal_schema"] == TERMINAL_COMPLETE_AGREEMENT
    assert record["decision"] == "accepted"
    assert record["instrument_valid"] is True
    assert record["absences"] == {}
    expected_rows = record["frozen_expectations"]["direction_count"]
    for name in ("source_faithful", "independent"):
        summary = record[name]
        assert len(summary["rows"]) == expected_rows
        assert summary["atom_hash"]
        assert summary["direction_hash"]
        assert summary["total_weight"] == record["frozen_expectations"]["total_weight"]
        assert summary["global_minimum"] == record["frozen_expectations"]["global_minimum"]
        assert record["row_minimums"][name] == [row["minimum"] for row in summary["rows"]]
    assert set(record["mutation_guards"]) == set(FROZEN_MUTATIONS)
    assert record["all_mutations_rejected"] is True
    assert record["shrink_and_scaling"]["all_hold"] is True

    for missing in ("source_faithful", "independent", "global_minimum", "row_minimums"):
        broken = json.loads(canonical_json(record))
        broken.pop(missing)
        with pytest.raises(SuccessorError):
            validate_result(broken)


def test_wrong_global_minimum_is_refused(tmp_path: Path) -> None:
    _, _, _, store, completed = _completed(tmp_path)
    record = _as_json(assemble_synthetic_result(completed, store))
    broken = json.loads(canonical_json(record))
    broken["source_faithful"]["global_minimum"] = "999/1"
    with pytest.raises(SuccessorError):
        validate_result(broken)
    broken = json.loads(canonical_json(record))
    broken["global_minimum"]["independent"] = "999/1"
    with pytest.raises(SuccessorError):
        validate_result(broken)


def test_decision_is_derived_from_the_emitted_fields(tmp_path: Path) -> None:
    _, _, _, store, completed = _completed(tmp_path)
    record = _as_json(assemble_synthetic_result(completed, store))
    assert derive_decision(record) == record["decision"]

    for mutation in (
        ("preconditions", "direction_unit"),
        ("mutation_guards", "atom_mutation_rejected"),
        ("shrink_and_scaling", "exact_side_decomposition"),
    ):
        broken = json.loads(canonical_json(record))
        block, key = mutation
        if isinstance(broken[block][key], list):
            broken[block][key][0] = False
        else:
            broken[block][key] = False
        with pytest.raises(SuccessorError):
            validate_result(broken)

    asserted = json.loads(canonical_json(record))
    asserted["instrument_valid"] = False
    with pytest.raises(SuccessorError):
        validate_result(asserted)
    asserted = json.loads(canonical_json(record))
    asserted["decision"] = "rejected"
    with pytest.raises(SuccessorError):
        validate_result(asserted)


def test_disagreement_schema_declares_every_absence(tmp_path: Path) -> None:
    receipt, _, _ = synthetic_receipt(tmp_path, "disagree")
    store = synthetic_successor_store(tmp_path, "disagree", receipt)
    atoms, _, outer_side, square_side = synthetic_inputs()

    def perturbed(
        call_atoms: tuple[Atom, ...],
        direction: Direction,
        call_outer: Fraction,
        call_square: Fraction,
    ) -> object:
        manifest = accumulate_target_independent(call_atoms, direction, call_outer, call_square)
        return replace(manifest, minimum=manifest.minimum + 1)

    with pytest.raises(SuccessorDisagreementStopError):
        SuccessorChainDriver(
            store,
            independent_accumulator=perturbed,  # pyright: ignore[reportArgumentType]
        ).run(atoms=atoms, outer_side=outer_side, square_side=square_side)

    retained = store.load()
    assert retained.rows[-1].agreement is False
    record = _as_json(assemble_synthetic_result(retained, store))
    assert record["terminal_schema"] == TERMINAL_EARLY_DISAGREEMENT
    assert record["decision"] == "rejected"
    assert set(record["absences"]) == set(DISAGREEMENT_ABSENCES)
    assert record["absences"]["suffix_rows"]["absent_count"] >= 1
    for absent in ("source_faithful", "independent", "global_minimum", "row_minimums"):
        assert absent not in record
    assert record["verified_prefix"]["chain_verified"] is True
    assert record["discrepant_pair"]["agreement"] is False
    assert record["first_disagreement"]["ordinal"] == retained.rows[-1].ordinal

    for absence in ("suffix_rows", "source_faithful_certificate_manifest"):
        broken = json.loads(canonical_json(record))
        broken["absences"].pop(absence)
        with pytest.raises(SuccessorError):
            validate_result(broken)
    smuggled = json.loads(canonical_json(record))
    smuggled["source_faithful"] = {"rows": []}
    with pytest.raises(SuccessorError):
        validate_result(smuggled)


def test_incomplete_chain_cannot_be_published(tmp_path: Path) -> None:
    _, _, _, store, completed = _completed(tmp_path)
    first_new = store.binding.first_new_ordinal
    for rows in (completed.rows[:-1], completed.rows[:first_new]):
        with pytest.raises(SuccessorError):
            assemble_synthetic_result(SuccessorCheckpoint(store.binding, rows), store)


def test_tampered_carried_row_is_refused(tmp_path: Path) -> None:
    _, _, _, store, _ = _completed(tmp_path)
    raw = json.loads(store.checkpoint_path.read_text(encoding="utf-8"))
    raw["rows"][0]["row_hash"] = "0" * 64
    store.checkpoint_path.write_text(canonical_json(raw) + "\n", encoding="utf-8")
    with pytest.raises(SuccessorError):
        store.load()


def test_result_overwrite_is_refused(tmp_path: Path) -> None:
    _, _, _, store, completed = _completed(tmp_path)
    record = _as_json(assemble_synthetic_result(completed, store))
    store.result_path.write_text(canonical_json(record) + "\n", encoding="utf-8")
    with pytest.raises(SuccessorError):
        store.refuse_existing_result()
    with pytest.raises(SuccessorError):
        store.load()


def test_interrupted_then_resumed_matches_uninterrupted(tmp_path: Path) -> None:
    receipt, _, _, _, uninterrupted = _completed(tmp_path, "control")
    interrupted = synthetic_successor_store(tmp_path, "interrupted", receipt)
    atoms, _, outer_side, square_side = synthetic_inputs()

    def stop_once(*_args: object) -> object:
        raise RuntimeError("synthetic interruption")

    with pytest.raises(RuntimeError):
        SuccessorChainDriver(
            interrupted,
            independent_accumulator=stop_once,  # pyright: ignore[reportArgumentType]
        ).run(atoms=atoms, outer_side=outer_side, square_side=square_side)
    assert len(interrupted.load().rows) == interrupted.binding.first_new_ordinal
    assert interrupted.progress_path.is_file()

    resumed = SuccessorChainDriver(interrupted).run(
        atoms=atoms, outer_side=outer_side, square_side=square_side
    )
    assert canonical_json(resumed.rows) == canonical_json(uninterrupted.rows)


def test_status_reports_both_ancestries(tmp_path: Path) -> None:
    _, _, _, store, completed = _completed(tmp_path)
    status = _as_json(chain_status(store.checkpoint_path))
    assert status["complete"] is True
    assert status["all_agree"] is True
    assert status["row_count"] == len(completed.rows)
    assert status["last_row_hash"] == completed.rows[-1].row_hash
    assert status["immediate_parent_experiment_id"] != status["chain_genesis_experiment_id"]


def test_production_expectations_are_the_registered_values() -> None:
    assert PRODUCTION_EXPECTATIONS.atom_count == 168
    assert PRODUCTION_EXPECTATIONS.direction_count == 181
    assert PRODUCTION_EXPECTATIONS.total_weight == Fraction(9744, 576)
    assert PRODUCTION_EXPECTATIONS.global_minimum == Fraction(576, 576)


@pytest.mark.slow
def test_real_ancestry_verifies_without_evaluating_a_direction() -> None:
    report = _as_json(ancestry_report())
    assert report["target_directions_evaluated"] == 0
    assert report["carried_row_count"] == IMMEDIATE_PARENT_ROW_COUNT
    assert report["first_new_ordinal"] == IMMEDIATE_PARENT_ROW_COUNT
    assert report["direction_count"] == 181
    parent = report["immediate_parent"]
    genesis = report["chain_genesis"]
    assert parent["experiment_id"] == "exp-056"
    assert genesis["experiment_id"] == "exp-052"
    assert parent["last_row_hash"] == IMMEDIATE_PARENT_LAST_ROW_HASH
    assert parent["resume_ordinal"] == 170
    assert parent["resume_stage"] == "independent_started"
    assert report["roles_distinct"] is True
    assert report["genesis_is_prefix_of_immediate_parent"] is True


def test_selftest_runs_every_named_guard_without_asserts() -> None:
    receipt = run_selftest()
    if receipt.get("passed") is not True or receipt.get("skipped") != 0:
        raise AssertionError("successor selftest did not report an unqualified pass")
    guards = receipt.get("receipts")
    if not isinstance(guards, dict) or len(guards) < 100 or not all(guards.values()):
        raise AssertionError("successor selftest guard inventory is incomplete")
    for named in (
        "changed-retained-row-refusal",
        "swapped-ancestry-refusal-identities",
        "noncanonical-checkpoint-refusal",
        "wrong-progress-binding-refusal",
        "wrong-previous-row-hash-refusal",
        "wrong-ordinal-refusal",
        "ancestry-wrong-stage-refusal",
        "missing-summary-refusal",
        "wrong-global-minimum-refusal",
        "false-precondition-refusal",
        "surviving-mutation-refusal",
        "result-overwrite-refusal",
        "lexical-escape-refusal",
        "exp-056-path-refusal",
        "incomplete-chain-refusal",
        "disagreement-stop",
        "interrupted-resume-equivalence",
    ):
        if guards.get(named) is not True:
            raise AssertionError(f"missing named guard {named}")


def test_selftest_receipt_is_identical_under_optimized_python() -> None:
    command = [
        sys.executable,
        "-m",
        "cases.n17_weighted_certificate_successor.run",
        "--selftest",
    ]
    normal = subprocess.run(command, capture_output=True, check=True, text=True)
    optimized = subprocess.run(
        [sys.executable, "-O", *command[1:]], capture_output=True, check=True, text=True
    )
    if normal.stdout != optimized.stdout:
        raise AssertionError("normal and optimized selftest receipts differ")
