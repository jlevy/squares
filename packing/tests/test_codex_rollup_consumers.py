"""Codex interval receipts stay explicit and separate at consumer boundaries."""

from __future__ import annotations

import json
import subprocess
from copy import deepcopy
from pathlib import Path

import pytest
import yaml

import devtools.close_session as closer
import devtools.render_pr_rollup as renderer
from sqpack.yamlio import safe_load


def _receipt(path: Path, *, live: bool = True) -> None:
    delta = {
        "session_count": 2,
        "task_count": 3,
        "completed_task_count": 2,
        "interrupted_task_count": 0,
        "agent_active_seconds": 5400.0,
        "elapsed_envelope_seconds": 3600.0,
        "active_union_seconds": 3500.0,
        "parallel_overlap_seconds": 1900.0,
        "timed_model_stream_seconds": 1200.0,
        "recorded_first_token_wait_seconds": 12.0,
        "tool_seconds_by_category": {"command": 600.0, "agent_wait": 300.0},
        "compaction_seconds": 20.0,
        "compaction_event_count": 1,
        "compaction_item_count": 1,
        "legacy_compaction_event_count": 0,
        "excluded_legacy_replay_task_count": 0,
        "models": [
            {
                "model": "gpt-test",
                "thinking_level": "high",
                "model_response_count": 7,
                "timed_model_stream_seconds": 1200.0,
                "timed_reasoning_seconds": 1000.0,
                "timed_message_seconds": 200.0,
                "recorded_first_token_wait_seconds": 12.0,
                "tokens": {
                    "input": 100,
                    "cached_input": 80,
                    "output": 30,
                    "reasoning_output": 20,
                },
            }
        ],
    }
    before = {
        **{name: 0 for name in delta if name not in {"tool_seconds_by_category", "models"}},
        "tool_seconds_by_category": {},
        "models": [],
    }
    document = {
        "softschema": {
            "contract": "packing.squares:CodexTaskTreeDelta/v1",
            "schema": "../schemas/codex-task-tree-delta.schema.yaml",
            "envelope": "rollup",
            "status": "enforced",
        },
        "rollup": {
            "source": {
                "harness": "codex",
                "source_schema": "CodexEfficiencyRollup/v2",
                "root_task_id": "opaque-root",
                "start_cutoff_at": "2026-09-01T06:27:10Z",
                "end_cutoff_at": "2026-09-01T07:27:10Z",
                "before_snapshot_at": "2026-09-01T06:27:09Z",
                "after_snapshot_at": "2026-09-01T07:27:09Z",
            },
            "completeness": {
                "snapshot_incomplete": live,
                "live_session_count": int(live),
            },
            "before": before,
            "after": deepcopy(delta),
            "delta": delta,
            "semantics": {
                "attribution": "operator-declared only",
                "delta": "after minus before",
                "cutoff_boundary": "completion events may straddle",
                "live_snapshot": "live snapshots are lower bounds",
                "retention": "aggregate fields only",
            },
        },
    }
    path.write_text(yaml.safe_dump(document, sort_keys=False), encoding="utf-8")


def _session(
    path: Path,
    receipt: str,
    *,
    branch: str = "codex/example",
    session_id: str = "session-999",
    duplicate: bool = False,
) -> None:
    declarations = f"  - packing/campaign/resource-usage/{receipt}\n"
    if duplicate:
        declarations += declarations
    path.write_text(
        f"---\nsession:\n  id: {session_id}\n  status: in_progress\n"
        f"  branch: {branch}\n"
        f"  resource_rollups:\n{declarations}"
        "---\n# fixture\n",
        encoding="utf-8",
    )


def test_codex_receipt_is_auto_discovered_from_its_branch_declaration(
    monkeypatch, tmp_path: Path
) -> None:
    usage = tmp_path / "usage"
    sessions = tmp_path / "sessions"
    usage.mkdir()
    sessions.mkdir()
    _receipt(usage / "codex.yaml")
    _session(sessions / "session-999-fixture.md", "codex.yaml")
    monkeypatch.setattr(renderer, "USAGE", usage)
    monkeypatch.setattr(renderer, "SESSIONS", sessions)

    rendered = renderer.render("codex/example")

    assert "`codex.yaml` — declared by `session-999`" in rendered
    assert "| model responses | 7 |" in rendered


def test_codex_renderer_accumulates_distinct_sessions_on_one_branch(
    monkeypatch, tmp_path: Path
) -> None:
    usage = tmp_path / "usage"
    sessions = tmp_path / "sessions"
    usage.mkdir()
    sessions.mkdir()
    _receipt(usage / "first.yaml")
    _receipt(usage / "second.yaml")
    _session(
        sessions / "session-998-first.md",
        "first.yaml",
        session_id="session-998",
    )
    _session(
        sessions / "session-999-second.md",
        "second.yaml",
        session_id="session-999",
    )
    monkeypatch.setattr(renderer, "USAGE", usage)
    monkeypatch.setattr(renderer, "SESSIONS", sessions)

    rendered = renderer.render("codex/example")

    assert rendered.count("| model responses | 7 |") == 2
    assert "`first.yaml` — declared by `session-998`" in rendered
    assert "`second.yaml` — declared by `session-999`" in rendered


def test_codex_renderer_rejects_one_receipt_claimed_for_two_branches(
    monkeypatch, tmp_path: Path
) -> None:
    usage = tmp_path / "usage"
    sessions = tmp_path / "sessions"
    usage.mkdir()
    sessions.mkdir()
    _receipt(usage / "codex.yaml")
    _session(
        sessions / "session-998-first.md",
        "codex.yaml",
        branch="codex/first",
        session_id="session-998",
    )
    _session(
        sessions / "session-999-second.md",
        "codex.yaml",
        branch="codex/second",
        session_id="session-999",
    )
    monkeypatch.setattr(renderer, "USAGE", usage)
    monkeypatch.setattr(renderer, "SESSIONS", sessions)

    with pytest.raises(ValueError, match="attributed to more than one branch"):
        renderer.render("codex/first")


def test_declared_codex_receipt_is_labeled_as_a_live_lower_bound(
    monkeypatch, tmp_path: Path
) -> None:
    usage = tmp_path / "usage"
    sessions = tmp_path / "sessions"
    usage.mkdir()
    sessions.mkdir()
    _receipt(usage / "codex.yaml")
    _session(sessions / "session-999-fixture.md", "codex.yaml")
    monkeypatch.setattr(renderer, "USAGE", usage)
    monkeypatch.setattr(renderer, "SESSIONS", sessions)

    rendered = renderer.render("codex/example", "session-999")

    assert "Codex task-tree intervals declared by AgentSessions" in rendered
    assert "`codex.yaml` — declared by `session-999`" in rendered
    assert "Codex logs expose no Git-branch field" in rendered
    assert "operator-recorded, not harness-observed" in rendered
    assert "**Lower bound:**" in rendered
    assert "| model responses | 7 |" in rendered
    assert "| recursive agent time | 1.5 h |" in rendered
    assert "opaque-root" not in rendered


def test_codex_receipt_cannot_be_rendered_against_an_undeclared_branch(
    monkeypatch, tmp_path: Path
) -> None:
    usage = tmp_path / "usage"
    sessions = tmp_path / "sessions"
    usage.mkdir()
    sessions.mkdir()
    _receipt(usage / "codex.yaml")
    _session(sessions / "session-999-fixture.md", "codex.yaml", branch="codex/owned")
    monkeypatch.setattr(renderer, "USAGE", usage)
    monkeypatch.setattr(renderer, "SESSIONS", sessions)

    assert renderer.render("codex/other", "session-999") == (
        "No rollup records any turn on `codex/other`.\n"
    )


def test_codex_renderer_does_not_collapse_a_declared_path_to_its_basename(
    monkeypatch, tmp_path: Path
) -> None:
    usage = tmp_path / "usage"
    sessions = tmp_path / "sessions"
    usage.mkdir()
    sessions.mkdir()
    _receipt(usage / "codex.yaml")
    _session(
        sessions / "session-999-fixture.md",
        "../resource-usage/codex.yaml",
    )
    monkeypatch.setattr(renderer, "USAGE", usage)
    monkeypatch.setattr(renderer, "SESSIONS", sessions)

    assert renderer.render("codex/example", "session-999") == (
        "No rollup records any turn on `codex/example`.\n"
    )


def test_completed_codex_receipt_does_not_claim_to_be_live(monkeypatch, tmp_path: Path) -> None:
    usage = tmp_path / "usage"
    sessions = tmp_path / "sessions"
    usage.mkdir()
    sessions.mkdir()
    _receipt(usage / "codex.yaml", live=False)
    _session(sessions / "session-999-fixture.md", "codex.yaml")
    monkeypatch.setattr(renderer, "USAGE", usage)
    monkeypatch.setattr(renderer, "SESSIONS", sessions)

    rendered = renderer.render("codex/example", "session-999")

    assert "contained no live task" in rendered
    assert "**Lower bound:**" not in rendered


def test_consumers_refuse_a_semantically_false_codex_receipt(
    monkeypatch, tmp_path: Path
) -> None:
    usage = tmp_path / "usage"
    sessions = tmp_path / "sessions"
    usage.mkdir()
    sessions.mkdir()
    receipt = usage / "codex.yaml"
    _receipt(receipt)
    document = safe_load(receipt.read_text(encoding="utf-8"))
    document["rollup"]["delta"]["agent_active_seconds"] = 0.0
    receipt.write_text(yaml.safe_dump(document, sort_keys=False), encoding="utf-8")
    _session(sessions / "session-999-fixture.md", "codex.yaml")
    monkeypatch.setattr(renderer, "USAGE", usage)
    monkeypatch.setattr(renderer, "SESSIONS", sessions)

    with pytest.raises(ValueError, match="fails semantic validation"):
        renderer.render("codex/example", "session-999")
    with pytest.raises(ValueError, match="fails semantic validation"):
        closer.codex_receipt_summary(receipt)


def test_close_report_keeps_unavailable_claude_metrics_null_for_codex(
    monkeypatch, tmp_path: Path
) -> None:
    packing = tmp_path / "packing"
    usage = packing / "campaign" / "resource-usage"
    sessions = packing / "campaign" / "agent-sessions"
    usage.mkdir(parents=True)
    sessions.mkdir(parents=True)
    _receipt(usage / "codex.yaml")
    _session(sessions / "session-999-fixture.md", "codex.yaml")
    monkeypatch.setattr(closer, "ROOT", packing)
    monkeypatch.setattr(closer, "USAGE", usage)
    monkeypatch.setattr(closer, "SESSIONS", sessions)

    report = closer.render_report()

    assert "turns: null" in report
    assert "tool_calls: null" in report
    assert "tool_errors: null" in report
    assert "one_off_code: null" in report
    assert "model_responses: 7" in report
    assert "snapshot_incomplete: true" in report
    assert closer.sum_rollups({"codex.yaml"}) == {
        "rollups": 0,
        "turns": 0,
        "tool_calls": 0,
        "tool_errors": 0,
        "one_off_code": 0,
        "wall_hours": 0,
    }


def test_close_report_defensively_deduplicates_one_sessions_declarations(
    monkeypatch, tmp_path: Path
) -> None:
    packing = tmp_path / "packing"
    usage = packing / "campaign" / "resource-usage"
    sessions = packing / "campaign" / "agent-sessions"
    usage.mkdir(parents=True)
    sessions.mkdir(parents=True)
    _receipt(usage / "codex.yaml")
    _session(sessions / "session-999-fixture.md", "codex.yaml", duplicate=True)
    monkeypatch.setattr(closer, "ROOT", packing)
    monkeypatch.setattr(closer, "USAGE", usage)
    monkeypatch.setattr(closer, "SESSIONS", sessions)

    report = closer.render_report()

    assert report.count("packing/campaign/resource-usage/codex.yaml") == 2
    assert report.count("model_responses: 7") == 1


def test_close_render_uses_cumulative_branch_cost_even_with_session_detail(
    monkeypatch, tmp_path: Path
) -> None:
    packing = tmp_path / "packing"
    packing.mkdir()
    report_path = packing / "report.yaml"
    synopsis_path = tmp_path / "SYNOPSIS.md"
    synopsis_path.write_text("synopsis", encoding="utf-8")
    calls: list[tuple[str, str | None]] = []
    monkeypatch.setattr(closer, "ROOT", packing)
    monkeypatch.setattr(closer, "REPORT", report_path)
    monkeypatch.setattr(closer, "SYNOPSIS", synopsis_path)
    monkeypatch.setattr(closer, "render_report", lambda: "report\n")
    monkeypatch.setattr(closer, "splice_synopsis", lambda text: text)
    monkeypatch.setattr(closer, "report", lambda session_id: 0)
    monkeypatch.setattr(closer, "current_branch", lambda: "codex/example")
    monkeypatch.setattr(
        closer,
        "render_branch_cost",
        lambda branch, session_id=None: calls.append((branch, session_id)) or "cost\n",
    )

    assert closer.main(["--render", "--session", "session-999"]) == 0
    assert calls == [("codex/example", None)]


def test_renderer_cli_contains_validation_errors(monkeypatch, capsys) -> None:
    def fail(_branch: str, _session_id: str | None = None) -> str:
        raise ValueError("codex.yaml fails semantic validation")

    monkeypatch.setattr(renderer, "render", fail)

    assert renderer.main(["--branch", "codex/example"]) == 1
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == "error: codex.yaml fails semantic validation\n"
    assert "Traceback" not in captured.err


def test_closer_cli_contains_validation_errors(monkeypatch, capsys) -> None:
    monkeypatch.setattr(
        closer,
        "render_report",
        lambda: (_ for _ in ()).throw(ValueError("codex.yaml fails semantic validation")),
    )

    assert closer.main(["--check"]) == 1
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == "error: codex.yaml fails semantic validation\n"
    assert "Traceback" not in captured.err


def test_close_render_validates_branch_cost_before_writing_views(
    monkeypatch, tmp_path: Path
) -> None:
    packing = tmp_path / "packing"
    packing.mkdir()
    report_path = packing / "report.yaml"
    synopsis_path = tmp_path / "SYNOPSIS.md"
    report_path.write_text("old report\n", encoding="utf-8")
    synopsis_path.write_text("old synopsis\n", encoding="utf-8")
    monkeypatch.setattr(closer, "ROOT", packing)
    monkeypatch.setattr(closer, "REPORT", report_path)
    monkeypatch.setattr(closer, "SYNOPSIS", synopsis_path)
    monkeypatch.setattr(closer, "render_report", lambda: "new report\n")
    monkeypatch.setattr(closer, "splice_synopsis", lambda _text: "new synopsis\n")
    monkeypatch.setattr(closer, "current_branch", lambda: "codex/example")
    monkeypatch.setattr(
        closer,
        "render_branch_cost",
        lambda _branch: (_ for _ in ()).throw(ValueError("conflicting declarations")),
    )

    assert closer.main(["--render"]) == 1
    assert report_path.read_text(encoding="utf-8") == "old report\n"
    assert synopsis_path.read_text(encoding="utf-8") == "old synopsis\n"


def test_agenda_closeout_renders_results_files_and_one_successor() -> None:
    agenda = {
        "id": "agenda-999",
        "items": [
            {
                "id": "BC-999",
                "outcomes": [
                    {
                        "scope": "finite search prefix",
                        "classification": "time-limited",
                        "result": "Seven rows agreed before the wall.",
                        "evidence": ["Checkpoint retained seven agreeing rows."],
                        "disposition": "continue",
                        "follow_up": "think-next",
                    }
                ],
            }
        ],
        "closeout": {
            "changes": [
                {
                    "name": "guard-tool",
                    "result": "Added one refusing guard.",
                    "paths": ["packing/devtools/check_guard.py"],
                }
            ],
            "validation": [
                {"scope": "focused", "status": "passed", "evidence": "Three tests."}
            ],
            "documentation_review": [
                {"path": "README.md", "decision": "updated", "reason": "New entry."}
            ],
            "replanning": {
                "operator_input": {"status": "revised", "note": "Added W9."},
                "candidates": [
                    {
                        "priority": 0,
                        "bead": "think-next",
                        "workflow": "research-loop",
                        "rationale": "Continue the retained prefix.",
                    }
                ],
                "selected": {
                    "bead": "think-next",
                    "workflow": "research-loop",
                    "rationale": "Highest-ranked valid continuation.",
                },
            },
        },
    }

    rendered = renderer.render_agenda_closeout(agenda)

    assert "Seven rows agreed before the wall." in rendered
    assert "`time-limited`" in rendered
    assert "Checkpoint retained seven agreeing rows." in rendered
    assert "`continue` via `think-next`" in rendered
    assert "`packing/devtools/check_guard.py`" in rendered
    assert "No completed bounded-negative search is claimed" in rendered
    assert rendered.count("**Selected next entry:**") == 1


def test_agenda_finalizer_bulk_checks_live_candidates(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls: list[tuple[str, ...]] = []
    agenda = {
        "closeout": {
            "replanning": {
                "candidates": [
                    {"bead": "think-next", "priority": 0},
                    {"bead": "think-backlog", "priority": 1},
                ],
                "selected": {"bead": "think-next"},
            }
        }
    }

    def run(command: list[str], **_kwargs: object) -> subprocess.CompletedProcess[str]:
        calls.append(tuple(command))
        if command[:2] == ["tbd", "show"]:
            output = json.dumps(
                [
                    {"displayId": "think-next", "status": "open", "priority": 0},
                    {"displayId": "think-backlog", "status": "open", "priority": 1},
                ]
            )
        elif command[:2] == ["tbd", "ready"]:
            output = json.dumps([{"id": "think-next"}])
        else:
            output = ""
        return subprocess.CompletedProcess(command, 0, stdout=output, stderr="")

    monkeypatch.setattr(closer, "agenda_payload", lambda _agenda_id: agenda)
    monkeypatch.setattr(closer.subprocess, "run", run)

    closer.finalize_agenda_views("agenda-999")

    show_calls = [call for call in calls if call[:2] == ("tbd", "show")]
    assert show_calls == [("tbd", "show", "think-next", "think-backlog", "--json")]


def test_close_main_reports_the_failed_finalizer_command(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    def fail(_options: object) -> int:
        raise subprocess.CalledProcessError(
            7,
            ["tbd", "sync"],
            stderr="live queue could not be synchronized",
        )

    monkeypatch.setattr(closer, "_run", fail)

    assert closer.main([]) == 1
    error = capsys.readouterr().err
    assert "command failed with exit 7: tbd sync" in error
    assert "live queue could not be synchronized" in error
