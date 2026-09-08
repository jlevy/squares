"""Synthetic quench outcomes preserve regression failures without assigning a cause."""

from __future__ import annotations

import json
import math
from pathlib import Path
from unittest.mock import Mock

import pytest

from devtools import check_regressions as checks
from sqpack.research.quench import FixedPointResult, QuenchResult


def result(side: float, reason: str, *, converged: bool = False) -> QuenchResult:
    return QuenchResult(
        side=side,
        x=[0.5],
        y=[0.5],
        theta=[0.0],
        lp_solves=17,
        angle_steps=3,
        converged=converged,
        cell_changes=2,
        reason=reason,
    )


@pytest.fixture(autouse=True)
def forbid_real_solver(monkeypatch: pytest.MonkeyPatch) -> None:
    def forbidden(*_args: object, **_kwargs: object) -> object:
        raise AssertionError("diagnostic tests must not solve an LP")

    monkeypatch.setattr(checks.quench_module, "linprog", forbidden)


def test_offset_budget_failure_reports_observation_not_inferred_cause(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(checks, "seed_config", lambda: {"x": [0.5], "y": [0.5], "t": [0.0]})
    solver = Mock(
        side_effect=[
            result(checks.TRUMP, "settled", converged=True),
            result(checks.TRUMP, "time budget exhausted during angle sweep"),
        ]
    )
    monkeypatch.setattr(checks, "quench_bracket", solver)
    message = checks.check_angle_search_converges()
    assert message is not None
    assert "two full turns" in message
    assert "reason='time budget exhausted during angle sweep'" in message
    assert "converged=False" in message
    assert "side_gap=+0.00e+00" in message
    assert "lp_solves=17" in message
    assert "has regressed" not in message
    assert [call.kwargs["time_budget"] for call in solver.call_args_list] == [60, 60]


def mock_cell_control(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    outcome: QuenchResult,
    *,
    closure: bool = False,
) -> Mock:
    archive = tmp_path / "campaign/series/series-000-smoke-and-calibration/results"
    archive.mkdir(parents=True)
    (archive / "exp-002-baseline-n10-positive-control.jsonl").write_text(
        json.dumps(
            {
                "kind": "chain",
                "n": 10,
                "seed": 2,
                "best_side": 4,
                "x": [0.5],
                "y": [0.5],
                "t": [0],
            }
        )
    )
    monkeypatch.setattr(checks, "ROOT", tmp_path)
    fixed = FixedPointResult(
        side=4.0,
        x=[0.5],
        y=[0.5],
        solves=5,
        changes=1,
        settled=True,
        reason="adjacent cell closure (synthetic)" if closure else "synthetic fixed cell",
    )
    monkeypatch.setattr(checks, "solve_to_fixed_point", Mock(return_value=fixed))

    def quench(*_args: object, **_kwargs: object) -> QuenchResult:
        checks.quench_module.solve_to_fixed_point([0.0], [0.5], [0.5], 1)
        return outcome

    solver = Mock(side_effect=quench)
    monkeypatch.setattr(checks, "quench_bracket", solver)
    return solver


@pytest.mark.parametrize(
    ("reason", "expected"),
    [
        (
            "time budget exhausted",
            "wall budget exhausted before adjacent-cell closure coverage",
        ),
        ("angle search settled", "no adjacent-cell closure observed"),
    ],
)
def test_missing_closure_reports_budget_separately(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, reason: str, expected: str
) -> None:
    outcome = result(3 + 0.5 * math.sqrt(2), reason)
    solver = mock_cell_control(monkeypatch, tmp_path, outcome)
    message = checks.check_cell_solve_is_not_a_quench()
    assert message is not None
    assert message.startswith("D-168:")
    assert expected in message
    assert f"reason={reason!r}" in message
    assert "converged=False" in message
    assert "side_gap=+0.00e+00" in message
    assert "lp_solves=17" in message
    assert "closure_count=0" in message
    assert solver.call_args.kwargs["time_budget"] == 60


def test_quench_gap_failure_retains_counts_and_observed_reason(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    outcome = result(3 + 0.5 * math.sqrt(2) + 1e-5, "time budget exhausted")
    mock_cell_control(monkeypatch, tmp_path, outcome, closure=True)
    message = checks.check_cell_solve_is_not_a_quench()
    assert message is not None
    assert message.startswith("D-029:")
    assert "reason='time budget exhausted'" in message
    assert "converged=False" in message
    assert "side_gap=+1.00e-05" in message
    assert "lp_solves=17" in message
    assert "closure_count=1" in message


def test_successful_controls_still_pass(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.setattr(checks, "seed_config", lambda: {"x": [0.5], "y": [0.5], "t": [0.0]})
    monkeypatch.setattr(
        checks,
        "quench_bracket",
        Mock(return_value=result(checks.TRUMP, "settled", converged=True)),
    )
    assert checks.check_angle_search_converges() is None
    mock_cell_control(
        monkeypatch,
        tmp_path,
        result(3 + 0.5 * math.sqrt(2), "settled", converged=True),
        closure=True,
    )
    assert checks.check_cell_solve_is_not_a_quench() is None


@pytest.mark.parametrize(("gap", "defect"), [(0.0, "D-019:"), (1e-5, "D-016:")])
def test_unshifted_failure_keeps_diagnostics(
    monkeypatch: pytest.MonkeyPatch, gap: float, defect: str
) -> None:
    monkeypatch.setattr(checks, "seed_config", lambda: {"x": [0.5], "y": [0.5], "t": [0.0]})
    solver = Mock(return_value=result(checks.TRUMP + gap, "time budget exhausted"))
    monkeypatch.setattr(checks, "quench_bracket", solver)
    message = checks.check_angle_search_converges()
    assert message is not None
    assert message.startswith(defect)
    assert "reason='time budget exhausted'" in message
    assert "converged=False" in message
    assert "lp_solves=17" in message
    assert solver.call_count == 1
    assert solver.call_args.kwargs["time_budget"] == 60


def test_fixed_cell_gap_failure_reports_settlement(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    analytic = 3 + 0.5 * math.sqrt(2)
    solver = mock_cell_control(monkeypatch, tmp_path, result(analytic, "unused"))
    fixed = FixedPointResult(
        side=analytic,
        x=[0.5],
        y=[0.5],
        solves=5,
        changes=1,
        settled=False,
        reason="synthetic unsettled fixed cell",
    )
    monkeypatch.setattr(checks, "solve_to_fixed_point", Mock(return_value=fixed))
    message = checks.check_cell_solve_is_not_a_quench()
    assert message is not None
    assert message.startswith("D-029:")
    assert "reason='synthetic unsettled fixed cell'" in message
    assert "settled=False" in message
    assert "solves=5" in message
    assert solver.call_count == 0
