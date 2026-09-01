"""Codex interval receipts stay explicit and separate at consumer boundaries."""

from __future__ import annotations

from pathlib import Path

import devtools.close_session as closer
import devtools.render_pr_rollup as renderer


def _receipt(path: Path, *, live: bool = True) -> None:
    path.write_text(
        """softschema:
  contract: packing.squares:CodexTaskTreeDelta/v1
  schema: ../schemas/codex-task-tree-delta.schema.yaml
  envelope: rollup
  status: enforced
rollup:
  source:
    harness: codex
    source_schema: CodexEfficiencyRollup/v2
    root_task_id: opaque-root
    start_cutoff_at: '2026-09-01T06:27:10Z'
    end_cutoff_at: '2026-09-01T07:27:10Z'
    before_snapshot_at: '2026-09-01T06:27:09Z'
    after_snapshot_at: '2026-09-01T07:27:09Z'
  completeness:
    snapshot_incomplete: LIVE
    live_session_count: 1
  delta:
    session_count: 2
    task_count: 3
    completed_task_count: 2
    interrupted_task_count: 0
    agent_active_seconds: 5400.0
    elapsed_envelope_seconds: 3600.0
    active_union_seconds: 3500.0
    parallel_overlap_seconds: 1900.0
    timed_model_stream_seconds: 1200.0
    recorded_first_token_wait_seconds: 12.0
    tool_seconds_by_category:
      command: 600.0
      agent_wait: 300.0
    compaction_seconds: 20.0
    compaction_event_count: 1
    compaction_item_count: 1
    legacy_compaction_event_count: 0
    excluded_legacy_replay_task_count: 0
    models:
    - model: gpt-test
      thinking_level: high
      model_response_count: 7
      timed_model_stream_seconds: 1200.0
      timed_reasoning_seconds: 1000.0
      timed_message_seconds: 200.0
      recorded_first_token_wait_seconds: 12.0
      tokens:
        input: 100
        cached_input: 80
        output: 30
        reasoning_output: 20
""".replace("LIVE", str(live).lower()),
        encoding="utf-8",
    )


def _session(path: Path, receipt: str) -> None:
    path.write_text(
        "---\nsession:\n  id: session-999\n  status: in_progress\n"
        f"  resource_rollups:\n  - packing/campaign/resource-usage/{receipt}\n"
        "---\n# fixture\n",
        encoding="utf-8",
    )


def test_codex_receipt_requires_an_explicit_session_declaration(
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

    assert renderer.render("codex/example") == (
        "No rollup records any turn on `codex/example`.\n"
    )


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

    assert "Codex task-tree interval (declared by `session-999`)" in rendered
    assert "Codex logs expose no Git-branch field" in rendered
    assert "operator-recorded, not harness-observed" in rendered
    assert "**Lower bound:**" in rendered
    assert "| model responses | 7 |" in rendered
    assert "| recursive agent time | 1.5 h |" in rendered
    assert "opaque-root" not in rendered


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
