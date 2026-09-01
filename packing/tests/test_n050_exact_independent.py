"""Independent replay tests for the immutable exp-050 refusal result."""

from __future__ import annotations

import copy
import hashlib
import subprocess
import sys
from pathlib import Path

import pytest

from cases.n050_exact.verify_source_semantics_result import (
    EXPECTED_RESULT_SHA256,
    RESULT_PATH,
    VerificationError,
    classify_source_receipt,
    load_json_strict,
    run_missing_semantics_control,
    verify_result,
)

PACKING = Path(__file__).resolve().parents[1]


def test_independent_replay_accepts_immutable_reason_three_result() -> None:
    replay = verify_result(PACKING / RESULT_PATH, root=PACKING)

    assert replay == {
        "result_sha256": EXPECTED_RESULT_SHA256,
        "reason": "attribution-unbound",
        "reason_index": 3,
        "cell_count": 0,
        "bound_artifact_count": 4,
        "n19_observed_pairs": 171,
        "skip_count": 0,
        "needs_review": True,
        "claim_boundary": "source-semantics-localization-only",
        "mutation_reason": "units-frame-or-rotation-undefined",
    }


def test_independent_missing_semantics_control_refuses_before_cells() -> None:
    reason, cells = run_missing_semantics_control()
    assert reason == "units-frame-or-rotation-undefined"
    assert cells == ()


def test_independent_reason_order_stops_at_unbound_attribution() -> None:
    receipt = load_json_strict(PACKING / "cases/n050_exact/w1_source_fixture.json")
    mutated = copy.deepcopy(receipt)
    mutated["semantics_context"] = None

    reason, cells = classify_source_receipt(mutated)

    assert reason == "attribution-unbound"
    assert cells == ()


def test_independent_replay_rejects_noncanonical_or_changed_result(
    tmp_path: Path,
) -> None:
    result = PACKING / RESULT_PATH
    changed = tmp_path / result.name
    changed.write_bytes(result.read_bytes() + b" ")

    with pytest.raises(VerificationError, match="result SHA-256"):
        verify_result(changed, root=PACKING)


def test_strict_loader_rejects_duplicate_json_keys(tmp_path: Path) -> None:
    duplicate = tmp_path / "duplicate.json"
    duplicate.write_text('{"cells":[],"cells":[]}\n', encoding="utf-8")

    with pytest.raises(VerificationError, match="duplicate JSON key"):
        load_json_strict(duplicate)


def test_registered_module_refuses_existing_result_before_republication() -> None:
    result = PACKING / RESULT_PATH
    before = hashlib.sha256(result.read_bytes()).hexdigest()
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "cases.n050_exact.source_semantics",
            "--record",
            str(RESULT_PATH),
        ],
        cwd=PACKING,
        capture_output=True,
        check=False,
        text=True,
    )

    assert completed.returncode != 0
    assert "result already exists" in completed.stderr
    assert hashlib.sha256(result.read_bytes()).hexdigest() == before
