"""Retain pinned SQUISH facts and bind a reviewed complete exact replay.

Use ``acquire --source PATH`` for the upstream submission directory, then ``check``.
``retain-reviewed-replay`` admits a completed independent review run, without claiming
a new execution. ``check-certification --replay`` explicitly repeats the exact decisions.
The upstream producer and its checker are never executed.
"""

from __future__ import annotations

import argparse
import copy
import gzip
import hashlib
import json
import lzma
import math
import re
import sys
import tempfile
from collections.abc import Iterable
from fractions import Fraction
from pathlib import Path
from typing import Any

from strif import atomic_output_file

from devtools import squish_upper_bound_packets as original
from sqpack.witness import load_witness, witness_document

REPO = original.REPO
PACKET = REPO / "packing/resources/web/squish-401-update-2026-10-07"
REVISION = "5e32bbd7028b6e3b869979278079cd37ed6770aa"
NUMBERS = (123, 126, 129, 153, 154, 155, 179, 208, 237, 238, 239, 258, 263)
NEW_NUMBERS = (123, 179, 208, 237, 239, 258, 263)
REPLACEMENTS = (126, 129, 154, 155, 238)
SOURCE_KEY = "[SQUISH update 2026-10-07]"
SOURCE_ROOT = (
    f"https://github.com/itsnaka/squish-certs/blob/{REVISION}/squish-submission-2026-10-07"
)
RETRIEVED = "2026-10-07"
DISPLAY_PLACES = 16
# Author-reported seed attribution, from issue 401's pinned update comment.
SEEDS = {
    123: "Francisco Couzo's s(102), grafted into n's Kingbird record",
    126: "Francisco Couzo's s(105), grafted into n's Kingbird record",
    129: "Francisco Couzo's s(131), squares removed",
    153: "SQUISH's own s(154), squares removed",
    154: "SQUISH's own s(155), squares removed",
    155: "Francisco Couzo's s(156), squares removed",
    179: "Francisco Couzo's s(180), squares removed",
    208: "Francisco Couzo's s(209), squares removed",
    237: "Francisco Couzo's s(238), squares removed",
    238: "SQUISH's own s(239), squares removed",
    239: "Francisco Couzo's s(210), grafted into n's Kingbird record",
    258: "Francisco Couzo's s(259), squares removed",
    263: "Francisco Couzo's s(297), carved down to n's Kingbird record",
}


# Confirmation names a new geometry roster; n153 keeps its original evidence.
RESULT_NUMBERS = tuple(n for n in NUMBERS if n != 153)
EXACT_EVIDENCE = "E-squish-update-2026-10-07-exact-replay"
WITNESSES = REPO / "packing/witnesses/squish-401-update-2026"
CERTIFICATION_FORMAT = "squish-update-exact-certification-v1"
MAX_RECEIPT_BYTES = original.MAX_RECEIPT_BYTES
MAX_XZ_MEMORY_BYTES = 32 * 1024 * 1024
CHECKERS = ("independent", "exact_verify")
CHECKER_ROUTES = ["devtools.check_rational_witness_independent", "sqpack.witness.exact_verify"]
REPLAY_ORIGIN = "reused-complete-review-replay"


def certificate_path(n: int) -> Path:
    if n not in RESULT_NUMBERS:
        raise original.PacketError("count absent from the new confirmation scope")
    return WITNESSES / f"n-{n:03d}-rational.yaml.gz"


def to_witness(fact: dict[str, Any]) -> dict[str, Any]:
    """Reuse exact conversion with revision-specific nongeometric metadata."""
    n = fact["n"]
    certificate_path(n)
    witness = original.to_witness(fact)
    witness["id"] = f"W-squish-update-2026-10-07-n{n:03d}"
    witness["source"] = {"path": fact_path(n).relative_to(REPO).as_posix()}
    witness["certificate"]["replay"] = (
        "uv run --frozen --all-extras --group dev python -m "
        f"devtools.squish_followup_packets check-certification --replay --n {n}"
    )
    return witness


def read_xz_receipt(path: Path) -> Any:
    """Admit one bounded XZ stream and the original strict semantic JSON object."""
    with path.open("rb") as stream:
        raw = stream.read(MAX_RECEIPT_BYTES + 1)
    if len(raw) > MAX_RECEIPT_BYTES:
        raise original.PacketError("compressed receipt exceeds byte ceiling")
    decoder = lzma.LZMADecompressor(format=lzma.FORMAT_XZ, memlimit=MAX_XZ_MEMORY_BYTES)
    try:
        data = decoder.decompress(raw, max_length=MAX_RECEIPT_BYTES + 1)
    except lzma.LZMAError as error:
        raise original.PacketError("invalid or memory-exceeding XZ receipt") from error
    if len(data) > MAX_RECEIPT_BYTES:
        raise original.PacketError("uncompressed receipt exceeds byte ceiling")
    if not decoder.eof or decoder.unused_data:
        raise original.PacketError("truncated or trailing XZ receipt")
    return json.loads(data, object_pairs_hook=original.unique_json_object)


def save_certificate(path: Path, data: bytes) -> None:
    """A linked mutation-worker proof root is readable, never a producer output."""
    if not path.resolve().is_relative_to(REPO.resolve()):
        raise original.PacketError("certificate output escapes the private checkout")
    save(path, data)


def json_bytes(value: object) -> bytes:
    """Serialize derived records deterministically, with no source prose copied."""
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode()


def save(path: Path, data: bytes) -> None:
    """Publish each derived artifact atomically."""
    guard_output(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with atomic_output_file(path) as temporary:
        temporary.write_bytes(data)


def guard_output(path: Path) -> None:
    """Refuse publication through links outside this checkout before making parents."""
    if not path.resolve().is_relative_to(REPO.resolve()):
        raise original.PacketError("packet output escapes the private checkout")


def display(side: str) -> str:
    """Round the claimed exact side upward, never below its rational value."""
    scale = 10**DISPLAY_PLACES
    value = Fraction(side) * scale
    ceiling = -(-value.numerator // value.denominator)
    integer, fractional = divmod(ceiling, scale)
    return f"{integer}.{fractional:0{DISPLAY_PLACES}d}"


def fact_path(n: int) -> Path:
    """Locate the revision-specific normalized geometry."""
    return PACKET / "facts" / f"n-{n:03d}.json.gz"


def source_url(n: int) -> str:
    """Name the pinned update certificate, never a historical attachment."""
    if n not in NUMBERS:
        raise original.PacketError("count absent from SQUISH update")
    return f"{SOURCE_ROOT}/n{n}/n{n}.cert.json"


def read_fact(n: int) -> dict[str, Any]:
    """Re-admit retained triples through the existing strict source parser."""
    if fact_path(n).stat().st_size > original.MAX_SOURCE_BYTES:
        raise original.PacketError("compressed update facts exceed byte ceiling")
    with gzip.open(fact_path(n), "rb") as stream:
        data = stream.read(original.MAX_SOURCE_BYTES + 1)
    if len(data) > original.MAX_SOURCE_BYTES:
        raise original.PacketError("update facts exceed byte ceiling")
    fact = json.loads(data, object_pairs_hook=original.unique_json_object)
    if type(fact) is not dict or set(fact) != {"n", "side", "printed_side", "squares"}:
        raise original.PacketError("invalid update fact schema")
    entries = fact["squares"]
    if type(entries) is not list or any(
        type(entry) is not dict or set(entry) != {"x", "y", "t"} for entry in entries
    ):
        raise original.PacketError("invalid update triple roster")
    source = {
        "n": fact["n"],
        "s_exact": fact["side"],
        "s_decimal": fact["printed_side"],
        "note": "Derived geometric facts; no producer prose retained.",
        "squares": [[entry[key] for key in ("x", "y", "t")] for entry in entries],
    }
    normalized, _raw = original.parse_source_bytes(json_bytes(source), n)
    if fact != normalized:
        raise original.PacketError("update facts are not normalized")
    return normalized


def claims(cases: list[dict[str, Any]]) -> dict[str, Any]:
    """Keep the unchanged n153 comparison outside the new result's scope."""
    return {
        "results": [
            {"n": row["n"], "offered_side": display(row["exact_side"])}
            for row in cases
            if row["n"] != 153
        ]
    }


def n153_comparison(fact: dict[str, Any]) -> dict[str, Any]:
    """Compare exact side and every ordered triple to the immutable attachment facts."""
    prior = original.read_fact(153)
    return {
        "n": 153,
        "prior_facts": original.fact_path(153).relative_to(REPO).as_posix(),
        "update_facts": fact_path(153).relative_to(REPO).as_posix(),
        "same_exact_side": fact["side"] == prior["side"],
        "same_ordered_rational_triples": fact["squares"] == prior["squares"],
        "prior_printed_side": prior["printed_side"],
        "update_printed_side": fact["printed_side"],
        "prior_evidence_preserved": True,
        "new_assurance_claimed": False,
    }


def acquire(source: Path) -> None:
    """Parse the entire revision before writing attributed derived facts."""
    parsed = [(n, *original.parse_source(source / f"n{n}/n{n}.cert.json", n)) for n in NUMBERS]
    cases = []
    for n, fact, raw in parsed:
        save(fact_path(n), gzip.compress(json_bytes(fact), mtime=0))
        cases.append(
            {
                "n": n,
                "exact_side": fact["side"],
                "side": fact["printed_side"],
                "source_url": f"{SOURCE_ROOT}/n{n}/n{n}.cert.json",
                "source_file": f"n{n}.cert.json",
                "source_sha256": hashlib.sha256(raw).hexdigest(),
                "source_bytes": len(raw),
                "facts": fact_path(n).relative_to(REPO).as_posix(),
                "raw_asset_retained": False,
                "reported_seed": SEEDS[n],
            }
        )
    save(
        PACKET / "acquisition/sources.json",
        json_bytes(
            {
                "format": "external-source-acquisition-v1",
                "retrieved": "2026-10-07",
                "source_commit": REVISION,
                "raw_asset_retained": False,
                "producer_checker_replayed": False,
                "cases": cases,
            }
        ),
    )
    save(PACKET / "acquisition/update-claims.json", json_bytes(claims(cases)))
    save(
        PACKET / "acquisition/n153-comparison.json", json_bytes(n153_comparison(read_fact(153)))
    )


def check(source: Path | None = None) -> None:
    """Check provenance and exact retained identity, optionally against upstream bytes."""
    acquisition = original.read_json(PACKET / "acquisition/sources.json")
    if (
        acquisition["source_commit"] != REVISION
        or acquisition["raw_asset_retained"] is not False
        or acquisition["producer_checker_replayed"] is not False
        or acquisition["format"] != "external-source-acquisition-v1"
        or acquisition["retrieved"] != "2026-10-07"
    ):
        raise original.PacketError("update source provenance mismatch")
    cases = acquisition["cases"]
    if [row["n"] for row in cases] != list(NUMBERS):
        raise original.PacketError("update acquisition roster mismatch")
    for row in cases:
        n = row["n"]
        fact = read_fact(n)
        if (
            row["facts"] != fact_path(n).relative_to(REPO).as_posix()
            or row["exact_side"] != fact["side"]
            or row["side"] != fact["printed_side"]
            or row["source_url"] != f"{SOURCE_ROOT}/n{n}/n{n}.cert.json"
            or row["reported_seed"] != SEEDS[n]
            or row["raw_asset_retained"] is not False
            or row["source_file"] != f"n{n}.cert.json"
            or type(row["source_bytes"]) is not int
            or not 1 <= row["source_bytes"] <= original.MAX_SOURCE_BYTES
            or type(row["source_sha256"]) is not str
            or re.fullmatch(r"[0-9a-f]{64}", row["source_sha256"]) is None
        ):
            raise original.PacketError(f"n={n} update provenance/facts mismatch")
        if source is not None:
            upstream, raw = original.parse_source(source / f"n{n}/n{n}.cert.json", n)
            if (
                upstream != fact
                or row["source_sha256"] != hashlib.sha256(raw).hexdigest()
                or row["source_bytes"] != len(raw)
            ):
                raise original.PacketError(
                    f"n={n} upstream bytes differ from pinned acquisition"
                )
    if original.read_json(PACKET / "acquisition/update-claims.json") != claims(cases):
        raise original.PacketError("update claims mismatch")
    comparison_record = original.read_json(PACKET / "acquisition/frontier-comparison.json")
    comparisons = comparison_record["cases"]
    if [row["n"] for row in comparisons] != [n for n in NUMBERS if n != 153]:
        raise original.PacketError("historical frontier comparison roster mismatch")
    for row in comparisons:
        n = row["n"]
        fact = read_fact(n)
        prior = row["prior_reported"]
        if (
            row["new_exact_side"] != fact["side"]
            or row["new_safe_display"] != display(fact["side"])
            or row["reported_seed"] != SEEDS[n]
            or not prior["source_key"]
            or type(prior["found_by"]) is not list
            or Fraction(prior["value"]) <= Fraction(fact["side"])
        ):
            raise original.PacketError(f"n={n} historical frontier comparison mismatch")
        if n in REPLACEMENTS:
            preceding = original.read_fact(n)
            if prior["exact_form"] != preceding["side"]:
                raise original.PacketError(f"n={n} predecessor differs from retained release")
    comparison = n153_comparison(read_fact(153))
    if original.read_json(PACKET / "acquisition/n153-comparison.json") != comparison:
        raise original.PacketError("n153 exact geometry comparison mismatch")
    if not comparison["same_exact_side"] or not comparison["same_ordered_rational_triples"]:
        raise original.PacketError("n153 differs; register new geometry separately")


def read_review_json(path: Path) -> Any:
    """Read bounded strict review data without trusting a filename-dependent ceiling."""
    with path.open("rb") as stream:
        data = stream.read(MAX_RECEIPT_BYTES + 1)
    if len(data) > MAX_RECEIPT_BYTES:
        raise original.PacketError("review JSON exceeds byte ceiling")
    return json.loads(data, object_pairs_hook=original.unique_json_object)


def roster(rows: Any, numbers: tuple[int, ...]) -> dict[int, Any]:
    if type(rows) is not list or any(type(row) is not dict for row in rows):
        raise original.PacketError("invalid replay roster")
    if any(type(row.get("n")) is not int for row in rows) or [row["n"] for row in rows] != list(
        numbers
    ):
        raise original.PacketError("missing, duplicate, extra or mistyped replay count")
    return {row["n"]: row for row in rows}


def seconds(value: Any) -> float:
    if type(value) not in (int, float) or not math.isfinite(value) or value < 0:
        raise original.PacketError("invalid measured replay time")
    return float(value)


def clearance(value: Any) -> Fraction:
    if (
        type(value) is not str
        or len(value) > original.MAX_CHECKER_LITERAL_CHARS
        or re.fullmatch(r"-?[0-9]+(?:/[0-9]+)?", value) is None
    ):
        raise original.PacketError("invalid exact containment diagnostic")
    return Fraction(value)


def validate_verdict(row: Any, n: int, *, passed: bool) -> None:
    if type(row) is not dict:
        raise original.PacketError("missing deciding checker verdict")
    if (
        row.get("verification_passed") is not passed
        or type(row.get("n")) is not int
        or row["n"] != n
        or type(row.get("pairs_tested")) is not int
        or row["pairs_tested"] != n * (n - 1) // 2
        or type(row.get("failures")) is not list
        or bool(row["failures"]) is passed
        or (passed and clearance(row["minimum_containment_clearance"]) < 0)
    ):
        raise original.PacketError(f"n={n} incomplete deciding checker coverage")
    clearance(row["minimum_containment_clearance"])


def control_witnesses() -> dict[str, dict[str, Any]]:
    """Keep both full-size controls in this revision's exact rational input frame."""
    witness = to_witness(read_fact(123))
    overlap = copy.deepcopy(witness)
    overlap["squares"][1]["corners"] = copy.deepcopy(overlap["squares"][0]["corners"])
    outside = copy.deepcopy(witness)
    for point in outside["squares"][0]["corners"]:
        point[0] = str(Fraction(point[0]) - 2 * Fraction(outside["side"]))
    return {
        "duplicate-square-overlap": overlap,
        "square-translated-outside-container": outside,
    }


def validate_controls(controls: Any, *, replay: bool = False) -> None:
    expected = control_witnesses()
    if (
        type(controls) is not dict
        or type(controls.get("n")) is not int
        or controls["n"] != 123
        or type(controls.get("controls")) is not list
        or len(controls["controls"]) != 2
        or [row.get("control") for row in controls["controls"]] != list(expected)
    ):
        raise original.PacketError("invalid full-size negative-control roster")
    for row in controls["controls"]:
        name = row["control"]
        witness = expected[name]
        if original.checker_input(row["checker_input"], receipt=True) != original.checker_input(
            witness
        ):
            raise original.PacketError("negative-control checker-input semantic mismatch")
        seconds(row["wall_seconds"])
        for checker in CHECKERS:
            validate_verdict(row[checker], 123, passed=False)
        if name == "duplicate-square-overlap":
            if not any(
                type(failure) is str and "overlapping pairs" in failure
                for failure in row["independent"]["failures"]
            ) or not any(
                type(failure) is list and failure and failure[0] == "overlap"
                for failure in row["exact_verify"]["failures"]
            ):
                raise original.PacketError("overlap control lacks both overlap refusals")
        elif any(
            clearance(row[checker]["minimum_containment_clearance"]) >= 0
            for checker in CHECKERS
        ):
            raise original.PacketError("container control lacks exact negative clearance")
        if replay and original.decide(witness) != {
            checker: row[checker] for checker in CHECKERS
        }:
            raise original.PacketError("negative-control exact replay mismatch")


def validate_replay_summary(summary: Any, rows: dict[int, Any], controls: Any) -> None:
    batch = summary["original_batch"]
    if (
        summary["format"] != "squish-reviewed-replay-origin-v1"
        or summary["replay_origin"] != REPLAY_ORIGIN
        or summary["source_commit"] != REVISION
        or batch["source_revision"] != REVISION
        or batch["counts"] != list(NUMBERS)
        or any(type(n) is not int for n in batch["counts"])
        or type(batch["certificates"]) is not int
        or batch["certificates"] != len(NUMBERS)
        or type(batch["squares"]) is not int
        or batch["squares"] != sum(NUMBERS)
        or type(batch["pairs_per_checker"]) is not int
        or batch["pairs_per_checker"] != sum(n * (n - 1) // 2 for n in NUMBERS)
        or batch["checker_routes"] != CHECKER_ROUTES
        or batch["all_positive_passed"] is not True
        or batch["all_full_size_controls_rejected"] is not True
        or summary["scoped_counts"] != list(RESULT_NUMBERS)
        or any(type(n) is not int for n in summary["scoped_counts"])
    ):
        raise original.PacketError("reviewed replay origin/scope mismatch")
    scoped = sum(seconds(row["wall_seconds"]) for row in rows.values())
    excluded = seconds(summary["excluded_n153_wall_seconds"])
    if not all(
        math.isclose(seconds(actual), expected, rel_tol=1e-12, abs_tol=1e-9)
        for actual, expected in (
            (summary["scoped_positive_wall_seconds"], scoped),
            (batch["positive_wall_seconds"], scoped + excluded),
            (
                batch["controls_wall_seconds"],
                sum(seconds(row["wall_seconds"]) for row in controls["controls"]),
            ),
        )
    ):
        raise original.PacketError("reviewed replay timing attribution mismatch")


def validate_case(row: Any, n: int, fact: dict[str, Any]) -> dict[str, Any]:
    witness = to_witness(fact)
    if (
        row["printed_side"] != fact["printed_side"]
        or row["certified_side"] != fact["side"]
        or row["verified_value"] != display(fact["side"])
        or row["exact_form"] != fact["side"]
        or row["side_inflation"] != "0"
        or row["certificate"] != certificate_path(n).relative_to(REPO).as_posix()
        or original.checker_input(row["checker_input"], receipt=True)
        != original.checker_input(witness)
    ):
        raise original.PacketError(f"n={n} receipt/fact/bound semantic mismatch")
    seconds(row["wall_seconds"])
    for checker in CHECKERS:
        validate_verdict(row[checker], n, passed=True)
    return witness


def retain_reviewed_replay(review_root: Path, source: Path) -> None:
    """Bind a complete reviewed run before publishing any revision-specific proof."""
    check()
    acquisition = original.read_json(PACKET / "acquisition/sources.json")
    acquired = roster(acquisition["cases"], NUMBERS)
    reviewed = read_review_json(review_root / "acquisition.json")
    if reviewed["revision"] != REVISION:
        raise original.PacketError("review source revision mismatch")
    sources = roster(reviewed["cases"], NUMBERS)
    batch = read_review_json(review_root / "summary.json")
    positives = {}
    for n in NUMBERS:
        fact = read_fact(n)
        upstream, raw = original.parse_source(source / f"n{n}.cert.json", n)
        entry, admission = sources[n], acquired[n]
        if (
            upstream != fact
            or entry["url"]
            != source_url(n)
            .replace("https://github.com/", "https://raw.githubusercontent.com/")
            .replace("/blob/", "/")
            or type(entry["bytes"]) is not int
            or entry["bytes"] != len(raw)
            or entry["sha256"] != hashlib.sha256(raw).hexdigest()
            or entry["sha256"] != admission["source_sha256"]
            or entry["bytes"] != admission["source_bytes"]
            or entry["side"] != fact["side"]
            or entry["source_print"] != fact["printed_side"]
        ):
            raise original.PacketError(f"n={n} reviewed raw source/acquisition mismatch")
        row = read_review_json(review_root / f"n{n}-receipt.json")
        witness = original.to_witness(fact) if n == 153 else to_witness(fact)
        if (
            type(row["n"]) is not int
            or row["n"] != n
            or row["side"] != fact["side"]
            or row["source_print"] != fact["printed_side"]
            or row["upward_ceiling"] != display(fact["side"])
            or original.checker_input(row["checker_input"], receipt=True)
            != original.checker_input(witness)
        ):
            raise original.PacketError(
                f"n={n} reviewed complete input differs from retained facts"
            )
        for checker in CHECKERS:
            validate_verdict(row[checker], n, passed=True)
        seconds(row["wall_seconds"])
        positives[n] = row
    raw_controls = read_review_json(review_root / "controls.json")
    controls = {
        "n": 123,
        "expectation": "both deciding checkers refuse both full-size controls",
        "controls": [
            {
                "control": row["name"],
                **{key: value for key, value in row.items() if key != "name"},
            }
            for row in raw_controls
        ],
    }
    validate_controls(controls)
    rows = [
        {
            "n": n,
            "printed_side": read_fact(n)["printed_side"],
            "certified_side": read_fact(n)["side"],
            "verified_value": display(read_fact(n)["side"]),
            "exact_form": read_fact(n)["side"],
            "side_inflation": "0",
            "certificate": certificate_path(n).relative_to(REPO).as_posix(),
            **{key: positives[n][key] for key in ("checker_input", "wall_seconds", *CHECKERS)},
        }
        for n in RESULT_NUMBERS
    ]
    summary = {
        "format": "squish-reviewed-replay-origin-v1",
        "replay_origin": REPLAY_ORIGIN,
        "source_commit": REVISION,
        "original_batch": batch,
        "scoped_counts": list(RESULT_NUMBERS),
        "scoped_positive_wall_seconds": sum(row["wall_seconds"] for row in rows),
        "excluded_n153_wall_seconds": positives[153]["wall_seconds"],
    }
    validate_replay_summary(summary, roster(rows, RESULT_NUMBERS), controls)
    receipt = {
        "format": CERTIFICATION_FORMAT,
        "source_commit": REVISION,
        "producer_checker_replayed": False,
        "replay_origin": REPLAY_ORIGIN,
        "checkers": CHECKER_ROUTES,
        "counts": list(RESULT_NUMBERS),
        "squares": sum(RESULT_NUMBERS),
        "pairs_per_checker": sum(n * (n - 1) // 2 for n in RESULT_NUMBERS),
        "reviewed_replay": "receipts/replay-summary.json",
        "cases": rows,
    }
    outputs = {
        certificate_path(row["n"]): gzip.compress(
            witness_document(
                validate_case(row, row["n"], read_fact(row["n"])),
                schema="../witness.schema.yaml",
            ).encode(),
            mtime=0,
        )
        for row in rows
    }
    outputs.update(
        {
            PACKET / "receipts/certification.json.xz": lzma.compress(json_bytes(receipt)),
            PACKET / "receipts/negative-controls.json.xz": lzma.compress(json_bytes(controls)),
            PACKET / "receipts/replay-summary.json": json_bytes(summary),
        }
    )
    for path in outputs:
        guard_output(path)
    for path, data in outputs.items():
        save(path, data)


def read_certificate(n: int) -> dict[str, Any]:
    path = certificate_path(n)
    if path.stat().st_size > MAX_RECEIPT_BYTES:
        raise original.PacketError("compressed certificate exceeds byte ceiling")
    with gzip.open(path, "rb") as stream:
        data = stream.read(MAX_RECEIPT_BYTES + 1)
    if len(data) > MAX_RECEIPT_BYTES:
        raise original.PacketError("certificate exceeds byte ceiling")
    with tempfile.TemporaryDirectory() as directory:
        temporary = Path(directory) / "certificate.yaml"
        temporary.write_bytes(data)
        return dict(load_witness(temporary, fallback_schema=original.SCHEMA))


def admit_certification() -> tuple[dict[int, Any], Any]:
    """Admit retained full replay data independently of generated witness files."""
    check()
    receipt = read_xz_receipt(PACKET / "receipts/certification.json.xz")
    if (
        receipt["format"] != CERTIFICATION_FORMAT
        or receipt["source_commit"] != REVISION
        or receipt["producer_checker_replayed"] is not False
        or receipt["replay_origin"] != REPLAY_ORIGIN
        or receipt["checkers"] != CHECKER_ROUTES
        or receipt["counts"] != list(RESULT_NUMBERS)
        or any(type(n) is not int for n in receipt["counts"])
        or type(receipt["squares"]) is not int
        or receipt["squares"] != sum(RESULT_NUMBERS)
        or type(receipt["pairs_per_checker"]) is not int
        or receipt["pairs_per_checker"] != sum(n * (n - 1) // 2 for n in RESULT_NUMBERS)
        or receipt["reviewed_replay"] != "receipts/replay-summary.json"
    ):
        raise original.PacketError("certification revision/checker/scope provenance mismatch")
    rows = roster(receipt["cases"], RESULT_NUMBERS)
    for n, row in rows.items():
        validate_case(row, n, read_fact(n))
    controls = read_xz_receipt(PACKET / "receipts/negative-controls.json.xz")
    validate_controls(controls)
    validate_replay_summary(
        read_review_json(PACKET / "receipts/replay-summary.json"), rows, controls
    )
    return rows, controls


def _check_certificate_input(n: int) -> dict[str, Any]:
    """Compare one complete proof with its admitted source, without a decision replay."""
    expected = to_witness(read_fact(n))
    certificate = read_certificate(n)
    if (
        certificate.get("id") != expected["id"]
        or certificate.get("source") != expected["source"]
        or certificate.get("certificate") != expected["certificate"]
        or original.checker_input(certificate) != original.checker_input(expected)
    ):
        raise original.PacketError(f"n={n} revision-specific witness metadata/input mismatch")
    return certificate


def check_certification(
    numbers: list[int] | None = None, *, replay: bool = False
) -> dict[int, Any]:
    """Validate complete retained input/provenance; rerun decisions only on request."""
    selected = list(RESULT_NUMBERS) if numbers is None else numbers
    if any(type(n) is not int or n not in RESULT_NUMBERS for n in selected) or len(
        set(selected)
    ) != len(selected):
        raise original.PacketError("count absent or duplicated in new confirmation scope")
    if not selected:
        raise original.PacketError("empty confirmation witness scope")
    rows, controls = admit_certification()
    for n in selected:
        row = rows[n]
        certificate = _check_certificate_input(n)
        if replay and original.decide(certificate) != {
            checker: row[checker] for checker in CHECKERS
        }:
            raise original.PacketError(f"n={n} exact replay mismatch")
    if replay:
        validate_controls(controls, replay=True)
    return rows


def restore_witnesses() -> None:
    """Recover deterministic proof files offline from admitted retained facts/receipts."""
    rows, _controls = admit_certification()
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
        save_certificate(path, data)


def linked_certificate_problems(
    paths: Iterable[str], *, repository: Path
) -> dict[str, str | None]:
    """Admit a complete private replay once, retaining per-proof refusal diagnostics."""
    selected = dict.fromkeys(paths)
    problems: dict[str, str | None] = dict.fromkeys(selected, "resolves outside the repository")
    if repository.resolve() != REPO.resolve() or not WITNESSES.is_symlink():
        return problems
    declared = {certificate_path(n).relative_to(REPO).as_posix(): n for n in RESULT_NUMBERS}
    eligible = {
        path: declared[path]
        for path in selected
        if path in declared and not certificate_path(declared[path]).is_symlink()
    }
    if not eligible:
        return problems
    try:
        admit_certification()
    except (original.PacketError, OSError, KeyError, TypeError, ValueError) as error:
        for path in eligible:
            problems[path] = f"linked reviewed proof custody mismatch: {error}"
        return problems
    for path, n in eligible.items():
        try:
            _check_certificate_input(n)
        except (original.PacketError, OSError, KeyError, TypeError, ValueError) as error:
            problems[path] = f"linked reviewed proof custody mismatch: {error}"
        else:
            problems[path] = None
    return problems


def linked_certificate_problem(path: str, *, repository: Path) -> str | None:
    """Admit one linked proof with a fresh complete private source/receipt transaction."""
    return linked_certificate_problems([path], repository=repository)[path]


def confirmed_bound(n: int) -> dict[str, Any]:
    row = check_certification([n])[n]
    return {
        "value": row["verified_value"],
        "exact_form": row["exact_form"],
        "evidence": [EXACT_EVIDENCE],
    }


def main(argv: list[str] | None = None) -> int:
    """Expose reported acquisition, reviewed retention and explicit exact replay."""
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    sub = parser.add_subparsers(dest="command", required=True)
    acquisition = sub.add_parser("acquire", allow_abbrev=False)
    acquisition.add_argument("--source", type=Path, required=True)
    checking = sub.add_parser("check", allow_abbrev=False)
    checking.add_argument("--source", type=Path)
    retaining = sub.add_parser("retain-reviewed-replay", allow_abbrev=False)
    retaining.add_argument("--review-root", type=Path, required=True)
    retaining.add_argument("--source", type=Path, required=True)
    sub.add_parser("restore-witnesses", allow_abbrev=False)
    certification = sub.add_parser("check-certification", allow_abbrev=False)
    certification.add_argument("--n", type=int, action="append")
    certification.add_argument("--replay", action="store_true")
    args = parser.parse_args(argv)
    try:
        if args.command == "acquire":
            acquire(args.source)
        elif args.command == "check":
            check(args.source)
        elif args.command == "retain-reviewed-replay":
            retain_reviewed_replay(args.review_root, args.source)
        elif args.command == "restore-witnesses":
            restore_witnesses()
        else:
            check_certification(args.n, replay=args.replay)
    except (original.PacketError, OSError, KeyError, TypeError, ValueError) as error:
        print(f"SQUISH update packet: {error}", file=sys.stderr)
        return 1
    if args.command == "acquire":
        print("SQUISH update packet: reported facts retained; run check for consistency")
    elif args.command == "check":
        print("SQUISH update packet: consistency checked; feasibility not decided")
    elif args.command == "retain-reviewed-replay":
        print(
            "SQUISH update packet: complete reviewed replay retained; no new checker execution"
        )
    elif args.command == "restore-witnesses":
        print("SQUISH update packet: witnesses restored from complete admitted retained inputs")
    else:
        print(
            "SQUISH update packet: certification bound"
            + (" and replayed" if args.replay else " without rerunning decisions")
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
