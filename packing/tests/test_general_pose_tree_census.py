"""Admission controls for the exact T-059 row census wrapper."""

from __future__ import annotations

import gzip
import hashlib
import json
import os
import subprocess
from pathlib import Path

import pytest

from devtools.check_general_pose_tree_census import (
    CensusError,
    inspect_legacy,
    pack_journal,
    parse_rows,
    run_bound,
    validate_bound,
)

PACKING = Path(__file__).resolve().parents[1]
RETAINED = PACKING / "resources/web/external-square-certificates-2026-09-22/kleddamag-11"
SAMPLE = PACKING / "resources/web/wand125-tools-2026-09-29/receipts/n11-sample.jsonl"


def _string_values(value: object) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, dict):
        return [item for child in value.values() for item in _string_values(child)]
    if isinstance(value, list):
        return [item for child in value for item in _string_values(child)]
    return []


def _write_source(checker: Path, *, sleep: bool = False) -> None:
    script = """
import argparse
import json
import sys
import time
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("certificate_dir", type=Path)
parser.add_argument("output", type=Path)
parser.add_argument("rows")
parser.add_argument("--leaf")
args = parser.parse_args()
if sys.flags.isolated != 1 or sys.flags.optimize != 0:
    raise RuntimeError("runner did not enforce isolated unoptimized Python")
reference = json.loads((args.certificate_dir / "evidence/portable/python.json").read_text())
for text in args.rows.split(","):
    selected = range(*[int(v) for v in text.split("-")], 1) if "-" in text else [int(text)]
    if "-" in text:
        left, right = map(int, text.split("-"))
        selected = range(left, right + 1)
    for row in selected:
        minimum = reference["rows"][row]["minimum_units"]
        record = {
            "row": row, "mode": "minimize", "minimum": minimum,
            "recorded": minimum, "agree": True, "witness": ["1", "1"],
            "witness_replayed": True, "setup_seconds": 0.0, "seconds": 0.0,
            "boxes_expanded": 1, "leaves": 1, "max_depth": 1, "cells": 1,
            "nodes_created": 1, "outside_pruned": 0, "bound_pruned": 0,
            "max_heap": 1,
        }
        with args.output.open("a") as stream:
            stream.write(json.dumps(record) + "\\n")
            stream.flush()
        if SLEEP:
            time.sleep(60)
""".replace("SLEEP", repr(sleep))
    path = checker / "general_pose_tree/run_n11.py"
    path.parent.mkdir(parents=True)
    path.write_text(script)
    subprocess.run(["git", "init", "-q"], cwd=checker, check=True)
    subprocess.run(["git", "add", "."], cwd=checker, check=True)
    subprocess.run(
        [
            "git",
            "-c",
            "user.name=Test",
            "-c",
            "user.email=test@example.com",
            "commit",
            "-qm",
            "fixture",
        ],
        cwd=checker,
        check=True,
    )


def _write_inputs(directory: Path, minima: list[int]) -> None:
    certificate = {
        "L": "3",
        "A": "1",
        "coordinate_denominator": 3,
        "point_orbits": [[3, 3, 11]],
        "charge_orbits": [],
        "entries": [["0", "1/10", "1/20", "1/2"] for _ in minima],
    }
    certificate_bytes = json.dumps(certificate).encode()
    (directory / "evidence/portable").mkdir(parents=True)
    (directory / "global-certificate.json").write_bytes(certificate_bytes)
    reference = {
        "certificate_sha256": hashlib.sha256(certificate_bytes).hexdigest(),
        "minimum_units": min(minima),
        "rows": [{"row": row, "minimum_units": minimum} for row, minimum in enumerate(minima)],
    }
    (directory / "evidence/portable/python.json").write_text(json.dumps(reference))


def _run_fixture(tmp_path: Path, rows: str = "0-2") -> tuple[Path, Path, Path]:
    checker = tmp_path / "checker"
    certificate = tmp_path / "certificate"
    output = tmp_path / "rows.jsonl"
    _write_source(checker)
    _write_inputs(certificate, [11, 11, 11])
    result = run_bound(
        checker,
        certificate,
        output,
        rows,
        # Allow startup and journal writes on loaded hosts; the separate sleeping
        # checker control below owns timeout behavior.
        max_seconds=30,
        expected_rows=3,
        expected_revision=None,
        expected_certificate_sha256=None,
        expected_reference_sha256=None,
        checker_files=("general_pose_tree/run_n11.py",),
    )
    assert result["verdict"] == (
        "COMPLETE_ROW_EQUALITY" if rows == "0-2" else "PARTIAL_ROW_EQUALITY"
    )
    return checker, certificate, output


def test_legacy_sample_is_only_unbound_partial_inventory() -> None:
    result = inspect_legacy(
        SAMPLE,
        RETAINED / "global-certificate.json",
        RETAINED / "evidence/portable/python.json",
    )
    assert result["verdict"] == "UNBOUND_INVENTORY_ONLY"
    assert result["bound_at_production"] is False
    assert result["rows_checked"] == 3
    assert result["complete"] is False
    assert result["global_minimum"] is None
    assert result["packing_bound_verified"] is False
    assert "no production-time" in str(result["warning"])


def test_row_parser_refuses_an_oversized_range_before_expansion() -> None:
    with pytest.raises(CensusError, match="malformed row range"):
        parse_rows("0-1000000000")
    with pytest.raises(CensusError, match="malformed row index"):
        parse_rows("²")


def test_runner_refuses_source_tree_and_existing_outputs_before_execution(
    tmp_path: Path,
) -> None:
    checker = tmp_path / "checker"
    certificate = tmp_path / "certificate"
    _write_source(checker)
    _write_inputs(certificate, [11, 11, 11])
    source = checker / "general_pose_tree/run_n11.py"
    original = source.read_bytes()
    with pytest.raises(CensusError, match="checker source tree"):
        run_bound(
            checker,
            certificate,
            checker / "new.jsonl",
            "0",
            max_seconds=2,
            expected_rows=3,
            expected_revision=None,
            expected_certificate_sha256=None,
            expected_reference_sha256=None,
            checker_files=("general_pose_tree/run_n11.py",),
        )
    assert source.read_bytes() == original
    existing = tmp_path / "existing.jsonl"
    existing.write_text("retained\n")
    with pytest.raises(CensusError, match="never overwrite evidence"):
        run_bound(
            checker,
            certificate,
            existing,
            "0",
            max_seconds=2,
            expected_rows=3,
            expected_revision=None,
            expected_certificate_sha256=None,
            expected_reference_sha256=None,
            checker_files=("general_pose_tree/run_n11.py",),
        )
    assert existing.read_text() == "retained\n"


def test_bound_runner_admits_only_the_exact_complete_row_census(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("PYTHONOPTIMIZE", "2")
    checker, certificate, output = _run_fixture(tmp_path)
    result = validate_bound(
        output,
        checker,
        certificate / "global-certificate.json",
        certificate / "evidence/portable/python.json",
        require_complete=True,
        expected_rows=3,
        expected_revision=None,
        expected_certificate_sha256=None,
        expected_reference_sha256=None,
        checker_files=("general_pose_tree/run_n11.py",),
    )
    assert result["complete"] is True
    assert result["global_minimum"] == 11
    assert result["global_minimum_matches_reference"] is True
    assert result["global_counting_theorem_verified"] is False
    header = json.loads(output.read_text().splitlines()[0])
    assert "input_paths" not in header
    assert not [value for value in _string_values(header) if Path(value).is_absolute()]
    wrapper = PACKING / "devtools/check_general_pose_tree_census.py"
    assert (
        header["binding"]["first_party_wrapper"]["sha256"]
        == hashlib.sha256(wrapper.read_bytes()).hexdigest()
    )


def test_proper_subset_is_partial_and_complete_claim_is_refused(tmp_path: Path) -> None:
    checker, certificate, output = _run_fixture(tmp_path, "0,2")
    result = validate_bound(
        output,
        checker,
        certificate / "global-certificate.json",
        certificate / "evidence/portable/python.json",
        expected_rows=3,
        expected_revision=None,
        expected_certificate_sha256=None,
        expected_reference_sha256=None,
        checker_files=("general_pose_tree/run_n11.py",),
    )
    assert result["verdict"] == "PARTIAL_ROW_EQUALITY"
    assert result["missing_ranges"] == ["1"]
    with pytest.raises(CensusError, match="requires exactly rows"):
        validate_bound(
            output,
            checker,
            certificate / "global-certificate.json",
            certificate / "evidence/portable/python.json",
            require_complete=True,
            expected_rows=3,
            expected_revision=None,
            expected_certificate_sha256=None,
            expected_reference_sha256=None,
            checker_files=("general_pose_tree/run_n11.py",),
        )


def test_duplicate_mismatch_and_malformed_exact_values_are_refused(tmp_path: Path) -> None:
    checker, certificate, output = _run_fixture(tmp_path)
    lines = output.read_text().splitlines()
    output.write_text("\n".join([*lines, lines[1]]) + "\n")
    with pytest.raises(CensusError, match="duplicate result row"):
        validate_bound(
            output,
            checker,
            certificate / "global-certificate.json",
            certificate / "evidence/portable/python.json",
            expected_rows=3,
            expected_revision=None,
            expected_certificate_sha256=None,
            expected_reference_sha256=None,
            checker_files=("general_pose_tree/run_n11.py",),
        )
    lines = lines[:]
    row = json.loads(lines[1])
    row["minimum"] = 13.0
    lines[1] = json.dumps(row)
    output.write_text("\n".join(lines) + "\n")
    with pytest.raises(CensusError, match="exact integer"):
        validate_bound(
            output,
            checker,
            certificate / "global-certificate.json",
            certificate / "evidence/portable/python.json",
            expected_rows=3,
            expected_revision=None,
            expected_certificate_sha256=None,
            expected_reference_sha256=None,
            checker_files=("general_pose_tree/run_n11.py",),
        )
    row["minimum"] = 11
    row["witness"] = ["1e999999999", "1"]
    lines[1] = json.dumps(row)
    output.write_text("\n".join(lines) + "\n")
    with pytest.raises(CensusError, match="not an exact rational"):
        validate_bound(
            output,
            checker,
            certificate / "global-certificate.json",
            certificate / "evidence/portable/python.json",
            expected_rows=3,
            expected_revision=None,
            expected_certificate_sha256=None,
            expected_reference_sha256=None,
            checker_files=("general_pose_tree/run_n11.py",),
        )
    row["witness"] = ["3/2", "3/2"]
    lines[1] = json.dumps(row)
    output.write_text("\n".join(lines) + "\n")
    with pytest.raises(CensusError, match="fails independent exact replay"):
        validate_bound(
            output,
            checker,
            certificate / "global-certificate.json",
            certificate / "evidence/portable/python.json",
            expected_rows=3,
            expected_revision=None,
            expected_certificate_sha256=None,
            expected_reference_sha256=None,
            checker_files=("general_pose_tree/run_n11.py",),
        )


def test_huge_json_integer_is_a_typed_refusal(tmp_path: Path) -> None:
    checker, certificate, output = _run_fixture(tmp_path)
    lines = output.read_text().splitlines()
    lines[1] = lines[1].replace('"row": 0', f'"row": {"9" * 5000}')
    output.write_text("\n".join(lines) + "\n")
    with pytest.raises(CensusError, match="invalid JSON"):
        validate_bound(
            output,
            checker,
            certificate / "global-certificate.json",
            certificate / "evidence/portable/python.json",
            expected_rows=3,
            expected_revision=None,
            expected_certificate_sha256=None,
            expected_reference_sha256=None,
            checker_files=("general_pose_tree/run_n11.py",),
        )


def test_stale_source_and_mixed_row_binding_are_refused(tmp_path: Path) -> None:
    checker, certificate, output = _run_fixture(tmp_path)
    lines = output.read_text().splitlines()
    row = json.loads(lines[2])
    row["binding_sha256"] = "0" * 64
    lines[2] = json.dumps(row)
    output.write_text("\n".join(lines) + "\n")
    with pytest.raises(CensusError, match="stale or mixed binding"):
        validate_bound(
            output,
            checker,
            certificate / "global-certificate.json",
            certificate / "evidence/portable/python.json",
            expected_rows=3,
            expected_revision=None,
            expected_certificate_sha256=None,
            expected_reference_sha256=None,
            checker_files=("general_pose_tree/run_n11.py",),
        )
    checker.joinpath("general_pose_tree/run_n11.py").write_text("raise SystemExit\n")
    with pytest.raises(CensusError, match="run binding is stale or mixed"):
        validate_bound(
            tmp_path / "rows.jsonl",
            checker,
            certificate / "global-certificate.json",
            certificate / "evidence/portable/python.json",
            expected_rows=3,
            expected_revision=None,
            expected_certificate_sha256=None,
            expected_reference_sha256=None,
            checker_files=("general_pose_tree/run_n11.py",),
        )


def test_timeout_retains_bound_partial_rows_without_complete_admission(tmp_path: Path) -> None:
    checker = tmp_path / "checker"
    certificate = tmp_path / "certificate"
    output = tmp_path / "rows.jsonl"
    _write_source(checker, sleep=True)
    _write_inputs(certificate, [11, 11, 11])
    result = run_bound(
        checker,
        certificate,
        output,
        "0-2",
        # The fake checker sleeps 60 s after its first row, so the timeout still fires
        # after at least one row; two seconds leaves a loaded runner the headroom to
        # start `python -I`, read the certificate and append that row first. At 0.2 s a
        # pull-request runner on 2026-10-03 produced an empty journal instead.
        max_seconds=2.0,
        expected_rows=3,
        expected_revision=None,
        expected_certificate_sha256=None,
        expected_reference_sha256=None,
        checker_files=("general_pose_tree/run_n11.py",),
    )
    assert result["verdict"] == "PARTIAL_ROW_EQUALITY"
    assert result["process_outcome"] == "TIMEOUT"
    assert result["rows_checked"] == 1
    assert result["complete"] is False


def test_publication_race_preserves_the_competing_evidence(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    checker = tmp_path / "checker"
    certificate = tmp_path / "certificate"
    output = tmp_path / "rows.jsonl"
    _write_source(checker)
    _write_inputs(certificate, [11, 11, 11])
    original_link = os.link

    def race(source: str | Path, target: str | Path) -> None:
        Path(target).write_text("competing evidence\n")
        original_link(source, target)

    monkeypatch.setattr("devtools.check_general_pose_tree_census.os.link", race)
    with pytest.raises(CensusError, match="appeared during execution"):
        run_bound(
            checker,
            certificate,
            output,
            "0",
            max_seconds=2,
            expected_rows=3,
            expected_revision=None,
            expected_certificate_sha256=None,
            expected_reference_sha256=None,
            checker_files=("general_pose_tree/run_n11.py",),
        )
    assert output.read_text() == "competing evidence\n"


def _validate_fixture(checker: Path, certificate: Path, journal: Path) -> dict[str, object]:
    return validate_bound(
        journal,
        checker,
        certificate / "global-certificate.json",
        certificate / "evidence/portable/python.json",
        require_complete=True,
        expected_rows=3,
        expected_revision=None,
        expected_certificate_sha256=None,
        expected_reference_sha256=None,
        checker_files=("general_pose_tree/run_n11.py",),
    )


def test_packed_journal_admits_with_the_digest_of_its_inflated_bytes(tmp_path: Path) -> None:
    checker, certificate, output = _run_fixture(tmp_path)
    packed = tmp_path / "rows.jsonl.gz"
    receipt = pack_journal(output, packed)
    assert packed.read_bytes() == gzip.compress(output.read_bytes(), compresslevel=9, mtime=0)
    assert receipt["journal_sha256"] == hashlib.sha256(output.read_bytes()).hexdigest()
    plain = _validate_fixture(checker, certificate, output)
    assert _validate_fixture(checker, certificate, packed) == plain
    assert plain["verdict"] == "COMPLETE_ROW_EQUALITY"


def test_packing_refuses_overwrite_and_double_compression(tmp_path: Path) -> None:
    _, _, output = _run_fixture(tmp_path)
    packed = tmp_path / "rows.jsonl.gz"
    pack_journal(output, packed)
    with pytest.raises(CensusError, match="already exists"):
        pack_journal(output, packed)
    with pytest.raises(CensusError, match="already gzipped"):
        pack_journal(packed, tmp_path / "again.jsonl.gz")
    with pytest.raises(CensusError, match=r"must end in \.gz"):
        pack_journal(output, tmp_path / "rows.packed")


def test_malformed_and_oversized_gzip_journals_are_typed_refusals(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    checker, certificate, output = _run_fixture(tmp_path)
    packed = tmp_path / "rows.jsonl.gz"
    pack_journal(output, packed)
    data = packed.read_bytes()
    truncated = tmp_path / "truncated.jsonl.gz"
    truncated.write_bytes(data[:-8])
    with pytest.raises(CensusError, match="malformed gzip"):
        _validate_fixture(checker, certificate, truncated)
    trailing = tmp_path / "trailing.jsonl.gz"
    trailing.write_bytes(data + b"junk")
    with pytest.raises(CensusError, match="malformed gzip"):
        _validate_fixture(checker, certificate, trailing)
    corrupt = tmp_path / "corrupt.jsonl.gz"
    corrupt.write_bytes(data[:20] + bytes([data[20] ^ 0xFF]) + data[21:])
    with pytest.raises(CensusError, match="malformed gzip"):
        _validate_fixture(checker, certificate, corrupt)
    bomb = tmp_path / "bomb.jsonl.gz"
    bomb.write_bytes(gzip.compress(b"0" * 5_000_000, mtime=0))
    monkeypatch.setattr("devtools.check_general_pose_tree_census.MAX_INPUT_BYTES", 1_000_000)
    with pytest.raises(CensusError, match="inflates beyond"):
        _validate_fixture(checker, certificate, bomb)
