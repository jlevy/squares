"""Controls for the retention gate.

The gate exists so that a rung cannot join the record on one route's word, or on
a lane's report of bytes that have since changed. What matters is that it refuses:
a gate nobody has watched refuse is a gate nobody has tested.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Never

import pytest

import devtools.decide_certificate as retention
from devtools.decide_certificate import decide, load

CASES = Path(__file__).resolve().parent.parent / "cases"
RUNG = CASES / "n11_fractional_certificate" / "certificate-19-5.json"


@dataclass(frozen=True)
class FakeDirection:
    boxes: int = 1
    stalled: int = 0


@dataclass(frozen=True)
class FakeIntervalVerdict:
    accepted: bool = True
    enclosure: tuple[Fraction, Fraction] | None = (
        Fraction(50003, 50000),
        Fraction(50003, 50000),
    )
    failures: tuple[str, ...] = ()
    directions: tuple[FakeDirection, ...] = (FakeDirection(),)


@dataclass(frozen=True)
class FakeExactVerdict:
    accepted: bool = True
    minimum_cell_mass: Fraction | None = Fraction(50003, 50000)
    failures: tuple[str, ...] = ()


def bomb(*_args: object, **_kwargs: object) -> Never:
    raise AssertionError("a certificate sweep ran after a decisive refusal")


def no_sweeps(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(retention, "verify", bomb)
    monkeypatch.setattr(retention, "verify_by_intervals", bomb)


def write(tmp_path: Path, edit) -> Path:
    record = json.loads(RUNG.read_text())
    edit(record)
    path = tmp_path / "candidate.json"
    path.write_text(json.dumps(record, indent=1))
    return path


def test_the_gate_reads_the_bytes_and_recomputes_rather_than_trusting_the_summary() -> None:
    certificate, record = load(RUNG)
    total_mass = record["total_mass"]
    assert isinstance(total_mass, str)
    assert certificate.total_mass == Fraction(total_mass)
    assert certificate.outer_side == Fraction(19, 5)
    assert len(certificate.atoms) == 425


def test_the_gate_describes_its_independence_boundary() -> None:
    assert retention.__doc__ is not None
    assert "share the certificate and theorem contract" in retention.__doc__
    assert "share no modelling assumption" not in retention.__doc__


def test_a_declared_mass_that_disagrees_with_the_atoms_is_refused(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    no_sweeps(monkeypatch)
    path = write(tmp_path, lambda r: r.__setitem__("total_mass", "1/2"))
    assert decide(path, quick=True) is False
    assert "declared total_mass" in capsys.readouterr().out


def test_a_side_above_the_ceiling_is_refused_before_any_sweep_runs(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Four B-squares across fit at 4, so C4 would force the mass past eleven."""

    def widen(record: dict) -> None:
        record["outer_side"] = "4"
        record["total_mass"] = str(sum(Fraction(a[2]) for a in record["atoms"]))

    no_sweeps(monkeypatch)
    path = write(tmp_path, widen)
    assert decide(path, quick=True) is False
    out = capsys.readouterr().out
    assert "above the ceiling" in out


def test_a_mass_that_does_not_fall_below_n_is_refused(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def heavy(record: dict) -> None:
        record["atoms"] = [[x, y, str(Fraction(w) * 2)] for x, y, w in record["atoms"]]
        record["total_mass"] = str(sum(Fraction(a[2]) for a in record["atoms"]))

    no_sweeps(monkeypatch)
    path = write(tmp_path, heavy)
    assert decide(path, quick=True) is False
    assert "does not fall below the declared n" in capsys.readouterr().out


def test_a_false_declared_claim_is_refused_before_any_sweep(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    no_sweeps(monkeypatch)
    path = write(tmp_path, lambda record: record.__setitem__("claim", "s(11) >= 4"))
    assert decide(path, quick=True) is False
    assert "theorem conclusion" in capsys.readouterr().out


@pytest.mark.parametrize("field", ["claim", "total_mass"])
def test_required_declarations_cannot_be_deleted(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
    field: str,
) -> None:
    no_sweeps(monkeypatch)
    path = write(tmp_path, lambda record: record.pop(field))
    assert decide(path, quick=True) is False
    assert f"missing required field '{field}'" in capsys.readouterr().out


def test_quick_mode_allows_an_undecided_least_mass_but_cannot_retain(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    path = write(tmp_path, lambda record: record.pop("least_cell_mass"))
    monkeypatch.setattr(
        retention,
        "verify_by_intervals",
        lambda *_args, **_kwargs: FakeIntervalVerdict(),
    )
    monkeypatch.setattr(retention, "verify", bomb)
    assert decide(path, quick=True) is True
    assert "NOT ENOUGH TO RETAIN" in capsys.readouterr().out


def test_full_mode_requires_the_declared_least_mass_before_any_sweep(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    no_sweeps(monkeypatch)
    path = write(tmp_path, lambda record: record.pop("least_cell_mass"))
    assert decide(path, quick=False) is False
    assert "missing required field 'least_cell_mass'" in capsys.readouterr().out


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("n", 11.9),
        ("n", "11"),
        ("n", True),
        ("direction_steps", 180.9),
        ("direction_steps", "180"),
        ("direction_steps", True),
    ],
)
def test_integer_fields_refuse_lossy_or_coercive_types(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
    field: str,
    value: object,
) -> None:
    no_sweeps(monkeypatch)
    path = write(tmp_path, lambda record: record.__setitem__(field, value))
    assert decide(path, quick=True) is False
    out = capsys.readouterr().out
    assert f"field '{field}'" in out or "inexact JSON number" in out


def test_duplicate_keys_are_refused(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    no_sweeps(monkeypatch)
    text = RUNG.read_text().replace('"n": 11,', '"n": 11,\n "n": 12,', 1)
    path = tmp_path / "duplicate.json"
    path.write_text(text)
    assert decide(path, quick=True) is False
    assert "duplicate JSON object key 'n'" in capsys.readouterr().out


def test_an_interval_refusal_stops_before_the_exact_sweep(
    capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(
        retention,
        "verify_by_intervals",
        lambda *_args, **_kwargs: FakeIntervalVerdict(
            accepted=False, failures=("C4",)
        ),
    )
    monkeypatch.setattr(retention, "verify", bomb)
    assert decide(RUNG, quick=False) is False
    assert "interval route refused" in capsys.readouterr().out


@pytest.mark.parametrize(
    "enclosure",
    [None, (Fraction(1), Fraction(1001, 1000))],
)
def test_full_mode_refuses_an_unusable_interval_enclosure_before_exact(
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
    enclosure: tuple[Fraction, Fraction] | None,
) -> None:
    monkeypatch.setattr(
        retention,
        "verify_by_intervals",
        lambda *_args, **_kwargs: FakeIntervalVerdict(enclosure=enclosure),
    )
    monkeypatch.setattr(retention, "verify", bomb)
    assert decide(RUNG, quick=False) is False
    out = capsys.readouterr().out
    assert "no enclosure" in out or "enclosure has width" in out


def test_an_exact_refusal_is_verdict_bearing(
    capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(
        retention,
        "verify_by_intervals",
        lambda *_args, **_kwargs: FakeIntervalVerdict(),
    )
    monkeypatch.setattr(
        retention,
        "verify",
        lambda _certificate: FakeExactVerdict(accepted=False, failures=("C4",)),
    )
    assert decide(RUNG, quick=False) is False
    assert "exact sweep refused" in capsys.readouterr().out


def test_exact_and_interval_disagreement_is_verdict_bearing(
    capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(
        retention,
        "verify_by_intervals",
        lambda *_args, **_kwargs: FakeIntervalVerdict(),
    )
    monkeypatch.setattr(
        retention,
        "verify",
        lambda _certificate: FakeExactVerdict(minimum_cell_mass=Fraction(1)),
    )
    assert decide(RUNG, quick=False) is False
    assert "two routes disagree" in capsys.readouterr().out


def test_a_declared_least_mass_must_match_both_routes(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    path = write(tmp_path, lambda record: record.__setitem__("least_cell_mass", "1"))
    monkeypatch.setattr(
        retention,
        "verify_by_intervals",
        lambda *_args, **_kwargs: FakeIntervalVerdict(),
    )
    monkeypatch.setattr(
        retention,
        "verify",
        lambda _certificate: FakeExactVerdict(),
    )
    assert decide(path, quick=False) is False
    assert "declared least_cell_mass 1 != 50003/50000" in capsys.readouterr().out


def test_every_positive_decision_message_is_flushed(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    flushes: list[object] = []

    def record_print(*_args: object, **kwargs: object) -> None:
        flushes.append(kwargs.get("flush"))

    monkeypatch.setattr(
        retention,
        "verify_by_intervals",
        lambda *_args, **_kwargs: FakeIntervalVerdict(),
    )
    monkeypatch.setattr(retention, "verify", lambda _certificate: FakeExactVerdict())
    monkeypatch.setattr("builtins.print", record_print)
    assert decide(RUNG, quick=False) is True
    assert flushes
    assert all(flush is True for flush in flushes)


def test_main_continues_after_a_malformed_path_and_aggregates_failure(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    no_sweeps(monkeypatch)
    broken = tmp_path / "broken.json"
    broken.write_text("{")
    missing = tmp_path / "missing.json"
    missing.write_text("{}")
    assert retention.main(["--quick", str(broken), str(missing)]) == 1
    out = capsys.readouterr().out
    assert "broken.json: REFUSED" in out
    assert "missing.json: REFUSED" in out


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
