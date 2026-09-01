"""Independent verifier for the immutable exp-050 source-semantics result.

This module deliberately imports neither the source-semantics producer nor its
publication runner. It replays the retained refusal from JSON bytes and frozen hashes.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
from pathlib import Path
from typing import Any

RESULT_PATH = Path(
    "campaign/series/series-000-smoke-and-calibration/results/"
    "exp-050-h-054-n50-source-semantics-e1-localization.json"
)
EXPECTED_RESULT_SHA256 = "ab00e50debe0bc60279ce3472ed0c09eb062e8271a481a38c6ac65036aff4a02"
EXPECTED_BINDINGS = {
    "focused_test": (
        "tests/test_n050_exact.py",
        "0bcbd7e6154dca5b688cb6baf5098d37b9eb938dc227d04e81e3e76329ca2707",
    ),
    "n19_control_receipt": (
        "cases/n050_exact/n19_control_receipt.json",
        "accd0d9ce40c6e06c959804d4455dffb21b6a7062276391ddb9421ac805daaae",
    ),
    "source_semantics_intake": (
        "cases/n050_exact/source_semantics.py",
        "fed71cf825906bd09f3711ec0a465dce0e4aecb91a1128f3a9d792e59c7c8d0c",
    ),
    "w1_source_fixture": (
        "cases/n050_exact/w1_source_fixture.json",
        "113a6b3c82f343f62a7b07e67777dd11d6fa30994576f227d86ea45f2f936c26",
    ),
}
EXPECTED_CLAIM_BOUNDARY = (
    "Executed source-semantics localization only: the checked hash-bound surfaces "
    "do not bind source-author and file-publisher roles. This is not an n = 50 "
    "geometry, feasibility, exactness, optimality, frontier, or H-054 verdict; H-054 "
    "remains instrument_ready false."
)
RESOURCE_ROLES = frozenset({"catalogue", "source_svg"})
ATTRIBUTION_ROLES = frozenset(
    {
        "packing_finder",
        "later_optimizer",
        "source_author",
        "file_publisher",
        "compilation_basis",
    }
)
SEMANTICS_FIELDS = frozenset(
    {
        "coordinate_units",
        "coordinate_frame",
        "rotation_convention",
        "exporter_version",
    }
)
_SHA256 = re.compile(r"[0-9a-f]{64}\Z")


class VerificationError(RuntimeError):
    """The retained result or one of its frozen bindings failed replay."""


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _strict_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise VerificationError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def load_json_strict(path: Path) -> dict[str, Any]:
    """Load one JSON object while rejecting duplicate keys and non-finite numbers."""

    try:
        value = json.loads(
            path.read_text(encoding="utf-8"),
            object_pairs_hook=_strict_object,
            parse_constant=lambda token: (_ for _ in ()).throw(
                VerificationError(f"non-finite JSON number: {token}")
            ),
        )
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        raise VerificationError(f"cannot read strict JSON: {path.name}") from error
    if not isinstance(value, dict):
        raise VerificationError(f"JSON root is not an object: {path.name}")
    return value


def _resource_map(receipt: dict[str, Any]) -> dict[str, dict[str, Any]] | None:
    resources = receipt.get("resources")
    if not isinstance(resources, list) or len(resources) != len(RESOURCE_ROLES):
        return None
    mapped: dict[str, dict[str, Any]] = {}
    for item in resources:
        if not isinstance(item, dict) or not isinstance(item.get("role"), str):
            return None
        role = item["role"]
        if role in mapped:
            return None
        mapped[role] = item
    return mapped if set(mapped) == RESOURCE_ROLES else None


def classify_source_receipt(
    receipt: dict[str, Any],
) -> tuple[str | None, tuple[object, ...]]:
    """Independently replay the ordered pre-cell E1 refusal reasons."""

    resources = _resource_map(receipt)
    if resources is None or any(
        item.get("available") is not True or item.get("http_status") != 200
        for item in resources.values()
    ):
        return "source-unavailable", ()

    for item in resources.values():
        digest = item.get("sha256")
        version = item.get("etag") or item.get("last_modified")
        if (
            not isinstance(digest, str)
            or _SHA256.fullmatch(digest) is None
            or not isinstance(version, str)
            or not version
        ):
            return "source-hash-or-version-unbound", ()

    artifact_hash = receipt.get("attribution_artifact_sha256")
    role_map = receipt.get("role_map")
    attribution_bound = (
        isinstance(artifact_hash, str)
        and _SHA256.fullmatch(artifact_hash) is not None
        and artifact_hash in {item["sha256"] for item in resources.values()}
        and isinstance(role_map, dict)
        and set(role_map) == ATTRIBUTION_ROLES
    )
    if attribution_bound and isinstance(role_map, dict):
        for role in ATTRIBUTION_ROLES:
            binding = role_map[role]
            if not isinstance(binding, dict) or set(binding) != {
                "name",
                "evidence_resource",
            }:
                attribution_bound = False
                break
            name = binding["name"]
            resource_role = binding["evidence_resource"]
            if (
                not isinstance(name, str)
                or not name
                or resource_role not in resources
                or resources[resource_role]["sha256"] != artifact_hash
            ):
                attribution_bound = False
                break
    if not attribution_bound:
        return "attribution-unbound", ()

    context = receipt.get("semantics_context")
    if (
        not isinstance(context, dict)
        or set(context) != SEMANTICS_FIELDS
        or any(
            not isinstance(context[field], str) or not context[field]
            for field in SEMANTICS_FIELDS
        )
    ):
        return "units-frame-or-rotation-undefined", ()

    return None, ()


def run_missing_semantics_control() -> tuple[str | None, tuple[object, ...]]:
    """Construct a source-independent reason-four mutation and replay it."""

    digest = "a" * 64
    receipt: dict[str, Any] = {
        "resources": [
            {
                "role": role,
                "available": True,
                "http_status": 200,
                "sha256": digest,
                "etag": '"synthetic-v1"',
            }
            for role in sorted(RESOURCE_ROLES)
        ],
        "attribution_artifact_sha256": digest,
        "role_map": {
            role: {
                "name": f"Synthetic {role}",
                "evidence_resource": "catalogue",
            }
            for role in sorted(ATTRIBUTION_ROLES)
        },
        "semantics_context": {
            "coordinate_units": "synthetic-unit",
            "coordinate_frame": "synthetic-right-up",
            "rotation_convention": None,
            "exporter_version": "synthetic-v1",
        },
    }
    return classify_source_receipt(copy.deepcopy(receipt))


def _verify_bindings(document: dict[str, Any], root: Path) -> None:
    bindings = document.get("bindings")
    if not isinstance(bindings, dict) or set(bindings) != set(EXPECTED_BINDINGS):
        raise VerificationError("result bindings do not match the frozen inventory")
    for name, (expected_path, expected_digest) in EXPECTED_BINDINGS.items():
        binding = bindings[name]
        if not isinstance(binding, dict) or binding != {
            "path": expected_path,
            "sha256": expected_digest,
        }:
            raise VerificationError(f"invalid frozen binding: {name}")
        if _sha256(root / expected_path) != expected_digest:
            raise VerificationError(f"bound artifact hash changed: {name}")


def _verify_n19(document: dict[str, Any], root: Path) -> None:
    receipt_path, _ = EXPECTED_BINDINGS["n19_control_receipt"]
    receipt = load_json_strict(root / receipt_path)
    if receipt.get("build_call") != "build(19)" or receipt.get("skip_count") != 0:
        raise VerificationError("n = 19 control call or skip count changed")
    expected_side = receipt.get("expected_side")
    observed_side = receipt.get("observed_side")
    if expected_side != {
        "field": "Q(sqrt(2))",
        "power_basis_coefficients": ["3", "4/3"],
        "serialized": "poly[3,4/3]",
    } or observed_side != {
        "equals_expected": True,
        "power_basis_coefficients": ["3", "4/3"],
        "serialized": "poly[3,4/3]",
    }:
        raise VerificationError("n = 19 exact side facts changed")
    verification = receipt.get("verification")
    mutation = receipt.get("mutation")
    if not isinstance(verification, dict) or verification != {
        "assurance": "exact-sign",
        "expected_pairs": 171,
        "observed_n": 19,
        "observed_pairs": 171,
        "pair_semantics": "all-unordered-pairs",
        "valid": True,
    }:
        raise VerificationError("n = 19 verification facts changed")
    if (
        not isinstance(mutation, dict)
        or mutation.get("kind") != "append-duplicate-of-square-1"
        or mutation.get("expected_pairs") != 190
        or mutation.get("observed_pairs") != 190
        or mutation.get("expected_valid") is not False
        or mutation.get("observed_valid") is not False
        or mutation.get("failure_kinds") != ["overlap"]
    ):
        raise VerificationError("n = 19 mutation facts changed")
    control_inputs = receipt.get("control_inputs")
    if not isinstance(control_inputs, list) or len(control_inputs) != 2:
        raise VerificationError("n = 19 control input inventory changed")
    for item in control_inputs:
        if (
            not isinstance(item, dict)
            or set(item) != {"path", "sha256"}
            or not isinstance(item["path"], str)
            or not isinstance(item["sha256"], str)
            or _sha256(root / item["path"]) != item["sha256"]
        ):
            raise VerificationError("n = 19 control input hash changed")

    expected_result_control = {
        "build_call": "build(19)",
        "mutation_observed_valid": False,
        "observed_pairs": 171,
        "observed_side": observed_side,
        "skip_count": 0,
    }
    if document.get("n19_control") != expected_result_control:
        raise VerificationError("result does not faithfully project the n = 19 receipt")


def verify_result(path: Path, *, root: Path) -> dict[str, object]:
    """Verify the frozen result, its refusal order, and every retained binding."""

    raw = path.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    if digest != EXPECTED_RESULT_SHA256:
        raise VerificationError("result SHA-256 does not match the frozen value")
    document = load_json_strict(path)
    canonical = (json.dumps(document, indent=2, sort_keys=True) + "\n").encode()
    if raw != canonical:
        raise VerificationError("result bytes are not canonical JSON")

    expected_keys = {
        "bindings",
        "cell_count",
        "cells",
        "claim_boundary",
        "executed",
        "experiment_id",
        "hypothesis_id",
        "n19_control",
        "needs_review",
        "outcome",
        "reason",
        "reason_index",
        "retention",
    }
    if set(document) != expected_keys:
        raise VerificationError("result field inventory changed")
    if (
        document.get("experiment_id") != "exp-050"
        or document.get("hypothesis_id") != "H-054"
        or document.get("executed") is not True
        or document.get("outcome") != "e1-refusal"
        or document.get("reason") != "attribution-unbound"
        or document.get("reason_index") != 3
        or document.get("cells") != []
        or document.get("cell_count") != 0
        or document.get("needs_review") is not True
        or document.get("claim_boundary") != EXPECTED_CLAIM_BOUNDARY
        or document.get("retention") != "sanitized-structured-source-seam-only"
    ):
        raise VerificationError("result decision or claim boundary changed")

    _verify_bindings(document, root)
    fixture_path, _ = EXPECTED_BINDINGS["w1_source_fixture"]
    reason, cells = classify_source_receipt(load_json_strict(root / fixture_path))
    if reason != "attribution-unbound" or cells:
        raise VerificationError("independent W1 replay did not stop at reason 3")
    mutation_reason, mutation_cells = run_missing_semantics_control()
    if mutation_reason != "units-frame-or-rotation-undefined" or mutation_cells:
        raise VerificationError("independent missing-semantics control did not refuse")
    _verify_n19(document, root)

    return {
        "result_sha256": digest,
        "reason": reason,
        "reason_index": 3,
        "cell_count": 0,
        "bound_artifact_count": len(EXPECTED_BINDINGS),
        "n19_observed_pairs": 171,
        "skip_count": 0,
        "needs_review": True,
        "claim_boundary": "source-semantics-localization-only",
        "mutation_reason": mutation_reason,
    }


def _main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--result", type=Path, required=True)
    arguments = parser.parse_args()
    try:
        replay = verify_result(arguments.result, root=Path())
    except (OSError, VerificationError) as error:
        parser.exit(1, f"verification failed: {error}\n")
    print(json.dumps(replay, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(_main())
