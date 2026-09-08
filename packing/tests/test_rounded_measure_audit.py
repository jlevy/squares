"""Exact source replay and refusal controls for the E.1 correction."""

from __future__ import annotations

import json
import subprocess
import sys
from fractions import Fraction
from pathlib import Path

from devtools.rounded_measure_audit import audit, load_certificate

PACKING = Path(__file__).resolve().parents[1]
CERTIFICATE = PACKING / "cases/n11_fractional_certificate/certificate.json"


def test_retained_measure_loses_the_corner_atom_after_scaling() -> None:
    certificate = load_certificate(CERTIFICATE)
    results = [
        audit(
            certificate,
            scale=scale,
            delta=delta,
            cx=Fraction(1, 2),
            cy=Fraction(1, 2),
            half_tangent=Fraction(0),
        )
        for scale, delta in ((Fraction(1), Fraction(0)), (Fraction(128, 127), Fraction(3, 500)))
    ]
    assert results[0]["rounded_square_mass"] == "4001/4000"
    assert results[1]["rounded_square_mass"] == "85353/100000"
    assert results[0]["status"] == "covered_pose"
    assert results[1]["status"] == "counterexample"
    assert all(result["independent_distance_agreement_count"] == 1121 for result in results)
    assert set(results[0]["included_atom_indices"]) - set(
        results[1]["included_atom_indices"]
    ) == {316}
    assert Fraction(certificate["atoms"][316][2]) == Fraction(917, 6250)


def test_cli_distinguishes_counterexample_replay_from_claim_failure(tmp_path: Path) -> None:
    output = tmp_path / "audit.json"
    command = [
        sys.executable,
        "-m",
        "devtools.rounded_measure_audit",
        str(CERTIFICATE),
        "--scale",
        "128/127",
        "--delta",
        "3/500",
        "--cx",
        "1/2",
        "--cy",
        "1/2",
        "--output",
        str(output),
    ]
    failure = subprocess.run(
        command, cwd=PACKING, check=False, capture_output=True, text=True, timeout=10
    )
    assert failure.returncode == 1
    assert json.loads(output.read_text())["status"] == "counterexample"
    checked = subprocess.run(
        [*command, "--expect", "below-one"],
        cwd=PACKING,
        check=False,
        capture_output=True,
        text=True,
        timeout=10,
    )
    assert checked.returncode == 0
    result = json.loads(checked.stdout)
    assert result == json.loads(output.read_text())
    assert result["expectation_met"] is True
    assert result["source"]["tool_path"] == "packing/devtools/rounded_measure_audit.py"
    invalid = subprocess.run(
        [*command, "--cx", "0"],
        cwd=PACKING,
        check=False,
        capture_output=True,
        text=True,
        timeout=10,
    )
    assert invalid.returncode == 2
    assert json.loads(invalid.stdout)["status"] == "error"


def test_measure_mass_guard_rejects_a_corrupt_record() -> None:
    certificate = load_certificate(CERTIFICATE)
    certificate["total_mass"] = "0"
    try:
        audit(
            certificate,
            scale=Fraction(1),
            delta=Fraction(0),
            cx=Fraction(1, 2),
            cy=Fraction(1, 2),
            half_tangent=Fraction(0),
        )
    except ValueError as error:
        assert "total_mass" in str(error)
    else:
        raise AssertionError("corrupt total_mass was accepted")
