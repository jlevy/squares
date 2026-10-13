"""Run and admit the pinned T-059 per-row minimum comparison.

This tool checks one narrow claim: equality between minima computed by the pinned
source search and the retained row minima of Overbeck's certificate.  Its separate
direct evaluator proves that each reported witness attains that value; it does not
independently prove global minimality.  A complete row inventory does not verify the
angle-folding, enclosure, counting-budget, or packing theorem arguments.

The ``run`` command snapshots the pinned checker and both inputs before execution,
uses a wall timeout, checks that those bytes did not change, and tags every emitted
row with that production-time binding.  ``validate`` refuses journals without that
binding.  ``pack`` gzips a journal deterministically for retention, and ``validate``
reads the gzip directly, with every digest over the inflated bytes.  ``inspect`` can describe
legacy JSONL, but always reports it as unbound inventory rather than as a verified replay.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import math
import os
import subprocess
import sys
import tempfile
import zlib
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any, Final

PINNED_CHECKER_REVISION: Final = "0d33ab61726c2ab03e3eb8f457dabaf22db8571f"
PINNED_CERTIFICATE_SHA256: Final = (
    "57e9927da5c13f42dd8bcbf8f08c84363635fece626657ee63a810c61cd44458"
)
PINNED_REFERENCE_SHA256: Final = (
    "68b6f360ecbc377c15d2ad95aad328b211716329a771c51f15e45bf2de127bc0"
)
EXPECTED_ROWS: Final = 12_028
SCHEMA: Final = "sqpack.general-pose-tree-census.v1"
MAX_INPUT_BYTES: Final = 64 * 1024 * 1024
MAX_SOURCE_BYTES: Final = 2 * 1024 * 1024
GZIP_MAGIC: Final = b"\x1f\x8b"
CHECKER_FILES: Final = (
    "general_pose_tree/run_n11.py",
    "general_pose_tree/measure.py",
    "general_pose_tree/enclosure.py",
    "general_pose_tree/branch.py",
)
INTEGER_STATS: Final = (
    "boxes_expanded",
    "leaves",
    "max_depth",
    "cells",
    "nodes_created",
    "outside_pruned",
    "bound_pruned",
)
WRAPPER_SOURCE: Final = Path(__file__).resolve()


class CensusError(ValueError):
    """The row journal cannot support the requested disposition."""


@dataclass(frozen=True)
class SourceSnapshot:
    binding: dict[str, object]
    certificate: dict[str, Any]
    reference: dict[str, Any]


@dataclass(frozen=True)
class WitnessEvaluator:
    """Independent exact direct evaluator for reported row witnesses."""

    side: Fraction
    parent_side: Fraction
    denominator: int
    coordinates: tuple[tuple[int, int], ...]
    weights: tuple[int, ...]
    features: tuple[tuple[tuple[int, ...], int, int], ...]
    entries: tuple[tuple[Fraction, Fraction, Fraction, Fraction], ...]

    def charge(self, row: int, x: Fraction, y: Fraction) -> int:
        left, right, direction, core_side = self.entries[row]
        cosine = (1 - direction**2) / (1 + direction**2)
        sine = 2 * direction / (1 + direction**2)
        widths = []
        for endpoint in (left, right):
            c = (1 - endpoint**2) / (1 + endpoint**2)
            s = 2 * endpoint / (1 + endpoint**2)
            widths.append(c + s)
        radius = self.parent_side * min(widths) / 2
        _require(
            radius < x < self.side - radius and radius < y < self.side - radius,
            f"row {row} witness is outside its open centre domain",
        )
        half = core_side / 2
        captured: set[int] = set()
        for index, (raw_x, raw_y) in enumerate(self.coordinates):
            dx = Fraction(raw_x, self.denominator) - x
            dy = Fraction(raw_y, self.denominator) - y
            if abs(cosine * dx + sine * dy) <= half and abs(-sine * dx + cosine * dy) <= half:
                captured.add(index)
        total = sum(self.weights[index] for index in captured)
        for members, threshold, weight in self.features:
            if sum(index in captured for index in members) >= threshold:
                total += weight
        return total


def _require(condition: object, message: str) -> None:
    if not condition:
        raise CensusError(message)


def _unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        _require(key not in result, f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _invalid_constant(value: str) -> None:
    raise CensusError(f"non-finite JSON number: {value}")


def _read_bytes(path: Path, *, limit: int = MAX_INPUT_BYTES) -> bytes:
    _require(path.is_file(), f"not a regular input file: {path}")
    with path.open("rb") as stream:
        data = stream.read(limit + 1)
    _require(len(data) <= limit, f"input exceeds {limit} bytes: {path}")
    return data


def _read_journal(path: Path, *, limit: int | None = None) -> bytes:
    """Read a journal, inflating a gzip one under the same decompressed ceiling.

    A complete 12,028-row journal is megabytes of repetitive JSON, so it is retained
    gzipped; every digest in a summary is over the inflated bytes, never the archive.
    """
    limit = MAX_INPUT_BYTES if limit is None else limit
    data = _read_bytes(path, limit=limit)
    if not data.startswith(GZIP_MAGIC):
        return data
    inflater = zlib.decompressobj(wbits=31)
    try:
        inflated = inflater.decompress(data, limit + 1)
    except zlib.error as error:
        raise CensusError(f"malformed gzip journal: {path}: {error}") from error
    _require(len(inflated) <= limit, f"journal inflates beyond {limit} bytes: {path}")
    _require(inflater.eof and not inflater.unused_data, f"malformed gzip journal: {path}")
    return inflated


def pack_journal(journal: Path, output: Path) -> dict[str, object]:
    """Write a deterministic gzip of ``journal`` whose inflated bytes match exactly."""
    _require(output.suffix == ".gz", "packed journal must end in .gz")
    _require(not output.exists(), "output already exists; fresh runs never overwrite evidence")
    _require(output.resolve() != journal.resolve(), "output may not overwrite the journal")
    inflated = _read_journal(journal)
    _require(not _read_bytes(journal).startswith(GZIP_MAGIC), "journal is already gzipped")
    packed = gzip.compress(inflated, compresslevel=9, mtime=0)
    output.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        dir=output.parent, prefix=f".{output.name}.", suffix=".tmp"
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(packed)
            stream.flush()
            os.fsync(stream.fileno())
        try:
            os.link(temporary, output)
        except FileExistsError as error:
            raise CensusError(
                "output appeared during packing; refusing to overwrite"
            ) from error
    finally:
        temporary.unlink(missing_ok=True)
    _require(_read_journal(output) == inflated, "packed journal does not round-trip")
    return {
        "journal_sha256": _sha256(inflated),
        "inflated_bytes": len(inflated),
        "packed_bytes": len(packed),
        "packed_sha256": _sha256(packed),
    }


def _json(data: bytes, *, label: str) -> Any:
    try:
        return json.loads(
            data,
            object_pairs_hook=_unique_object,
            parse_constant=_invalid_constant,
        )
    except CensusError:
        raise
    except (UnicodeDecodeError, ValueError) as error:
        raise CensusError(f"invalid JSON in {label}: {error}") from error


def _ascii_digits(value: str) -> bool:
    return value.isascii() and value.isdigit()


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _canonical(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()


def _git(checker: Path, *arguments: str) -> bytes:
    try:
        return subprocess.run(
            ["git", *arguments], cwd=checker, check=True, capture_output=True
        ).stdout
    except (OSError, subprocess.CalledProcessError) as error:
        raise CensusError(f"cannot establish checker Git identity: {error}") from error


def _checker_binding(
    checker: Path,
    *,
    expected_revision: str | None = PINNED_CHECKER_REVISION,
    checker_files: tuple[str, ...] = CHECKER_FILES,
) -> dict[str, object]:
    revision = _git(checker, "rev-parse", "HEAD").decode().strip()
    if expected_revision is not None:
        _require(revision == expected_revision, "checker is not at the pinned revision")
    files: dict[str, str] = {}
    for relative in checker_files:
        data = _read_bytes(checker / relative, limit=MAX_SOURCE_BYTES)
        if expected_revision is not None:
            try:
                frozen = _git(checker, "cat-file", "blob", f"{expected_revision}:{relative}")
            except CensusError as error:
                raise CensusError(f"pinned checker omits {relative}") from error
            _require(data == frozen, f"checker source differs from pin: {relative}")
        files[relative] = _sha256(data)
    return {"git_revision": revision, "files": files}


def _integer(value: object, field: str) -> int:
    if type(value) is not int or value < 0:
        raise CensusError(f"{field} must be a nonnegative exact integer")
    return value


def _list(value: object, message: str) -> list[Any]:
    if not isinstance(value, list):
        raise CensusError(message)
    return value


def _object(value: object, message: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise CensusError(message)
    return value


def _certificate_rational(value: object, field: str) -> Fraction:
    if not isinstance(value, str):
        raise CensusError(f"{field} must be a rational string")
    return _rational(value, field)


def witness_evaluator(certificate: dict[str, Any], expected_rows: int) -> WitnessEvaluator:
    """Build the direct evaluator without importing any producer code."""
    side = _certificate_rational(certificate.get("L"), "certificate L")
    parent_side = _certificate_rational(certificate.get("A"), "certificate A")
    denominator = _integer(certificate.get("coordinate_denominator"), "coordinate denominator")
    _require(denominator > 0, "coordinate denominator must be positive")
    span = side * denominator
    _require(span.denominator == 1, "container side is not on the coordinate lattice")
    extent = span.numerator
    raw_orbits = _list(certificate.get("point_orbits"), "missing point orbits")
    coordinates: list[tuple[int, int]] = []
    weights: list[int] = []
    for orbit_index, raw_orbit in enumerate(raw_orbits):
        orbit = _list(raw_orbit, "malformed point orbit")
        _require(len(orbit) == 3, "malformed point orbit")
        x = _integer(orbit[0], f"point orbit {orbit_index} x")
        y = _integer(orbit[1], f"point orbit {orbit_index} y")
        weight = _integer(orbit[2], f"point orbit {orbit_index} weight")
        _require(x <= extent and y <= extent, "point lies outside the container")
        images = sorted(
            {
                (a, b)
                for u, v in ((x, y), (y, x))
                for a in (u, extent - u)
                for b in (v, extent - v)
            }
        )
        coordinates.extend(images)
        weights.extend([weight] * len(images))
    _require(len(coordinates) == len(set(coordinates)), "duplicate expanded point")
    raw_features = _list(certificate.get("charge_orbits"), "missing charge orbits")
    features: list[tuple[tuple[int, ...], int, int]] = []
    for feature_index, raw_feature in enumerate(raw_features):
        feature = _object(raw_feature, "malformed charge orbit")
        threshold = _integer(
            feature.get("threshold"), f"charge orbit {feature_index} threshold"
        )
        weight = _integer(feature.get("weight"), f"charge orbit {feature_index} weight")
        groups = _list(feature.get("sets"), "charge orbit sets")
        for raw_group in groups:
            group = _list(raw_group, "charge set")
            members = tuple(_integer(value, "charge site index") for value in group)
            _require(len(members) == len(set(members)), "repeated charge site")
            _require(all(index < len(coordinates) for index in members), "charge site index")
            _require(0 < threshold <= len(members), "invalid charge threshold")
            if weight > 0:
                features.append((members, threshold, weight))
    raw_entries = _list(certificate.get("entries"), "certificate row count")
    _require(len(raw_entries) == expected_rows, "certificate row count")
    entries: list[tuple[Fraction, Fraction, Fraction, Fraction]] = []
    for row, raw_entry in enumerate(raw_entries):
        entry = _list(raw_entry, f"malformed entry {row}")
        _require(len(entry) == 4, f"malformed entry {row}")
        values = [
            _certificate_rational(value, f"entry {row} field {index}")
            for index, value in enumerate(entry)
        ]
        entries.append((values[0], values[1], values[2], values[3]))
    return WitnessEvaluator(
        side=side,
        parent_side=parent_side,
        denominator=denominator,
        coordinates=tuple(coordinates),
        weights=tuple(weights),
        features=tuple(features),
        entries=tuple(entries),
    )


def _reference_rows(reference: dict[str, Any], expected_rows: int) -> list[int]:
    rows = _list(reference.get("rows"), "reference row count")
    _require(len(rows) == expected_rows, "reference row count")
    minima: list[int] = []
    for index, raw_row in enumerate(rows):
        row = _object(raw_row, f"reference row {index} is not an object")
        _require(
            _integer(row.get("row"), f"reference row {index} index") == index,
            "reference rows are not an exact census",
        )
        minima.append(_integer(row.get("minimum_units"), f"reference row {index} minimum"))
    return minima


def snapshot_sources(
    checker: Path,
    certificate_path: Path,
    reference_path: Path,
    *,
    expected_rows: int = EXPECTED_ROWS,
    expected_revision: str | None = PINNED_CHECKER_REVISION,
    expected_certificate_sha256: str | None = PINNED_CERTIFICATE_SHA256,
    expected_reference_sha256: str | None = PINNED_REFERENCE_SHA256,
    checker_files: tuple[str, ...] = CHECKER_FILES,
) -> SourceSnapshot:
    """Read and cross-bind the exact checker, certificate, and recorded minima."""
    certificate_bytes = _read_bytes(certificate_path)
    reference_bytes = _read_bytes(reference_path)
    certificate = _json(certificate_bytes, label=str(certificate_path))
    reference = _json(reference_bytes, label=str(reference_path))
    _require(isinstance(certificate, dict), "certificate must be a JSON object")
    _require(isinstance(reference, dict), "reference must be a JSON object")
    entries = certificate.get("entries")
    _require(
        isinstance(entries, list) and len(entries) == expected_rows, "certificate row count"
    )
    minima = _reference_rows(reference, expected_rows)
    certificate_sha256 = _sha256(certificate_bytes)
    reference_sha256 = _sha256(reference_bytes)
    if expected_certificate_sha256 is not None:
        _require(
            certificate_sha256 == expected_certificate_sha256,
            "certificate differs from the retained T-059 pin",
        )
    if expected_reference_sha256 is not None:
        _require(
            reference_sha256 == expected_reference_sha256,
            "reference differs from the retained T-059 pin",
        )
    _require(
        reference.get("certificate_sha256") == certificate_sha256,
        "reference is detached from the certificate",
    )
    _require(
        _integer(reference.get("minimum_units"), "reference global minimum") == min(minima),
        "reference global minimum disagrees with its rows",
    )
    binding: dict[str, object] = {
        "checker": _checker_binding(
            checker,
            expected_revision=expected_revision,
            checker_files=checker_files,
        ),
        "certificate_sha256": certificate_sha256,
        "reference_sha256": reference_sha256,
        "first_party_wrapper": {
            "path": "packing/devtools/check_general_pose_tree_census.py",
            "sha256": _sha256(_read_bytes(WRAPPER_SOURCE, limit=MAX_SOURCE_BYTES)),
        },
        "expected_rows": expected_rows,
        "python": sys.version,
    }
    return SourceSnapshot(binding=binding, certificate=certificate, reference=reference)


def parse_rows(spec: str, *, expected_rows: int = EXPECTED_ROWS) -> list[int]:
    """Parse the upstream row syntax while refusing repeats and out-of-range rows."""
    rows: list[int] = []
    for part in spec.split(","):
        _require(bool(part), "empty row selector")
        if "-" in part:
            pieces = part.split("-")
            _require(
                len(pieces) == 2
                and all(
                    _ascii_digits(piece) and len(piece) <= len(str(expected_rows - 1))
                    for piece in pieces
                ),
                "malformed row range",
            )
            left, right = map(int, pieces)
            _require(left <= right, "descending row range")
            _require(right < expected_rows, "row outside the census")
            rows.extend(range(left, right + 1))
        else:
            _require(
                _ascii_digits(part) and len(part) <= len(str(expected_rows - 1)),
                "malformed row index",
            )
            rows.append(int(part))
    _require(bool(rows), "empty row selection")
    _require(all(0 <= row < expected_rows for row in rows), "row outside the census")
    _require(len(rows) == len(set(rows)), "duplicate requested row")
    return rows


def _documents(
    data: bytes, *, bound: bool
) -> tuple[dict[str, Any] | None, list[dict[str, Any]]]:
    lines = data.splitlines()
    _require(bool(lines), "empty row journal")
    documents: list[dict[str, Any]] = []
    for index, line in enumerate(lines, start=1):
        _require(bool(line.strip()), f"blank JSONL line {index}")
        value = _json(line, label=f"journal line {index}")
        _require(isinstance(value, dict), f"journal line {index} is not an object")
        documents.append(value)
    if not bound:
        return None, documents
    header, *rows = documents
    _require(
        header.get("schema") == SCHEMA and header.get("kind") == "run",
        "missing bound run header",
    )
    _require(bool(rows), "bound journal has no rows")
    return header, rows


def _rational(value: object, field: str) -> Fraction:
    if not isinstance(value, str) or not value:
        raise CensusError(f"{field} must be a rational string")
    _require(len(value) <= 4096, f"{field} is too large")
    numerator, separator, denominator = value.partition("/")
    digits = numerator[1:] if numerator[:1] in ("+", "-") else numerator
    _require(bool(digits) and _ascii_digits(digits), f"{field} is not an exact rational")
    _require("/" not in denominator, f"{field} is not an exact rational")
    if separator:
        _require(
            bool(denominator) and _ascii_digits(denominator) and int(denominator) != 0,
            f"{field} is not an exact rational",
        )
        result = Fraction(int(numerator), int(denominator))
    else:
        result = Fraction(int(numerator))
    _require(result.denominator.bit_length() <= 16_384, f"{field} denominator is too large")
    _require(abs(result.numerator).bit_length() <= 16_384, f"{field} numerator is too large")
    return result


def _validate_row(
    raw: dict[str, Any],
    *,
    minima: list[int],
    evaluator: WitnessEvaluator,
    run_id: str | None,
) -> tuple[int, int]:
    row = _integer(raw.get("row"), "row")
    _require(row < len(minima), "row outside the census")
    _require(raw.get("mode") == "minimize", "row was not produced in minimize mode")
    minimum = _integer(raw.get("minimum"), f"row {row} minimum")
    recorded = _integer(raw.get("recorded"), f"row {row} recorded minimum")
    _require(minimum == recorded == minima[row], f"row {row} minimum mismatch")
    _require(raw.get("agree") is True, f"row {row} does not report agreement")
    witness = _list(raw.get("witness"), f"row {row} witness")
    _require(len(witness) == 2, f"row {row} witness")
    witness_x = _rational(witness[0], f"row {row} witness x")
    witness_y = _rational(witness[1], f"row {row} witness y")
    _require(
        raw.get("witness_replayed") is True,
        f"row {row} witness was not replayed by the producer",
    )
    _require(
        evaluator.charge(row, witness_x, witness_y) == minimum,
        f"row {row} witness fails independent exact replay",
    )
    for field in INTEGER_STATS:
        _integer(raw.get(field), f"row {row} {field}")
    if "max_heap" in raw:
        _integer(raw["max_heap"], f"row {row} max_heap")
    for field in ("seconds", "setup_seconds"):
        value = raw.get(field)
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise CensusError(f"row {row} {field}")
        _require(
            math.isfinite(value) and value >= 0,
            f"row {row} {field}",
        )
    if run_id is not None:
        _require(raw.get("binding_sha256") == run_id, f"row {row} has stale or mixed binding")
    return row, minimum


def _missing_ranges(rows: set[int], expected_rows: int) -> list[str]:
    missing = sorted(set(range(expected_rows)) - rows)
    if not missing:
        return []
    ranges: list[str] = []
    left = right = missing[0]
    for value in missing[1:]:
        if value == right + 1:
            right = value
            continue
        ranges.append(str(left) if left == right else f"{left}-{right}")
        left = right = value
    ranges.append(str(left) if left == right else f"{left}-{right}")
    return ranges


def _summary(
    rows: list[dict[str, Any]],
    certificate: dict[str, Any],
    reference: dict[str, Any],
    *,
    expected_rows: int,
    run_id: str | None,
    bound: bool,
    require_complete: bool,
) -> dict[str, object]:
    minima = _reference_rows(reference, expected_rows)
    evaluator = witness_evaluator(certificate, expected_rows)
    seen: set[int] = set()
    observed: list[int] = []
    for raw in rows:
        row, minimum = _validate_row(
            raw,
            minima=minima,
            evaluator=evaluator,
            run_id=run_id,
        )
        _require(row not in seen, f"duplicate result row: {row}")
        seen.add(row)
        observed.append(minimum)
    complete = seen == set(range(expected_rows))
    if require_complete:
        _require(complete, "complete replay requires exactly rows 0..12027")
    result: dict[str, object] = {
        "verdict": (
            "COMPLETE_ROW_EQUALITY"
            if bound and complete
            else "PARTIAL_ROW_EQUALITY"
            if bound
            else "UNBOUND_INVENTORY_ONLY"
        ),
        "bound_at_production": bound,
        "complete": complete,
        "rows_checked": len(seen),
        "expected_rows": expected_rows,
        "missing_rows": expected_rows - len(seen),
        "missing_ranges": _missing_ranges(seen, expected_rows),
        "sample_minimum": min(observed),
        "all_minima_match": True,
        "producer_reported_witness_replays": len(rows),
        "independent_exact_witness_replays": len(rows),
        "minimum_search_evidence": "pinned source branch-and-bound",
        "independent_witness_evidence": "exact attainment at the reported point",
        "independent_global_minimum_proof": False,
        "scope": "per-row exact minimum equality only",
        "global_counting_theorem_verified": False,
        "packing_bound_verified": False,
    }
    if complete:
        result["global_minimum"] = min(observed)
        result["global_minimum_matches_reference"] = min(observed) == min(minima)
    else:
        result["global_minimum"] = None
        result["global_minimum_matches_reference"] = False
    return result


def inspect_legacy(
    journal: Path,
    certificate_path: Path,
    reference_path: Path,
    *,
    expected_rows: int = EXPECTED_ROWS,
) -> dict[str, object]:
    """Structurally compare legacy rows without authenticating their producer."""
    journal_bytes = _read_journal(journal)
    certificate_bytes = _read_bytes(certificate_path)
    reference_bytes = _read_bytes(reference_path)
    certificate = _json(certificate_bytes, label=str(certificate_path))
    reference = _json(reference_bytes, label=str(reference_path))
    _require(isinstance(certificate, dict), "certificate must be a JSON object")
    _require(isinstance(reference, dict), "reference must be a JSON object")
    _require(
        _sha256(certificate_bytes) == PINNED_CERTIFICATE_SHA256,
        "certificate differs from the retained T-059 pin",
    )
    _require(
        _sha256(reference_bytes) == PINNED_REFERENCE_SHA256,
        "reference differs from the retained T-059 pin",
    )
    _require(
        reference.get("certificate_sha256") == _sha256(certificate_bytes),
        "reference is detached from the certificate",
    )
    _, rows = _documents(journal_bytes, bound=False)
    summary = _summary(
        rows,
        certificate,
        reference,
        expected_rows=expected_rows,
        run_id=None,
        bound=False,
        require_complete=False,
    )
    summary["journal_sha256"] = _sha256(journal_bytes)
    summary["certificate_sha256"] = _sha256(certificate_bytes)
    summary["reference_sha256"] = _sha256(reference_bytes)
    summary["warning"] = (
        "Legacy rows carry no production-time input/checker binding; "
        "agreement is inventory only."
    )
    return summary


def validate_bound(
    journal: Path,
    checker: Path,
    certificate_path: Path,
    reference_path: Path,
    *,
    require_complete: bool = False,
    expected_rows: int = EXPECTED_ROWS,
    expected_revision: str | None = PINNED_CHECKER_REVISION,
    expected_certificate_sha256: str | None = PINNED_CERTIFICATE_SHA256,
    expected_reference_sha256: str | None = PINNED_REFERENCE_SHA256,
    checker_files: tuple[str, ...] = CHECKER_FILES,
) -> dict[str, object]:
    """Validate a wrapper-produced journal against its still-pinned sources."""
    journal_bytes = _read_journal(journal)
    header, rows = _documents(journal_bytes, bound=True)
    assert header is not None
    snapshot = snapshot_sources(
        checker,
        certificate_path,
        reference_path,
        expected_rows=expected_rows,
        expected_revision=expected_revision,
        expected_certificate_sha256=expected_certificate_sha256,
        expected_reference_sha256=expected_reference_sha256,
        checker_files=checker_files,
    )
    _require(header.get("binding") == snapshot.binding, "run binding is stale or mixed")
    settings = _object(header.get("settings"), "missing run settings")
    _require(
        settings.get("python_isolated") is True and settings.get("python_optimize") == 0,
        "run did not bind isolated unoptimized Python",
    )
    requested = _list(settings.get("requested_rows"), "missing requested row inventory")
    requested_rows = [_integer(value, "requested row") for value in requested]
    _require(len(requested_rows) == len(set(requested_rows)), "duplicate requested row")
    _require(all(row < expected_rows for row in requested_rows), "requested row outside census")
    run_id = _sha256(_canonical({"binding": snapshot.binding, "settings": settings}))
    _require(header.get("binding_sha256") == run_id, "run binding digest mismatch")
    process = _object(header.get("process"), "missing process disposition")
    outcome = process.get("outcome")
    _require(outcome in ("COMPLETE", "TIMEOUT"), "invalid process disposition")
    observed_rows = {_integer(row.get("row"), "row") for row in rows}
    _require(observed_rows <= set(requested_rows), "journal contains an unrequested row")
    if outcome == "COMPLETE":
        _require(observed_rows == set(requested_rows), "completed run omitted requested rows")
    summary = _summary(
        rows,
        snapshot.certificate,
        snapshot.reference,
        expected_rows=expected_rows,
        run_id=run_id,
        bound=True,
        require_complete=require_complete,
    )
    summary["journal_sha256"] = _sha256(journal_bytes)
    summary["binding_sha256"] = run_id
    summary["process_outcome"] = outcome
    return summary


def _write_bound_journal(
    output: Path,
    *,
    header: dict[str, object],
    rows: list[dict[str, Any]],
    run_id: str,
    protected_paths: tuple[Path, ...],
) -> None:
    _require(not output.exists(), "output already exists; fresh runs never overwrite evidence")
    protected = {path.resolve() for path in protected_paths}
    _require(output.resolve() not in protected, "output may not overwrite an input")
    lines = [json.dumps(header, sort_keys=True)]
    lines.extend(json.dumps(row | {"binding_sha256": run_id}, sort_keys=True) for row in rows)
    encoded = ("\n".join(lines) + "\n").encode()
    output.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        dir=output.parent,
        prefix=f".{output.name}.",
        suffix=".tmp",
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(encoded)
            stream.flush()
            os.fsync(stream.fileno())
        try:
            os.link(temporary, output)
        except FileExistsError as error:
            raise CensusError(
                "output appeared during execution; refusing to overwrite"
            ) from error
    finally:
        temporary.unlink(missing_ok=True)


def _preflight_output(output: Path, checker: Path, certificate_directory: Path) -> None:
    resolved = output.resolve()
    _require(not output.exists(), "output already exists; fresh runs never overwrite evidence")
    _require(
        not resolved.is_relative_to(checker.resolve()),
        "output may not be inside the checker source tree",
    )
    _require(
        not resolved.is_relative_to(certificate_directory.resolve()),
        "output may not be inside the certificate source tree",
    )


def run_bound(
    checker: Path,
    certificate_directory: Path,
    output: Path,
    row_spec: str,
    *,
    max_seconds: float,
    leaf: int = 10,
    expected_rows: int = EXPECTED_ROWS,
    expected_revision: str | None = PINNED_CHECKER_REVISION,
    expected_certificate_sha256: str | None = PINNED_CERTIFICATE_SHA256,
    expected_reference_sha256: str | None = PINNED_REFERENCE_SHA256,
    checker_files: tuple[str, ...] = CHECKER_FILES,
) -> dict[str, object]:
    """Run the source checker under a wall ceiling and bind every resulting row."""
    _require(math.isfinite(max_seconds) and max_seconds > 0, "max-seconds must be positive")
    _require(type(leaf) is int and leaf > 0, "leaf must be a positive integer")
    _preflight_output(output, checker, certificate_directory)
    requested_rows = parse_rows(row_spec, expected_rows=expected_rows)
    certificate_path = certificate_directory / "global-certificate.json"
    reference_path = certificate_directory / "evidence/portable/python.json"
    before = snapshot_sources(
        checker,
        certificate_path,
        reference_path,
        expected_rows=expected_rows,
        expected_revision=expected_revision,
        expected_certificate_sha256=expected_certificate_sha256,
        expected_reference_sha256=expected_reference_sha256,
        checker_files=checker_files,
    )
    settings: dict[str, object] = {
        "requested_rows": requested_rows,
        "leaf": leaf,
        "max_seconds": max_seconds,
        "mode": "minimize",
        "python_isolated": True,
        "python_optimize": 0,
    }
    run_id = _sha256(_canonical({"binding": before.binding, "settings": settings}))
    with tempfile.TemporaryDirectory(prefix="general-pose-tree-") as directory:
        raw_output = Path(directory) / "rows.jsonl"
        command = [
            sys.executable,
            "-I",
            str(checker / "general_pose_tree/run_n11.py"),
            str(certificate_directory),
            str(raw_output),
            row_spec,
            "--leaf",
            str(leaf),
        ]
        outcome = "COMPLETE"
        returncode: int | None = 0
        stdout = b""
        stderr = b""
        try:
            completed = subprocess.run(
                command,
                check=False,
                capture_output=True,
                timeout=max_seconds,
            )
            returncode = completed.returncode
            stdout, stderr = completed.stdout, completed.stderr
            _require(returncode == 0, f"checker exited {returncode}")
        except subprocess.TimeoutExpired as error:
            outcome = "TIMEOUT"
            returncode = None
            stdout = error.stdout or b""
            stderr = error.stderr or b""
        _require(raw_output.is_file(), "checker produced no row journal")
        raw_bytes = _read_bytes(raw_output)
        _, rows = _documents(raw_bytes, bound=False)
    after = snapshot_sources(
        checker,
        certificate_path,
        reference_path,
        expected_rows=expected_rows,
        expected_revision=expected_revision,
        expected_certificate_sha256=expected_certificate_sha256,
        expected_reference_sha256=expected_reference_sha256,
        checker_files=checker_files,
    )
    _require(before.binding == after.binding, "checker or input changed during execution")
    header: dict[str, object] = {
        "schema": SCHEMA,
        "kind": "run",
        "binding": before.binding,
        "binding_sha256": run_id,
        "settings": settings,
        "process": {
            "outcome": outcome,
            "returncode": returncode,
            "stdout_sha256": _sha256(stdout),
            "stderr_sha256": _sha256(stderr),
        },
    }
    protected_paths = (
        certificate_path,
        reference_path,
        WRAPPER_SOURCE,
        *(checker / relative for relative in checker_files),
    )
    _write_bound_journal(
        output,
        header=header,
        rows=rows,
        run_id=run_id,
        protected_paths=protected_paths,
    )
    return validate_bound(
        output,
        checker,
        certificate_path,
        reference_path,
        require_complete=False,
        expected_rows=expected_rows,
        expected_revision=expected_revision,
        expected_certificate_sha256=expected_certificate_sha256,
        expected_reference_sha256=expected_reference_sha256,
        checker_files=checker_files,
    )


def _paths(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--checker", type=Path, required=True)
    parser.add_argument("--certificate-dir", type=Path, required=True)


def parser() -> argparse.ArgumentParser:
    command = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    subcommands = command.add_subparsers(dest="command", required=True)
    inspect = subcommands.add_parser("inspect", help="inspect unbound legacy JSONL")
    inspect.add_argument("journal", type=Path)
    inspect.add_argument("--certificate-dir", type=Path, required=True)
    validate = subcommands.add_parser("validate", help="validate a wrapper-bound journal")
    validate.add_argument("journal", type=Path)
    _paths(validate)
    validate.add_argument("--require-complete", action="store_true")
    pack = subcommands.add_parser("pack", help="gzip a journal deterministically for retention")
    pack.add_argument("journal", type=Path)
    pack.add_argument("output", type=Path)
    run = subcommands.add_parser("run", help="run the pinned checker and bind its rows")
    run.add_argument("output", type=Path)
    run.add_argument("rows")
    _paths(run)
    run.add_argument("--leaf", type=int, default=10)
    run.add_argument("--max-seconds", type=float, required=True)
    return command


def main(argv: list[str] | None = None) -> int:
    arguments = parser().parse_args(argv)
    try:
        if arguments.command == "inspect":
            directory = arguments.certificate_dir
            result = inspect_legacy(
                arguments.journal,
                directory / "global-certificate.json",
                directory / "evidence/portable/python.json",
            )
        elif arguments.command == "pack":
            result = pack_journal(arguments.journal, arguments.output)
        elif arguments.command == "validate":
            directory = arguments.certificate_dir
            result = validate_bound(
                arguments.journal,
                arguments.checker,
                directory / "global-certificate.json",
                directory / "evidence/portable/python.json",
                require_complete=arguments.require_complete,
            )
        else:
            result = run_bound(
                arguments.checker,
                arguments.certificate_dir,
                arguments.output,
                arguments.rows,
                max_seconds=arguments.max_seconds,
                leaf=arguments.leaf,
            )
    except (CensusError, OSError) as error:
        print(json.dumps({"verdict": "REFUSED", "reason": str(error)}, sort_keys=True))
        return 2
    print(json.dumps(result, indent=2, sort_keys=True))
    if arguments.command == "run" and result["complete"] is not True:
        return 3
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
