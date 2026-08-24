#!/usr/bin/env python3
"""Check the small-n terminal-component assignment policy against exact models.

This is deliberately not a general component finder.  It freezes the evidence boundary
needed before one is built: complete exact quotient models may assign members to a
component, while endpoint hashes, contact signatures, samples, and floating-point
compatibility may not.  The exact ``n = 3`` interval and exact ``n = 4`` point are the
known answers; all retained floating-point observations remain unresolved unless a
future instrument supplies an independent membership certificate.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
import time
from pathlib import Path
from typing import cast

from strif import atomic_output_file

from cases.small_n.optimal_moduli import build_result as build_small_n_result

ROOT = Path(__file__).resolve().parents[2]
SCHEMA_VERSION = 1
RESULTS = ROOT / "campaign/series/series-000-smoke-and-calibration/results"
N3_MODEL = RESULTS / "exp-014-h-032-n3-optimal-moduli.json"
N4_MODEL = RESULTS / "exp-015-h-032-n4-optimal-moduli.json"
EVENT_RECORDS = (
    RESULTS / "exp-021-h-021-n3-basin-event-v3.jsonl",
    RESULTS / "exp-022-h-021-n3-basin-event-v3-completion.jsonl",
    RESULTS / "exp-023-h-021-n4-basin-event-v3.jsonl",
    RESULTS / "exp-024-h-021-n4-basin-event-v3-repair.jsonl",
    RESULTS / "exp-025-h-021-n5-basin-event-v3.jsonl",
)
N3_COMPONENT_ID = "F3(2)/(D4xS3):0"
N4_COMPONENT_ID = "F4(2)/(D4xS4):0"
QUOTIENT_SCOPE = "container D4 x square relabelling x per-square quarter turns"


def require_dict(value: object, label: str) -> dict[str, object]:
    """Return a JSON object or fail with its semantic label."""
    if not isinstance(value, dict):
        raise TypeError(f"{label} must be an object")
    return cast(dict[str, object], value)


def require_list(value: object, label: str) -> list[object]:
    """Return a JSON array or fail with its semantic label."""
    if not isinstance(value, list):
        raise TypeError(f"{label} must be an array")
    return cast(list[object], value)


def sha256_file(path: Path) -> str:
    """Hash retained evidence bytes."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_json(path: Path) -> dict[str, object]:
    """Load one retained JSON object."""
    return require_dict(json.loads(path.read_text(encoding="utf-8")), str(path))


def read_jsonl(path: Path) -> list[dict[str, object]]:
    """Load nonblank JSONL records."""
    records: list[dict[str, object]] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if line.strip():
            records.append(require_dict(json.loads(line), f"{path.name}:{line_number}"))
    if not records:
        raise ValueError(f"{path} contains no records")
    return records


def verified_exact_model(n: int, path: Path) -> dict[str, object]:
    """Regenerate one exact model and require byte-semantic agreement."""
    retained = read_json(path)
    regenerated, _ = build_small_n_result(n)
    if retained != regenerated:
        raise ValueError(f"retained n={n} exact model differs from regeneration")
    return retained


def stratum_for_parameter(parameter: str) -> str:
    """Name the exact n=3 quotient stratum containing one retained sample."""
    if parameter == "0":
        return "C"
    if parameter == "1/2":
        return "M"
    if parameter in {"1/8", "1/4"}:
        return "G"
    raise ValueError(f"undeclared exact n=3 sample parameter: {parameter}")


def scalar_exceeds(value: object, threshold: float) -> bool:
    """Check an untrusted JSON scalar without accepting booleans as numbers."""
    return isinstance(value, (int, float)) and not isinstance(value, bool) and value > threshold


def exact_n3_fixture(model: dict[str, object]) -> dict[str, object]:
    """Assign exact n=3 representatives by the complete quotient model."""
    spaces = require_dict(model.get("spaces"), "n=3 spaces")
    quotient = require_dict(spaces.get("d4_s3_quotient"), "n=3 quotient")
    samples = require_list(model.get("samples"), "n=3 samples")
    assignments: list[dict[str, object]] = []
    for raw_sample in samples:
        sample = require_dict(raw_sample, "n=3 sample")
        parameter = str(sample.get("parameter"))
        assignments.append(
            {
                "member": f"lambda={parameter}",
                "status": "assigned",
                "component_id": N3_COMPONENT_ID,
                "evidence": "complete exact quotient parameter membership",
                "stratum": stratum_for_parameter(parameter),
                "geometric_key": str(sample.get("geometric_key")),
                "contact_key": str(sample.get("contact_certificate")),
            }
        )
    return {
        "n": 3,
        "quotient_scope": QUOTIENT_SCOPE,
        "model_kind": "complete_exact_connected_model",
        "component_id": N3_COMPONENT_ID,
        "component_count": quotient.get("component_count"),
        "topology": quotient.get("homeomorphism_type"),
        "strata": quotient.get("strata"),
        "sample_assignments": assignments,
        "source": str(N3_MODEL.relative_to(ROOT)),
        "source_sha256": sha256_file(N3_MODEL),
    }


def exact_n4_fixture(model: dict[str, object]) -> dict[str, object]:
    """Assign every exact labelled n=4 grid through the complete quotient model."""
    spaces = require_dict(model.get("spaces"), "n=4 spaces")
    labelled = require_dict(spaces.get("labelled"), "n=4 labelled space")
    quotient = require_dict(spaces.get("d4_s4_quotient"), "n=4 quotient")
    states = sorted(str(state) for state in require_list(labelled.get("states"), "n=4 states"))
    state_digest = hashlib.sha256(
        (json.dumps(states, separators=(",", ":")) + "\n").encode()
    ).hexdigest()
    return {
        "n": 4,
        "quotient_scope": QUOTIENT_SCOPE,
        "model_kind": "complete_exact_isolated_model",
        "component_id": N4_COMPONENT_ID,
        "component_count": quotient.get("component_count"),
        "topology": quotient.get("homeomorphism_type"),
        "labelled_state_count": len(states),
        "labelled_state_sha256": state_digest,
        "all_labelled_states_assign_to": N4_COMPONENT_ID,
        "source": str(N4_MODEL.relative_to(ROOT)),
        "source_sha256": sha256_file(N4_MODEL),
    }


def floating_observations() -> list[dict[str, object]]:
    """Preserve retained f64 observations as unresolved by this exact-only policy."""
    observations: list[dict[str, object]] = []
    for path in EVENT_RECORDS:
        for event in read_jsonl(path):
            endpoint = require_dict(event.get("endpoint"), "event endpoint")
            termination = require_dict(event.get("termination"), "event termination")
            observations.append(
                {
                    "event_id": str(event.get("event_id")),
                    "n": event.get("n"),
                    "side": endpoint.get("side"),
                    "scientifically_admissible": termination.get(
                        "scientifically_admissible_terminal_event"
                    ),
                    "status": "unresolved",
                    "reason": (
                        "f64 compatibility is not an exact component-membership certificate"
                    ),
                    "source": str(path.relative_to(ROOT)),
                }
            )
    return observations


def validate_result(result: dict[str, object]) -> None:
    """Enforce the frozen evidence boundary and both known answers."""
    policy = require_dict(result.get("policy"), "policy")
    if policy.get("quotient_scope") != QUOTIENT_SCOPE:
        raise ValueError("component assignments use the wrong quotient scope")
    if policy.get("endpoint_keys_are_component_evidence") is not False:
        raise ValueError("endpoint keys may not determine terminal components")
    models = require_dict(result.get("exact_models"), "exact models")
    n3 = require_dict(models.get("n3"), "n=3 exact model")
    n4 = require_dict(models.get("n4"), "n=4 exact model")
    if (
        n3.get("model_kind") != "complete_exact_connected_model"
        or n3.get("component_count") != 1
        or n3.get("topology") != "closed interval [0,1/2]"
        or n3.get("quotient_scope") != QUOTIENT_SCOPE
        or n3.get("source_sha256") != sha256_file(N3_MODEL)
    ):
        raise ValueError("n=3 exact component model does not match the frozen control")
    assignments = [
        require_dict(item, "n=3 assignment")
        for item in require_list(n3.get("sample_assignments"), "n=3 assignments")
    ]
    if len(assignments) != 4:
        raise ValueError("n=3 control must retain four exact quotient samples")
    if {assignment.get("status") for assignment in assignments} != {"assigned"}:
        raise ValueError("an exact n=3 member was left unassigned")
    if {assignment.get("component_id") for assignment in assignments} != {N3_COMPONENT_ID}:
        raise ValueError("n=3 samples were split despite the exact connected model")
    if len({assignment.get("geometric_key") for assignment in assignments}) != 4:
        raise ValueError("n=3 geometric-key control no longer has four distinct keys")
    if len({assignment.get("contact_key") for assignment in assignments}) != 2:
        raise ValueError("n=3 contact-stratum control no longer has two signatures")
    if {assignment.get("stratum") for assignment in assignments} != {"C", "G", "M"}:
        raise ValueError("n=3 exact quotient strata are incomplete")
    if (
        n4.get("model_kind") != "complete_exact_isolated_model"
        or n4.get("component_count") != 1
        or n4.get("topology") != "point"
        or n4.get("quotient_scope") != QUOTIENT_SCOPE
        or n4.get("labelled_state_count") != 24
        or n4.get("all_labelled_states_assign_to") != N4_COMPONENT_ID
        or n4.get("source_sha256") != sha256_file(N4_MODEL)
    ):
        raise ValueError("n=4 exact point model does not match the frozen control")
    observations = [
        require_dict(item, "floating observation")
        for item in require_list(result.get("floating_observations"), "floating observations")
    ]
    if not observations or any(item.get("status") != "unresolved" for item in observations):
        raise ValueError("f64 observations were assigned without exact membership evidence")
    if not any(
        item.get("n") == 3 and scalar_exceeds(item.get("side"), 2.1) for item in observations
    ):
        raise ValueError("the nonoptimal n=3 unresolved control is missing")
    if not any(item.get("n") == 5 for item in observations):
        raise ValueError("the out-of-domain n=5 unresolved control is missing")
    determination = require_dict(result.get("determination"), "determination")
    if determination.get("outcome") != "criterion_met":
        raise ValueError("known-answer component controls did not meet their criterion")


def mutation_rejected(result: dict[str, object], mutation: str) -> bool:
    """Apply one named false policy and require validation to reject it."""
    altered = copy.deepcopy(result)
    models = require_dict(altered["exact_models"], "mutated exact models")
    n3 = require_dict(models["n3"], "mutated n=3 model")
    n4 = require_dict(models["n4"], "mutated n=4 model")
    assignments = [
        require_dict(item, "mutated n=3 assignment")
        for item in require_list(n3["sample_assignments"], "mutated assignments")
    ]
    observations = [
        require_dict(item, "mutated observation")
        for item in require_list(altered["floating_observations"], "mutated observations")
    ]
    if mutation == "geometric_keys_as_components":
        for assignment in assignments:
            assignment["component_id"] = assignment["geometric_key"]
    elif mutation == "contact_keys_as_components":
        for assignment in assignments:
            assignment["component_id"] = assignment["contact_key"]
    elif mutation == "samples_as_components":
        for index, assignment in enumerate(assignments):
            assignment["component_id"] = f"sample-{index}"
    elif mutation == "labelled_scope_as_quotient":
        n3["quotient_scope"] = "labelled configurations"
    elif mutation == "n4_labelled_states_as_components":
        n4["component_count"] = 24
    elif mutation == "f64_event_forced_assigned":
        observations[0]["status"] = "assigned"
    elif mutation == "n5_event_forced_assigned":
        next(item for item in observations if item.get("n") == 5)["status"] = "assigned"
    elif mutation == "exact_model_digest_ignored":
        n3["source_sha256"] = "0" * 64
    else:
        raise ValueError(f"unknown mutation: {mutation}")
    try:
        validate_result(altered)
    except ValueError:
        return True
    return False


def build_result() -> dict[str, object]:
    """Build the deterministic BC-009 known-answer record."""
    n3_model = verified_exact_model(3, N3_MODEL)
    n4_model = verified_exact_model(4, N4_MODEL)
    observations = floating_observations()
    result: dict[str, object] = {
        "schema_version": SCHEMA_VERSION,
        "contract": "packing.squares:TerminalComponentControl/v1",
        "policy": {
            "quotient_scope": QUOTIENT_SCOPE,
            "assignment_rule": (
                "assign only from a complete exact component model or an independently "
                "replayable membership certificate"
            ),
            "ambiguity_rule": "otherwise preserve the observation as unresolved",
            "endpoint_keys_are_component_evidence": False,
        },
        "exact_models": {
            "n3": exact_n3_fixture(n3_model),
            "n4": exact_n4_fixture(n4_model),
        },
        "floating_observations": observations,
        "determination": {
            "outcome": "criterion_met",
            "claim": (
                "the frozen policy recovers the exact n=3 quotient interval and n=4 "
                "quotient point without using keys, strata, or samples as components"
            ),
            "scope": (
                "known-answer controls at exact side 2 only; no n=5 component or "
                "sampled-basin claim"
            ),
        },
    }
    validate_result(result)
    mutation_names = (
        "geometric_keys_as_components",
        "contact_keys_as_components",
        "samples_as_components",
        "labelled_scope_as_quotient",
        "n4_labelled_states_as_components",
        "f64_event_forced_assigned",
        "n5_event_forced_assigned",
        "exact_model_digest_ignored",
    )
    selftests = {name: mutation_rejected(result, name) for name in mutation_names}
    if not all(selftests.values()):
        failed = [name for name, passed in selftests.items() if not passed]
        raise ValueError(f"terminal-component selftests failed: {failed}")
    result["selftests"] = selftests
    return result


def write_json_atomic(path: Path, value: dict[str, object]) -> None:
    """Write a deterministic retained JSON record."""
    with atomic_output_file(path, make_parents=True) as temporary:
        temporary.write_text(
            json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )


def require_replay_match(result: dict[str, object], path: Path) -> None:
    """Reject a retained record that differs from deterministic regeneration."""
    retained = read_json(path)
    if retained != result:
        raise ValueError("retained terminal-component record differs from regeneration")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--record", type=Path, help="write the deterministic control record")
    mode.add_argument("--replay", type=Path, help="rebuild and compare a retained record")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    started = time.monotonic()
    try:
        result = build_result()
        if args.record is not None:
            write_json_atomic(args.record, result)
        else:
            require_replay_match(result, args.replay)
        models = require_dict(result["exact_models"], "exact models")
        n3 = require_dict(models["n3"], "n=3 model")
        n4 = require_dict(models["n4"], "n=4 model")
        summary = {
            "schema_version": SCHEMA_VERSION,
            "record_written": args.record is not None,
            "record_replayed": args.replay is not None,
            "n3_component_count": n3["component_count"],
            "n3_contact_strata": len(
                {
                    require_dict(item, "n=3 assignment")["contact_key"]
                    for item in require_list(n3["sample_assignments"], "n=3 assignments")
                }
            ),
            "n4_component_count": n4["component_count"],
            "floating_unresolved": len(
                require_list(result["floating_observations"], "floating observations")
            ),
            "determination_outcome": require_dict(result["determination"], "determination")[
                "outcome"
            ],
            "selftests": result["selftests"],
            "elapsed_seconds": round(time.monotonic() - started, 6),
        }
    except (OSError, TypeError, ValueError, json.JSONDecodeError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
