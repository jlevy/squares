"""Failure-path contracts for repository-bound campaign applications."""

from __future__ import annotations

import datetime as dt
from copy import deepcopy
from pathlib import Path
from typing import cast

import pytest
import yaml
from jsonschema import Draft202012Validator

from cases.campaign_smoke import baseline_sweep
from sqpack.campaign import ledger, runner


def test_review_pending_round_does_not_disposition_hypothesis() -> None:
    hypothesis = {
        "kind": "hypothesis",
        "instrument_ready": True,
        "instrument": "A frozen checker.",
    }
    pending = {"verdict": {"decision": "accepted", "needs_review": True}}

    assert ledger.status_of(hypothesis, [pending]) == "needs review"


def test_review_pending_round_does_not_override_reviewed_disposition() -> None:
    hypothesis = {"kind": "hypothesis"}
    reviewed = {"verdict": {"decision": "accepted", "needs_review": False}}
    pending = {"verdict": {"decision": "rejected", "needs_review": True}}

    assert ledger.status_of(hypothesis, [reviewed, pending]) == "confirmed"
    pending["verdict"]["needs_review"] = False
    assert ledger.status_of(hypothesis, [reviewed, pending]) == "refuted"


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
        "primary_bead": "think-test",
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


def _terminal_agenda() -> dict[str, object]:
    """Smallest post-agenda fixture exercising W10 relationships."""
    return {
        "id": "agenda-015",
        "_path": Path("agenda-015-contract-test.md"),
        "status": "completed",
        "items": [
            {
                "id": "BC-999",
                "state": "complete",
                "hypotheses": [],
                "depends_on": [],
                "bead": "think-next",
                "artifacts": ["retained evidence"],
                "outcomes": [
                    {
                        "scope": "bounded contract",
                        "classification": "achieved",
                        "disposition": "retire-success",
                        "follow_up": None,
                    }
                ],
            }
        ],
        "closeout": {
            "documentation_review": [
                {"path": path} for path in sorted(ledger.POST_AGENDA_DOCUMENTS)
            ],
            "changes": [
                {
                    "name": "closeout-contract",
                    "paths": ["README.md"],
                }
            ],
            "replanning": {
                "candidates": [
                    {
                        "bead": "think-next",
                        "workflow": "research-loop",
                    }
                ],
                "selected": {
                    "bead": "think-next",
                    "workflow": "research-loop",
                },
            },
        },
    }


def _agenda_problems(monkeypatch: pytest.MonkeyPatch, agenda: dict[str, object]) -> list[str]:
    monkeypatch.setattr(ledger, "dead_links", list)
    monkeypatch.setattr(ledger, "board_ids", _empty_board_ids)
    return ledger.check(
        [],
        [],
        [],
        [],
        [],
        agendas=[agenda],
        now=dt.datetime(2026, 9, 2, tzinfo=dt.UTC),
    )


def test_terminal_agenda_rejects_classification_disposition_mismatch(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    agenda = _terminal_agenda()
    outcome = cast(dict[str, object], cast(list[object], agenda["items"])[0])["outcomes"]
    cast(list[dict[str, object]], outcome)[0].update(
        classification="bounded-negative", disposition="continue", follow_up="think-next"
    )

    problems = _agenda_problems(monkeypatch, agenda)

    assert any(
        "classifies 'bounded contract' as bounded-negative but gives disposition continue"
        in problem
        for problem in problems
    )


def test_terminal_agenda_requires_the_complete_document_impact_review(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    agenda = deepcopy(_terminal_agenda())
    closeout = cast(dict[str, object], agenda["closeout"])
    documentation = cast(list[object], closeout["documentation_review"])
    documentation.pop()

    problems = _agenda_problems(monkeypatch, agenda)

    assert any("documentation review covers" in problem for problem in problems)


def test_terminal_agenda_selected_bead_must_be_a_unique_candidate(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    agenda = deepcopy(_terminal_agenda())
    closeout = cast(dict[str, object], agenda["closeout"])
    replanning = cast(dict[str, object], closeout["replanning"])
    selected = cast(dict[str, object], replanning["selected"])
    selected["bead"] = "think-missing"

    problems = _agenda_problems(monkeypatch, agenda)

    assert any("is not one unique replanning candidate" in problem for problem in problems)


def _experiment_problems(
    monkeypatch: pytest.MonkeyPatch,
    *,
    decision: str,
    results: list[dict[str, object]],
    lease: dict[str, str] | None,
    now: dt.datetime,
) -> list[str]:
    """Run experiment cross-field invariants without repository link state."""
    monkeypatch.setattr(ledger, "dead_links", list)
    monkeypatch.setattr(ledger, "board_ids", _empty_board_ids)
    experiment: dict[str, object] = {
        "id": "exp-999",
        "_path": Path("exp-999-contract-test.md"),
        "series": "series-999",
        "hypotheses": ["H-999"],
        "subject": {"assurance": "verified", "method": "exact-algebraic"},
        "instance": {"axis": "n", "point": 5, "role": "target"},
        "results": results,
        "verdict": {"decision": decision},
    }
    if decision != "in-progress":
        experiment["effort"] = {"stopped_by": "dependency", "wall_seconds": 0}
    if lease is not None:
        experiment["lease"] = lease
    return ledger.check(
        [{"id": "series-999", "status": "open", "_path": Path("series-999.md")}],
        [],
        [{"id": "H-999", "_path": Path("H-999.md")}],
        [experiment],
        [],
        agendas=[],
        now=now,
    )


def _logbook_entry(path: Path) -> dict[str, object]:
    """Minimal run synopsis whose rollup matches `_bounded_session`."""
    sections = []
    for heading in ledger.REQUIRED_LOGBOOK_SECTIONS:
        section = f"## {heading}\n\nRecorded."
        if heading == "Results":
            section += "\n\n" + "\n\n".join(
                f"### {subheading}\n\nRecorded."
                for subheading in ledger.REQUIRED_LOGBOOK_RESULT_SECTIONS
            )
        sections.append(section)
    path.write_text(
        f"---\nplaceholder: true\n---\n\n# Test run\n\n{'\n\n'.join(sections)}\n",
        encoding="utf-8",
    )
    return {
        "id": "run-001",
        "_path": path,
        "source_sessions": ["session-999"],
        "primary_bead": "think-test",
        "timebox": {
            "target_wall_minutes": 60,
            "cycle_minutes": 30,
            "planned_cycle_slots": 2,
        },
        "rollup": {
            "session_count": 1,
            "phase_count": 2,
            "workflow_counts": {"process-review": 2},
            "phase_status_counts": {"completed": 1, "stopped": 1},
            "focus_counts": {"process": 2},
            "clock_role_counts": {"work": 2},
            "delegation_count": 0,
            "delegation_status_counts": {},
            "new_round_decision_counts": {},
        },
        "new_round_results": [],
        "prior_retained_results": [],
        "defects": {"opened_in_run": [], "preexisting_relevant": []},
        "pipeline_changes": [],
    }


def _logbook_problems(
    monkeypatch: pytest.MonkeyPatch,
    entry: dict[str, object],
) -> list[str]:
    """Run logbook reconciliation without unrelated repository link state."""
    monkeypatch.setattr(ledger, "dead_links", list)
    monkeypatch.setattr(ledger, "board_ids", _empty_board_ids)
    return ledger.check(
        [],
        [],
        [],
        [],
        [_bounded_session(max_cycles=2)],
        agendas=[],
        now=dt.datetime(2026, 8, 24, tzinfo=dt.UTC),
        logbook_entries=[entry],
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


def test_research_loop_logbook_rejects_phase_rollup_drift(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    entry = _logbook_entry(tmp_path / "run-001-contract-test.md")
    rollup = cast(dict[str, object], entry["rollup"])
    rollup["phase_count"] = 1

    problems = _logbook_problems(monkeypatch, entry)

    assert "run-001-contract-test.md: rollup.phase_count is 1, expected 2" in problems


def test_research_loop_logbook_requires_the_reader_first_sections(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    entry = _logbook_entry(tmp_path / "run-001-contract-test.md")
    path = cast(Path, entry["_path"])
    path.write_text(
        path.read_text(encoding="utf-8").replace("## What Did Not Work\n", ""),
        encoding="utf-8",
    )

    problems = _logbook_problems(monkeypatch, entry)

    assert (
        "run-001-contract-test.md: needs exactly one '## What Did Not Work' section" in problems
    )


def test_research_loop_logbook_validates_prior_retained_result_ids(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    entry = _logbook_entry(tmp_path / "run-001-contract-test.md")
    prior_results = cast(list[dict[str, object]], entry["prior_retained_results"])
    prior_results.append(
        {
            "id": "exp-999",
            "use": "control",
            "summary": "A prior control result.",
        }
    )

    problems = _logbook_problems(monkeypatch, entry)

    assert "run-001-contract-test.md: references unknown prior result exp-999" in problems


def test_research_loop_logbook_requires_evidence_for_rechecked_results(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    entry = _logbook_entry(tmp_path / "run-001-contract-test.md")
    prior_results = cast(list[dict[str, object]], entry["prior_retained_results"])
    prior_results.append(
        {
            "id": "exp-999",
            "use": "rechecked",
            "summary": "A prior result was said to be rechecked.",
        }
    )

    problems = _logbook_problems(monkeypatch, entry)

    assert (
        "run-001-contract-test.md: rechecked prior result exp-999 has no recheck_evidence"
        in problems
    )


def test_research_loop_logbook_rejects_new_and_prior_overlap(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    entry = _logbook_entry(tmp_path / "run-001-contract-test.md")
    new_results = cast(list[dict[str, object]], entry["new_round_results"])
    new_results.append({"id": "exp-999", "decision": "accepted", "summary": "A new result."})
    rollup = cast(dict[str, object], entry["rollup"])
    rollup["new_round_decision_counts"] = {"accepted": 1}
    prior_results = cast(list[dict[str, object]], entry["prior_retained_results"])
    prior_results.append({"id": "exp-999", "use": "control", "summary": "A prior control."})

    problems = _logbook_problems(monkeypatch, entry)

    assert (
        "run-001-contract-test.md: exp-999 is both a new round result and a prior result"
        in problems
    )


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


def test_live_offset_lease_is_compared_as_the_same_utc_instant(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    problems = _experiment_problems(
        monkeypatch,
        decision="in-progress",
        results=[],
        lease={"expires": "2026-08-24T03:00:00-07:00"},
        now=dt.datetime(2026, 8, 24, 9, tzinfo=dt.UTC).replace(tzinfo=None),
    )

    assert not any("STALE CLAIM" in problem for problem in problems)


def test_terminal_round_requires_a_real_result(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    problems = _experiment_problems(
        monkeypatch,
        decision="blocked",
        results=[],
        lease=None,
        now=dt.datetime(2026, 8, 24, tzinfo=dt.UTC).replace(tzinfo=None),
    )

    assert "exp-999-contract-test.md: terminal round without results" in problems


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


def test_a_registered_result_stops_its_hypothesis_reading_as_untouched() -> None:
    """The register's `produced_by` joins back to the hypothesis; the ledger shows it.

    H-061 had T-017 and T-018 standing on it and read `open` with zero rounds, because
    the only link was prose. No round is invented for it: the status says a result is
    registered, and the `results` column names which.
    """
    hypothesis = {
        "id": "H-061",
        "kind": "hypothesis",
        "lane": "proof",
        "claim": "A first-party certificate proves s(12) >= 19/5.",
        "instrument_ready": True,
        "instrument": "A frozen generator and verifier.",
    }
    assert ledger.status_of(hypothesis, []) == "open"
    assert ledger.status_of(hypothesis, [], results=["T-017"]) == "result registered"
    reviewed = {"verdict": {"decision": "accepted", "needs_review": False}}
    assert ledger.status_of(hypothesis, [reviewed], results=["T-017"]) == "confirmed"

    results = [
        {"id": "T-017", "produced_by": {"hypothesis": "H-061"}},
        {"id": "T-018", "produced_by": {"hypothesis": "H-061"}},
        {"id": "T-019", "produced_by": {"agenda_cell": "BC-161"}},
    ]
    assert ledger.results_of(results) == {"H-061": ["T-017", "T-018"]}
    text = ledger.render([], [], [hypothesis], [], [], agendas=[], results=results)
    row = next(line for line in text.splitlines() if line.startswith("| H-061 "))
    assert "| result registered |" in row
    assert "| 0 | T-017, T-018 |" in row


def test_the_live_ledger_carries_the_results_column_for_h061() -> None:
    text = ledger.LEDGER.read_text(encoding="utf-8")
    header = next(line for line in text.splitlines() if line.startswith("| id | status | lane"))
    assert header == "| id | status | lane | claim | sweep | rounds | results | spent |"
    row = next(line for line in text.splitlines() if line.startswith("| H-061 "))
    assert "T-017" in row


def _cell(cell_id: str, state: str, depends_on: list[str]) -> dict[str, object]:
    return {
        "id": cell_id,
        "state": state,
        "hypotheses": [],
        "depends_on": depends_on,
        "bead": f"think-{cell_id[3:].lower()}",
        "artifacts": ["retained evidence"] if state == "complete" else [],
    }


def test_depends_on_resolves_across_agendas_like_discharged_by(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A later agenda may wait on an earlier one's cell; only a missing id is refused."""
    monkeypatch.setattr(ledger, "dead_links", list)
    monkeypatch.setattr(ledger, "board_ids", _empty_board_ids)
    earlier = {
        "id": "agenda-019",
        "_path": Path("agenda-019-contract-test.md"),
        "status": "paused",
        "items": [_cell("BC-901", "complete", []), _cell("BC-902", "ready", [])],
    }
    later = {
        "id": "agenda-021",
        "_path": Path("agenda-021-contract-test.md"),
        "status": "paused",
        "items": [
            _cell("BC-903", "ready", ["BC-901"]),
            _cell("BC-904", "blocked", ["BC-902"]),
            _cell("BC-905", "blocked", ["BC-999"]),
            _cell("BC-906", "ready", ["BC-902"]),
        ],
    }
    problems = ledger.check(
        [], [], [], [], [], agendas=[earlier, later], now=dt.datetime(2026, 9, 5, tzinfo=dt.UTC)
    )
    assert not any("BC-903" in problem or "BC-904" in problem for problem in problems)
    assert any("BC-905 depends on unknown items ['BC-999']" in problem for problem in problems)
    assert any(
        "BC-906 is ready with incomplete dependencies ['BC-902']" in problem
        for problem in problems
    )
