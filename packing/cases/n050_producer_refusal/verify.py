"""Independently verify one H-059 producer-refusal result receipt.

This verifier intentionally imports neither the producer-refusal harness nor the frozen
producer. It treats the result as data and checks the frozen files directly.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections.abc import Sequence
from pathlib import Path
from typing import Any, cast

LAUNCH_REVISION = "909efafa0773fbea23b24de072ef59a03a01317a"
SCIENTIFIC_REVISION = "81177148e404aa283c2a6ec7d696f2b39a9e361c"
RUNNER_PATH = Path("cases/n050_exact/source_semantics_runner.py")
IMMUTABLE_RESULT_PATH = Path(
    "campaign/series/series-000-smoke-and-calibration/results/"
    "exp-050-h-054-n50-source-semantics-e1-localization.json"
)
EXPECTED_RUNNER_SHA256 = "52baeb1b6ad52aa504498ba21aeb6b3d361aaaec2461c76904a357d8d95cf29d"
EXPECTED_RESULT_SHA256 = "ab00e50debe0bc60279ce3472ed0c09eb062e8271a481a38c6ac65036aff4a02"
EXPECTED_REFUSAL = f"result already exists: {IMMUTABLE_RESULT_PATH}"
STAGES = (
    "binding_observation",
    "fixture_loading",
    "receipt_evaluation",
    "publication",
)
INSTRUMENT_PATHS = (
    Path("cases/n050_producer_refusal/__init__.py"),
    Path("cases/n050_producer_refusal/harness.py"),
    Path("cases/n050_producer_refusal/run.py"),
    Path("cases/n050_producer_refusal/verify.py"),
    Path("tests/test_n050_producer_refusal.py"),
    Path("tests/test_n050_producer_refusal_independent.py"),
)
EXPECTED_CLAIM_BOUNDARY = (
    "Prospective producer-refusal protocol only; this does not repair exp-050, "
    "change H-054, establish n = 50 feasibility or authorize source or geometry work."
)


class VerificationError(RuntimeError):
    """A result, binding, or registered control does not match the frozen contract."""


def canonical_bytes(value: object) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n").encode()


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _strict_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise VerificationError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def load_result(path: Path) -> dict[str, Any]:
    raw = path.read_bytes()
    try:
        document = json.loads(
            raw,
            object_pairs_hook=_strict_object,
            parse_constant=lambda token: (_ for _ in ()).throw(
                VerificationError(f"non-finite JSON number: {token}")
            ),
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise VerificationError("result is not strict JSON") from error
    if not isinstance(document, dict) or canonical_bytes(document) != raw:
        raise VerificationError("result is not canonical JSON")
    return document


def _require(condition: object, message: str) -> None:
    if not condition:
        raise VerificationError(message)


def _is_sha256(value: object) -> bool:
    return (
        isinstance(value, str)
        and len(value) == 64
        and all(character in "0123456789abcdef" for character in value)
    )


def _verify_calibrations(calibrations: object) -> None:
    _require(isinstance(calibrations, dict), "calibrations are not an object")
    calibrations = cast(dict[str, Any], calibrations)
    _require(set(calibrations) == set(STAGES), "calibration inventory changed")
    for stage in STAGES:
        item = calibrations[stage]
        _require(isinstance(item, dict), f"calibration is not an object: {stage}")
        expected_counts = dict.fromkeys(STAGES, 0)
        expected_counts[stage] = 1
        _require(
            item
            == {
                "schema": "packing.squares:n050-stage-calibration/v1",
                "stage": stage,
                "raised": f"forbidden stage reached: {stage}",
                "counts": expected_counts,
            },
            f"sentinel calibration changed: {stage}",
        )


def _verify_observation(observation: object) -> None:
    expected_counts = dict.fromkeys(STAGES, 0)
    _require(isinstance(observation, dict), "observation is not an object")
    observation = cast(dict[str, Any], observation)
    _require(
        observation
        == {
            "schema": "packing.squares:n050-producer-observation/v1",
            "fake_intake_injected_before_import": True,
            "producer": {
                "path": str(RUNNER_PATH),
                "sha256": EXPECTED_RUNNER_SHA256,
            },
            "immutable_result": {
                "path": str(IMMUTABLE_RESULT_PATH),
                "sha256_before": EXPECTED_RESULT_SHA256,
                "sha256_after": EXPECTED_RESULT_SHA256,
            },
            "refusal": {
                "type": "SourceApplicationError",
                "text": EXPECTED_REFUSAL,
            },
            "stage_trace": {
                "schema": "packing.squares:n050-producer-stage-trace/v1",
                "calls": [],
                "counts": expected_counts,
            },
        },
        "observation is not the canonical zero-call refusal",
    )


def _verify_mutations(mutations: object) -> None:
    _require(isinstance(mutations, dict), "mutations are not an object")
    mutations = cast(dict[str, Any], mutations)
    _require(
        set(mutations)
        == {
            "changed_runner",
            "changed_result",
            "reordered_stage",
            "missing_sentinel",
            "overwrite",
            "changed_refusal_text",
        },
        "mutation inventory changed",
    )
    for name, frozen, reason in (
        (
            "changed_runner",
            EXPECTED_RUNNER_SHA256,
            "producer runner SHA-256 changed before import",
        ),
        (
            "changed_result",
            EXPECTED_RESULT_SHA256,
            "immutable exp-050 result SHA-256 changed before import",
        ),
    ):
        item = mutations[name]
        _require(isinstance(item, dict), f"mutation is not an object: {name}")
        _require(
            set(item) == {"rejected", "observed_sha256", "reason"},
            f"mutation fields changed: {name}",
        )
        _require(item.get("rejected") is True, f"mutation was not rejected: {name}")
        observed = item.get("observed_sha256")
        _require(
            _is_sha256(observed) and observed != frozen,
            f"mutation did not change its binding: {name}",
        )
        _require(item.get("reason") == reason, f"mutation refusal changed: {name}")
    for key, prefix in (
        ("reordered_stage", "forbidden stage reached: "),
        ("missing_sentinel", "missing sentinel: "),
    ):
        inventory = mutations[key]
        _require(isinstance(inventory, dict), f"mutation is not an object: {key}")
        _require(set(inventory) == set(STAGES), f"mutation stage inventory changed: {key}")
        for stage in STAGES:
            expected: dict[str, Any] = {
                "rejected": True,
                "reason": f"{prefix}{stage}",
            }
            if key == "reordered_stage":
                counts = dict.fromkeys(STAGES, 0)
                counts[stage] = 1
                expected["counts"] = counts
            _require(
                inventory[stage] == expected,
                f"stage mutation changed: {key}/{stage}",
            )
    overwrite = mutations["overwrite"]
    _require(isinstance(overwrite, dict), "overwrite mutation is not an object")
    _require(
        set(overwrite)
        == {"rejected", "reason", "sha256_before", "sha256_after"},
        "overwrite mutation fields changed",
    )
    _require(overwrite.get("rejected") is True, "overwrite mutation was not rejected")
    _require(
        overwrite.get("sha256_before") == overwrite.get("sha256_after"),
        "overwrite mutation changed existing bytes",
    )
    _require(
        overwrite.get("reason") == "result already exists: fresh successor result",
        "overwrite mutation emitted the wrong refusal",
    )
    _require(
        mutations["changed_refusal_text"]
        == {"rejected": True, "reason": "existing-result refusal changed"},
        "changed-refusal mutation changed",
    )


def verify_result(path: Path, *, root: Path = Path()) -> dict[str, Any]:
    """Verify the full receipt and current executable closure without importing it."""

    document = load_result(path)
    _require(
        set(document)
        == {
            "schema",
            "experiment_id",
            "hypothesis_id",
            "launch_revision",
            "scientific_revision",
            "instrument_bindings",
            "needs_review",
            "outcome",
            "conditions",
            "mutations",
            "immutable_result_sha256_after",
            "claim_boundary",
        },
        "result field inventory changed",
    )
    _require(
        document.get("schema") == "packing.squares:n050-producer-refusal-result/v1",
        "result schema changed",
    )
    _require(document.get("experiment_id") == "exp-055", "experiment id changed")
    _require(document.get("hypothesis_id") == "H-059", "hypothesis id changed")
    _require(document.get("launch_revision") == LAUNCH_REVISION, "launch revision changed")
    _require(
        document.get("scientific_revision") == SCIENTIFIC_REVISION,
        "scientific revision changed",
    )
    _require(document.get("needs_review") is True, "needs_review is not true")
    _require(document.get("outcome") == "criterion-met", "criterion was not met")
    _require(
        document.get("claim_boundary") == EXPECTED_CLAIM_BOUNDARY,
        "claim boundary changed",
    )

    bindings = document.get("instrument_bindings")
    _require(isinstance(bindings, dict), "instrument bindings are not an object")
    bindings = cast(dict[str, Any], bindings)
    expected_paths = {str(item) for item in INSTRUMENT_PATHS}
    _require(set(bindings) == expected_paths, "instrument binding inventory changed")
    for instrument in INSTRUMENT_PATHS:
        _require(
            _is_sha256(bindings[str(instrument)]),
            f"instrument binding is not SHA-256: {instrument}",
        )
        _require(
            bindings[str(instrument)] == sha256_file(root / instrument),
            f"instrument binding changed: {instrument}",
        )
    _require(
        sha256_file(root / RUNNER_PATH) == EXPECTED_RUNNER_SHA256,
        "producer runner binding changed",
    )
    _require(
        sha256_file(root / IMMUTABLE_RESULT_PATH) == EXPECTED_RESULT_SHA256,
        "immutable exp-050 result binding changed",
    )

    conditions = document.get("conditions")
    _require(isinstance(conditions, dict), "conditions are not an object")
    conditions = cast(dict[str, Any], conditions)
    _require(
        set(conditions)
        == {
            "calibrations",
            "normal_stdout_sha256",
            "optimized_stdout_sha256",
            "stdout_byte_identical",
            "observation",
        },
        "condition field inventory changed",
    )
    _verify_calibrations(conditions.get("calibrations"))
    _require(
        conditions.get("stdout_byte_identical") is True,
        "normal and optimized bytes differ",
    )
    normal_hash = conditions.get("normal_stdout_sha256")
    _require(
        _is_sha256(normal_hash)
        and normal_hash == conditions.get("optimized_stdout_sha256"),
        "normal and optimized stdout digests differ",
    )
    _verify_observation(conditions.get("observation"))
    _verify_mutations(document.get("mutations"))
    _require(
        document.get("immutable_result_sha256_after") == EXPECTED_RESULT_SHA256,
        "post-control exp-050 result binding changed",
    )
    return {
        "schema": "packing.squares:n050-producer-refusal-verification/v1",
        "experiment_id": "exp-055",
        "verified": True,
        "result_sha256": sha256_file(path),
        "producer_sha256": EXPECTED_RUNNER_SHA256,
        "immutable_result_sha256": EXPECTED_RESULT_SHA256,
        "needs_review": True,
    }


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("result", type=Path)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    arguments = _parser().parse_args(argv)
    try:
        receipt = verify_result(arguments.result)
    except (OSError, VerificationError) as error:
        _parser().exit(1, f"verification failed: {error}\n")
    print(json.dumps(receipt, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
