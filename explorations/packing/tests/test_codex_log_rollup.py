"""Behavioral tests for recursive Codex JSONL efficiency rollups."""

from __future__ import annotations

import json
from pathlib import Path

from devtools.codex_log_rollup import build_rollup, render_markdown


def _write_log(path: Path, records: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "".join(f"{json.dumps(record)}\n" for record in records),
        encoding="utf-8",
    )


def _session_meta(
    session_id: str,
    *,
    timestamp: str,
    parent_id: str | None = None,
    agent_path: str | None = None,
    history_start_ordinal: int | None = None,
) -> dict[str, object]:
    payload: dict[str, object] = {
        "id": session_id,
        "thread_source": "subagent" if parent_id else "user",
        "cwd": "/workspace",
    }
    if parent_id:
        payload.update(
            {
                "parent_thread_id": parent_id,
                "agent_path": agent_path,
                "subagent_history_start_ordinal": history_start_ordinal,
                "source": {
                    "subagent": {
                        "thread_spawn": {
                            "parent_thread_id": parent_id,
                            "depth": 1,
                            "agent_path": agent_path,
                        }
                    }
                },
            }
        )
    return {"timestamp": timestamp, "type": "session_meta", "payload": payload}


def _turn_context(
    turn_id: str,
    *,
    timestamp: str,
    model: str,
    effort: str,
) -> dict[str, object]:
    return {
        "timestamp": timestamp,
        "type": "turn_context",
        "payload": {
            "turn_id": turn_id,
            "model": model,
            "effort": effort,
        },
    }


def _event(timestamp: str, event_type: str, **payload: object) -> dict[str, object]:
    return {
        "timestamp": timestamp,
        "type": "event_msg",
        "payload": {"type": event_type, **payload},
    }


def _item(
    item_type: str,
    *,
    timestamp: str,
    turn_id: str,
    started_ms: int,
    completed_ms: int,
    **item_fields: object,
) -> dict[str, object]:
    return _event(
        timestamp,
        "item_completed",
        thread_id="root",
        turn_id=turn_id,
        item={"type": item_type, "id": f"{item_type}-{completed_ms}", **item_fields},
        started_at_ms=started_ms,
        completed_at_ms=completed_ms,
    )


def _token_count(
    *,
    timestamp: str,
    input_tokens: int,
    cached_tokens: int,
    output_tokens: int,
    reasoning_tokens: int,
) -> dict[str, object]:
    usage = {
        "input_tokens": input_tokens,
        "cached_input_tokens": cached_tokens,
        "cache_write_input_tokens": 0,
        "output_tokens": output_tokens,
        "reasoning_output_tokens": reasoning_tokens,
        "total_tokens": input_tokens + output_tokens,
    }
    return _event(
        timestamp,
        "token_count",
        info={"last_token_usage": usage, "total_token_usage": usage},
    )


def test_rollup_subtracts_tools_and_groups_model_responses_by_model_and_effort(
    tmp_path: Path,
) -> None:
    root_id = "00000000-0000-0000-0000-000000000001"
    turn_id = "turn-root"
    path = tmp_path / "2026" / "08" / "25" / "root.jsonl"
    _write_log(
        path,
        [
            _session_meta(root_id, timestamp="2026-08-25T00:00:00.000Z"),
            _event(
                "2026-08-25T00:00:00.000Z",
                "task_started",
                turn_id=turn_id,
                started_at=1_000,
            ),
            _turn_context(
                turn_id,
                timestamp="2026-08-25T00:00:00.000Z",
                model="gpt-test",
                effort="high",
            ),
            _item(
                "Reasoning",
                timestamp="2026-08-25T00:00:04.000Z",
                turn_id=turn_id,
                started_ms=1_001_000,
                completed_ms=1_004_000,
            ),
            {
                "timestamp": "2026-08-25T00:00:05.000Z",
                "type": "response_item",
                "payload": {
                    "type": "custom_tool_call",
                    "name": "exec",
                    "call_id": "call-1",
                    "input": "const r = await tools.exec_command({cmd: 'pytest'});",
                },
            },
            _item(
                "CommandExecution",
                timestamp="2026-08-25T00:00:07.000Z",
                turn_id=turn_id,
                started_ms=1_005_000,
                completed_ms=1_007_000,
                command=["/bin/bash", "-lc", "uv run pytest -q"],
                status="completed",
            ),
            {
                "timestamp": "2026-08-25T00:00:07.000Z",
                "type": "response_item",
                "payload": {
                    "type": "custom_tool_call_output",
                    "call_id": "call-1",
                    "output": [],
                },
            },
            _token_count(
                timestamp="2026-08-25T00:00:07.000Z",
                input_tokens=100,
                cached_tokens=60,
                output_tokens=20,
                reasoning_tokens=10,
            ),
            _item(
                "AgentMessage",
                timestamp="2026-08-25T00:00:10.000Z",
                turn_id=turn_id,
                started_ms=1_008_000,
                completed_ms=1_010_000,
            ),
            _token_count(
                timestamp="2026-08-25T00:00:10.000Z",
                input_tokens=120,
                cached_tokens=80,
                output_tokens=30,
                reasoning_tokens=5,
            ),
            _event(
                "2026-08-25T00:00:10.000Z",
                "task_complete",
                turn_id=turn_id,
                started_at=1_000,
                completed_at=1_010,
                duration_ms=10_000,
                time_to_first_token_ms=1_000,
            ),
        ],
    )

    result = build_rollup(tmp_path, [root_id])
    root = result["roots"][0]
    own = root["own"]
    model = own["models"][0]

    assert own["active_seconds"] == 10.0
    assert own["tool_seconds_by_category"] == {"command": 2.0}
    assert own["response_envelope_seconds"] == 8.0
    assert own["timed_model_stream_seconds"] == 5.0
    assert result["schema"] == "CodexEfficiencyRollup/v2"
    assert own["unattributed_response_seconds"] == 3.0
    assert own["recorded_first_token_wait_seconds"] == 1.0
    assert own["residual_response_seconds"] == 2.0
    assert own["native_turn_timing"] == {
        "completed_turn_count": 1,
        "duration_available_count": 1,
        "time_to_first_token_available_count": 1,
        "duration_coverage": 1.0,
        "time_to_first_token_coverage": 1.0,
        "reported_duration_seconds": {
            "count": 1,
            "total": 10.0,
            "min": 10.0,
            "p50": 10.0,
            "p95": 10.0,
            "max": 10.0,
        },
        "time_to_first_token_seconds": {
            "count": 1,
            "total": 1.0,
            "min": 1.0,
            "p50": 1.0,
            "p95": 1.0,
            "max": 1.0,
        },
        "matching_interval_seconds": 10.0,
        "reported_minus_interval_seconds": 0.0,
    }
    assert model["model"] == "gpt-test"
    assert model["thinking_level"] == "high"
    assert model["model_response_count"] == 2
    assert model["response_envelope_seconds"] == 8.0
    assert model["timed_reasoning_seconds"] == 3.0
    assert model["timed_message_seconds"] == 2.0
    assert model["timed_model_stream_seconds"] == 5.0
    assert model["unattributed_response_seconds"] == 3.0
    assert model["recorded_first_token_wait_seconds"] == 1.0
    assert model["residual_response_seconds"] == 2.0
    assert model["native_turn_timing"]["reported_duration_seconds"]["total"] == 10.0
    assert model["stream_timing_available"] is True
    assert model["tokens"] == {
        "input": 220,
        "cached_input": 140,
        "output": 50,
        "reasoning_output": 15,
    }
    assert model["response_interval_seconds"]["p50"] == 4.0
    assert own["top_commands"][0]["category"] == "pytest"
    assert own["top_commands"][0]["total_seconds"] == 2.0
    markdown = render_markdown(result)
    assert "8.0s envelope; 1.0s first-token wait; 5.0s timed stream" in markdown
    assert "10.0s native turn duration" in markdown


def test_rollup_builds_recursive_tree_and_keeps_agent_time_out_of_parent_wall(
    tmp_path: Path,
) -> None:
    root_id = "00000000-0000-0000-0000-000000000010"
    child_id = "00000000-0000-0000-0000-000000000011"
    root_turn = "turn-root"
    child_turn = "turn-child"
    _write_log(
        tmp_path / "root.jsonl",
        [
            _session_meta(root_id, timestamp="2026-08-25T00:00:00.000Z"),
            _event(
                "2026-08-25T00:00:00.000Z",
                "task_started",
                turn_id=root_turn,
                started_at=2_000,
            ),
            _turn_context(
                root_turn,
                timestamp="2026-08-25T00:00:00.000Z",
                model="gpt-parent",
                effort="xhigh",
            ),
            _token_count(
                timestamp="2026-08-25T00:00:10.000Z",
                input_tokens=10,
                cached_tokens=0,
                output_tokens=1,
                reasoning_tokens=1,
            ),
            _event(
                "2026-08-25T00:00:10.000Z",
                "task_complete",
                turn_id=root_turn,
                started_at=2_000,
                completed_at=2_010,
                duration_ms=10_000,
                time_to_first_token_ms=1_000,
            ),
        ],
    )
    _write_log(
        tmp_path / "child.jsonl",
        [
            {
                **_session_meta(
                    child_id,
                    timestamp="2026-08-25T00:00:02.000Z",
                    parent_id=root_id,
                    agent_path="/root/reviewer",
                    history_start_ordinal=3,
                ),
                "ordinal": 0,
            },
            {
                **_event(
                    "2026-08-25T00:00:02.000Z",
                    "task_started",
                    turn_id="inherited-parent-turn",
                    started_at=2_000,
                ),
                "ordinal": 1,
            },
            {
                **_token_count(
                    timestamp="2026-08-25T00:00:02.000Z",
                    input_tokens=999,
                    cached_tokens=999,
                    output_tokens=999,
                    reasoning_tokens=999,
                ),
                "ordinal": 2,
            },
            _event(
                "2026-08-25T00:00:02.000Z",
                "task_started",
                turn_id=child_turn,
                started_at=2_002,
            )
            | {"ordinal": 3},
            _turn_context(
                child_turn,
                timestamp="2026-08-25T00:00:02.000Z",
                model="gpt-child",
                effort="medium",
            )
            | {"ordinal": 4},
            _token_count(
                timestamp="2026-08-25T00:00:08.000Z",
                input_tokens=20,
                cached_tokens=5,
                output_tokens=2,
                reasoning_tokens=1,
            )
            | {"ordinal": 5},
            _event(
                "2026-08-25T00:00:08.000Z",
                "task_complete",
                turn_id=child_turn,
                started_at=2_002,
                completed_at=2_008,
                duration_ms=6_000,
                time_to_first_token_ms=500,
            )
            | {"ordinal": 6},
        ],
    )

    result = build_rollup(tmp_path, [root_id])
    root = result["roots"][0]

    assert root["own"]["active_seconds"] == 10.0
    assert root["children"][0]["session_id"] == child_id
    assert root["children"][0]["agent_path"] == "/root/reviewer"
    assert root["subtree"]["agent_active_seconds"] == 16.0
    assert root["subtree"]["elapsed_envelope_seconds"] == 10.0
    assert root["subtree"]["active_union_seconds"] == 10.0
    assert root["subtree"]["parallel_overlap_seconds"] == 6.0
    assert root["subtree"]["recorded_first_token_wait_seconds"] == 1.5
    assert root["subtree"]["residual_response_seconds"] == 14.5
    assert root["subtree"]["native_turn_timing"]["reported_duration_seconds"] == {
        "count": 2,
        "total": 16.0,
        "min": 6.0,
        "p50": 8.0,
        "p95": 9.8,
        "max": 10.0,
    }
    assert [
        (entry["model"], entry["thinking_level"]) for entry in root["subtree"]["models"]
    ] == [("gpt-child", "medium"), ("gpt-parent", "xhigh")]


def test_rollup_closes_interrupted_task_at_the_next_task_start(tmp_path: Path) -> None:
    root_id = "00000000-0000-0000-0000-000000000015"
    _write_log(
        tmp_path / "interrupted.jsonl",
        [
            _session_meta(root_id, timestamp="2026-08-25T00:00:00.000Z"),
            _event(
                "2026-08-25T00:00:00.000Z",
                "task_started",
                turn_id="turn-interrupted",
                started_at=2_000,
            ),
            _turn_context(
                "turn-interrupted",
                timestamp="2026-08-25T00:00:00.000Z",
                model="gpt-test",
                effort="high",
            ),
            _event(
                "2026-08-25T00:01:00.000Z",
                "task_started",
                turn_id="turn-completed",
                started_at=2_060,
            ),
            _turn_context(
                "turn-completed",
                timestamp="2026-08-25T00:01:00.000Z",
                model="gpt-test",
                effort="high",
            ),
            _event(
                "2026-08-25T00:01:10.000Z",
                "task_complete",
                turn_id="turn-completed",
                started_at=2_060,
                completed_at=2_070,
                duration_ms=10_000,
            ),
        ],
    )

    own = build_rollup(tmp_path, [root_id])["roots"][0]["own"]

    assert own["active_seconds"] == 70.0
    assert own["completed_task_count"] == 1
    assert own["interrupted_task_count"] == 1
    assert own["snapshot_incomplete"] is False
    assert [turn["state"] for turn in own["turns"]] == ["interrupted", "completed"]


def test_rollup_marks_live_task_at_last_recorded_event(tmp_path: Path) -> None:
    root_id = "00000000-0000-0000-0000-000000000020"
    turn_id = "turn-live"
    _write_log(
        tmp_path / "live.jsonl",
        [
            _session_meta(root_id, timestamp="2026-08-25T00:00:00.000Z"),
            _event(
                "2026-08-25T00:00:00.000Z",
                "task_started",
                turn_id=turn_id,
                started_at=3_000,
            ),
            _turn_context(
                turn_id,
                timestamp="2026-08-25T00:00:00.000Z",
                model="gpt-live",
                effort="low",
            ),
            _token_count(
                timestamp="2026-08-25T00:00:03.000Z",
                input_tokens=5,
                cached_tokens=0,
                output_tokens=1,
                reasoning_tokens=0,
            ),
        ],
    )

    result = build_rollup(tmp_path, [root_id])
    own = result["roots"][0]["own"]

    assert own["active_seconds"] == 3.0
    assert own["task_count"] == 1
    assert own["completed_task_count"] == 0
    assert own["snapshot_incomplete"] is True
    assert own["snapshot_at"] == "2026-08-25T00:00:03.000Z"


def test_rollup_freezes_a_live_tree_at_an_explicit_cutoff(tmp_path: Path) -> None:
    root_id = "00000000-0000-0000-0000-000000000023"
    child_id = "00000000-0000-0000-0000-000000000024"
    turn_id = "turn-live"
    _write_log(
        tmp_path / "root.jsonl",
        [
            _session_meta(root_id, timestamp="2026-08-25T00:00:00.000Z"),
            _event(
                "2026-08-25T00:00:00.000Z",
                "task_started",
                turn_id=turn_id,
            ),
            _turn_context(
                turn_id,
                timestamp="2026-08-25T00:00:00.000Z",
                model="gpt-live",
                effort="low",
            ),
            _token_count(
                timestamp="2026-08-25T00:00:03.000Z",
                input_tokens=5,
                cached_tokens=0,
                output_tokens=1,
                reasoning_tokens=0,
            ),
            _token_count(
                timestamp="2026-08-25T00:00:08.000Z",
                input_tokens=500,
                cached_tokens=0,
                output_tokens=100,
                reasoning_tokens=50,
            ),
            _event(
                "2026-08-25T00:00:10.000Z",
                "task_complete",
                turn_id=turn_id,
                duration_ms=10_000,
                time_to_first_token_ms=1_000,
            ),
        ],
    )
    _write_log(
        tmp_path / "future-child.jsonl",
        [
            _session_meta(
                child_id,
                timestamp="2026-08-25T00:00:07.000Z",
                parent_id=root_id,
                agent_path="/root/future",
            ),
        ],
    )

    result = build_rollup(
        tmp_path,
        [root_id],
        through="2026-08-25T00:00:05.000Z",
    )
    root = result["roots"][0]

    assert result["cutoff_at"] == "2026-08-25T00:00:05.000Z"
    assert result["snapshot_at"] == "2026-08-25T00:00:03.000Z"
    assert root["own"]["active_seconds"] == 3.0
    assert root["own"]["models"][0]["tokens"]["input"] == 5
    assert root["children"] == []


def test_rollup_treats_missing_or_invalid_native_timing_as_unavailable(
    tmp_path: Path,
) -> None:
    root_id = "00000000-0000-0000-0000-000000000025"
    _write_log(
        tmp_path / "compatibility.jsonl",
        [
            _session_meta(root_id, timestamp="2026-08-25T00:00:00.000Z"),
            _event(
                "2026-08-25T00:00:00.000Z",
                "task_started",
                turn_id="turn-missing",
            ),
            _turn_context(
                "turn-missing",
                timestamp="2026-08-25T00:00:00.000Z",
                model="gpt-test",
                effort="medium",
            ),
            _event(
                "2026-08-25T00:00:01.000Z",
                "task_complete",
                turn_id="turn-missing",
            ),
            _event(
                "2026-08-25T00:00:01.000Z",
                "task_started",
                turn_id="turn-invalid",
            ),
            _turn_context(
                "turn-invalid",
                timestamp="2026-08-25T00:00:01.000Z",
                model="gpt-test",
                effort="medium",
            ),
            _event(
                "2026-08-25T00:00:02.000Z",
                "task_complete",
                turn_id="turn-invalid",
                duration_ms=-1,
                time_to_first_token_ms="not-a-number",
            ),
            _event(
                "2026-08-25T00:00:02.000Z",
                "task_started",
                turn_id="turn-native",
            ),
            _turn_context(
                "turn-native",
                timestamp="2026-08-25T00:00:02.000Z",
                model="gpt-test",
                effort="medium",
            ),
            _event(
                "2026-08-25T00:00:04.000Z",
                "task_complete",
                turn_id="turn-native",
                duration_ms=2_000,
                time_to_first_token_ms=250,
            ),
        ],
    )

    own = build_rollup(tmp_path, [root_id])["roots"][0]["own"]

    assert own["native_turn_timing"]["completed_turn_count"] == 3
    assert own["native_turn_timing"]["duration_available_count"] == 1
    assert own["native_turn_timing"]["time_to_first_token_available_count"] == 1
    assert own["native_turn_timing"]["duration_coverage"] == 0.333
    assert own["native_turn_timing"]["time_to_first_token_coverage"] == 0.333
    assert [turn["client_duration_seconds"] for turn in own["turns"]] == [
        None,
        None,
        2.0,
    ]
    assert [turn["client_time_to_first_token_seconds"] for turn in own["turns"]] == [
        None,
        None,
        0.25,
    ]


def test_rollup_counts_current_compaction_items_without_double_counting_legacy_events(
    tmp_path: Path,
) -> None:
    root_id = "00000000-0000-0000-0000-000000000027"
    turn_id = "turn-compaction"
    _write_log(
        tmp_path / "compaction.jsonl",
        [
            _session_meta(root_id, timestamp="2026-08-25T00:00:00.000Z"),
            _event(
                "2026-08-25T00:00:00.000Z",
                "task_started",
                turn_id=turn_id,
            ),
            _turn_context(
                turn_id,
                timestamp="2026-08-25T00:00:00.000Z",
                model="gpt-test",
                effort="high",
            ),
            _item(
                "ContextCompaction",
                timestamp="2026-08-25T00:00:04.000Z",
                turn_id=turn_id,
                started_ms=1_787_616_002_000,
                completed_ms=1_787_616_004_000,
            ),
            _event("2026-08-25T00:00:04.000Z", "context_compacted"),
            _event(
                "2026-08-25T00:00:10.000Z",
                "task_complete",
                turn_id=turn_id,
                duration_ms=10_000,
                time_to_first_token_ms=1_000,
            ),
        ],
    )

    own = build_rollup(tmp_path, [root_id])["roots"][0]["own"]

    assert own["compaction_seconds"] == 2.0
    assert own["compaction_item_count"] == 1
    assert own["legacy_compaction_event_count"] == 1
    assert own["compaction_event_count"] == 1


def test_legacy_subagent_skips_replayed_history_and_recovers_command_timing(
    tmp_path: Path,
) -> None:
    root_id = "00000000-0000-0000-0000-000000000030"
    child_id = "00000000-0000-0000-0000-000000000031"
    child_turn = "turn-child"
    _write_log(
        tmp_path / "root.jsonl",
        [
            _session_meta(root_id, timestamp="2026-08-25T00:00:00.000Z"),
            _event(
                "2026-08-25T00:00:00.000Z",
                "task_started",
                turn_id="turn-root",
            ),
            _event(
                "2026-08-25T00:00:10.000Z",
                "task_complete",
                turn_id="turn-root",
            ),
        ],
    )
    inherited_meta = _session_meta(root_id, timestamp="2026-08-25T00:00:02.001Z")
    _write_log(
        tmp_path / "child.jsonl",
        [
            _session_meta(
                child_id,
                timestamp="2026-08-25T00:00:02.000Z",
                parent_id=root_id,
                agent_path="/root/legacy",
            ),
            inherited_meta,
            _event(
                "2026-08-25T00:00:02.002Z",
                "task_started",
                turn_id="inherited-turn",
            ),
            _event("2026-08-25T00:00:02.003Z", "thread_settings_applied"),
            inherited_meta | {"timestamp": "2026-08-25T00:00:02.004Z"},
            _event("2026-08-25T00:00:02.005Z", "thread_settings_applied"),
            _event(
                "2026-08-25T00:00:02.006Z",
                "task_started",
                turn_id="compressed-replay-turn",
            ),
            _turn_context(
                "compressed-replay-turn",
                timestamp="2026-08-25T00:00:02.006Z",
                model="gpt-parent-replay",
                effort="max",
            ),
            _token_count(
                timestamp="2026-08-25T00:00:02.007Z",
                input_tokens=1_000_000,
                cached_tokens=900_000,
                output_tokens=50_000,
                reasoning_tokens=25_000,
            ),
            _event(
                "2026-08-25T00:00:02.008Z",
                "task_complete",
                turn_id="compressed-replay-turn",
                duration_ms=1_000_000,
                time_to_first_token_ms=5_000,
            ),
            _event("2026-08-25T00:00:02.009Z", "thread_settings_applied"),
            _event(
                "2026-08-25T00:00:03.000Z",
                "task_started",
                turn_id=child_turn,
            ),
            _turn_context(
                child_turn,
                timestamp="2026-08-25T00:00:03.000Z",
                model="gpt-legacy",
                effort="medium",
            ),
            {
                "timestamp": "2026-08-25T00:00:04.000Z",
                "type": "response_item",
                "payload": {
                    "type": "custom_tool_call",
                    "name": "exec",
                    "call_id": "legacy-command",
                    "input": (
                        'const r = await tools.exec_command({"cmd":"uv run pytest -q"});'
                    ),
                },
            },
            {
                "timestamp": "2026-08-25T00:00:05.000Z",
                "type": "response_item",
                "payload": {
                    "type": "custom_tool_call_output",
                    "call_id": "legacy-command",
                    "output": [{"type": "input_text", "text": '{"session_id":42}'}],
                },
            },
            {
                "timestamp": "2026-08-25T00:00:05.000Z",
                "type": "response_item",
                "payload": {
                    "type": "custom_tool_call",
                    "name": "exec",
                    "call_id": "legacy-poll",
                    "input": ("const r = await tools.write_stdin({session_id:42,chars:''});"),
                },
            },
            {
                "timestamp": "2026-08-25T00:00:07.000Z",
                "type": "response_item",
                "payload": {
                    "type": "custom_tool_call_output",
                    "call_id": "legacy-poll",
                    "output": "completed",
                },
            },
            _token_count(
                timestamp="2026-08-25T00:00:08.000Z",
                input_tokens=20,
                cached_tokens=10,
                output_tokens=2,
                reasoning_tokens=1,
            ),
            _event(
                "2026-08-25T00:00:09.000Z",
                "task_complete",
                turn_id=child_turn,
            ),
        ],
    )

    child = build_rollup(tmp_path, [root_id])["roots"][0]["children"][0]

    assert child["own"]["task_count"] == 1
    assert child["own"]["excluded_legacy_replay_task_count"] == 1
    assert child["own"]["active_seconds"] == 6.0
    assert child["own"]["models"][0]["tokens"]["input"] == 20
    assert child["own"]["stream_timing_available"] is False
    assert child["own"]["top_commands"] == [
        {
            "category": "pytest",
            "display": "uv run pytest -q",
            "invocation_count": 1,
            "timing_segment_count": 2,
            "total_seconds": 3.0,
            "max_seconds": 2.0,
        }
    ]
