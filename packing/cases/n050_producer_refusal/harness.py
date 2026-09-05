"""Inject live stage sentinels into the frozen exp-050 producer.

This module reads only the frozen producer and immutable exp-050 result.  It installs a
fake intake module before dynamically importing the producer, so neither the real intake
nor any source or geometry dependency can load.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import sys
from collections.abc import Callable
from pathlib import Path
from types import ModuleType
from typing import Any, Never

RUNNER_PATH = Path("cases/n050_exact/source_semantics_runner.py")
RESULT_PATH = Path(
    "campaign/series/series-000-smoke-and-calibration/results/"
    "exp-050-h-054-n50-source-semantics-e1-localization.json"
)
EXPECTED_RUNNER_SHA256 = "52baeb1b6ad52aa504498ba21aeb6b3d361aaaec2461c76904a357d8d95cf29d"
EXPECTED_RESULT_SHA256 = "ab00e50debe0bc60279ce3472ed0c09eb062e8271a481a38c6ac65036aff4a02"
EXPECTED_REFUSAL = f"result already exists: {RESULT_PATH}"
STAGES = (
    "binding_observation",
    "fixture_loading",
    "receipt_evaluation",
    "publication",
)
_INTAKE_MODULE = "cases.n050_exact.source_semantics"
_DYNAMIC_MODULE = "_bc125_frozen_source_semantics_runner"


class AdmissionError(RuntimeError):
    """The frozen binding, injection contract, or expected refusal failed."""


class StageSentinelError(RuntimeError):
    """A forbidden downstream producer stage ran before existing-result refusal."""

    def __init__(self, stage: str) -> None:
        super().__init__(f"forbidden stage reached: {stage}")
        self.stage = stage


def sha256_file(path: Path) -> str:
    """Return the SHA-256 identity of one frozen file."""

    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_bytes(value: object) -> bytes:
    """Encode one receipt without ambient ordering or whitespace choices."""

    return (json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n").encode()


def bind_frozen_inputs(*, root: Path) -> dict[str, str]:
    """Bind both frozen inputs before any producer import or evaluation."""

    runner_hash = sha256_file(root / RUNNER_PATH)
    if runner_hash != EXPECTED_RUNNER_SHA256:
        raise AdmissionError("producer runner SHA-256 changed before import")
    result_hash = sha256_file(root / RESULT_PATH)
    if result_hash != EXPECTED_RESULT_SHA256:
        raise AdmissionError("immutable exp-050 result SHA-256 changed before import")
    return {"producer": runner_hash, "immutable_result": result_hash}


def _empty_counts() -> dict[str, int]:
    return dict.fromkeys(STAGES, 0)


def _bomb(stage: str, counts: dict[str, int]) -> Callable[..., Never]:
    if stage not in STAGES:
        raise AdmissionError(f"unknown sentinel stage: {stage}")

    def fire(*_args: object, **_kwargs: object) -> Never:
        counts[stage] += 1
        raise StageSentinelError(stage)

    return fire


def calibrate_stage(stage: str) -> dict[str, Any]:
    """Fire one sentinel exactly once in this process."""

    counts = _empty_counts()
    observed: str | None = None
    try:
        _bomb(stage, counts)()
    except StageSentinelError as error:
        observed = error.stage
    if observed != stage or counts[stage] != 1 or sum(counts.values()) != 1:
        raise AdmissionError(f"sentinel calibration failed: {stage}")
    return {
        "schema": "packing.squares:n050-stage-calibration/v1",
        "stage": stage,
        "raised": f"forbidden stage reached: {stage}",
        "counts": counts,
    }


def probe_reordered_stage(stage: str) -> dict[str, Any]:
    """Model a downstream call moved before refusal and require its bomb to fire."""

    counts = _empty_counts()
    try:
        _bomb(stage, counts)()
    except StageSentinelError as error:
        if error.stage != stage or counts[stage] != 1 or sum(counts.values()) != 1:
            raise AdmissionError(f"reordered-stage probe misfired: {stage}") from error
        return {
            "schema": "packing.squares:n050-reordered-stage-rejection/v1",
            "stage": stage,
            "rejected": True,
            "reason": str(error),
            "counts": counts,
        }
    raise AdmissionError(f"reordered-stage probe escaped: {stage}")


def _fake_intake(counts: dict[str, int]) -> ModuleType:
    module = ModuleType(_INTAKE_MODULE)
    module.load_receipt = _bomb("fixture_loading", counts)  # type: ignore[attr-defined]
    module.evaluate_receipt = _bomb("receipt_evaluation", counts)  # type: ignore[attr-defined]
    return module


def _load_frozen_runner(root: Path, counts: dict[str, int]) -> ModuleType:
    """Load the hash-bound runner after installing the fake intake module."""

    if _INTAKE_MODULE in sys.modules:
        raise AdmissionError("real intake module was loaded before fake-module injection")
    if _DYNAMIC_MODULE in sys.modules:
        raise AdmissionError("dynamic producer module name is already occupied")

    runner_path = root / RUNNER_PATH
    observed_hash = sha256_file(runner_path)
    if observed_hash != EXPECTED_RUNNER_SHA256:
        raise AdmissionError("producer runner SHA-256 changed before import")

    fake_intake = _fake_intake(counts)
    sys.modules[_INTAKE_MODULE] = fake_intake
    try:
        spec = importlib.util.spec_from_file_location(_DYNAMIC_MODULE, runner_path)
        if spec is None or spec.loader is None:
            raise AdmissionError("cannot create the frozen producer import specification")
        module = importlib.util.module_from_spec(spec)
        sys.modules[_DYNAMIC_MODULE] = module
        spec.loader.exec_module(module)
        module.observed_bindings = _bomb(  # type: ignore[attr-defined]
            "binding_observation", counts
        )
        module.atomic_publish_new = _bomb("publication", counts)  # type: ignore[attr-defined]
        return module
    finally:
        sys.modules.pop(_INTAKE_MODULE, None)
        sys.modules.pop(_DYNAMIC_MODULE, None)


def observe(*, root: Path = Path()) -> dict[str, Any]:
    """Observe the frozen existing-result branch with every later stage bombed."""

    if root != Path():
        raise AdmissionError(
            "the production observation requires the packing working directory"
        )
    bindings = bind_frozen_inputs(root=root)
    runner_hash = bindings["producer"]
    result_hash_before = bindings["immutable_result"]

    counts = _empty_counts()
    module = _load_frozen_runner(root, counts)
    refusal_type: str | None = None
    refusal_text: str | None = None
    reached_stage: str | None = None
    try:
        module.run_exp050(RESULT_PATH, root=root)
    except StageSentinelError as error:
        reached_stage = error.stage
    except Exception as error:  # The dynamically loaded frozen exception has no static type.
        refusal_type = type(error).__name__
        refusal_text = str(error)
    else:
        raise AdmissionError("frozen producer did not refuse the existing result")

    result_hash_after = sha256_file(root / RESULT_PATH)
    if result_hash_after != result_hash_before:
        raise AdmissionError("immutable exp-050 result changed during observation")
    if reached_stage is not None:
        raise AdmissionError(f"downstream stage ran before refusal: {reached_stage}")
    if refusal_type != "SourceApplicationError" or refusal_text != EXPECTED_REFUSAL:
        raise AdmissionError("frozen producer emitted the wrong existing-result refusal")
    if any(counts.values()):
        raise AdmissionError("target observation contains a nonzero downstream call")

    return {
        "schema": "packing.squares:n050-producer-observation/v1",
        "fake_intake_injected_before_import": True,
        "producer": {"path": str(RUNNER_PATH), "sha256": runner_hash},
        "immutable_result": {
            "path": str(RESULT_PATH),
            "sha256_before": result_hash_before,
            "sha256_after": result_hash_after,
        },
        "refusal": {"type": refusal_type, "text": refusal_text},
        "stage_trace": {
            "schema": "packing.squares:n050-producer-stage-trace/v1",
            "calls": [],
            "counts": counts,
        },
    }


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--observe", action="store_true")
    group.add_argument("--calibrate-stage", choices=STAGES)
    group.add_argument("--probe-reordered-stage", choices=STAGES)
    return parser


def main(argv: list[str] | None = None) -> int:
    arguments = _parser().parse_args(argv)
    try:
        if arguments.calibrate_stage is not None:
            receipt = calibrate_stage(arguments.calibrate_stage)
        elif arguments.probe_reordered_stage is not None:
            receipt = probe_reordered_stage(arguments.probe_reordered_stage)
        else:
            receipt = observe()
    except (AdmissionError, OSError) as error:
        _parser().exit(1, f"admission failed: {error}\n")
    sys.stdout.buffer.write(canonical_bytes(receipt))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
