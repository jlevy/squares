"""Controls for the threshold-certificate gate.

The gate exists so that a threshold certificate cannot be retained on one route's word.
What matters is that it refuses: a lowered orbit is refused by the interval route before
the sweep runs, a declaration that disagrees with either route is refused, a closed-form
failure is refused before either route runs, and the positive control prints
``RETAINABLE`` only with both routes agreeing on the digit and the bytes' digest.
"""

from __future__ import annotations

import hashlib
import json
from collections.abc import Callable
from fractions import Fraction
from pathlib import Path
from typing import Never

import pytest

import devtools.decide_threshold_certificate as gate
from devtools.decide_threshold_certificate import decide, load, main
from sqpack.fractional.threshold import ThresholdAtom, ThresholdCertificate
from tests.test_fractional_threshold_interval import rescaled, tight_certificate


def bomb(*_args: object, **_kwargs: object) -> Never:
    raise AssertionError("a route ran after a decisive refusal")


def no_routes(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(gate, "verify_threshold_by_intervals", bomb)
    monkeypatch.setattr(gate, "minimum_charge", bomb)


def _record(certificate: ThresholdCertificate) -> dict[str, object]:
    return {
        "id": "C-test-threshold",
        "variant": "threshold",
        "n": certificate.n,
        "claim": f"s({certificate.n}) >= {certificate.outer_side}",
        "outer_side": str(certificate.outer_side),
        "square_side": str(certificate.square_side),
        "angle_limit": "207107/500000",
        "direction_steps": 6,
        "symmetry": "D4",
        "total_budget": str(certificate.total_budget),
        "atoms": [[str(a.x), str(a.y), str(a.weight)] for a in certificate.atoms],
        "threshold_atoms": [t.to_record() for t in certificate.threshold_atoms],
    }


def write(
    tmp_path: Path,
    certificate: ThresholdCertificate,
    edit: Callable[[dict[str, object]], None] | None = None,
) -> Path:
    record = _record(certificate)
    if edit is not None:
        edit(record)
    path = tmp_path / "candidate.json"
    path.write_text(json.dumps(record, indent=1))
    return path


@pytest.fixture(scope="module")
def tight() -> ThresholdCertificate:
    return tight_certificate()


def test_the_loader_rebuilds_the_certificate_from_its_own_bytes(
    tmp_path: Path, tight: ThresholdCertificate
) -> None:
    path = write(tmp_path, tight)
    certificate, record = load(path.read_bytes())
    # The loader labels atoms by index; everything the theorem reads must round-trip.
    assert [(a.x, a.y, a.weight) for a in certificate.atoms] == [
        (a.x, a.y, a.weight) for a in tight.atoms
    ]
    assert certificate.threshold_atoms == tight.threshold_atoms
    assert certificate.half_tangents == tight.half_tangents
    assert (certificate.n, certificate.outer_side, certificate.square_side) == (
        tight.n,
        tight.outer_side,
        tight.square_side,
    )
    assert record["variant"] == "threshold"
    assert certificate.total_budget == Fraction(str(record["total_budget"]))


def test_the_two_route_gate_retains_the_tight_fixture_and_prints_its_digest(
    tmp_path: Path, tight: ThresholdCertificate, capsys: pytest.CaptureFixture[str]
) -> None:
    path = write(tmp_path, tight)
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    assert decide(path, workers=1) is True
    out = capsys.readouterr().out
    assert "interval accepted=True enclosure=(Fraction(1, 1), Fraction(1, 1))" in out
    assert "exact    least cell charge 1 = 1.000000000" in out
    assert f"RETAINABLE: both routes accept and agree at 1; sha256 {digest}" in out
    assert "no least_cell_charge is declared" in out


def test_a_declared_least_charge_is_checked_against_both_routes(
    tmp_path: Path, tight: ThresholdCertificate, capsys: pytest.CaptureFixture[str]
) -> None:
    path = write(tmp_path, tight, lambda r: r.__setitem__("least_cell_charge", "1"))
    assert decide(path, workers=1) is True
    assert "RETAINABLE" in capsys.readouterr().out
    path = write(tmp_path, tight, lambda r: r.__setitem__("least_cell_charge", "1/2"))
    assert decide(path, workers=1) is False
    out = capsys.readouterr().out
    assert "declared least_cell_charge 1/2 != interval enclosure 1" in out
    assert "RETAINABLE" not in out


def test_quick_mode_accepts_but_says_it_cannot_retain(
    tmp_path: Path, tight: ThresholdCertificate, capsys: pytest.CaptureFixture[str]
) -> None:
    path = write(tmp_path, tight)
    assert decide(path, workers=1, mode="quick") is True
    out = capsys.readouterr().out
    assert "NOT ENOUGH TO RETAIN" in out
    assert "RETAINABLE" not in out
    assert "exact    least" not in out


def test_exact_only_mode_is_the_spike_tools_one_route(
    tmp_path: Path, tight: ThresholdCertificate, capsys: pytest.CaptureFixture[str]
) -> None:
    path = write(tmp_path, tight)
    assert decide(path, workers=1, mode="exact-only") is True
    out = capsys.readouterr().out
    assert "ACCEPTED (one exact route; retention wants an independent verifier)" in out
    assert "RETAINABLE" not in out
    assert "interval accepted" not in out


def test_a_lightened_orbit_is_refused_by_the_interval_route_before_the_sweep(
    tmp_path: Path,
    tight: ThresholdCertificate,
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Every weight scaled by 9/10 keeps Condition 1' and drops the least charge to 9/10:
    the interval route refutes it, the exact witness is re-evaluated in rationals and
    printed, and the sweep never runs."""
    monkeypatch.setattr(gate, "minimum_charge", bomb)
    path = write(tmp_path, rescaled(tight, Fraction(9, 10)))
    assert decide(path, workers=1) is False
    out = capsys.readouterr().out
    assert "the interval route refused it" in out
    assert "REFUTING WITNESS" in out
    assert "exact charge 9/10 = 0.900000000, admissible True" in out
    assert "RETAINABLE" not in out


def test_a_broken_symmetry_is_refused_before_either_route(
    tmp_path: Path,
    tight: ThresholdCertificate,
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    no_routes(monkeypatch)
    first = tight.threshold_atoms[0]
    lightened = ThresholdAtom(first.points, first.threshold, first.weight / 2)
    broken = ThresholdCertificate(
        n=tight.n,
        outer_side=tight.outer_side,
        square_side=tight.square_side,
        atoms=tight.atoms,
        threshold_atoms=(lightened, *tight.threshold_atoms[1:]),
        half_tangents=tight.half_tangents,
    )
    path = write(tmp_path, broken)
    assert decide(path, workers=1) is False
    out = capsys.readouterr().out
    assert "Condition 1' threshold atoms carry the declared symmetry failed" in out


@pytest.mark.parametrize(
    "case",
    [
        ("claim", "s(100) >= 4", "theorem conclusion"),
        ("total_budget", "1/2", "declared total_budget"),
        ("variant", "class", "decides only 'threshold' certificates"),
        ("n", 10, "Condition 2' total budget below n failed"),
    ],
)
def test_declarations_and_closed_form_failures_are_refused_before_either_route(
    tmp_path: Path,
    tight: ThresholdCertificate,
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
    case: tuple[str, object, str],
) -> None:
    field, value, message = case
    no_routes(monkeypatch)
    path = write(tmp_path, tight, lambda r: r.__setitem__(field, value))
    assert decide(path, workers=1) is False
    assert message in capsys.readouterr().out


def test_an_inexact_number_anywhere_in_the_file_is_refused(
    tmp_path: Path, tight: ThresholdCertificate, capsys: pytest.CaptureFixture[str]
) -> None:
    path = write(tmp_path, tight, lambda r: r.__setitem__("provenance", {"objective": 1.5}))
    assert decide(path, workers=1) is False
    assert "inexact JSON number '1.5'" in capsys.readouterr().out


@pytest.mark.parametrize(
    "fields",
    [
        {"variant": "weighted-threshold/v1", "multiplicities": []},
        {"variant": "weighted-threshold/v1", "multiplicities": [1, 1, 1]},
        {"variant": "weighted-threshold/v1", "multiplicities": [True, 1, 1]},
        {"variant": None},
        {"multiplicities": None},
        {"weighted_points": None},
    ],
)
def test_declared_weighted_fields_are_refused_before_normalization_or_coverage(
    tmp_path: Path,
    tight: ThresholdCertificate,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    fields: dict[str, object],
) -> None:
    no_routes(monkeypatch)
    record = json.loads(json.dumps(_record(tight)))
    record["threshold_atoms"][0].update(fields)
    data = json.dumps(record).encode()
    with pytest.raises(gate.FormatError, match="unweighted atoms only"):
        load(data)
    path = tmp_path / "weighted.json"
    path.write_bytes(data)
    assert decide(path, workers=1) is False
    out = capsys.readouterr().out
    assert "REFUSED" in out
    assert "unweighted atoms only" in out
    assert "RETAINABLE" not in out


def test_a_current_weighted_model_record_cannot_enter_coverage(
    tight: ThresholdCertificate, monkeypatch: pytest.MonkeyPatch
) -> None:
    no_routes(monkeypatch)
    first = tight.threshold_atoms[0]
    weighted = ThresholdAtom(first.points, first.threshold, first.weight, (2, 1, 1))
    record = json.loads(json.dumps(_record(tight)))
    record["threshold_atoms"][0] = weighted.to_record()
    assert "points" not in record["threshold_atoms"][0]
    with pytest.raises(gate.FormatError, match="unweighted atoms only"):
        load(json.dumps(record).encode())


def test_the_command_line_runs_the_modes_and_skips_a_duplicate_path(
    tmp_path: Path, tight: ThresholdCertificate, capsys: pytest.CaptureFixture[str]
) -> None:
    path = write(tmp_path, tight)
    assert main(["--quick", str(path), str(path)]) == 0
    out = capsys.readouterr().out
    assert "SKIPPED duplicate path" in out
    assert "NOT ENOUGH TO RETAIN" in out
    assert main(["--exact-only", "--workers", "2", str(path)]) == 0
    assert "one exact route" in capsys.readouterr().out
    assert main([str(tmp_path / "missing.json")]) == 1
    assert "REFUSED" in capsys.readouterr().out
