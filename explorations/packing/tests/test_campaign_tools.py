"""Failure-path contracts for repository-bound campaign applications."""

from __future__ import annotations

import datetime as dt
from pathlib import Path
from typing import cast

import pytest
import yaml
from jsonschema import Draft202012Validator

from cases.campaign_smoke import baseline_sweep
from sqpack.campaign import ledger, runner


def _empty_board_ids() -> tuple[set[str], set[str]]:
    """Remove unrelated idea-board state from isolated session tests."""
    return set(), set()


def _bounded_phase(
    number: int,
    *,
    status: str,
    objective: str,
    start_minute: int,
    clock_role: str = "work",
) -> dict[str, object]:
    """One complete contemporaneous phase for whole-session contract tests."""
    entered_by = "session_start" if number == 1 else "evidence_checkpoint"
    switch_reason = None if number == 1 else "The prior bounded objective closed."
    return {
        "workflow": "process-review",
        "focus": "process",
        "recording": "contemporaneous",
        "clock_role": clock_role,
        "objective": objective,
        "status": status,
        "entered_by": entered_by,
        "switch_reason": switch_reason,
        "budget_minutes": 10,
        "started_at": f"2026-08-24T00:{start_minute:02d}:00+00:00",
        "deadline_at": f"2026-08-24T00:{start_minute + 10:02d}:00+00:00",
        "expected_output": "A bounded contract receipt.",
        "validation_command": "packing-ledger check",
        "kill_condition": "Stop at the phase deadline.",
        "fallback": "Retain the last valid receipt.",
        "outcome": "The bounded objective closed.",
        "evidence": ["Focused contract fixture"],
        "stop_reason": "The declared output was retained.",
        "next_action": "Proceed to the next declared phase.",
    }


def _bounded_session(*, max_cycles: int, active: bool = False) -> dict[str, object]:
    """Minimal clocked session accepted by the whole-set checker."""
    phases = [
        _bounded_phase(
            1, status="completed", objective="Check the first slice.", start_minute=0
        ),
        _bounded_phase(
            2,
            status="in_progress" if active else "stopped",
            objective="Check the renewed slice.",
            start_minute=10,
        ),
    ]
    session: dict[str, object] = {
        "id": "session-999",
        "_path": Path("session-999-contract-test.md"),
        "status": "in_progress" if active else "stopped",
        "stop_reason": (
            None if active else "The contract test reached its terminal checkpoint."
        ),
        "started_at": "2026-08-24T00:00:00+00:00",
        "deadline_at": "2026-08-24T01:00:00+00:00",
        "budget": {
            "wall_minutes": 60,
            "max_cycles": max_cycles,
            "finalization_minutes": 10,
        },
        "progress": {
            "metric": "bounded contract checks",
            "before": "No retained receipt.",
            "after": None if active else "One retained receipt.",
        },
        "workflow_phases": phases,
        "delegations": [],
    }
    if active:
        final_phase = phases[-1]
        final_phase["outcome"] = None
        final_phase["evidence"] = []
        final_phase["stop_reason"] = None
    return session


def _session_problems(
    monkeypatch: pytest.MonkeyPatch,
    session: dict[str, object],
    *,
    now: dt.datetime | None = None,
) -> list[str]:
    """Run only whole-session invariants, isolated from repository link state."""
    monkeypatch.setattr(ledger, "dead_links", list)
    monkeypatch.setattr(ledger, "board_ids", _empty_board_ids)
    return ledger.check(
        [],
        [],
        [],
        [],
        [session],
        agendas=[],
        now=now or dt.datetime(2026, 8, 24, tzinfo=dt.UTC),
    )


def test_gate_refusal_has_a_specific_type_and_recovery_message(tmp_path: Path) -> None:
    marker = tmp_path / ".gate-running"
    marker.touch()

    with pytest.raises(runner.GateRunningError, match=r"delete \.gate-running if a crash"):
        runner.refuse_if_gate_running(marker)


def test_git_failure_reports_the_command_and_stderr() -> None:
    with pytest.raises(runner.RefusalError, match=r"git rev-parse --verify") as raised:
        runner.git("rev-parse", "--verify", "definitely-not-a-revision")

    assert "fatal:" in str(raised.value)


def test_campaign_artifacts_use_the_stable_module_entry_point() -> None:
    assert runner.CAMPAIGN_ENTRY_POINT == "sqpack.campaign.runner:main"


def test_agent_session_rejects_more_contemporaneous_phases_than_max_cycles(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    problems = _session_problems(monkeypatch, _bounded_session(max_cycles=1))

    assert (
        "session-999-contract-test.md: contemporaneous workflow phases exceed budget.max_cycles"
    ) in problems


def test_active_delegation_rejects_unfrozen_uv_validation(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    session = _bounded_session(max_cycles=2)
    session["delegations"] = [
        {
            "status": "queued",
            "recording": "contemporaneous",
            "phase": 1,
            "budget_minutes": 10,
            "expected_output": "One read-only audit receipt.",
            "validation_command": "uv run pytest tests/test_campaign_tools.py",
            "kill_condition": "Stop at ten minutes.",
            "fallback": "Return the unresolved audit boundary.",
            "write_scope": ["tests/test_campaign_tools.py"],
            "excluded_commands": ["./test.sh --strict"],
            "elapsed_seconds": None,
            "elapsed_quality": None,
        }
    ]

    problems = _session_problems(monkeypatch, session)

    assert (
        "session-999-contract-test.md: queued delegation has an unfrozen uv command"
    ) in problems


def test_active_agent_session_rejects_an_expired_absolute_deadline(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    problems = _session_problems(
        monkeypatch,
        _bounded_session(max_cycles=2, active=True),
        now=dt.datetime(2026, 8, 24, 2, tzinfo=dt.UTC),
    )

    assert (
        "session-999-contract-test.md: in-progress session deadline_at has passed"
    ) in problems


def test_active_phase_and_delegation_reject_expired_slice_deadlines(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    session = _bounded_session(max_cycles=2, active=True)
    session["delegations"] = [
        {
            "status": "in_progress",
            "recording": "contemporaneous",
            "phase": 2,
            "budget_minutes": 5,
            "started_at": "2026-08-24T00:10:00+00:00",
            "deadline_at": "2026-08-24T00:15:00+00:00",
            "expected_output": "One bounded receipt.",
            "validation_command": "packing-ledger check",
            "kill_condition": "Stop at five minutes.",
            "fallback": "Return the partial receipt.",
            "write_scope": ["campaign/agent-sessions/"],
            "excluded_commands": ["./test.sh --strict"],
            "elapsed_seconds": None,
            "elapsed_quality": None,
        }
    ]

    problems = _session_problems(
        monkeypatch,
        session,
        now=dt.datetime(2026, 8, 24, 0, 21, tzinfo=dt.UTC),
    )

    assert (
        "session-999-contract-test.md: in-progress workflow phase 2 deadline_at has passed"
    ) in problems
    assert (
        "session-999-contract-test.md: in-progress delegation deadline_at has passed"
    ) in problems


def test_work_phase_cannot_consume_the_finalization_reserve(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    session = _bounded_session(max_cycles=2)
    phases = cast(list[dict[str, object]], session["workflow_phases"])
    phases[-1].update(
        {
            "budget_minutes": 11,
            "started_at": "2026-08-24T00:40:00+00:00",
            "deadline_at": "2026-08-24T00:51:00+00:00",
        }
    )

    problems = _session_problems(monkeypatch, session)

    assert (
        "session-999-contract-test.md: workflow phase 2 work deadline enters "
        "finalization reserve"
    ) in problems


def test_designated_finalization_phase_may_use_the_reserve(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    session = _bounded_session(max_cycles=2)
    phases = cast(list[dict[str, object]], session["workflow_phases"])
    phases[-1].update(
        {
            "clock_role": "finalization",
            "started_at": "2026-08-24T00:50:00+00:00",
            "deadline_at": "2026-08-24T01:00:00+00:00",
        }
    )

    assert _session_problems(monkeypatch, session) == []


def test_malformed_phase_clock_is_reported_without_crashing(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    session = _bounded_session(max_cycles=2)
    phases = cast(list[dict[str, object]], session["workflow_phases"])
    phases[-1]["deadline_at"] = "not-a-clock"

    problems = _session_problems(monkeypatch, session)

    assert (
        "session-999-contract-test.md: workflow phase 2 deadline_at is not an "
        "offset-aware ISO timestamp"
    ) in problems


@pytest.mark.parametrize(
    "missing_field",
    ["phase", "outcome", "evidence", "files", "checks", "uncertainty", "elapsed_quality"],
)
def test_terminal_bounded_delegation_requires_a_complete_receipt(
    monkeypatch: pytest.MonkeyPatch, missing_field: str
) -> None:
    session = _bounded_session(max_cycles=2)
    delegation: dict[str, object] = {
        "task": "Return one bounded read-only audit.",
        "operator": "contract-test",
        "status": "completed",
        "recording": "contemporaneous",
        "phase": 1,
        "outcome": "The audit completed.",
        "evidence": ["One focused receipt"],
        "files": [],
        "checks": [],
        "uncertainty": "No integration claim follows.",
        "elapsed_seconds": None,
        "elapsed_quality": "unavailable",
        "next_action": "Return control to the coordinator.",
    }
    delegation[missing_field] = None
    session["delegations"] = [delegation]

    problems = _session_problems(monkeypatch, session)

    assert (
        f"session-999-contract-test.md: terminal delegation has no {missing_field}"
    ) in problems


def test_progress_after_is_nullable_only_while_session_is_active(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    schema = yaml.safe_load(ledger.SESSION_SCHEMA.read_text())
    after_schema = schema["properties"]["progress"]["properties"]["after"]
    assert Draft202012Validator(after_schema).is_valid(None)

    session = _bounded_session(max_cycles=2)
    progress = cast(dict[str, object], session["progress"])
    progress["after"] = None

    assert (
        "session-999-contract-test.md: terminal session needs nonempty progress.after"
        in _session_problems(monkeypatch, session)
    )


@pytest.mark.parametrize(
    ("axis", "value", "message"),
    [("--instances", "0", "each instance"), ("--seeds", "0", "each seed")],
)
def test_baseline_rejects_invalid_axes_before_work_or_output(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    axis: str,
    value: str,
    message: str,
) -> None:
    engine = tmp_path / "sqsearch"
    engine.touch()
    output = tmp_path / "result.jsonl"

    with pytest.raises(SystemExit) as raised:
        baseline_sweep.main(
            [str(output), "--engine", str(engine), axis, value, "--budget-moves", "1"]
        )

    assert raised.value.code == 2
    assert message in capsys.readouterr().err
    assert not output.exists()
