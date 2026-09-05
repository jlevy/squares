"""Run the H-059 normal/optimized control and publish one fresh receipt."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
import tempfile
from collections.abc import Collection, Sequence
from copy import deepcopy
from pathlib import Path
from shutil import copyfile
from typing import Any

from cases.n050_producer_refusal.harness import (
    EXPECTED_REFUSAL,
    EXPECTED_RESULT_SHA256,
    EXPECTED_RUNNER_SHA256,
    RESULT_PATH,
    RUNNER_PATH,
    STAGES,
    AdmissionError,
    bind_frozen_inputs,
    canonical_bytes,
)

LAUNCH_REVISION = "909efafa0773fbea23b24de072ef59a03a01317a"
SCIENTIFIC_REVISION = "81177148e404aa283c2a6ec7d696f2b39a9e361c"
FRESH_RESULT_PATH = Path(
    "campaign/series/series-000-smoke-and-calibration/results/"
    "exp-055-h-059-n50-producer-refusal-ordering.json"
)
HARNESS_MODULE = "cases.n050_producer_refusal.harness"
INSTRUMENT_PATHS = (
    Path("cases/n050_producer_refusal/__init__.py"),
    Path("cases/n050_producer_refusal/harness.py"),
    Path("cases/n050_producer_refusal/run.py"),
    Path("cases/n050_producer_refusal/verify.py"),
    Path("tests/test_n050_producer_refusal.py"),
    Path("tests/test_n050_producer_refusal_independent.py"),
)


class ControlError(RuntimeError):
    """A condition, mutation, binding, or publication guard failed."""


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _strict_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ControlError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def strict_json(value: bytes) -> dict[str, Any]:
    """Read canonical JSON output while rejecting duplicate keys and non-finite values."""

    try:
        document = json.loads(
            value,
            object_pairs_hook=_strict_object,
            parse_constant=lambda token: (_ for _ in ()).throw(
                ControlError(f"non-finite JSON number: {token}")
            ),
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ControlError("harness output is not strict JSON") from error
    if not isinstance(document, dict) or canonical_bytes(document) != value:
        raise ControlError("harness output is not canonical JSON")
    return document


def _subprocess(args: list[str], *, optimized: bool = False) -> bytes:
    command = [sys.executable]
    if optimized:
        command.append("-O")
    command.extend(["-m", HARNESS_MODULE, *args])
    completed = subprocess.run(command, capture_output=True, check=False)
    if completed.returncode != 0:
        message = completed.stderr.decode(errors="replace").strip()
        raise ControlError(f"harness subprocess failed: {message}")
    return completed.stdout


def validate_observation(document: dict[str, Any]) -> None:
    """Apply the frozen H-059 criterion to one observation receipt."""

    expected_counts = dict.fromkeys(STAGES, 0)
    if document.get("schema") != "packing.squares:n050-producer-observation/v1":
        raise ControlError("observation schema changed")
    if document.get("fake_intake_injected_before_import") is not True:
        raise ControlError("fake intake was not injected before producer import")
    if document.get("producer") != {
        "path": str(RUNNER_PATH),
        "sha256": EXPECTED_RUNNER_SHA256,
    }:
        raise ControlError("producer binding changed")
    if document.get("immutable_result") != {
        "path": str(RESULT_PATH),
        "sha256_before": EXPECTED_RESULT_SHA256,
        "sha256_after": EXPECTED_RESULT_SHA256,
    }:
        raise ControlError("immutable result binding changed")
    if document.get("refusal") != {
        "type": "SourceApplicationError",
        "text": EXPECTED_REFUSAL,
    }:
        raise ControlError("existing-result refusal changed")
    if document.get("stage_trace") != {
        "schema": "packing.squares:n050-producer-stage-trace/v1",
        "calls": [],
        "counts": expected_counts,
    }:
        raise ControlError("downstream stage trace is not the canonical zero-call trace")


def run_conditions() -> dict[str, Any]:
    """Calibrate four isolated sentinels, then compare normal and optimized receipts."""

    calibrations: dict[str, dict[str, Any]] = {}
    for stage in STAGES:
        calibration = strict_json(_subprocess(["--calibrate-stage", stage]))
        if calibration.get("stage") != stage:
            raise ControlError(f"wrong calibration stage: {stage}")
        counts = calibration.get("counts")
        if not isinstance(counts, dict) or counts.get(stage) != 1 or sum(counts.values()) != 1:
            raise ControlError(f"sentinel did not fire exactly once: {stage}")
        calibrations[stage] = calibration

    normal = _subprocess(["--observe"])
    optimized = _subprocess(["--observe"], optimized=True)
    if normal != optimized:
        raise ControlError("normal and optimized observation bytes differ")
    observation = strict_json(normal)
    validate_observation(observation)
    return {
        "calibrations": calibrations,
        "normal_stdout_sha256": sha256_bytes(normal),
        "optimized_stdout_sha256": sha256_bytes(optimized),
        "stdout_byte_identical": True,
        "observation": observation,
    }


def _must_reject_observation(document: dict[str, Any], label: str) -> dict[str, object]:
    try:
        validate_observation(document)
    except ControlError as error:
        return {"rejected": True, "reason": str(error)}
    raise ControlError(f"mutation survived: {label}")


def _validate_sentinel_inventory(inventory: Collection[str]) -> None:
    if inventory != set(STAGES):
        missing = sorted(set(STAGES) - set(inventory))
        raise ControlError(f"missing sentinel: {','.join(missing)}")


def _mutated_binding(
    *, mutate: Path, expected_reason: str
) -> dict[str, object]:
    with tempfile.TemporaryDirectory(prefix="bc125-binding-") as directory:
        root = Path(directory)
        runner = root / RUNNER_PATH
        result = root / RESULT_PATH
        runner.parent.mkdir(parents=True)
        result.parent.mkdir(parents=True)
        copyfile(RUNNER_PATH, runner)
        copyfile(RESULT_PATH, result)
        target = root / mutate
        target.write_bytes(target.read_bytes() + b"\n")
        observed_hash = sha256_bytes(target.read_bytes())
        try:
            bind_frozen_inputs(root=root)
        except AdmissionError as error:
            if str(error) != expected_reason:
                raise ControlError("binding mutation emitted the wrong refusal") from error
            return {
                "rejected": True,
                "observed_sha256": observed_hash,
                "reason": str(error),
            }
    raise ControlError(f"binding mutation survived: {mutate}")


def _overwrite_mutation() -> dict[str, object]:
    with tempfile.TemporaryDirectory(prefix="bc125-overwrite-") as directory:
        target = Path(directory) / "result.json"
        target.write_bytes(b"frozen\n")
        before = sha256_bytes(target.read_bytes())
        try:
            atomic_publish_new(target, b"replacement\n")
        except ControlError as error:
            after = sha256_bytes(target.read_bytes())
            if before != after:
                raise ControlError("overwrite mutation changed existing bytes") from error
            if str(error) != f"result already exists: {target}":
                raise ControlError("overwrite mutation emitted the wrong refusal") from error
            return {
                "rejected": True,
                "reason": "result already exists: fresh successor result",
                "sha256_before": before,
                "sha256_after": after,
            }
    raise ControlError("overwrite mutation survived")


def run_mutation_matrix(observation: dict[str, Any]) -> dict[str, Any]:
    """Fire every preregistered target-blind H-059 mutation."""

    changed_runner = _mutated_binding(
        mutate=RUNNER_PATH,
        expected_reason="producer runner SHA-256 changed before import",
    )
    changed_result = _mutated_binding(
        mutate=RESULT_PATH,
        expected_reason="immutable exp-050 result SHA-256 changed before import",
    )

    reordered: dict[str, dict[str, object]] = {}
    for stage in STAGES:
        probe = strict_json(_subprocess(["--probe-reordered-stage", stage]))
        if probe.get("counts", {}).get(stage) != 1 or probe.get("rejected") is not True:
            raise ControlError(f"reordered-stage mutation escaped: {stage}")
        reordered[stage] = {
            "rejected": True,
            "reason": f"forbidden stage reached: {stage}",
            "counts": probe["counts"],
        }

    missing: dict[str, dict[str, object]] = {}
    for stage in STAGES:
        observed_inventory = set(STAGES) - {stage}
        try:
            _validate_sentinel_inventory(observed_inventory)
        except ControlError as error:
            missing[stage] = {"rejected": True, "reason": str(error)}
        else:
            raise ControlError(f"missing-sentinel mutation escaped: {stage}")

    wrong_refusal = deepcopy(observation)
    wrong_refusal["refusal"]["text"] = "result already exists after evaluation"

    return {
        "changed_runner": changed_runner,
        "changed_result": changed_result,
        "reordered_stage": reordered,
        "missing_sentinel": missing,
        "overwrite": _overwrite_mutation(),
        "changed_refusal_text": _must_reject_observation(wrong_refusal, "changed refusal"),
    }


def atomic_publish_new(path: Path, content: bytes) -> None:
    """Publish one fresh successor result without replacing an existing path."""

    if path.exists():
        raise ControlError(f"result already exists: {path}")
    if not path.parent.is_dir():
        raise ControlError(f"result parent does not exist: {path.parent}")
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
            raise ControlError(f"result already exists: {path}") from error
        directory = os.open(path.parent, os.O_RDONLY)
        try:
            os.fsync(directory)
        finally:
            os.close(directory)
    finally:
        temporary.unlink(missing_ok=True)


def build_result() -> dict[str, Any]:
    conditions = run_conditions()
    observation = conditions["observation"]
    mutations = run_mutation_matrix(observation)
    result_hash_after = hashlib.sha256(Path(RESULT_PATH).read_bytes()).hexdigest()
    if result_hash_after != EXPECTED_RESULT_SHA256:
        raise ControlError("immutable exp-050 result changed before publication")
    return {
        "schema": "packing.squares:n050-producer-refusal-result/v1",
        "experiment_id": "exp-055",
        "hypothesis_id": "H-059",
        "launch_revision": LAUNCH_REVISION,
        "scientific_revision": SCIENTIFIC_REVISION,
        "instrument_bindings": {
            str(path): sha256_bytes(path.read_bytes()) for path in INSTRUMENT_PATHS
        },
        "needs_review": True,
        "outcome": "criterion-met",
        "conditions": conditions,
        "mutations": mutations,
        "immutable_result_sha256_after": result_hash_after,
        "claim_boundary": (
            "Prospective producer-refusal protocol only; this does not repair exp-050, "
            "change H-054, establish n = 50 feasibility or authorize source or geometry work."
        ),
    }


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--selftest", action="store_true")
    group.add_argument("--record", type=Path)
    return parser


def _publish_registered_result(path: Path, result: dict[str, Any]) -> None:
    if path != FRESH_RESULT_PATH:
        raise ControlError(f"result path must be exactly {FRESH_RESULT_PATH}")
    atomic_publish_new(path, canonical_bytes(result))


def main(argv: Sequence[str] | None = None) -> int:
    arguments = _parser().parse_args(argv)
    try:
        result = build_result()
        if arguments.record is not None:
            _publish_registered_result(arguments.record, result)
    except (ControlError, OSError) as error:
        _parser().exit(1, f"control failed: {error}\n")
    sys.stdout.buffer.write(canonical_bytes(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
