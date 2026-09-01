"""Behavioral tests for retained Codex task-tree delta receipts."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

import pytest
import yaml
from jsonschema_rs import Draft202012Validator

import devtools.codex_task_tree_delta as delta_module
from devtools.codex_task_tree_delta import build_delta
from sqpack.yamlio import load_yaml

ROOT_ID = "00000000-0000-0000-0000-000000000001"
START = "2026-09-01T12:00:00Z"
END = "2026-09-01T13:00:00Z"
SCHEMA = (
    Path(__file__).resolve().parent.parent
    / "campaign"
    / "schemas"
    / "codex-task-tree-delta.schema.yaml"
)


def _model(*, responses: int, tokens: int, stream_seconds: float) -> dict[str, object]:
    return {
        "model": "gpt-test",
        "thinking_level": "high",
        "model_response_count": responses,
        "response_envelope_seconds": 999.0,
        "timed_model_stream_seconds": stream_seconds,
        "timed_reasoning_seconds": stream_seconds - 1.0,
        "timed_message_seconds": 1.0,
        "unattributed_response_seconds": 998.0,
        "recorded_first_token_wait_seconds": float(responses),
        "residual_response_seconds": 997.0,
        "native_turn_timing": {"private_distribution": [1, 2, 3]},
        "response_interval_seconds": {"p50": 5.0},
        "tokens": {
            "input": tokens,
            "cached_input": tokens // 2,
            "output": responses * 3,
            "reasoning_output": responses * 2,
        },
    }


def _snapshot(
    *,
    cutoff: str,
    snapshot: str,
    tasks: int,
    responses: int,
    tokens: int,
    active_seconds: float,
    snapshot_incomplete: bool,
) -> dict[str, object]:
    own = {
        "snapshot_incomplete": snapshot_incomplete,
        "task_count": tasks,
        "completed_task_count": tasks - int(snapshot_incomplete),
        "interrupted_task_count": 0,
        "active_seconds": active_seconds,
        "timed_model_stream_seconds": float(responses * 2),
        "recorded_first_token_wait_seconds": float(responses),
        "tool_seconds_by_category": {"command": float(responses)},
        "compaction_seconds": float(responses) / 2,
        "compaction_event_count": responses,
        "compaction_item_count": responses,
        "legacy_compaction_event_count": 0,
        "excluded_legacy_replay_task_count": 0,
        "models": [_model(responses=responses, tokens=tokens, stream_seconds=responses * 2)],
        "turns": [{"turn_id": "PRIVATE-TURN", "private_prose": "do not retain"}],
        "top_commands": [{"display": "curl https://secret.invalid/?token=PRIVATE"}],
        "command_categories": [{"category": "private-tool"}],
    }
    subtree = {
        "session_count": 1,
        "agent_active_seconds": active_seconds,
        "elapsed_envelope_seconds": active_seconds + 10.0,
        "active_union_seconds": active_seconds - 1.0,
        "parallel_overlap_seconds": 1.0,
        "timed_model_stream_seconds": float(responses * 2),
        "recorded_first_token_wait_seconds": float(responses),
        "compaction_event_count": responses,
        "compaction_item_count": responses,
        "legacy_compaction_event_count": 0,
        "excluded_legacy_replay_task_count": 0,
        "models": own["models"],
    }
    return {
        "schema": "CodexEfficiencyRollup/v2",
        "cutoff_at": cutoff,
        "snapshot_at": snapshot,
        "sessions_root": "/Users/private/.codex/sessions",
        "semantics": {"private": "not retained"},
        "roots": [
            {
                "session_id": ROOT_ID,
                "parent_session_id": None,
                "agent_path": "/root/private-agent",
                "log_path": "/Users/private/.codex/sessions/private.jsonl",
                "source_kind": "user",
                "own": own,
                "subtree": subtree,
                "children": [],
            }
        ],
    }


def test_build_delta_subtracts_only_safe_additive_tree_metrics(
    monkeypatch, tmp_path: Path
) -> None:
    before = _snapshot(
        cutoff=START,
        snapshot=START,
        tasks=1,
        responses=1,
        tokens=100,
        active_seconds=20.0,
        snapshot_incomplete=False,
    )
    after = _snapshot(
        cutoff=END,
        snapshot=END,
        tasks=3,
        responses=4,
        tokens=460,
        active_seconds=50.0,
        snapshot_incomplete=True,
    )
    calls: list[str] = []

    def fake_build_rollup(
        sessions_root: Path, root_ids: list[str], *, through: str
    ) -> dict[str, object]:
        assert sessions_root == tmp_path
        assert root_ids == [ROOT_ID]
        calls.append(through)
        return before if through == START else after

    monkeypatch.setattr(delta_module, "build_rollup", fake_build_rollup)

    document = build_delta(tmp_path, ROOT_ID, start=START, end=END)

    assert calls == [START, END]
    assert document["softschema"] == {
        "contract": "packing.squares:CodexTaskTreeDelta/v1",
        "schema": "../schemas/codex-task-tree-delta.schema.yaml",
        "envelope": "rollup",
        "status": "enforced",
    }
    rollup = document["rollup"]
    assert rollup["completeness"] == {
        "snapshot_incomplete": True,
        "live_session_count": 1,
    }
    assert rollup["delta"]["task_count"] == 2
    assert rollup["delta"]["completed_task_count"] == 1
    assert rollup["delta"]["agent_active_seconds"] == 30.0
    assert rollup["delta"]["tool_seconds_by_category"] == {"command": 3.0}
    assert rollup["delta"]["models"] == [
        {
            "model": "gpt-test",
            "thinking_level": "high",
            "model_response_count": 3,
            "timed_model_stream_seconds": 6.0,
            "timed_reasoning_seconds": 6.0,
            "timed_message_seconds": 0.0,
            "recorded_first_token_wait_seconds": 3.0,
            "tokens": {
                "input": 360,
                "cached_input": 180,
                "output": 9,
                "reasoning_output": 6,
            },
        }
    ]

    retained = yaml.safe_dump(document, sort_keys=False)
    for private in (
        "sessions_root",
        "log_path",
        "agent_path",
        "turn_id",
        "top_commands",
        "PRIVATE",
        "private-tool",
        "/Users/private",
    ):
        assert private not in retained


def test_build_delta_rejects_a_nonmonotone_selected_measurement(
    monkeypatch, tmp_path: Path
) -> None:
    before = _snapshot(
        cutoff=START,
        snapshot=START,
        tasks=1,
        responses=1,
        tokens=100,
        active_seconds=20.0,
        snapshot_incomplete=False,
    )
    after = _snapshot(
        cutoff=END,
        snapshot=END,
        tasks=2,
        responses=2,
        tokens=90,
        active_seconds=30.0,
        snapshot_incomplete=False,
    )

    monkeypatch.setattr(
        delta_module,
        "build_rollup",
        lambda _root, _ids, *, through: before if through == START else after,
    )

    with pytest.raises(ValueError, match=r"non-monotone.*tokens.input"):
        build_delta(tmp_path, ROOT_ID, start=START, end=END)


def test_retained_delta_validates_against_its_enforced_schema(
    monkeypatch, tmp_path: Path
) -> None:
    before = _snapshot(
        cutoff=START,
        snapshot=START,
        tasks=1,
        responses=1,
        tokens=100,
        active_seconds=20.0,
        snapshot_incomplete=False,
    )
    after = _snapshot(
        cutoff=END,
        snapshot=END,
        tasks=2,
        responses=2,
        tokens=200,
        active_seconds=30.0,
        snapshot_incomplete=False,
    )
    monkeypatch.setattr(
        delta_module,
        "build_rollup",
        lambda _root, _ids, *, through: before if through == START else after,
    )
    document = build_delta(tmp_path, ROOT_ID, start=START, end=END)

    schema = load_yaml(SCHEMA.read_text(encoding="utf-8"))
    errors = list(Draft202012Validator(schema).iter_errors(document["rollup"]))

    assert errors == []


def test_cli_writes_one_explicit_pure_yaml_artifact(
    monkeypatch, tmp_path: Path, capsys
) -> None:
    before = _snapshot(
        cutoff=START,
        snapshot=START,
        tasks=1,
        responses=1,
        tokens=100,
        active_seconds=20.0,
        snapshot_incomplete=False,
    )
    after = _snapshot(
        cutoff=END,
        snapshot=END,
        tasks=2,
        responses=2,
        tokens=200,
        active_seconds=30.0,
        snapshot_incomplete=False,
    )
    monkeypatch.setattr(
        delta_module,
        "build_rollup",
        lambda _root, _ids, *, through: before if through == START else after,
    )
    destination = tmp_path / "resource-usage" / "codex-current.yaml"

    status = delta_module.main(
        [
            "--sessions-root",
            str(tmp_path),
            "--root-id",
            ROOT_ID,
            "--start",
            START,
            "--end",
            END,
            "--out",
            str(destination),
        ]
    )

    assert status == 0
    assert destination.is_file()
    written = load_yaml(destination.read_text(encoding="utf-8"))
    assert written["softschema"]["contract"] == "packing.squares:CodexTaskTreeDelta/v1"
    assert written["rollup"]["delta"]["task_count"] == 1
    assert capsys.readouterr().out == f"wrote {destination}\n"


def test_cli_rejects_reversed_cutoffs_without_writing(tmp_path: Path, capsys) -> None:
    destination = tmp_path / "must-not-exist.yaml"

    status = delta_module.main(
        [
            "--sessions-root",
            str(tmp_path),
            "--root-id",
            ROOT_ID,
            "--start",
            END,
            "--end",
            START,
            "--out",
            str(destination),
        ]
    )

    captured = capsys.readouterr()
    assert status == 1
    assert captured.out == ""
    assert "end cutoff must be later" in captured.err
    assert not destination.exists()


def test_build_delta_consumes_the_real_codex_v2_scanner_shape(tmp_path: Path) -> None:
    turn_id = "turn-private"
    task_started = "2026-09-01T12:00:00Z"
    start = "2026-09-01T12:00:05Z"
    end = "2026-09-01T12:00:20Z"
    epoch_ms = int(
        datetime.fromisoformat(task_started.replace("Z", "+00:00")).timestamp() * 1000
    )

    def event(timestamp: str, event_type: str, **payload: object) -> dict[str, object]:
        return {
            "timestamp": timestamp,
            "type": "event_msg",
            "payload": {"type": event_type, **payload},
        }

    usage = {
        "input_tokens": 100,
        "cached_input_tokens": 50,
        "cache_write_input_tokens": 0,
        "output_tokens": 7,
        "reasoning_output_tokens": 3,
        "total_tokens": 107,
    }
    records = [
        {
            "timestamp": task_started,
            "type": "session_meta",
            "payload": {"id": ROOT_ID, "thread_source": "user", "cwd": "/private/repo"},
        },
        event(task_started, "task_started", turn_id=turn_id),
        {
            "timestamp": task_started,
            "type": "turn_context",
            "payload": {
                "turn_id": turn_id,
                "model": "gpt-test",
                "effort": "high",
            },
        },
        event(
            "2026-09-01T12:00:10Z",
            "item_completed",
            turn_id=turn_id,
            item={"type": "Reasoning", "id": "reasoning-1", "private_prose": "secret"},
            started_at_ms=epoch_ms + 6_000,
            completed_at_ms=epoch_ms + 10_000,
        ),
        event(
            "2026-09-01T12:00:10Z",
            "token_count",
            info={"last_token_usage": usage, "total_token_usage": usage},
        ),
        event(
            "2026-09-01T12:00:15Z",
            "item_completed",
            turn_id=turn_id,
            item={
                "type": "CommandExecution",
                "id": "command-1",
                "command": ["/bin/bash", "-lc", "curl https://secret.invalid"],
                "status": "completed",
            },
            started_at_ms=epoch_ms + 13_000,
            completed_at_ms=epoch_ms + 15_000,
        ),
        event(
            end,
            "task_complete",
            turn_id=turn_id,
            duration_ms=20_000,
            time_to_first_token_ms=2_000,
        ),
    ]
    log = tmp_path / "2026" / "09" / "01" / "root.jsonl"
    log.parent.mkdir(parents=True)
    log.write_text("".join(f"{json.dumps(record)}\n" for record in records), encoding="utf-8")

    document = build_delta(tmp_path, ROOT_ID, start=start, end=end)

    delta = document["rollup"]["delta"]
    assert delta["completed_task_count"] == 1
    assert delta["agent_active_seconds"] == 20.0
    assert delta["timed_model_stream_seconds"] == 4.0
    assert delta["tool_seconds_by_category"] == {"command": 2.0}
    assert delta["models"][0]["tokens"] == {
        "input": 100,
        "cached_input": 50,
        "output": 7,
        "reasoning_output": 3,
    }
    assert "secret.invalid" not in yaml.safe_dump(document)
