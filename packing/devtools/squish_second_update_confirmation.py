"""Bind issue 422's reviewed complete exact run to canonical publication artifacts.

Historical replay objects are retained unchanged. Canonical witness metadata is an
explicit publication transform whose complete ordered geometry must remain equal.
No acquisition, source producer execution or new exact replay is implied by retention.
"""

from __future__ import annotations

import argparse
import ast
import copy
import gzip
import hashlib
import json
import lzma
import re
import tempfile
from collections.abc import Iterable
from fractions import Fraction
from pathlib import Path, PurePosixPath
from typing import Any

import yaml
from strif import atomic_output_file

from devtools import squish_followup_packets as shared
from devtools import squish_second_update_packets as reported
from devtools import squish_upper_bound_packets as original
from sqpack.witness import load_witness, witness_document
from sqpack.yamlio import safe_load

REPO = original.REPO
PACKET = REPO / "packing/resources/web/squish-422-second-update-2026-10-07"
WITNESSES = REPO / "packing/witnesses/squish-422-second-update-2026"
SCHEMA = REPO / "packing/witnesses/witness.schema.yaml"
REVISION = reported.REVISION
NUMBERS = reported.NUMBERS
EXACT_EVIDENCE = "E-squish-second-update-2026-10-07-exact-replay"
CHECKERS = shared.CHECKERS
CHECKER_ROUTES = shared.CHECKER_ROUTES
JOBS = ("positive", "duplicate-square-overlap", "square-translated-outside-container")
FORMAT = "squish-second-update-exact-certification-v1"
CASE_FORMAT = "squish-second-update-reviewed-case-v1"
REPLAY_ORIGIN = "reused-complete-reviewed-422-replay"
MAX_REVIEW_ROSTER_BYTES = 16_000_000


def guard_output(path: Path) -> None:
    if not path.resolve().is_relative_to(REPO.resolve()):
        raise original.PacketError("confirmation output escapes the private checkout")


def save(path: Path, data: bytes) -> None:
    guard_output(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with atomic_output_file(path) as temporary:
        temporary.write_bytes(data)


def fact_path(n: int) -> Path:
    reported.source_url(n)
    return PACKET / "facts" / f"n-{n:03d}.json.gz"


def certificate_path(n: int) -> Path:
    reported.source_url(n)
    return WITNESSES / f"n-{n:03d}-rational.yaml.gz"


def case_path(n: int) -> Path:
    reported.source_url(n)
    return PACKET / "receipts" / f"n-{n:03d}.json.xz"


def private_input_paths() -> tuple[Path, ...]:
    """Exact scientific inputs copied privately before linking the nine proof outputs."""
    return (
        SCHEMA,
        *(fact_path(n) for n in NUMBERS),
        *(case_path(n) for n in NUMBERS),
        PACKET / "acquisition/sources.json",
        PACKET / "acquisition/frontier-comparison.json",
        PACKET / "receipts/certification.json.xz",
        PACKET / "receipts/replay-protocol.json",
        PACKET / "receipts/house-atlas-metadata.json.xz",
        PACKET / "reviews/math-review.md",
        PACKET / "reviews/receipt-binding-review.txt",
        PACKET / "reviews/math-review.json.xz",
        PACKET / "reviews/receipt-binding-review.json.xz",
        PACKET / "protocol/witness.schema.yaml",
        PACKET / "protocol/replay-adapter.py",
    )


def read_fact(n: int) -> dict[str, Any]:
    path = fact_path(n)
    if path.stat().st_size > original.MAX_SOURCE_BYTES:
        raise original.PacketError("compressed confirmation facts exceed ceiling")
    with gzip.open(path, "rb") as stream:
        raw = stream.read(original.MAX_SOURCE_BYTES + 1)
    if len(raw) > original.MAX_SOURCE_BYTES:
        raise original.PacketError("confirmation facts exceed ceiling")
    fact = json.loads(raw, object_pairs_hook=original.unique_json_object)
    if type(fact) is not dict or set(fact) != {"n", "side", "printed_side", "squares"}:
        raise original.PacketError("invalid confirmation fact schema")
    if type(fact["squares"]) is not list or any(
        type(square) is not dict or set(square) != {"x", "y", "t"} for square in fact["squares"]
    ):
        raise original.PacketError("invalid confirmation triple roster")
    source = {
        "n": fact["n"],
        "s_exact": fact["side"],
        "s_decimal": fact["printed_side"],
        "note": "Derived facts",
        "squares": [[square[k] for k in ("x", "y", "t")] for square in fact["squares"]],
    }
    with tempfile.TemporaryDirectory() as directory:
        temporary = Path(directory) / "source.json"
        temporary.write_bytes(shared.json_bytes(source))
        normalized, _ = original.parse_source(temporary, n)
    if shared.json_bytes(normalized) != shared.json_bytes(fact):
        raise original.PacketError("confirmation facts differ from normalized complete roster")
    return fact


def to_witness(fact: dict[str, Any]) -> dict[str, Any]:
    n = fact["n"]
    certificate_path(n)
    witness = original.to_witness(fact)
    witness["id"] = reported.witness_id(n)
    witness["source"] = {"path": fact_path(n).relative_to(REPO).as_posix()}
    witness["certificate"]["replay"] = (
        "uv run --frozen --all-extras --group dev python -m "
        f"devtools.squish_second_update_confirmation check-certification --replay --n {n}"
    )
    return witness


def transform_geometry(witness: dict[str, Any], name: str) -> dict[str, Any]:
    transformed = copy.deepcopy(witness)
    if name == JOBS[1]:
        transformed["squares"][1]["corners"] = copy.deepcopy(
            transformed["squares"][0]["corners"]
        )
    elif name == JOBS[2]:
        shift = max(Fraction(point[0]) for point in transformed["squares"][0]["corners"]) + 1
        for point in transformed["squares"][0]["corners"]:
            point[0] = str(Fraction(point[0]) - shift)
    elif name != JOBS[0]:
        raise original.PacketError("unknown full-roster confirmation job")
    return transformed


def canonical_witness(fact: dict[str, Any], name: str) -> dict[str, Any]:
    return _canonical_witness(to_witness(fact), name)


def _canonical_witness(positive: dict[str, Any], name: str) -> dict[str, Any]:
    witness = transform_geometry(positive, name)
    if name != JOBS[0]:
        witness["claim"]["coordinate_provenance"] = "reported"
        witness["claim"]["limitations"] = (
            "Full-roster negative control; exact feasibility must fail."
        )
    return witness


def metadata(witness: dict[str, Any]) -> dict[str, Any]:
    semantic_keys = set(original.checker_input(witness))
    return {key: value for key, value in witness.items() if key not in semantic_keys}


def _metadata_from_checked_input(
    witness: dict[str, Any], checked_input: dict[str, Any]
) -> dict[str, Any]:
    """Use the semantic keys from a completed whole-input normalization."""
    return {key: value for key, value in witness.items() if key not in checked_input}


def acquisition() -> dict[int, Any]:
    value = shared.read_review_json(PACKET / "acquisition/sources.json")
    if (
        value["source_commit"] != REVISION
        or value["source_key"] != reported.SOURCE_KEY
        or value["source_issue"] != "https://github.com/jlevy/squares/issues/422"
        or value["producer_checker_replayed"] is not False
    ):
        raise original.PacketError("confirmation acquisition identity mismatch")
    rows = shared.roster(value["cases"], NUMBERS)
    for n, row in rows.items():
        fact = read_fact(n)
        if (
            row["exact_side"] != fact["side"]
            or row["side"] != fact["printed_side"]
            or row["safe_ceiling_16"] != shared.display(fact["side"])
            or row["source_url"] != reported.source_url(n)
            or row["facts"] != fact_path(n).relative_to(REPO).as_posix()
            or row["reported_seed"] != reported.SEEDS[n]
            or type(row["source_bytes"]) is not int
            or not 1 <= row["source_bytes"] <= original.MAX_SOURCE_BYTES
            or type(row["source_sha256"]) is not str
            or re.fullmatch("[0-9a-f]{64}", row["source_sha256"]) is None
        ):
            raise original.PacketError("confirmation fact/acquisition/source-credit mismatch")
    return rows


def historical_witness(
    fact: dict[str, Any], pin: dict[str, Any], anchor: str, name: str
) -> dict[str, Any]:
    return _historical_witness(original.to_witness(fact), pin, anchor, name)


def _historical_witness(
    positive: dict[str, Any], pin: dict[str, Any], anchor: str, name: str
) -> dict[str, Any]:
    witness = transform_geometry(positive, name)
    witness["id"] = pin["witness_id_reserved"]
    witness["claim"]["coordinate_provenance"] = "reported"
    witness["claim"]["limitations"] = (
        "Prepared reported geometry; exact feasibility replay pending. No optimality claim."
    )
    witness["source"]["path"] = str(PurePosixPath(anchor).parent / pin["facts"])
    witness["certificate"]["replay"] = (
        "Run this prepared input with the separate explicit replay command."
    )
    return witness


def validate_job(
    row: Any, fact: dict[str, Any], pin: dict[str, Any], protocol: dict[str, Any], name: str
) -> None:
    expected = historical_witness(fact, pin, protocol["source_custody_anchor"], name)
    _validate_job(row, fact["n"], expected, protocol, name)


def _validate_job(
    row: Any, n: int, expected: dict[str, Any], protocol: dict[str, Any], name: str
) -> None:
    if (
        type(row) is not dict
        or type(row.get("n")) is not int
        or row["n"] != n
        or row.get("format") != "squish-second-update-dual-exact-replay-v1"
        or row.get("source_revision") != REVISION
        or row.get("control") != name
        or row.get("expectation") != ("pass" if name == JOBS[0] else "reject")
        or type(row.get("expected_pairs_per_checker")) is not int
        or row["expected_pairs_per_checker"] != n * (n - 1) // 2
        or row.get("expected_verdict_confirmed") is not True
        or row.get("witness_id") != expected["id"]
        or row.get("source_custody_anchor") != protocol["source_custody_anchor"]
        or shared.json_bytes(row.get("witness")) != shared.json_bytes(expected)
        or shared.json_bytes(row.get("checker_runtime"))
        != shared.json_bytes(protocol["historical_runtime"])
        or original.checker_input(row["checker_input"], receipt=True)
        != original.checker_input(expected)
    ):
        raise original.PacketError("historical full replay identity/provenance/input mismatch")
    shared.seconds(row["wall_seconds"])
    summary_job = next(
        job
        for job in protocol["historical_execution_summary"]["jobs"]
        if job["n"] == n and job["name"] == name
    )
    if row["wall_seconds"] != summary_job["dual_route_decision_wall_seconds"]:
        raise original.PacketError("receipt timing differs from complete summary")
    for checker in CHECKERS:
        shared.validate_verdict(row[checker], n, passed=name == JOBS[0])
    if name == JOBS[1] and not (
        any(
            type(failure) is str and "overlapping pairs" in failure
            for failure in row["independent"]["failures"]
        )
        and any(
            type(failure) is list and failure and failure[0] == "overlap"
            for failure in row["exact_verify"]["failures"]
        )
    ):
        raise original.PacketError("both overlap-control reasons are required")
    if name == JOBS[2] and any(
        shared.clearance(row[checker]["minimum_containment_clearance"]) >= 0
        for checker in CHECKERS
    ):
        raise original.PacketError("both containment-control negative clearances are required")


def reviewed_roster(path: Path) -> dict[tuple[int, str], Any]:
    with gzip.open(path, "rb") as stream:
        raw = stream.read(MAX_REVIEW_ROSTER_BYTES + 1)
    if len(raw) > MAX_REVIEW_ROSTER_BYTES:
        raise original.PacketError("complete review roster exceeds ceiling")
    rows = json.loads(raw, object_pairs_hook=original.unique_json_object)
    if type(rows) is not list or any(
        type(row) is not dict or type(row.get("n")) is not int for row in rows
    ):
        raise original.PacketError("invalid complete independent review roster")
    if [(row["n"], row.get("job")) for row in rows] != [
        (n, name) for n in NUMBERS for name in JOBS
    ]:
        raise original.PacketError("independent review requires all 27 ordered jobs")
    return {(row["n"], row["job"]): row for row in rows}


def validate_case(
    value: Any, n: int, admitted: dict[int, Any], protocol: dict[str, Any]
) -> dict[str, Any]:
    fact = read_fact(n)
    if (
        type(value) is not dict
        or value.get("format") != CASE_FORMAT
        or value.get("source_commit") != REVISION
        or type(value.get("n")) is not int
        or value["n"] != n
        or shared.json_bytes(value.get("acquisition")) != shared.json_bytes(admitted[n])
    ):
        raise original.PacketError("canonical retained-case acquisition mismatch")
    pin = next(row for row in protocol["source_custody"]["cases"] if row["n"] == n)
    if (
        pin["source_sha256"] != admitted[n]["source_sha256"]
        or pin["source_bytes"] != admitted[n]["source_bytes"]
        or pin["exact_side"] != fact["side"]
        or pin["source_print"] != fact["printed_side"]
        or pin["source_url"] != reported.source_url(n)
        or pin["witness_id_reserved"] != reported.witness_id(n)
    ):
        raise original.PacketError("historical custody differs from canonical acquisition")
    rows = value["historical_actual_receipts"]
    if type(rows) is not list or len(rows) != len(JOBS):
        raise original.PacketError("retained case requires all three actual replay jobs")
    transforms = value["canonicalization"]
    if type(transforms) is not list or len(transforms) != len(JOBS):
        raise original.PacketError("retained case requires explicit canonical transforms")
    reviews = value["independent_review_inputs"]
    if type(reviews) is not dict or set(reviews) != {"math", "binding"}:
        raise original.PacketError(
            "both distinct complete independent input reviews are required"
        )
    # Derive rational corners once for this case, then copy each full-roster variant.
    # The baseline is private to this admission; later invocations read facts afresh.
    positive = to_witness(fact)
    for name, actual, transform in zip(JOBS, rows, transforms, strict=True):
        expected = _historical_witness(positive, pin, protocol["source_custody_anchor"], name)
        _validate_job(actual, n, expected, protocol, name)
        canonical = _canonical_witness(positive, name)
        historical = actual["witness"]
        historical_input = original.checker_input(historical)
        canonical_input = original.checker_input(canonical)
        expected_transform = {
            "kind": "canonical-publication-metadata-v1",
            "job": name,
            "historical_metadata": _metadata_from_checked_input(historical, historical_input),
            "canonical_metadata": _metadata_from_checked_input(canonical, canonical_input),
        }
        if (
            shared.json_bytes(transform) != shared.json_bytes(expected_transform)
            or historical_input != canonical_input
        ):
            raise original.PacketError(
                "canonical transformation changed geometry or misstates metadata"
            )
    for reviewer, entries in reviews.items():
        if type(entries) is not list or len(entries) != len(JOBS):
            raise original.PacketError("independent case review requires three complete jobs")
        for name, entry, actual in zip(JOBS, entries, rows, strict=True):
            if (
                type(entry) is not dict
                or type(entry.get("n")) is not int
                or entry["n"] != n
                or entry.get("job") != name
                or shared.json_bytes(entry.get("checker_input"))
                != shared.json_bytes(actual["checker_input"])
                or (
                    reviewer == "binding"
                    and shared.json_bytes(entry.get("witness"))
                    != shared.json_bytes(actual["witness"])
                )
            ):
                raise original.PacketError(
                    "canonical case differs from complete independent review"
                )
    return positive


def validate_protocol(protocol: dict[str, Any], admitted: dict[int, Any]) -> None:
    """Admit historical runtime roles, complete job summary and source attribution."""
    runtime = protocol["historical_runtime"]
    historical = "/workspace/squares-422-exact-replay-preparation"
    expected_runtime = {
        "adapter_module": historical + "/runtime/devtools/squish_upper_bound_packets.py",
        "independent_module": "/workspace/squares-confirmation/packing/devtools/"
        "check_rational_witness_independent.py",
        "exact_verify_module": "/workspace/squares-confirmation/packing/src/sqpack/witness.py",
        "executable": "/workspace/squares/packing/.venv/bin/python3",
        "python": "3.14.7 (main, Sep 24 2026, 17:58:18) [Clang 22.1.3 ]",
        "routes": CHECKER_ROUTES,
        "schema_selected": historical + "/base/witness.schema.yaml",
        "schema_retained": "runtime/witness.schema.yaml",
    }
    summary = protocol["historical_execution_summary"]
    if (
        runtime != expected_runtime
        or protocol["source_custody_anchor"]
        != "/workspace/squares-422-import-preparation/source-pin.json"
        or summary["source_revision"] != REVISION
        or summary["source_producer_executed"] is not False
        or summary["feasibility_checked"] is not True
        or summary["observed_checker_runtime"] != runtime
        or summary["positive_pairs_per_checker"] != 190303
        or type(summary["positive_pairs_per_checker"]) is not int
        or summary["all_job_pairs_per_checker"] != 570909
        or type(summary["all_job_pairs_per_checker"]) is not int
        or type(summary["jobs"]) is not list
        or len(summary["jobs"]) != 27
    ):
        raise original.PacketError("historical runtime or complete summary mismatch")
    times = []
    for job, (n, name) in zip(
        summary["jobs"], ((n, name) for n in NUMBERS for name in JOBS), strict=True
    ):
        if (
            type(job["n"]) is not int
            or job["n"] != n
            or job["name"] != name
            or type(job["pairs_per_checker"]) is not int
            or job["pairs_per_checker"] != n * (n - 1) // 2
        ):
            raise original.PacketError("historical summary job scope mismatch")
        times.append(shared.seconds(job["dual_route_decision_wall_seconds"]))
    if summary["sum_dual_route_decision_wall_seconds"] != sum(times):
        raise original.PacketError("historical job timing sum mismatch")
    pins = shared.roster(protocol["source_custody"]["cases"], NUMBERS)
    for n, pin in pins.items():
        fact = read_fact(n)
        if (
            pin["reported_seed"] != admitted[n]["reported_seed"]
            or pin["safe_ceiling_16"] != shared.display(fact["side"])
            or pin["sourceprint_below_exact"]
            is not (Fraction(fact["printed_side"]) < Fraction(fact["side"]))
            or pin["facts"] != f"facts/n-{n:03d}.json.gz"
            or type(pin["source_git_blob_sha"]) is not str
            or re.fullmatch("[0-9a-f]{40}", pin["source_git_blob_sha"]) is None
        ):
            raise original.PacketError("historical source credit/custody mismatch")


def validate_review_records(protocol: dict[str, Any]) -> None:
    """Keep both final reviews associated with this complete historical execution."""
    math = shared.read_xz_receipt(PACKET / "reviews/math-review.json.xz")
    binding = shared.read_xz_receipt(PACKET / "reviews/receipt-binding-review.json.xz")
    if (
        math["format"] != "squish-422-independent-mathematics-receipt-review-v1"
        or math["status"] != "accepted-exact-feasibility-evidence"
        or math["source_revision"] != REVISION
        or math["numbers"] != list(NUMBERS)
        or any(type(n) is not int for n in math["numbers"])
        or math["positive_jobs"] != 9
        or math["invalid_control_jobs"] != 18
        or math["route_results_reviewed"] != 54
        or math["all_jobs_pair_decisions_both_routes"] != 1141818
        or math["child_process_exit_statuses"] != [0] * 27
        or any(type(code) is not int for code in math["child_process_exit_statuses"])
        or type(math["outer_exit_status"]) is not int
        or math["outer_exit_status"] != 0
        or math["deciders_rerun_for_review"] is not False
        or math["runtime"]["routes"] != CHECKER_ROUTES
        or math["runtime"]["python"] != protocol["historical_runtime"]["python"]
        or binding["format"] != "issue422-independent-binding-actual-receipt-review-v1"
        or binding["disposition"] != "ACCEPT_COMPLETE_NINE_EXACT_FEASIBLE_UPPER_BOUNDS"
        or binding["source_revision"] != REVISION
        or binding["numbers"] != list(NUMBERS)
        or any(type(n) is not int for n in binding["numbers"])
        or binding["jobs"] != 27
        or binding["positive_jobs_accepted_by_both_routes"] != 9
        or binding["full_roster_control_jobs_rejected_by_both_routes"] != 18
        or binding["runtime"] != protocol["historical_runtime"]
        or binding["review_reran_deciders"] is not False
        or binding["source_producer_executed"] is not False
        or type(binding["outer_batch_exit_code"]) is not int
        or binding["outer_batch_exit_code"] != 0
        or type(binding["all_27_child_exit_codes"]) is not int
        or binding["all_27_child_exit_codes"] != 0
    ):
        raise original.PacketError("both distinct final receipt acceptances are required")
    for record, fields in (
        (
            math,
            {
                "triples": 1762,
                "positive_corners": 7048,
                "positive_pairs_per_route": 190303,
                "all_jobs_pairs_per_route": 570909,
                "all_jobs_pair_decisions_both_routes": 1141818,
            },
        ),
        (
            binding,
            {
                "rational_triples": 1762,
                "positive_pairs_per_route": 190303,
                "all_job_pairs_per_route": 570909,
                "all_pairs_across_both_routes": 1141818,
            },
        ),
    ):
        if any(
            type(record[key]) is not int or record[key] != value
            for key, value in fields.items()
        ):
            raise original.PacketError("final review scope/count metadata mismatch")
    total = protocol["historical_execution_summary"]["sum_dual_route_decision_wall_seconds"]
    if (
        math["timing"]["sum_dual_route_decision_wall_seconds"] != total
        or math["timing"]["parallel_batch_elapsed_seconds"] is not None
        or binding["sum_per_job_dual_route_decision_wall_seconds"] != total
        or binding["parallel_batch_elapsed_seconds"] is not None
    ):
        raise original.PacketError("final review timing scope differs from actual summary")
    if safe_load((PACKET / "protocol/witness.schema.yaml").read_text()) != safe_load(
        SCHEMA.read_text()
    ):
        raise original.PacketError("retained historical schema differs from trusted schema")
    archive = ast.parse((PACKET / "protocol/replay-adapter.py").read_text())
    decide = next(
        node
        for node in archive.body
        if isinstance(node, ast.FunctionDef) and node.name == "decide"
    )
    # Require the reviewed schema call before normalizing it for body comparison.
    calls = [
        node
        for node in ast.walk(decide)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "witness_document"
    ]
    expected_schema = ast.dump(ast.parse("SCHEMA.as_posix()", mode="eval").body)
    if (
        len(calls) != 1
        or len(calls[0].keywords) != 1
        or calls[0].keywords[0].arg != "schema"
        or ast.dump(calls[0].keywords[0].value) != expected_schema
    ):
        raise original.PacketError("historical adapter does not select its absolute schema")
    calls[0].keywords = []
    trusted = ast.parse(Path(original.__file__).read_text())
    expected = next(
        node
        for node in trusted.body
        if isinstance(node, ast.FunctionDef) and node.name == "decide"
    )
    for node in ast.walk(expected):
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "witness_document"
        ):
            node.keywords = [keyword for keyword in node.keywords if keyword.arg != "schema"]
    if ast.dump(decide, include_attributes=False) != ast.dump(
        expected, include_attributes=False
    ):
        raise original.PacketError("archived historical decide body differs from trusted route")


def protocol_record(review_root: Path) -> dict[str, Any]:
    summary = shared.read_review_json(review_root / "replay-summary.json")
    custody = shared.read_review_json(review_root / "source-custody.json")
    first = shared.read_review_json(review_root / "receipts/n-088-positive.json")
    if (
        summary["source_revision"] != REVISION
        or summary["feasibility_checked"] is not True
        or custody["source_commit"] != REVISION
        or [row["n"] for row in custody["cases"]] != list(NUMBERS)
        or (review_root / "batch-replay.exit-status").read_text().strip() != "0"
    ):
        raise original.PacketError("reviewed complete batch did not terminate successfully")
    protocol = {
        "replay_origin": REPLAY_ORIGIN,
        "source_commit": REVISION,
        "source_custody_anchor": first["source_custody_anchor"],
        "source_custody": custody,
        "historical_runtime": first["checker_runtime"],
        "historical_execution_summary": summary,
        "batch_exit_code": 0,
        "producer_checker_replayed": False,
        "geometry_binding": (
            "Complete ordered checker-input equality; canonical metadata is a distinct object."
        ),
    }

    validate_protocol(protocol, acquisition())
    return protocol


def retain_reviewed_replay(review_root: Path, math_root: Path, binding_root: Path) -> None:
    admitted = acquisition()
    protocol = protocol_record(review_root)
    math_inputs = reviewed_roster(math_root / "reviewed-checker-inputs.json.gz")
    binding_inputs = reviewed_roster(binding_root / "reviewed-complete-inputs.json.gz")
    outputs: dict[Path, bytes] = {}
    cases = []
    for n in NUMBERS:
        fact = read_fact(n)
        raw_fact, raw = original.parse_source(
            review_root / "raw_original" / f"n-{n:03d}.cert.json", n
        )
        pin = next(row for row in protocol["source_custody"]["cases"] if row["n"] == n)
        if (
            raw_fact != fact
            or len(raw) != pin["source_bytes"]
            or hashlib.sha256(raw).hexdigest() != pin["source_sha256"]
            or hashlib.sha1(f"blob {len(raw)}\0".encode() + raw).hexdigest()
            != pin["source_git_blob_sha"]
        ):
            raise original.PacketError(
                "raw reviewed source differs from canonical facts/custody"
            )
        actual = [
            shared.read_review_json(review_root / "receipts" / f"n-{n:03d}-{name}.json")
            for name in JOBS
        ]
        value = {
            "format": CASE_FORMAT,
            "source_commit": REVISION,
            "n": n,
            "acquisition": admitted[n],
            "historical_actual_receipts": actual,
            "independent_review_inputs": {
                "math": [math_inputs[n, name] for name in JOBS],
                "binding": [binding_inputs[n, name] for name in JOBS],
            },
            "canonicalization": [
                {
                    "kind": "canonical-publication-metadata-v1",
                    "job": name,
                    "historical_metadata": metadata(row["witness"]),
                    "canonical_metadata": metadata(canonical_witness(fact, name)),
                }
                for name, row in zip(JOBS, actual, strict=True)
            ],
        }
        witness = validate_case(value, n, admitted, protocol)
        data = shared.json_bytes(value)
        if len(data) > original.MAX_RECEIPT_BYTES:
            raise original.PacketError(
                "one complete retained case exceeds the existing receipt ceiling"
            )
        outputs[case_path(n)] = lzma.compress(data)
        outputs[certificate_path(n)] = gzip.compress(
            witness_document(witness, schema="../witness.schema.yaml").encode(), mtime=0
        )
        cases.append(
            {
                "n": n,
                "receipt": case_path(n).relative_to(PACKET).as_posix(),
                "certificate": certificate_path(n).relative_to(REPO).as_posix(),
                "verified_value": shared.display(fact["side"]),
                "exact_form": fact["side"],
                "side_inflation": "0",
            }
        )
    index = {
        "format": FORMAT,
        "source_commit": REVISION,
        "replay_origin": REPLAY_ORIGIN,
        "counts": list(NUMBERS),
        "squares": sum(NUMBERS),
        "checkers": CHECKER_ROUTES,
        "positive_pairs_per_checker": sum(n * (n - 1) // 2 for n in NUMBERS),
        "all_job_pairs_per_checker": 3 * sum(n * (n - 1) // 2 for n in NUMBERS),
        "producer_checker_replayed": False,
        "protocol": "receipts/replay-protocol.json",
        "cases": cases,
    }
    outputs[PACKET / "receipts/replay-protocol.json"] = shared.json_bytes(protocol)
    outputs[PACKET / "receipts/certification.json.xz"] = lzma.compress(shared.json_bytes(index))
    outputs[PACKET / "reviews/math-review.md"] = (
        math_root / "issue-422-exact-feasibility-review.md"
    ).read_bytes()
    outputs[PACKET / "reviews/receipt-binding-review.txt"] = (
        binding_root / "publication-review.txt"
    ).read_bytes()
    outputs[PACKET / "reviews/math-review.json.xz"] = lzma.compress(
        (math_root / "final-receipt-review.json").read_bytes()
    )
    outputs[PACKET / "reviews/receipt-binding-review.json.xz"] = lzma.compress(
        (binding_root / "actual-receipt-review.json").read_bytes()
    )
    outputs[PACKET / "protocol/witness.schema.yaml"] = (
        review_root / "runtime/witness.schema.yaml"
    ).read_bytes()
    outputs[PACKET / "protocol/replay-adapter.py"] = (
        review_root / "runtime/devtools/squish_upper_bound_packets.py"
    ).read_bytes()
    for path in outputs:
        guard_output(path)
    for path, data in outputs.items():
        save(path, data)


def admit_certification() -> dict[int, Any]:
    if any(not path.resolve().is_relative_to(REPO.resolve()) for path in private_input_paths()):
        raise original.PacketError("private confirmation input escapes the worker checkout")
    admitted = acquisition()
    index = shared.read_xz_receipt(PACKET / "receipts/certification.json.xz")
    if (
        index["format"] != FORMAT
        or index["source_commit"] != REVISION
        or index["replay_origin"] != REPLAY_ORIGIN
        or index["counts"] != list(NUMBERS)
        or any(type(n) is not int for n in index["counts"])
        or index["checkers"] != CHECKER_ROUTES
        or index["producer_checker_replayed"] is not False
        or type(index["squares"]) is not int
        or index["squares"] != sum(NUMBERS)
        or type(index["positive_pairs_per_checker"]) is not int
        or index["positive_pairs_per_checker"] != sum(n * (n - 1) // 2 for n in NUMBERS)
        or type(index["all_job_pairs_per_checker"]) is not int
        or index["all_job_pairs_per_checker"] != 3 * sum(n * (n - 1) // 2 for n in NUMBERS)
        or index["protocol"] != "receipts/replay-protocol.json"
    ):
        raise original.PacketError("confirmation index scope/revision/route mismatch")
    protocol = shared.read_review_json(PACKET / index["protocol"])
    if (
        protocol["source_commit"] != REVISION
        or protocol["replay_origin"] != REPLAY_ORIGIN
        or protocol["batch_exit_code"] != 0
        or type(protocol["batch_exit_code"]) is not int
        or protocol["producer_checker_replayed"] is not False
        or protocol["source_custody"]["source_commit"] != REVISION
        or [row["n"] for row in protocol["source_custody"]["cases"]] != list(NUMBERS)
    ):
        raise original.PacketError("retained replay protocol mismatch")
    validate_protocol(protocol, admitted)
    validate_review_records(protocol)
    rows = shared.roster(index["cases"], NUMBERS)
    for n, row in rows.items():
        fact = read_fact(n)
        if (
            row["receipt"] != case_path(n).relative_to(PACKET).as_posix()
            or row["certificate"] != certificate_path(n).relative_to(REPO).as_posix()
            or row["verified_value"] != shared.display(fact["side"])
            or row["exact_form"] != fact["side"]
            or row["side_inflation"] != "0"
        ):
            raise original.PacketError("canonical proof path or safe bound mismatch")
        case = shared.read_xz_receipt(case_path(n))
        validate_case(case, n, admitted, protocol)
        row["case"] = case
    return rows


def read_certificate(n: int) -> dict[str, Any]:
    path = certificate_path(n)
    if path.stat().st_size > original.MAX_RECEIPT_BYTES:
        raise original.PacketError("compressed canonical certificate exceeds ceiling")
    with gzip.open(path, "rb") as stream:
        data = stream.read(original.MAX_RECEIPT_BYTES + 1)
    if len(data) > original.MAX_RECEIPT_BYTES:
        raise original.PacketError("canonical certificate exceeds ceiling")
    document = safe_load(data.decode())
    if not isinstance(document, dict) or document.get("softschema") != {
        "schema": "../witness.schema.yaml",
        "contract": "packing.squares:Witness/v2",
        "envelope": "witness",
        "status": "enforced",
    }:
        raise original.PacketError("canonical witness must name its canonical schema")
    with tempfile.TemporaryDirectory() as directory:
        temporary = Path(directory) / "certificate.yaml"
        temporary.write_text(witness_document(document["witness"], schema=SCHEMA.as_posix()))
        return dict(load_witness(temporary, fallback_schema=SCHEMA))


def decide(witness: dict[str, Any]) -> dict[str, Any]:
    """Explicit fresh replay using both trusted routes and the selected private schema."""
    witness = {**witness, **original.checker_input(witness)}
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "certificate.yaml"
        path.write_text(witness_document(witness, schema=SCHEMA.as_posix()))
        corner = original.independent.check(path)
        exact, _report = original.exact_verify(load_witness(path, fallback_schema=SCHEMA))
    keys = (
        "verification_passed",
        "n",
        "pairs_tested",
        "minimum_containment_clearance",
        "failures",
    )
    return json.loads(
        shared.json_bytes(
            {
                "independent": {key: corner[key] for key in keys},
                "exact_verify": {key: exact[key] for key in keys},
            }
        )
    )


def check_certification(
    numbers: list[int] | None = None, *, replay: bool = False
) -> dict[int, Any]:
    selected = list(NUMBERS) if numbers is None else numbers
    if (
        not selected
        or any(type(n) is not int or n not in NUMBERS for n in selected)
        or len(set(selected)) != len(selected)
    ):
        raise original.PacketError("empty, repeated or unknown canonical confirmation scope")
    rows = admit_certification()
    for n in selected:
        _check_certificate(n)
        if replay:
            for name, retained in zip(
                JOBS, rows[n]["case"]["historical_actual_receipts"], strict=True
            ):
                if decide(canonical_witness(read_fact(n), name)) != {
                    key: retained[key] for key in CHECKERS
                }:
                    raise original.PacketError(
                        "canonical replay differs from historical exact verdict"
                    )
    return rows


def _check_certificate(n: int) -> None:
    expected = to_witness(read_fact(n))
    actual = read_certificate(n)
    if shared.json_bytes(actual) != shared.json_bytes(expected):
        raise original.PacketError("canonical whole witness metadata/geometry mismatch")


def restore_witnesses() -> None:
    rows = admit_certification()
    outputs = {
        certificate_path(n): gzip.compress(
            witness_document(
                to_witness(read_fact(n)), schema="../witness.schema.yaml"
            ).encode(),
            mtime=0,
        )
        for n in rows
    }
    for path in outputs:
        guard_output(path)
    for path, data in outputs.items():
        save(path, data)


def linked_certificate_problem(path: str, *, repository: Path) -> str | None:
    return linked_certificate_problems([path], repository=repository)[path]


def linked_certificate_problems(
    paths: Iterable[str], *, repository: Path
) -> dict[str, str | None]:
    """Admit one invocation's complete custody, then check every selected leaf freshly."""
    selected = dict.fromkeys(paths)
    if repository.resolve() != REPO.resolve() or not WITNESSES.is_symlink():
        return dict.fromkeys(selected, "resolves outside the repository")
    declared = {certificate_path(n).relative_to(REPO).as_posix(): n for n in NUMBERS}
    eligible: dict[str, int] = {}
    problems: dict[str, str | None] = {}
    for path in selected:
        n = declared.get(path)
        if n is None or certificate_path(n).is_symlink():
            problems[path] = "resolves outside the repository"
        else:
            eligible[path] = n
    if not eligible:
        return problems
    try:
        _ = admit_certification()
    except (original.PacketError, OSError, KeyError, TypeError, ValueError) as error:
        problems.update(
            dict.fromkeys(eligible, f"linked second-update proof custody mismatch: {error}")
        )
        return problems
    for path, n in eligible.items():
        try:
            _check_certificate(n)
        except (original.PacketError, OSError, KeyError, TypeError, ValueError) as error:
            problems[path] = f"linked second-update proof custody mismatch: {error}"
        else:
            problems[path] = None
    return problems


def confirmed_bound(n: int) -> dict[str, Any]:
    return _bound(check_certification([n])[n])


def _bound(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "value": row["verified_value"],
        "exact_form": row["exact_form"],
        "evidence": [EXACT_EVIDENCE],
    }


def adopt_verified(n: int, existing: str, generated: str | None = None) -> str:
    """Publish an admitted ceiling while preserving the report's complete history."""
    return _adopt_verified(n, existing, generated, confirmed_bound(n))


def _adopt_verified(n: int, existing: str, generated: str | None, bound: dict[str, Any]) -> str:
    """Apply one bound from the caller's completed full certification admission."""
    from devtools import render_case_verifiers  # noqa: PLC0415

    document = safe_load(existing.split("---\n", 2)[1])
    case = document["packing"]
    if (
        type(case["n"]) is not int
        or case["n"] != n
        or case["reported_upper_bound"]["source_key"] != reported.SOURCE_KEY
    ):
        raise original.PacketError("confirmation case is not the selected second update")
    declarations = case["verified_upper_bound"]["evidence"]
    if any(
        evidence.startswith("E-squish-second-update-") and evidence != EXACT_EVIDENCE
        for evidence in declarations
    ):
        raise original.PacketError("unmapped second-update confirmation evidence")
    prior = reported.prior_lanes()[n]
    expected = bound if EXACT_EVIDENCE in declarations else prior["prior_verified"]
    if case["verified_upper_bound"] != expected:
        raise original.PacketError(
            "selected confirmation ceiling differs from admitted evidence"
        )
    # Direct re-publication of the same confirmed pose keeps its owned assessment.
    # A generator draft leaves assessment to its separate promotion step, and initial
    # confirmation cannot transfer rigidity from the earlier geometry.
    current_rigidity = (
        copy.deepcopy(case["rigidity"])
        if generated is None and EXACT_EVIDENCE in declarations
        else None
    )
    # The reported-only owner still rebuilds its own report and lower/history lanes.
    # Its temporary older verified lane is replaced only after complete admission.
    case["verified_upper_bound"] = copy.deepcopy(prior["prior_verified"])
    body = existing.split("---\n", 2)[2]
    provisional = (
        "---\n"
        + yaml.safe_dump(document, sort_keys=False, allow_unicode=True, width=98)
        + "---\n"
        + body
    )
    adapted = reported.adopt_report(n, provisional, generated)
    _, front, body = adapted.split("---\n", 2)
    body = body.replace(
        "## Earlier SQUISH update\n\nNate Chaoweeraprasit",
        "## Earlier SQUISH update\n\nPreviously, Nate Chaoweeraprasit",
    )
    document = safe_load(front)
    case = document["packing"]
    case["verified_upper_bound"] = bound
    case["rigidity"] = current_rigidity
    conjecture = prior["prior_conjectured_optimum"]
    if conjecture is not None and Fraction(bound["exact_form"]) < Fraction(conjecture):
        pending_claim = (
            f"Earlier conjectured optimum s({n}) = {conjecture}; the smaller second-update "
            "report is pending confirmation, and no current optimum is conjectured."
        )
        case["priority_notes"] = [
            note for note in case["priority_notes"] if note["claim"] != pending_claim
        ]
        refuted_claim = (
            f"Earlier conjectured optimum s({n}) = {conjecture} is refuted by the "
            f"confirmed feasible upper bound {bound['value']}; the earlier packing, "
            "source credit and certificate remain historical evidence. No new optimum "
            "is conjectured or established."
        )
        if not any(note["claim"] == refuted_claim for note in case["priority_notes"]):
            case["priority_notes"].append(
                {
                    "claim": refuted_claim,
                    "claimed_by": prior["prior_reported"]["found_by"],
                    "published": None,
                    "year": prior["prior_reported"]["found_year"],
                }
            )
    if EXACT_EVIDENCE not in case["evidence"]:
        case["evidence"].append(EXACT_EVIDENCE)
    case["blockers"] = [
        blocker
        for blocker in case["blockers"]
        if not (
            blocker["kind"] == "mathematics"
            and blocker.get("evidence") == [reported.EVIDENCE_ID]
            and blocker["detail"].startswith("The second SQUISH update is reported only;")
        )
    ]
    fact = read_fact(n)
    seed = reported.SEEDS[n].replace("'", chr(0x2019))
    section = (
        f"{reported.HEADING}\n\nNate Chaoweeraprasit, using SQUISH,\n"
        "[reports this packing](https://github.com/jlevy/squares/issues/422):\n"
        f"$s({n}) \\le {bound['value']}$, with exact side ${fact['side']}$.\n"
        "Two independently implemented exact rational SAT routes accepted the complete\n"
        "packing and rejected both complete-roster controls. Two separately prompted\n"
        "AI reviews accepted the mathematical inputs and full receipt bindings.\n"
        f"The author reports the seed as {seed}.\n\n"
        "The [revision-specific packet]"
        "(../resources/web/squish-422-second-update-2026-10-07/README.md)\n"
        f"retains the source print ${fact['printed_side']}$ separately from the verified\n"
        "upward decimal ceiling. The exact side is unchanged; this certifies feasibility\n"
        "and an upper bound, without optimality, rigidity or human oversight claims.\n"
        "Earlier source geometry, certificates, credit and verification lanes remain\n"
        "historical evidence for their own packings.\n\n"
        f"{reported.REPORT_END}\n\n"
    )
    body, count = re.subn(
        rf"{re.escape(reported.HEADING)}\n.*?{re.escape(reported.REPORT_END)}\n+",
        lambda _: section,
        body,
        flags=re.DOTALL,
    )
    if count != 1:
        raise original.PacketError("confirmation needs exactly one current report section")
    rendered = render_case_verifiers.refresh(
        "---\n"
        + yaml.safe_dump(document, sort_keys=False, allow_unicode=True, width=98)
        + "---\n"
        + body
    )
    if current_rigidity is not None:
        from devtools.assess_frontier_rigidity import preserve_block_rendering  # noqa: PLC0415

        rendered = preserve_block_rendering(existing, rendered, n)
    return rendered


def main() -> None:
    parser = argparse.ArgumentParser(allow_abbrev=False)
    commands = parser.add_subparsers(dest="command", required=True)
    retain = commands.add_parser("retain-reviewed-replay", allow_abbrev=False)
    retain.add_argument("--review-root", type=Path, required=True)
    retain.add_argument("--math-review-root", type=Path, required=True)
    retain.add_argument("--binding-review-root", type=Path, required=True)
    check = commands.add_parser("check-certification", allow_abbrev=False)
    check.add_argument("--n", type=int, choices=NUMBERS, action="append")
    check.add_argument("--replay", action="store_true")
    _ = commands.add_parser("restore-witnesses", allow_abbrev=False)
    _ = commands.add_parser("record", allow_abbrev=False)
    args = parser.parse_args()
    if args.command == "retain-reviewed-replay":
        retain_reviewed_replay(
            args.review_root, args.math_review_root, args.binding_review_root
        )
    elif args.command == "check-certification":
        _ = check_certification(args.n, replay=args.replay)
    elif args.command == "record":
        rows = check_certification()
        outputs = {
            REPO / f"packing/frontier/n-{n:03d}.md": _adopt_verified(
                n,
                (REPO / f"packing/frontier/n-{n:03d}.md").read_text(),
                None,
                _bound(rows[n]),
            ).encode()
            for n in NUMBERS
        }
        for path in outputs:
            guard_output(path)
        for path, data in outputs.items():
            save(path, data)
    else:
        restore_witnesses()


if __name__ == "__main__":
    main()
