"""Target-blind controls for the parent-bound exp-056 child chain."""

from __future__ import annotations

import json
import subprocess
import sys
from dataclasses import replace
from fractions import Fraction
from pathlib import Path

import pytest

from cases.n17_weighted_certificate.fixture import RETAINED_SHA256
from cases.n17_weighted_certificate.model import Atom, Direction, canonical_json
from cases.n17_weighted_certificate.target_independent import (
    accumulate_target_independent,
)
from cases.n17_weighted_certificate_child.run import (
    OUTPUT_ROOT,
    ChildChainDriver,
    ChildCheckpoint,
    ChildCheckpointStore,
    ChildError,
    DisagreementStopError,
    chain_status,
    child_result,
    require_writable,
    run_selftest,
    synthetic_child_store,
)

PARENT_CHECKPOINT_NAME = "exp-052-h-052-n17-resumable-certificate-agreement.checkpoint.json"


def _run(tmp_path: Path, name: str = "case") -> tuple[ChildCheckpointStore, ChildCheckpoint]:
    store, atoms, outer_side, square_side = synthetic_child_store(tmp_path, name)
    completed = ChildChainDriver(store).run(
        atoms=atoms, outer_side=outer_side, square_side=square_side
    )
    return store, completed


def test_child_chain_continues_the_parent_prefix(tmp_path: Path) -> None:
    store, completed = _run(tmp_path)
    parent_rows = store.binding.parent_row_count
    assert len(completed.rows) == len(store.directions)
    assert completed.rows[:parent_rows] == store.parent_rows
    assert completed.rows[parent_rows].previous_row_hash == store.binding.parent_last_row_hash
    assert all(row.agreement for row in completed.rows)
    assert not store.progress_path.exists()


def test_tampered_row_is_rejected(tmp_path: Path) -> None:
    store, _ = _run(tmp_path)
    raw = json.loads(store.checkpoint_path.read_text(encoding="utf-8"))
    raw["rows"][-1]["source"]["minimum"] = "999/1"
    store.checkpoint_path.write_text(canonical_json(raw) + "\n", encoding="utf-8")

    with pytest.raises(ChildError):
        store.load()


def test_tampered_carried_parent_row_is_rejected(tmp_path: Path) -> None:
    store, _ = _run(tmp_path)
    raw = json.loads(store.checkpoint_path.read_text(encoding="utf-8"))
    raw["rows"][0]["row_hash"] = "0" * 64
    store.checkpoint_path.write_text(canonical_json(raw) + "\n", encoding="utf-8")

    with pytest.raises(ChildError):
        store.load()


def test_parent_path_write_is_refused(tmp_path: Path) -> None:
    store, _ = _run(tmp_path)
    for candidate in (
        OUTPUT_ROOT / PARENT_CHECKPOINT_NAME,
        Path("cases/n17_weighted_certificate_resume/run.py"),
        store.output_root / ".." / "escaped.json",
        tmp_path / "outside.json",
    ):
        with pytest.raises(ChildError):
            require_writable(candidate, store.output_root, "checkpoint path")


def test_interrupted_then_resumed_matches_uninterrupted(tmp_path: Path) -> None:
    store, atoms, outer_side, square_side = synthetic_child_store(tmp_path, "control")
    uninterrupted = ChildChainDriver(store).run(
        atoms=atoms, outer_side=outer_side, square_side=square_side
    )
    interrupted, _, _, _ = synthetic_child_store(tmp_path, "interrupted", spec=None)

    calls = 0

    def stop_once(*args: object) -> object:
        nonlocal calls
        calls += 1
        if calls == 1:
            raise RuntimeError("synthetic interruption")
        return accumulate_target_independent(*args)  # pyright: ignore[reportArgumentType]

    with pytest.raises(RuntimeError):
        ChildChainDriver(
            interrupted,
            independent_accumulator=stop_once,  # pyright: ignore[reportArgumentType]
        ).run(atoms=atoms, outer_side=outer_side, square_side=square_side)
    assert len(interrupted.load().rows) == interrupted.binding.parent_row_count
    assert interrupted.progress_path.is_file()

    resumed = ChildChainDriver(interrupted).run(
        atoms=atoms, outer_side=outer_side, square_side=square_side
    )
    payload = [
        (row.ordinal, row.direction, row.source, row.independent, row.agreement)
        for row in resumed.rows
    ]
    control = [
        (row.ordinal, row.direction, row.source, row.independent, row.agreement)
        for row in uninterrupted.rows
    ]
    assert canonical_json(payload) == canonical_json(control)


def test_result_overwrite_is_refused(tmp_path: Path) -> None:
    store, completed = _run(tmp_path)
    result = child_result(completed, retained_sha256=RETAINED_SHA256)
    store.result_path.write_text(canonical_json(result) + "\n", encoding="utf-8")

    with pytest.raises(ChildError):
        store.refuse_existing_result()
    with pytest.raises(ChildError):
        store.load()


def test_incomplete_chain_cannot_be_published(tmp_path: Path) -> None:
    store, completed = _run(tmp_path)
    with pytest.raises(ChildError):
        child_result(
            ChildCheckpoint(store.binding, completed.rows[:-1]),
            retained_sha256=RETAINED_SHA256,
        )


def test_disagreement_stops_and_is_retained(tmp_path: Path) -> None:
    store, atoms, outer_side, square_side = synthetic_child_store(tmp_path, "disagree")

    def perturbed(
        call_atoms: tuple[Atom, ...],
        direction: Direction,
        call_outer: Fraction,
        call_square: Fraction,
    ) -> object:
        manifest = accumulate_target_independent(call_atoms, direction, call_outer, call_square)
        return replace(manifest, minimum=manifest.minimum + 1)

    with pytest.raises(DisagreementStopError):
        ChildChainDriver(
            store,
            independent_accumulator=perturbed,  # pyright: ignore[reportArgumentType]
        ).run(atoms=atoms, outer_side=outer_side, square_side=square_side)

    retained = store.load()
    assert len(retained.rows) == store.binding.parent_row_count + 1
    assert retained.rows[-1].agreement is False
    status = chain_status(store.checkpoint_path)
    assert status["first_disagreement_ordinal"] == store.binding.parent_row_count
    assert status["all_agree"] is False


def test_status_reports_the_observable_chain_state(tmp_path: Path) -> None:
    store, completed = _run(tmp_path)
    status = chain_status(store.checkpoint_path)
    assert status["row_count"] == len(completed.rows)
    assert status["last_ordinal"] == completed.rows[-1].ordinal
    assert status["last_row_hash"] == completed.rows[-1].row_hash
    assert status["all_agree"] is True
    assert status["complete"] is True
    assert status["chain_verified"] is True


def test_selftest_runs_every_named_guard_without_asserts() -> None:
    receipt = run_selftest()
    if receipt.get("passed") is not True or receipt.get("skipped") != 0:
        raise AssertionError("child selftest did not report an unqualified pass")
    guards = receipt.get("receipts")
    if not isinstance(guards, dict) or len(guards) < 30 or not all(guards.values()):
        raise AssertionError("child selftest guard inventory is incomplete")
    for named in (
        "tampered-child-row-payload",
        "parent-path-write-refusal",
        "interrupted-resume-equivalence",
        "result-overwrite-refusal",
        "disagreement-retained-as-row",
        "child-chain-continuity",
    ):
        if guards.get(named) is not True:
            raise AssertionError(f"missing named guard {named}")


def test_selftest_receipt_is_identical_under_optimized_python() -> None:
    command = [sys.executable, "-m", "cases.n17_weighted_certificate_child.run", "--selftest"]
    normal = subprocess.run(command, capture_output=True, check=True, text=True)
    optimized = subprocess.run(
        [sys.executable, "-O", *command[1:]], capture_output=True, check=True, text=True
    )
    if normal.stdout != optimized.stdout:
        raise AssertionError("normal and optimized selftest receipts differ")
