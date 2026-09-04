"""Controls for the retention gate.

The gate exists so that a rung cannot join the record on one route's word, or on
a lane's report of bytes that have since changed. What matters is that it refuses:
a gate nobody has watched refuse is a gate nobody has tested.
"""

from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path

import pytest

from devtools.decide_certificate import decide, load

CASES = Path(__file__).resolve().parent.parent / "cases"
RUNG = CASES / "n11_fractional_certificate" / "certificate-19-5.json"


def write(tmp_path: Path, edit) -> Path:
    record = json.loads(RUNG.read_text())
    edit(record)
    path = tmp_path / "candidate.json"
    path.write_text(json.dumps(record, indent=1))
    return path


def test_the_gate_reads_the_bytes_and_recomputes_rather_than_trusting_the_summary() -> None:
    certificate, record = load(RUNG)
    assert certificate.total_mass == Fraction(record["total_mass"])
    assert certificate.outer_side == Fraction(19, 5)
    assert len(certificate.atoms) == 425


def test_a_declared_mass_that_disagrees_with_the_atoms_is_refused(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    path = write(tmp_path, lambda r: r.__setitem__("total_mass", "1/2"))
    assert decide(path, quick=True) is False
    assert "declared total_mass" in capsys.readouterr().out


def test_a_side_above_the_ceiling_is_refused_before_any_sweep_runs(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """Four B-squares across fit at 4, so C4 would force the mass past eleven."""

    def widen(record: dict) -> None:
        record["outer_side"] = "4"
        record["total_mass"] = str(sum(Fraction(a[2]) for a in record["atoms"]))

    path = write(tmp_path, widen)
    assert decide(path, quick=True) is False
    out = capsys.readouterr().out
    assert "above the ceiling" in out


def test_a_mass_that_does_not_fall_below_n_is_refused(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    def heavy(record: dict) -> None:
        record["atoms"] = [[x, y, str(Fraction(w) * 2)] for x, y, w in record["atoms"]]
        record["total_mass"] = str(sum(Fraction(a[2]) for a in record["atoms"]))

    path = write(tmp_path, heavy)
    assert decide(path, quick=True) is False
    assert "does not fall below the declared n" in capsys.readouterr().out


def test_quick_mode_says_it_cannot_retain(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """A passing quick run must not read as a retention decision."""
    assert decide(RUNG, quick=True) is True
    assert "NOT ENOUGH TO RETAIN" in capsys.readouterr().out


@pytest.mark.exhaustive_exact
def test_a_retained_rung_passes_both_routes_and_they_agree(
    capsys: pytest.CaptureFixture[str],
) -> None:
    assert decide(RUNG, quick=False) is True
    out = capsys.readouterr().out
    assert "RETAINABLE" in out
    assert "50003/50000" in out
