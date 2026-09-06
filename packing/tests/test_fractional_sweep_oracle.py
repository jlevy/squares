"""Falsify both standalone sweeps with a separate exact geometry and mass oracle.

These tests run in the ordinary quick lane. Larger seeded campaigns belong to
``python -m devtools.check_fractional_sweep --cases 20000 --seed 89213``.
Agreement on a finite corpus is a regression check, not a proof of either verifier.
"""

from __future__ import annotations

import json
from fractions import Fraction

import pytest

from devtools import check_fractional_sweep as oracle


def test_oblique_domain_and_boundary_only_cells_are_distinguished() -> None:
    """A bounding-box corner is unreachable; contact alone has no open-cell witness."""
    rotation = (Fraction(3, 5), Fraction(4, 5))
    assert not oracle.open_cell_meets_domain(
        (Fraction(13, 5), Fraction(27, 10), Fraction(1), Fraction(11, 10)),
        rotation,
        Fraction(0),
        Fraction(2),
    )
    upright = (Fraction(1), Fraction(0))
    touching = (Fraction(1), Fraction(2), Fraction(0), Fraction(1))
    assert not oracle.open_cell_meets_domain(touching, upright, Fraction(0), Fraction(1))
    narrow = (Fraction(1) - Fraction(1, 10**20), *touching[1:])
    assert oracle.open_cell_meets_domain(narrow, upright, Fraction(0), Fraction(1))


def test_coincident_events_and_closed_boundaries_preserve_the_exact_minimum() -> None:
    """At x or y = 1 two atoms enter together; those boundaries cannot lower the mass."""
    case = oracle.SweepCase(
        Fraction(2),
        Fraction(1),
        Fraction(0),
        (
            (Fraction(1, 2), Fraction(1, 2), Fraction(2, 7)),
            (Fraction(1, 2), Fraction(3, 2), Fraction(3, 11)),
            (Fraction(3, 2), Fraction(1, 2), Fraction(5, 13)),
            (Fraction(3, 2), Fraction(3, 2), Fraction(7, 17)),
        ),
    )
    result, minimal_checked = oracle.compare_case(case)
    assert result == oracle.OracleResult(Fraction(3, 11), 4)
    assert minimal_checked


def test_singleton_empty_and_empty_support_cases_are_decided() -> None:
    centered = ((Fraction(1, 4), Fraction(1, 4), Fraction(7, 11)),)
    singleton = oracle.SweepCase(Fraction(1, 2), Fraction(1, 2), Fraction(0), centered)
    result, minimal_checked = oracle.compare_case(singleton)
    assert result == oracle.OracleResult(Fraction(7, 11), 1)
    assert not minimal_checked
    empty = oracle.SweepCase(Fraction(1, 2), Fraction(1, 2), Fraction(1, 2), centered)
    result, minimal_checked = oracle.compare_case(empty)
    assert result == oracle.OracleResult(None, 0)
    assert not minimal_checked
    unsupported = oracle.SweepCase(Fraction(2), Fraction(1), Fraction(1, 2), ())
    result, minimal_checked = oracle.compare_case(unsupported)
    assert result == oracle.OracleResult(Fraction(0), 1)
    assert minimal_checked


def test_seeded_rational_corpus_checks_both_verifiers() -> None:
    report = oracle.check_cases(cases=200, seed=89213)
    assert report["verify_claim"] == 200
    assert report["minimal_verify"] > 0
    assert report["vacuous"] > 0


def test_cli_reports_reproduction_parameters(capsys: pytest.CaptureFixture[str]) -> None:
    assert oracle.main(["--cases", "12", "--seed", "89213"]) == 0
    report = json.loads(capsys.readouterr().out)
    assert report["cases"] == 12
    assert report["seed"] == 89213
    assert report["result"] == "agreement on every tested minimum and cell count"


def test_cli_refuses_an_empty_campaign() -> None:
    with pytest.raises(SystemExit) as error:
        oracle.main(["--cases", "0"])
    assert error.value.code == 2


def test_an_inflated_verifier_minimum_is_reported_with_a_reproduction(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr(
        oracle.verify_claim, "least_mass", lambda *_args: (Fraction(10**6), None, 1)
    )
    assert oracle.main(["--cases", "1", "--seed", "89213"]) == 1
    report = json.loads(capsys.readouterr().out)
    assert report["result"] == "disagreement"
    assert "seed=89213, case=0" in report["detail"]
    assert "verify_claim: expected" in report["detail"]


def test_a_wrong_cell_count_is_detected_even_when_the_minimum_agrees(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    case = oracle.SweepCase(Fraction(2), Fraction(1), Fraction(1, 2), ())
    monkeypatch.setattr(oracle.minimal_verify, "sweep", lambda *_args: (0, 99))
    with pytest.raises(AssertionError, match="minimal_verify: expected"):
        oracle.compare_case(case)
