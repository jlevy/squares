"""Public command behavior for Witness/v2 artifacts."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path

from sqpack.cli.witness import main
from sqpack.witness import load_witness, witness_document

ROOT = Path(__file__).resolve().parents[1]
WITNESSES = ROOT / "witnesses"


def test_inspect_makes_no_assurance_claim(capsys) -> None:
    status = main(["inspect", str(WITNESSES / "grid-n004.yaml")])

    captured = capsys.readouterr()
    assert status == 0
    assert "INSPECTED — no assurance claim" in captured.out
    assert "VERIFIED" not in captured.out


def test_numerical_check_is_never_reported_as_verification(capsys) -> None:
    status = main(
        [
            "check",
            str(WITNESSES / "grid-n004.yaml"),
            "--method",
            "numerical-f64",
            "--precision",
            "53",
            "--tolerance",
            "1e-12",
        ]
    )

    captured = capsys.readouterr()
    assert status == 0
    assert "NUMERIC CHECK PASSED — not verification" in captured.out
    assert "VERIFIED" not in captured.out


def test_exact_rational_witness_is_verified(capsys) -> None:
    status = main(["verify", str(WITNESSES / "grid-n004.yaml")])

    captured = capsys.readouterr()
    assert status == 0
    assert captured.out.startswith("VERIFIED\n")
    assert "method: exact-algebraic" in captured.out


def test_exact_algebraic_witness_can_be_inspected_and_verified(capsys) -> None:
    witness = WITNESSES / "rotated-n001-sqrt2.yaml"
    assert main(["inspect", str(witness)]) == 0
    inspected = capsys.readouterr()
    assert "INSPECTED — no assurance claim" in inspected.out

    assert main(["verify", str(witness)]) == 0
    verified = capsys.readouterr()
    assert verified.out.startswith("VERIFIED\n")


def test_decimal_witness_has_a_typed_formal_gap(capsys) -> None:
    status = main(["verify", str(WITNESSES / "schadt-n029-2025-decimal.yaml")])

    captured = capsys.readouterr()
    assert status == 2
    assert "formal-certificate-missing" in captured.err
    assert "decimal geometry is numerical data" in captured.err


def test_binary64_rejects_a_fictitious_precision(capsys) -> None:
    status = main(
        [
            "check",
            str(WITNESSES / "grid-n004.yaml"),
            "--method",
            "numerical-f64",
            "--precision",
            "64",
            "--tolerance",
            "1e-12",
        ]
    )

    captured = capsys.readouterr()
    assert status == 2
    assert "numerical-f64 has exactly 53 binary precision bits" in captured.err


def test_interval_witness_reports_that_replay_is_unbuilt(capsys, tmp_path: Path) -> None:
    interval = deepcopy(load_witness(WITNESSES / "grid-n004.yaml"))
    interval["id"] = "W-interval-replay-control"
    interval["claim"]["method"] = "interval-certified"
    path = tmp_path / "interval.yaml"
    path.write_text(witness_document(interval), encoding="utf-8")

    status = main(["verify", str(path)])

    captured = capsys.readouterr()
    assert status == 2
    assert "checker-not-built" in captured.err
    assert "generic interval certificate checker is not built" in captured.err


def test_interval_promotion_reports_the_unbuilt_checker(capsys, tmp_path: Path) -> None:
    status = main(
        [
            "promote",
            str(WITNESSES / "schadt-n029-2025-decimal.yaml"),
            "--strategy",
            "interval-existence",
            "--max-side-increase",
            "0",
            "--output-witness",
            str(tmp_path / "unused.yaml"),
        ]
    )

    captured = capsys.readouterr()
    assert status == 2
    assert "checker-not-built" in captured.err
    assert "buildable path for suitable contact systems" in captured.err
