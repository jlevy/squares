"""Atomic, hash-bound exp-050 source-semantics application runner."""

from __future__ import annotations

import hashlib
import json
import os
import tempfile
from pathlib import Path
from typing import Any

from cases.n050_exact.source_semantics import evaluate_receipt, load_receipt

RESULT_PATH = Path(
    "campaign/series/series-000-smoke-and-calibration/results/"
    "exp-050-h-054-n50-source-semantics-e1-localization.json"
)
INPUT_PATHS = {
    "w1_source_fixture": Path("cases/n050_exact/w1_source_fixture.json"),
    "source_semantics_intake": Path("cases/n050_exact/source_semantics.py"),
    "focused_test": Path("tests/test_n050_exact.py"),
    "n19_control_receipt": Path("cases/n050_exact/n19_control_receipt.json"),
}
EXPECTED_INPUT_HASHES = {
    "w1_source_fixture": ("113a6b3c82f343f62a7b07e67777dd11d6fa30994576f227d86ea45f2f936c26"),
    "source_semantics_intake": (
        "fed71cf825906bd09f3711ec0a465dce0e4aecb91a1128f3a9d792e59c7c8d0c"
    ),
    "focused_test": ("0bcbd7e6154dca5b688cb6baf5098d37b9eb938dc227d04e81e3e76329ca2707"),
    "n19_control_receipt": ("accd0d9ce40c6e06c959804d4455dffb21b6a7062276391ddb9421ac805daaae"),
}


class SourceApplicationError(RuntimeError):
    """A frozen binding, expected outcome, or publication guard failed."""


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def observed_bindings(root: Path) -> dict[str, str]:
    """Hash exactly the four preregistered, target-blind inputs."""

    return {name: _sha256(root / path) for name, path in INPUT_PATHS.items()}


def build_result(
    receipt: dict[str, Any], bindings: dict[str, str], n19_receipt: dict[str, Any]
) -> dict[str, object]:
    """Evaluate the structured receipt and require the sole admissible outcome."""

    decision = evaluate_receipt(receipt)
    if decision.accepted or decision.reason != "attribution-unbound" or decision.cells:
        raise SourceApplicationError(
            "frozen W1 fixture did not produce E1 reason 3 with zero cells"
        )
    if (
        n19_receipt.get("skip_count") != 0
        or n19_receipt.get("verification", {}).get("valid") is not True
        or n19_receipt.get("mutation", {}).get("observed_valid") is not False
    ):
        raise SourceApplicationError("bound n = 19 control receipt is not admissible")
    return {
        "experiment_id": "exp-050",
        "hypothesis_id": "H-054",
        "executed": True,
        "outcome": "e1-refusal",
        "reason_index": 3,
        "reason": "attribution-unbound",
        "cells": [],
        "cell_count": 0,
        "needs_review": True,
        "bindings": {
            name: {"path": str(INPUT_PATHS[name]), "sha256": digest}
            for name, digest in bindings.items()
        },
        "n19_control": {
            "build_call": n19_receipt.get("build_call"),
            "observed_side": n19_receipt.get("observed_side"),
            "observed_pairs": n19_receipt.get("verification", {}).get("observed_pairs"),
            "mutation_observed_valid": n19_receipt.get("mutation", {}).get("observed_valid"),
            "skip_count": n19_receipt.get("skip_count"),
        },
        "claim_boundary": (
            "Executed source-semantics localization only: the checked hash-bound "
            "surfaces do not bind source-author and file-publisher roles. This is not "
            "an n = 50 geometry, feasibility, exactness, optimality, frontier, or "
            "H-054 verdict; H-054 remains instrument_ready false."
        ),
        "retention": "sanitized-structured-source-seam-only",
    }


def canonical_result_bytes(result: dict[str, object]) -> bytes:
    """Encode the immutable result deterministically."""

    return (json.dumps(result, indent=2, sort_keys=True) + "\n").encode()


def atomic_publish_new(path: Path, content: bytes) -> None:
    """Flush and atomically publish a new file without replacing any result."""

    if path.exists():
        raise SourceApplicationError(f"result already exists: {path}")
    if not path.parent.is_dir():
        raise SourceApplicationError(f"result parent does not exist: {path.parent}")
    descriptor, temporary_name = tempfile.mkstemp(
        dir=path.parent, prefix=f".{path.name}.", suffix=".tmp"
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        try:
            os.link(temporary, path)
        except FileExistsError as error:
            raise SourceApplicationError(f"result already exists: {path}") from error
        directory = os.open(path.parent, os.O_RDONLY)
        try:
            os.fsync(directory)
        finally:
            os.close(directory)
    finally:
        temporary.unlink(missing_ok=True)


def run_exp050(record: Path, *, root: Path = Path()) -> dict[str, object]:
    """Run exp-050 once from its fixed structured fixture and publish its result."""

    if record != RESULT_PATH:
        raise SourceApplicationError(f"result path must be exactly {RESULT_PATH}")
    target = root / record
    if target.exists():
        raise SourceApplicationError(f"result already exists: {target}")
    bindings = observed_bindings(root)
    if bindings != EXPECTED_INPUT_HASHES:
        raise SourceApplicationError("one or more frozen input hashes changed")
    fixture = load_receipt(root / INPUT_PATHS["w1_source_fixture"])
    n19_receipt = load_receipt(root / INPUT_PATHS["n19_control_receipt"])
    result = build_result(fixture, bindings, n19_receipt)
    atomic_publish_new(target, canonical_result_bytes(result))
    return result
