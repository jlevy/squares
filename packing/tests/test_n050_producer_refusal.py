"""Target-blind controls for the H-059 producer-refusal harness."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

import pytest

from cases.n050_producer_refusal.harness import (
    EXPECTED_REFUSAL,
    EXPECTED_RESULT_SHA256,
    EXPECTED_RUNNER_SHA256,
    RESULT_PATH,
    STAGES,
    calibrate_stage,
    canonical_bytes,
    observe,
    probe_reordered_stage,
)
from cases.n050_producer_refusal.run import (
    ControlError,
    atomic_publish_new,
    run_conditions,
    run_mutation_matrix,
)

PACKING = Path(__file__).resolve().parents[1]


@pytest.mark.parametrize("stage", STAGES)
def test_each_sentinel_calibrates_once_in_an_isolated_process(stage: str) -> None:
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "cases.n050_producer_refusal.harness",
            "--calibrate-stage",
            stage,
        ],
        cwd=PACKING,
        capture_output=True,
        check=False,
    )
    assert completed.returncode == 0, completed.stderr.decode()
    receipt = json.loads(completed.stdout)
    assert receipt == calibrate_stage(stage)
    assert receipt["counts"][stage] == 1
    assert sum(receipt["counts"].values()) == 1


@pytest.mark.parametrize("stage", STAGES)
def test_each_reordered_stage_mutation_is_rejected_in_an_isolated_process(
    stage: str,
) -> None:
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "cases.n050_producer_refusal.harness",
            "--probe-reordered-stage",
            stage,
        ],
        cwd=PACKING,
        capture_output=True,
        check=False,
    )
    assert completed.returncode == 0, completed.stderr.decode()
    receipt = json.loads(completed.stdout)
    assert receipt == probe_reordered_stage(stage)
    assert receipt["rejected"] is True
    assert receipt["counts"][stage] == 1
    assert sum(receipt["counts"].values()) == 1


def test_frozen_producer_refuses_with_canonical_zero_call_trace(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.chdir(PACKING)
    result = PACKING / RESULT_PATH
    before = hashlib.sha256(result.read_bytes()).hexdigest()

    receipt = observe()

    assert receipt["producer"]["sha256"] == EXPECTED_RUNNER_SHA256
    assert receipt["fake_intake_injected_before_import"] is True
    assert receipt["immutable_result"]["sha256_before"] == EXPECTED_RESULT_SHA256
    assert receipt["immutable_result"]["sha256_after"] == EXPECTED_RESULT_SHA256
    assert receipt["refusal"] == {
        "type": "SourceApplicationError",
        "text": EXPECTED_REFUSAL,
    }
    assert receipt["stage_trace"] == {
        "schema": "packing.squares:n050-producer-stage-trace/v1",
        "calls": [],
        "counts": dict.fromkeys(STAGES, 0),
    }
    assert canonical_bytes(receipt).endswith(b"\n")
    assert hashlib.sha256(result.read_bytes()).hexdigest() == before


def test_normal_and_optimized_receipts_are_byte_identical(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.chdir(PACKING)
    conditions = run_conditions()

    assert conditions["stdout_byte_identical"] is True
    assert conditions["normal_stdout_sha256"] == conditions["optimized_stdout_sha256"]
    assert set(conditions["calibrations"]) == set(STAGES)


def test_full_controller_is_normal_optimized_equivalent() -> None:
    base = ["-m", "cases.n050_producer_refusal.run", "--selftest"]
    normal = subprocess.run(
        [sys.executable, *base], cwd=PACKING, capture_output=True, check=False
    )
    optimized = subprocess.run(
        [sys.executable, "-O", *base], cwd=PACKING, capture_output=True, check=False
    )
    assert normal.returncode == 0, normal.stderr.decode()
    assert optimized.returncode == 0, optimized.stderr.decode()
    assert normal.stdout == optimized.stdout


def test_registered_mutation_matrix_rejects(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(PACKING)
    receipt = observe()
    mutations = run_mutation_matrix(receipt)

    assert mutations["changed_runner"]["rejected"] is True
    assert mutations["changed_result"]["rejected"] is True
    assert mutations["overwrite"]["rejected"] is True
    assert mutations["changed_refusal_text"]["rejected"] is True
    assert all(item["rejected"] is True for item in mutations["reordered_stage"].values())
    assert all(item["rejected"] is True for item in mutations["missing_sentinel"].values())


def test_successor_publisher_refuses_overwrite(tmp_path: Path) -> None:
    target = tmp_path / "result.json"
    atomic_publish_new(target, b"one\n")
    with pytest.raises(ControlError, match="already exists"):
        atomic_publish_new(target, b"two\n")
    assert target.read_bytes() == b"one\n"
