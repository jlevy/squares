"""Independent result-verifier controls for H-059."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

import pytest

from cases.n050_producer_refusal.verify import (
    IMMUTABLE_RESULT_PATH,
    VerificationError,
    canonical_bytes,
    verify_result,
)

PACKING = Path(__file__).resolve().parents[1]


@pytest.fixture
def prospective_result(tmp_path: Path) -> Path:
    completed = subprocess.run(
        [sys.executable, "-m", "cases.n050_producer_refusal.run", "--selftest"],
        cwd=PACKING,
        capture_output=True,
        check=False,
    )
    assert completed.returncode == 0, completed.stderr.decode()
    path = tmp_path / "result.json"
    path.write_bytes(completed.stdout)
    return path


def _mutate(path: Path, mutation: str) -> None:
    document: dict[str, Any] = json.loads(path.read_bytes())
    if mutation == "producer-binding":
        document["conditions"]["observation"]["producer"]["sha256"] = "0" * 64
    elif mutation == "nonzero-stage":
        document["conditions"]["observation"]["stage_trace"]["counts"][
            "fixture_loading"
        ] = 1
    elif mutation == "review-cleared":
        document["needs_review"] = False
    elif mutation == "missing-overwrite":
        del document["mutations"]["overwrite"]
    elif mutation == "instrument-binding":
        first = next(iter(document["instrument_bindings"]))
        document["instrument_bindings"][first] = "0" * 64
    else:
        raise AssertionError(f"unknown mutation: {mutation}")
    path.write_bytes(canonical_bytes(document))


def test_independent_verifier_imports_no_harness_or_producer() -> None:
    script = (
        "import sys; import cases.n050_producer_refusal.verify; "
        "blocked = {'cases.n050_producer_refusal.harness', "
        "'cases.n050_producer_refusal.run', "
        "'_bc125_frozen_source_semantics_runner'}; "
        "raise SystemExit(1 if blocked & sys.modules.keys() else 0)"
    )
    completed = subprocess.run(
        [sys.executable, "-c", script], cwd=PACKING, capture_output=True, check=False
    )
    assert completed.returncode == 0, completed.stderr.decode()


def test_independent_verifier_accepts_prospective_receipt(
    prospective_result: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.chdir(PACKING)
    frozen = PACKING / IMMUTABLE_RESULT_PATH
    before = hashlib.sha256(frozen.read_bytes()).hexdigest()

    receipt = verify_result(prospective_result)

    assert receipt["verified"] is True
    assert receipt["needs_review"] is True
    assert hashlib.sha256(frozen.read_bytes()).hexdigest() == before


def test_independent_verifier_is_normal_optimized_equivalent(
    prospective_result: Path,
) -> None:
    base = ["-m", "cases.n050_producer_refusal.verify", str(prospective_result)]
    normal = subprocess.run(
        [sys.executable, *base], cwd=PACKING, capture_output=True, check=False
    )
    optimized = subprocess.run(
        [sys.executable, "-O", *base], cwd=PACKING, capture_output=True, check=False
    )
    assert normal.returncode == 0, normal.stderr.decode()
    assert optimized.returncode == 0, optimized.stderr.decode()
    assert normal.stdout == optimized.stdout


@pytest.mark.parametrize(
    "mutation",
    (
        "producer-binding",
        "nonzero-stage",
        "review-cleared",
        "missing-overwrite",
        "instrument-binding",
    ),
)
def test_independent_verifier_rejects_named_mutations(
    prospective_result: Path,
    mutation: str,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.chdir(PACKING)
    _mutate(prospective_result, mutation)
    with pytest.raises(VerificationError):
        verify_result(prospective_result)
