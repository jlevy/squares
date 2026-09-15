#!/usr/bin/env python3
"""Admit Route S's exact, target-blind threshold-certificate compression surface.

This command does not optimize a certificate and does not run a coverage verifier.  It
binds the fixed T-025 control and T-026 support/rescaling sentinel to one deterministic
orbit catalogue, checks the predeclared compression policy, and exercises the
decompressor on a synthetic selection.  ``--output`` writes only the typed admission
receipt; ``--check`` recomputes that receipt and compares it with the retained bytes.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import stat
import sys
from collections.abc import Sequence
from fractions import Fraction
from pathlib import Path, PurePosixPath
from typing import Any, Never, cast

from strif import atomic_output_file

from devtools.decide_threshold_certificate import load as load_threshold_certificate
from sqpack.fractional.threshold_compression import (
    CompressionPolicy,
    PointOrbitSelection,
    ThresholdOrbitSelection,
    canonical_catalog_record,
    catalog_sha256,
    compare_scaled_support,
    decompress_selection,
    inventory_certificate,
    measure_selection,
    ordered_support,
    quantized_inventory_budget,
)

PACKING = Path(__file__).resolve().parent.parent
REPOSITORY = PACKING.parent
ADMISSION = PACKING / "cases/n11_threshold_certificate/route-s-compression-admission.json"
RECEIPT = PACKING / (
    "cases/n11_threshold_certificate/route-s-compression-admission-receipt.json"
)
ADMISSION_PATH = "packing/cases/n11_threshold_certificate/route-s-compression-admission.json"
SOURCE_PATH = "packing/cases/n11_threshold_certificate/certificate.json"
SENTINEL_PATH = "packing/cases/n11_threshold_certificate/t-026-dilation-limit-corollary.json"
SENTINEL_SOURCE_PATH = "packing/cases/n11_threshold_certificate/certificate-191-50-net1440.json"
SCHEMA = "packing.squares:ThresholdCompressionAdmission/v1"
RECEIPT_SCHEMA = "packing.squares:ThresholdCompressionAdmissionReceipt/v1"
MAX_JSON_BYTES = 256 * 1024
MAX_JSON_DEPTH = 16
MAX_INTEGER_DIGITS = 6
SHA256_LENGTH = 64
MAX_CERTIFICATE_BYTES = 2 * 1024 * 1024
QUANTIZATION_DENOMINATOR = 30_000
SYNTHETIC_WEIGHT = Fraction(1, QUANTIZATION_DENOMINATOR)


class AdmissionError(ValueError):
    """The admission record or one of its bound sources is not admissible."""


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise AdmissionError(f"duplicate JSON object key {key!r}")
        result[key] = value
    return result


def _integer(raw: str) -> int:
    digits = raw.removeprefix("-")
    if len(digits) > MAX_INTEGER_DIGITS:
        raise AdmissionError("JSON integer exceeds the digit limit")
    return int(raw)


def _inexact(raw: str) -> Never:
    raise AdmissionError(f"floating or nonfinite JSON number {raw!r} is forbidden")


def _bounded_regular_bytes(path: Path, *, limit: int, label: str) -> bytes:
    """Read a regular, non-symlink file without letting its size drive allocation."""
    flags = os.O_RDONLY | getattr(os, "O_NONBLOCK", 0) | getattr(os, "O_NOFOLLOW", 0)
    descriptor = os.open(path, flags)
    with os.fdopen(descriptor, "rb") as stream:
        if not stat.S_ISREG(os.fstat(stream.fileno()).st_mode):
            raise AdmissionError(f"{label} must be a regular file")
        data = stream.read(limit + 1)
    if len(data) > limit:
        raise AdmissionError(f"{label} exceeds the {limit}-byte limit")
    return data


def _check_depth(text: str) -> None:
    depth = 0
    quoted = False
    escaped = False
    for char in text:
        if quoted:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                quoted = False
            continue
        if char == '"':
            quoted = True
        elif char in "[{":
            depth += 1
            if depth > MAX_JSON_DEPTH:
                raise AdmissionError("JSON nesting exceeds the depth limit")
        elif char in "]}":
            depth -= 1


def load_json(
    path: Path, *, label: str, limit: int = MAX_JSON_BYTES
) -> tuple[dict[str, Any], bytes]:
    """Load one bounded exact JSON object, refusing aliases and approximate numbers."""
    try:
        data = _bounded_regular_bytes(path, limit=limit, label=label)
        text = data.decode("utf-8")
        _check_depth(text)
        decoded = json.loads(
            text,
            object_pairs_hook=_unique_object,
            parse_int=_integer,
            parse_float=_inexact,
            parse_constant=_inexact,
        )
    except AdmissionError:
        raise
    except (OSError, UnicodeError, json.JSONDecodeError, RecursionError) as error:
        raise AdmissionError(f"cannot read {label}: {error}") from None
    if not isinstance(decoded, dict):
        raise AdmissionError(f"{label} must be a JSON object")
    return cast(dict[str, Any], decoded), data


def _keys(value: object, expected: set[str], label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise AdmissionError(f"{label} must be a JSON object")
    actual = set(value)
    if actual != expected:
        missing = sorted(expected - actual)
        extra = sorted(actual - expected)
        raise AdmissionError(f"{label} fields differ: missing={missing}, extra={extra}")
    return cast(dict[str, Any], value)


def _repo_path(value: object, *, expected: str, label: str) -> Path:
    """Accept exactly one normalized repository-relative path and keep it in the repo."""
    if not isinstance(value, str):
        raise AdmissionError(f"{label} must be a repository-relative path string")
    pure = PurePosixPath(value)
    malformed = (
        pure.is_absolute()
        or "." in pure.parts
        or ".." in pure.parts
        or pure.as_posix() != value
    )
    if malformed:
        raise AdmissionError(f"{label} is not a normalized repository-relative path")
    if value != expected:
        raise AdmissionError(f"{label} is {value!r}; expected frozen path {expected!r}")
    path = (REPOSITORY / pure).resolve()
    if not path.is_relative_to(REPOSITORY.resolve()):
        raise AdmissionError(f"{label} escapes the repository")
    return path


def _digest(value: object, *, label: str) -> str:
    if (
        not isinstance(value, str)
        or len(value) != SHA256_LENGTH
        or any(char not in "0123456789abcdef" for char in value)
    ):
        raise AdmissionError(f"{label} must be a lowercase SHA-256 digest")
    return value


def _canonical_json(value: object) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n").encode()


def _load_certificate(path: Path, *, label: str) -> tuple[object, bytes]:
    data = _bounded_regular_bytes(path, limit=MAX_CERTIFICATE_BYTES, label=label)
    try:
        certificate, _ = load_threshold_certificate(data)
    except (TypeError, ValueError, RecursionError) as error:
        raise AdmissionError(f"cannot load {label}: {error}") from None
    return certificate, data


def _expected_admission(
    *,
    source_digest: str,
    source_inventory: Any,
    sentinel_digest: str,
    sentinel_source_digest: str,
    sentinel_inventory: Any,
) -> dict[str, Any]:
    relation = compare_scaled_support(source_inventory, sentinel_inventory)
    if not relation.matches:
        raise AdmissionError("T-026 does not preserve T-025 support under one exact scale")
    rounded_budget = quantized_inventory_budget(source_inventory, QUANTIZATION_DENOMINATOR)
    if rounded_budget >= source_inventory.n:
        raise AdmissionError("the denominator-30000 upward-rounding control exceeds budget")
    return {
        "schema": SCHEMA,
        "control": {
            "role": "matched T-025 control",
            "path": SOURCE_PATH,
            "sha256": source_digest,
            "n": source_inventory.n,
            "outer_side": str(source_inventory.outer_side),
            "square_side": str(source_inventory.square_side),
            "symmetry": source_inventory.symmetry,
            "total_budget": str(source_inventory.total_budget),
            "catalog_sha256": catalog_sha256(source_inventory),
            "point_orbits": source_inventory.point_orbit_count,
            "threshold_orbits": source_inventory.threshold_orbit_count,
            "orbits": source_inventory.orbit_count,
            "point_atoms": source_inventory.point_atom_count,
            "threshold_atoms": source_inventory.threshold_atom_count,
            "atoms": source_inventory.atom_count,
        },
        "sentinel": {
            "role": "T-026 support and rescaling sentinel",
            "path": SENTINEL_PATH,
            "sha256": sentinel_digest,
            "source_path": SENTINEL_SOURCE_PATH,
            "source_sha256": sentinel_source_digest,
            "catalog_sha256": catalog_sha256(sentinel_inventory),
            "point_support_equal": relation.point_support_equal,
            "threshold_support_equal": relation.threshold_support_equal,
            "common_weight_scale": str(relation.common_weight_scale),
            "support_equal": relation.support_equal,
            "weights_have_common_scale": relation.weights_have_common_scale,
        },
        "family": {
            "kind": "fixed-source-support D4-orbit selection",
            "catalog_schema": canonical_catalog_record(source_inventory)["schema"],
            "selection_unit": "one complete source D4 orbit",
            "geometry_rule": "select source orbit representatives without moving sites",
            "weight_rule": "one positive exact rational weight per selected orbit",
            "max_orbits": 23,
            "minimum_compression_factor": "5",
            "baseline_orbits": source_inventory.orbit_count,
            "success_rule": (
                "at most 23 selected orbits and compression factor at least 5, followed "
                "on a later branch by unchanged exact budget and complete coverage replay"
            ),
            "park_rule": (
                "park only this fixed-source-support family after exact infeasibility or "
                "retained counterexample cells; do not refute Route S"
            ),
        },
        "quantization_control": {
            "role": "arithmetic control only; not support-compression success",
            "direction": "upward",
            "denominator": QUANTIZATION_DENOMINATOR,
            "rounded_budget": str(rounded_budget),
            "budget_below_n": True,
        },
        "execution_boundary": {
            "target_ran": False,
            "optimizer_ran": False,
            "coverage_ran": False,
            "candidate_created": False,
            "experiment_created": False,
        },
    }


def _validate_paths_and_digests(
    admission: dict[str, Any],
    *,
    source_digest: str,
    sentinel_digest: str,
    sentinel_source_digest: str,
) -> None:
    """Refuse path aliases and digest substitutions before deriving the full record."""
    _keys(
        admission,
        {
            "schema",
            "control",
            "sentinel",
            "family",
            "quantization_control",
            "execution_boundary",
        },
        "admission",
    )
    if admission["schema"] != SCHEMA:
        raise AdmissionError(f"admission schema must be {SCHEMA!r}")
    control = _keys(
        admission["control"],
        {
            "role",
            "path",
            "sha256",
            "n",
            "outer_side",
            "square_side",
            "symmetry",
            "total_budget",
            "catalog_sha256",
            "point_orbits",
            "threshold_orbits",
            "orbits",
            "point_atoms",
            "threshold_atoms",
            "atoms",
        },
        "control",
    )
    _repo_path(control["path"], expected=SOURCE_PATH, label="control.path")
    declared = _digest(control["sha256"], label="control.sha256")
    if declared != source_digest:
        raise AdmissionError("control digest does not match the frozen T-025 bytes")
    _digest(control["catalog_sha256"], label="control.catalog_sha256")
    sentinel = _keys(
        admission["sentinel"],
        {
            "role",
            "path",
            "sha256",
            "source_path",
            "source_sha256",
            "catalog_sha256",
            "point_support_equal",
            "threshold_support_equal",
            "common_weight_scale",
            "support_equal",
            "weights_have_common_scale",
        },
        "sentinel",
    )
    _repo_path(sentinel["path"], expected=SENTINEL_PATH, label="sentinel.path")
    _repo_path(
        sentinel["source_path"],
        expected=SENTINEL_SOURCE_PATH,
        label="sentinel.source_path",
    )
    if _digest(sentinel["sha256"], label="sentinel.sha256") != sentinel_digest:
        raise AdmissionError("sentinel digest does not match the frozen T-026 record")
    if (
        _digest(sentinel["source_sha256"], label="sentinel.source_sha256")
        != sentinel_source_digest
    ):
        raise AdmissionError("sentinel source digest does not match the frozen T-026 bytes")
    _digest(sentinel["catalog_sha256"], label="sentinel.catalog_sha256")


def _synthetic_decompressor_check(inventory: Any) -> dict[str, Any]:
    """Exercise the admitted family at its ceiling without making a candidate."""
    policy = CompressionPolicy()
    point_count = min(len(inventory.point_orbits), policy.max_orbits - 1)
    point_selections = tuple(
        PointOrbitSelection(orbit.representative, SYNTHETIC_WEIGHT)
        for orbit in inventory.point_orbits[:point_count]
    )
    threshold_needed = policy.max_orbits - point_count
    threshold_selections = tuple(
        ThresholdOrbitSelection(orbit.representative, SYNTHETIC_WEIGHT)
        for orbit in inventory.threshold_orbits[:threshold_needed]
    )
    metrics = measure_selection(inventory, point_selections, threshold_selections, policy)
    decompressed = decompress_selection(
        inventory, point_selections, threshold_selections, policy
    )
    if len(decompressed.atoms) + len(decompressed.threshold_atoms) != metrics.expanded_atoms:
        raise AdmissionError("synthetic decompressor disagrees with its exact atom metric")
    if decompressed.total_budget != metrics.total_budget:
        raise AdmissionError("synthetic decompressor changed its uniform exact weights")
    return {
        "role": "target-blind decompressor control",
        "synthetic_weight": str(SYNTHETIC_WEIGHT),
        "baseline_orbits": metrics.baseline_orbits,
        "point_orbits": metrics.point_orbits,
        "threshold_orbits": metrics.threshold_orbits,
        "selected_orbits": metrics.selected_orbits,
        "expanded_atoms": metrics.expanded_atoms,
        "coordinate_parameters": metrics.coordinate_parameters,
        "distinct_weights": metrics.distinct_weights,
        "threshold_templates": metrics.threshold_templates,
        "compression_factor": str(metrics.compression_factor),
        "within_orbit_ceiling": metrics.within_orbit_ceiling,
        "meets_compression_factor": metrics.meets_compression_factor,
        "satisfies_policy": metrics.satisfies_policy,
        "decompressed_point_atoms": len(decompressed.atoms),
        "decompressed_threshold_atoms": len(decompressed.threshold_atoms),
        "decompressed_budget": str(decompressed.total_budget),
    }


def _full_control_roundtrip(inventory: Any) -> dict[str, Any]:
    """Decompress every authenticated T-025 orbit and compare the canonical result."""
    points = tuple(
        PointOrbitSelection(orbit.representative, orbit.weight)
        for orbit in inventory.point_orbits
    )
    thresholds = tuple(
        ThresholdOrbitSelection(orbit.representative, orbit.weight)
        for orbit in inventory.threshold_orbits
    )
    policy = CompressionPolicy(
        max_orbits=inventory.orbit_count,
        minimum_compression_factor=Fraction(1),
    )
    reconstructed = inventory_certificate(
        decompress_selection(inventory, points, thresholds, policy)
    )
    source_record = canonical_catalog_record(inventory)
    reconstructed_record = canonical_catalog_record(reconstructed)
    if reconstructed_record != source_record:
        raise AdmissionError("full T-025 decompression is not canonically equivalent")
    return {
        "role": "full authenticated T-025 decompressor control",
        "canonical_equivalent": True,
        "catalog_sha256": catalog_sha256(reconstructed),
        "orbits": reconstructed.orbit_count,
        "atoms": reconstructed.atom_count,
        "total_budget": str(reconstructed.total_budget),
    }


def build_receipt(admission_path: Path = ADMISSION) -> dict[str, Any]:
    """Recompute the complete admission receipt without any scientific target work."""
    admission, admission_bytes = load_json(admission_path, label="admission record")
    top = _keys(
        admission,
        {
            "schema",
            "control",
            "sentinel",
            "family",
            "quantization_control",
            "execution_boundary",
        },
        "admission",
    )
    if not isinstance(top["control"], dict) or not isinstance(top["sentinel"], dict):
        raise AdmissionError("control and sentinel must be JSON objects")
    control = cast(dict[str, Any], top["control"])
    sentinel = cast(dict[str, Any], top["sentinel"])
    source_path = _repo_path(control.get("path"), expected=SOURCE_PATH, label="control.path")
    sentinel_path = _repo_path(
        sentinel.get("path"), expected=SENTINEL_PATH, label="sentinel.path"
    )
    sentinel_source_path = _repo_path(
        sentinel.get("source_path"),
        expected=SENTINEL_SOURCE_PATH,
        label="sentinel.source_path",
    )
    source_certificate, source_bytes = _load_certificate(source_path, label="T-025 certificate")
    sentinel_record, sentinel_bytes = load_json(sentinel_path, label="T-026 limit record")
    sentinel_source_certificate, sentinel_source_bytes = _load_certificate(
        sentinel_source_path, label="T-026 source certificate"
    )
    sentinel_source = _keys(
        sentinel_record.get("source"),
        {
            "accepted_conditions",
            "certificate",
            "coarse_containment",
            "half_gap_tangent",
            "minimum_cell_charge",
            "n",
            "outer_side",
            "point_atoms",
            "sha256",
            "square_side",
            "threshold_atoms",
            "total_budget",
            "variant",
        },
        "T-026 source",
    )
    if sentinel_source.get("certificate") != SENTINEL_SOURCE_PATH:
        raise AdmissionError("T-026 record names a foreign source certificate")
    if sentinel_source.get("sha256") != _sha256(sentinel_source_bytes):
        raise AdmissionError("T-026 record does not bind its frozen source bytes")
    source_inventory = inventory_certificate(source_certificate)  # type: ignore[arg-type]
    sentinel_inventory = inventory_certificate(sentinel_source_certificate)  # type: ignore[arg-type]
    source_support = ordered_support(source_inventory)
    if len(source_support) != source_inventory.orbit_count:
        raise AdmissionError("ordered source support does not cover every orbit once")
    source_digest = _sha256(source_bytes)
    sentinel_digest = _sha256(sentinel_bytes)
    sentinel_source_digest = _sha256(sentinel_source_bytes)
    _validate_paths_and_digests(
        admission,
        source_digest=source_digest,
        sentinel_digest=sentinel_digest,
        sentinel_source_digest=sentinel_source_digest,
    )
    expected = _expected_admission(
        source_digest=source_digest,
        source_inventory=source_inventory,
        sentinel_digest=sentinel_digest,
        sentinel_source_digest=sentinel_source_digest,
        sentinel_inventory=sentinel_inventory,
    )
    if admission != expected:
        raise AdmissionError("admission record differs from its exact derived contract")
    relation = compare_scaled_support(source_inventory, sentinel_inventory)
    rounded_budget = quantized_inventory_budget(source_inventory, QUANTIZATION_DENOMINATOR)
    return {
        "schema": RECEIPT_SCHEMA,
        "status": "blocked",
        "admission_blockers": [
            "pin all T-025/T-026 digests outside the mutable admission record",
            "bind both the 720-step and 1440-step T-026 provenance sentinels",
            "admit a canonical selection-manifest parser and serializer",
            "exercise every mutation refusal declared by X-032",
        ],
        "admission": {
            "path": ADMISSION_PATH,
            "sha256": _sha256(admission_bytes),
        },
        "control": {
            "path": SOURCE_PATH,
            "sha256": source_digest,
            "catalog_sha256": catalog_sha256(source_inventory),
            "support_keys": len(source_support),
            "orbits": source_inventory.orbit_count,
            "atoms": source_inventory.atom_count,
            "total_budget": str(source_inventory.total_budget),
            "reproduced": True,
            "decompressor_roundtrip": _full_control_roundtrip(source_inventory),
        },
        "sentinel": {
            "path": SENTINEL_PATH,
            "sha256": sentinel_digest,
            "source_path": SENTINEL_SOURCE_PATH,
            "source_sha256": sentinel_source_digest,
            "point_support_equal": relation.point_support_equal,
            "threshold_support_equal": relation.threshold_support_equal,
            "support_equal": relation.support_equal,
            "common_weight_scale": str(relation.common_weight_scale),
            "weights_have_common_scale": relation.weights_have_common_scale,
            "reproduced": relation.matches,
        },
        "quantization_control": {
            "denominator": QUANTIZATION_DENOMINATOR,
            "rounded_budget": str(rounded_budget),
            "budget_below_n": rounded_budget < source_inventory.n,
            "support_changed": False,
            "research_success": False,
        },
        "synthetic_decompressor": _synthetic_decompressor_check(source_inventory),
        "target_ran": False,
        "optimizer_ran": False,
        "coverage_ran": False,
        "candidate_created": False,
        "experiment_created": False,
        "scope": (
            "Incomplete instrument checkpoint only. Admission is blocked; no coverage, "
            "optimizer, candidate certificate, compression verdict, or improved n=11 "
            "bound is established."
        ),
    }


def _check_receipt(path: Path, encoded: bytes) -> None:
    retained = _bounded_regular_bytes(path, limit=MAX_JSON_BYTES, label="retained receipt")
    if retained != encoded:
        raise AdmissionError("retained Route S compression admission receipt is stale")


def _write_receipt(output: Path, encoded: bytes, *, admission: Path) -> None:
    protected = {
        admission.resolve(),
        (REPOSITORY / SOURCE_PATH).resolve(),
        (REPOSITORY / SENTINEL_PATH).resolve(),
        (REPOSITORY / SENTINEL_SOURCE_PATH).resolve(),
    }
    if output.resolve() in protected:
        raise AdmissionError("receipt output may not overwrite an input")
    with atomic_output_file(output) as temporary:
        temporary.write_bytes(encoded)


def parser() -> argparse.ArgumentParser:
    command = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    command.add_argument("--admission", type=Path, default=ADMISSION)
    command.add_argument("--receipt", type=Path, default=RECEIPT)
    mode = command.add_mutually_exclusive_group(required=True)
    mode.add_argument("--output", type=Path, help="write the recomputed receipt here")
    mode.add_argument("--check", action="store_true", help="compare with the retained receipt")
    return command


def main(argv: Sequence[str] | None = None) -> int:
    options = parser().parse_args(argv)
    try:
        receipt = build_receipt(options.admission)
        encoded = _canonical_json(receipt)
        if options.check:
            _check_receipt(options.receipt, encoded)
            print("Route S compression checkpoint check passed")
        else:
            output = cast(Path, options.output)
            _write_receipt(output, encoded, admission=options.admission)
            print(f"Route S compression admission receipt written: {output}")
    except (OSError, ValueError) as error:
        print(f"Route S compression admission refused: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
