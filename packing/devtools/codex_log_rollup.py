"""Build prose-excluding efficiency rollups from Codex JSONL session logs."""

from __future__ import annotations

import argparse
import json
import math
import re
import statistics
import sys
from collections import defaultdict
from collections.abc import Iterable, Sequence
from dataclasses import dataclass, field
from datetime import UTC, datetime
from itertools import pairwise
from pathlib import Path
from typing import Any

ROLLUP_SCHEMA = "CodexEfficiencyRollup/v2"
UNKNOWN_MODEL = "unknown"
UNKNOWN_THINKING_LEVEL = "unknown"
DISPLAY_COMMAND_LIMIT = 140
SECONDS_PER_MINUTE = 60
SECONDS_PER_HOUR = 60 * SECONDS_PER_MINUTE
MILLISECONDS_PER_SECOND = 1_000
TOOL_CATEGORY_PRIORITY = (
    "agent_wait",
    "command",
    "mcp",
    "agent_control",
    "file_change",
    "extension",
    "compaction",
)
MODEL_ITEM_TYPES = {"Reasoning", "AgentMessage"}
TOOL_ITEM_CATEGORIES = {
    "CollabAgentToolCall": "agent_control",
    "CommandExecution": "command",
    "Extension": "extension",
    "FileChange": "file_change",
    "McpToolCall": "mcp",
}
INSPECTION_COMMANDS = {"head", "jq", "rg", "sed", "tail", "wc"}
WORKTREE_PATTERN = re.compile(r"/Users/[^/]+/\.codex/worktrees/[^/]+/[^\s'\"]+")
WHITESPACE_PATTERN = re.compile(r"\s+")


@dataclass(frozen=True)
class Interval:
    """One half-open time interval measured in Unix milliseconds."""

    start_ms: float
    end_ms: float
    category: str


@dataclass(frozen=True)
class TaskWindow:
    """One Codex task turn, complete or live at the log snapshot."""

    turn_id: str
    start_ms: float
    end_ms: float
    completed: bool
    state: str
    client_duration_ms: float | None = None
    client_time_to_first_token_ms: float | None = None


@dataclass(frozen=True)
class TurnContext:
    """Model and thinking setting active from one recorded context event."""

    turn_id: str
    at_ms: float
    model: str
    thinking_level: str


@dataclass(frozen=True)
class TokenEvent:
    """Per-response token usage emitted by Codex."""

    at_ms: float
    usage: dict[str, int]


@dataclass(frozen=True)
class StreamItem:
    """Timed model-output item."""

    turn_id: str
    item_type: str
    start_ms: float
    end_ms: float


@dataclass(frozen=True)
class CommandEvent:
    """One completed command with its normalized identity."""

    turn_id: str
    duration_ms: float
    normalized: str
    display: str
    category: str
    invocation_start: bool


@dataclass
class ModelAccumulator:
    """Mutable model metrics before stable output serialization."""

    response_envelope_ms: float = 0
    streamed_reasoning_ms: float = 0
    streamed_message_ms: float = 0
    stream_item_count: int = 0
    latencies_ms: list[float] = field(default_factory=list)
    calls: int = 0
    input_tokens: int = 0
    cached_input_tokens: int = 0
    output_tokens: int = 0
    reasoning_output_tokens: int = 0
    completed_turn_count: int = 0
    native_duration_samples_ms: list[float] = field(default_factory=list)
    native_interval_samples_ms: list[float] = field(default_factory=list)
    first_token_samples_ms: list[float] = field(default_factory=list)


@dataclass
class ParsedSession:
    """Data required to summarize one JSONL session without retaining prose."""

    session_id: str
    path: Path
    parent_session_id: str | None
    agent_path: str | None
    source_kind: str
    snapshot_at: str
    snapshot_ms: float
    tasks: list[TaskWindow]
    contexts: list[TurnContext]
    tokens: list[TokenEvent]
    streams: list[StreamItem]
    explicit_intervals: list[Interval]
    commands: list[CommandEvent]
    compaction_event_count: int
    compaction_item_count: int
    legacy_compaction_event_count: int
    excluded_legacy_replay_task_count: int


@dataclass(frozen=True)
class PendingToolCall:
    """One tool request awaiting its matching output record."""

    start_ms: float
    name: str
    input_value: Any


@dataclass(frozen=True)
class LegacyCommand:
    """Command timing reconstructed from legacy tool request/output records."""

    start_ms: float
    duration_ms: float
    input_value: Any
    invocation_start: bool


def _timestamp_ms(value: str) -> float:
    return (
        datetime.fromisoformat(value.replace("Z", "+00:00")).timestamp()
        * MILLISECONDS_PER_SECOND
    )


def _utc_now() -> str:
    return datetime.now(UTC).isoformat(timespec="milliseconds").replace("+00:00", "Z")


def _seconds(milliseconds: float) -> float:
    return round(milliseconds / MILLISECONDS_PER_SECOND, 3)


def _nonnegative_milliseconds(value: Any) -> float | None:
    if isinstance(value, bool) or not isinstance(value, int | float):
        return None
    milliseconds = float(value)
    if not math.isfinite(milliseconds) or milliseconds < 0:
        return None
    return milliseconds


def _merged_ranges(intervals: Iterable[tuple[float, float]]) -> list[tuple[float, float]]:
    ordered = sorted((start, end) for start, end in intervals if end > start)
    merged: list[tuple[float, float]] = []
    for start, end in ordered:
        if not merged or start > merged[-1][1]:
            merged.append((start, end))
            continue
        previous_start, previous_end = merged[-1]
        merged[-1] = (previous_start, max(previous_end, end))
    return merged


def _range_measure(intervals: Iterable[tuple[float, float]]) -> float:
    return sum(end - start for start, end in _merged_ranges(intervals))


def _intersection_measure(
    intervals: Iterable[tuple[float, float]],
    start_ms: float,
    end_ms: float,
) -> float:
    return _range_measure(
        (max(start, start_ms), min(end, end_ms))
        for start, end in intervals
        if start < end_ms and end > start_ms
    )


def _native_duration_matches_interval(task: TaskWindow) -> bool:
    if task.client_duration_ms is None:
        return True
    interval_ms = max(0.0, task.end_ms - task.start_ms)
    tolerance_ms = max(1_000.0, 0.05 * max(interval_ms, task.client_duration_ms))
    return abs(task.client_duration_ms - interval_ms) <= tolerance_ms


def _partition_intervals(
    intervals: Sequence[Interval],
    active_ranges: Sequence[tuple[float, float]],
) -> dict[str, list[tuple[float, float]]]:
    clipped: list[Interval] = []
    for interval in intervals:
        for active_start, active_end in active_ranges:
            start = max(interval.start_ms, active_start)
            end = min(interval.end_ms, active_end)
            if end > start:
                clipped.append(Interval(start, end, interval.category))
    endpoints = sorted({point for item in clipped for point in (item.start_ms, item.end_ms)})
    partitioned: dict[str, list[tuple[float, float]]] = defaultdict(list)
    for start, end in pairwise(endpoints):
        active_categories = {
            item.category for item in clipped if item.start_ms < end and item.end_ms > start
        }
        if not active_categories:
            continue
        category = min(
            active_categories,
            key=lambda value: (
                TOOL_CATEGORY_PRIORITY.index(value)
                if value in TOOL_CATEGORY_PRIORITY
                else len(TOOL_CATEGORY_PRIORITY),
                value,
            ),
        )
        partitioned[category].append((start, end))
    return {category: _merged_ranges(ranges) for category, ranges in partitioned.items()}


def _context_for(
    contexts: Sequence[TurnContext],
    turn_id: str,
    at_ms: float,
) -> TurnContext:
    matching = [context for context in contexts if context.turn_id == turn_id]
    preceding = [context for context in matching if context.at_ms <= at_ms]
    if preceding:
        return preceding[-1]
    if matching:
        return matching[0]
    return TurnContext(turn_id, at_ms, UNKNOWN_MODEL, UNKNOWN_THINKING_LEVEL)


def _usage(payload: dict[str, Any]) -> dict[str, int]:
    info = payload.get("info")
    if not isinstance(info, dict):
        return {}
    usage = info.get("last_token_usage")
    if not isinstance(usage, dict):
        return {}
    return {
        "input": int(usage.get("input_tokens", 0)),
        "cached_input": int(usage.get("cached_input_tokens", 0)),
        "output": int(usage.get("output_tokens", 0)),
        "reasoning_output": int(usage.get("reasoning_output_tokens", 0)),
    }


def _tool_category(name: str) -> str:
    if name in {"wait", "wait_agent", "wait_threads"}:
        return "agent_wait"
    if name in {
        "followup_task",
        "interrupt_agent",
        "list_agents",
        "send_message",
        "spawn_agent",
    }:
        return "agent_control"
    if name in {"exec", "exec_command", "write_stdin"}:
        return "command"
    if "automation" in name or name in {
        "open_in_codex",
        "read_thread",
        "read_thread_terminal",
    }:
        return "mcp"
    return "extension"


def _tool_call_category(name: str, input_value: Any) -> str:
    if name not in {"exec", "functions.exec"}:
        return _tool_category(name)
    text = str(input_value or "")
    categories = {
        "agent_wait": ("tools.wait(", "tools.wait_agent(", "tools.wait_threads("),
        "command": ("tools.exec_command(", "tools.write_stdin("),
        "agent_control": (
            "tools.followup_task(",
            "tools.interrupt_agent(",
            "tools.list_agents(",
            "tools.send_message(",
            "tools.spawn_agent(",
        ),
        "file_change": ("tools.apply_patch(",),
        "mcp": ("tools.mcp__", "tools.read_thread(", "tools.open_in_codex("),
    }
    matching = {
        category
        for category, markers in categories.items()
        if any(marker in text for marker in markers)
    }
    if not matching:
        return "extension"
    return min(matching, key=TOOL_CATEGORY_PRIORITY.index)


def _embedded_session_ids(value: Any) -> set[str]:
    if isinstance(value, dict):
        direct = value.get("session_id")
        found = {str(direct)} if isinstance(direct, int | str) else set()
        for nested in value.values():
            found.update(_embedded_session_ids(nested))
        return found
    if isinstance(value, list):
        found: set[str] = set()
        for nested in value:
            found.update(_embedded_session_ids(nested))
        return found
    if not isinstance(value, str):
        return set()
    try:
        decoded = json.loads(value)
    except json.JSONDecodeError:
        decoded = None
    if decoded is not None and decoded != value:
        return _embedded_session_ids(decoded)
    return set(re.findall(r'(?:"session_id"|\bsession_id)\s*:\s*["\']?(\d+)', value))


def _command_text(command: Any) -> str:
    if isinstance(command, list):
        parts = [str(part) for part in command]
        if len(parts) >= 3 and parts[1] in {"-c", "-lc"}:
            return parts[2]
        return " ".join(parts)
    return str(command or "")


def _normalized_command(command: Any) -> str:
    text = WORKTREE_PATTERN.sub("<worktree>", _command_text(command))
    return WHITESPACE_PATTERN.sub(" ", text).strip()


def _command_display(normalized: str) -> str:
    if len(normalized) <= DISPLAY_COMMAND_LIMIT:
        return normalized
    return f"{normalized[: DISPLAY_COMMAND_LIMIT - 1].rstrip()}…"


def _command_category(normalized: str) -> str:
    if "tools.write_stdin" in normalized:
        return "command polling"
    if "gh pr checks" in normalized or "gh run watch" in normalized:
        return "CI wait"
    category: str | None = None
    if "packing-validate" in normalized:
        if "--deep" in normalized:
            category = "packing-validate --deep"
        elif "--strict" in normalized:
            category = "packing-validate --strict"
        elif "--fast" in normalized:
            category = "packing-validate --fast"
        else:
            category = "packing-validate"
    categories = (
        ("run_negative_controls", "negative controls"),
        ("pytest", "pytest"),
        ("test.sh", "test.sh"),
        ("packing-ledger", "packing-ledger"),
        ("softschema", "softschema"),
        ("basedpyright", "basedpyright"),
        ("ruff", "ruff"),
        ("tbd ", "tbd"),
        ("git push", "git push"),
        ("git commit", "git commit"),
        ("python - <<", "inline Python diagnostic"),
        ("python -c", "inline Python diagnostic"),
    )
    if category is None:
        category = next(
            (candidate for marker, candidate in categories if marker in normalized),
            None,
        )
    if category is not None:
        return category
    first = normalized.split(maxsplit=1)[0] if normalized else "unknown"
    if first in INSPECTION_COMMANDS:
        return "repository/log inspection"
    return first


def _session_identity(
    path: Path,
) -> tuple[str, str | None, str | None, str, int | None] | None:
    try:
        with path.open(encoding="utf-8") as handle:
            first_line = handle.readline()
        record = json.loads(first_line)
    except OSError, UnicodeDecodeError, json.JSONDecodeError:
        return None
    if record.get("type") != "session_meta" or not isinstance(record.get("payload"), dict):
        return None
    payload = record["payload"]
    session_id = payload.get("id")
    if not isinstance(session_id, str):
        return None
    parent_id = payload.get("parent_thread_id")
    agent_path = payload.get("agent_path")
    history_start = payload.get("subagent_history_start_ordinal")
    return (
        session_id,
        parent_id if isinstance(parent_id, str) else None,
        agent_path if isinstance(agent_path, str) else None,
        str(payload.get("thread_source", "unknown")),
        history_start if isinstance(history_start, int) else None,
    )


def _legacy_history_start_line(path: Path, session_id: str) -> int | None:
    """Find the first owned record after replayed history in legacy subagent logs."""

    last_foreign_meta_line: int | None = None
    settings_lines: list[int] = []
    try:
        with path.open(encoding="utf-8") as handle:
            for line_number, line in enumerate(handle):
                try:
                    record = json.loads(line)
                except json.JSONDecodeError:
                    continue
                payload = record.get("payload")
                if not isinstance(payload, dict):
                    continue
                if record.get("type") == "session_meta" and payload.get("id") != session_id:
                    last_foreign_meta_line = line_number
                if (
                    record.get("type") == "event_msg"
                    and payload.get("type") == "thread_settings_applied"
                ):
                    settings_lines.append(line_number)
    except OSError, UnicodeDecodeError:
        return None
    if last_foreign_meta_line is None:
        return settings_lines[0] if settings_lines else None
    return next(
        (line for line in settings_lines if line > last_foreign_meta_line),
        last_foreign_meta_line,
    )


def _discover_sessions(
    sessions_root: Path,
) -> dict[str, tuple[Path, str | None, str | None, str, int | None]]:
    discovered: dict[str, tuple[Path, str | None, str | None, str, int | None]] = {}
    for path in sorted(sessions_root.rglob("*.jsonl")):
        identity = _session_identity(path)
        if identity is None:
            continue
        session_id, parent_id, agent_path, source_kind, history_start = identity
        discovered[session_id] = (
            path,
            parent_id,
            agent_path,
            source_kind,
            history_start,
        )
    return discovered


def _parse_session(
    path: Path,
    *,
    session_id: str,
    parent_session_id: str | None,
    agent_path: str | None,
    source_kind: str,
    history_start_ordinal: int | None,
    cutoff_ms: float,
    retrospective_cutoff: bool,
) -> ParsedSession:
    contexts: list[TurnContext] = []
    tokens: list[TokenEvent] = []
    streams: list[StreamItem] = []
    intervals: list[Interval] = []
    commands: list[CommandEvent] = []
    task_starts: dict[str, float] = {}
    task_windows: list[TaskWindow] = []
    pending_calls: dict[str, PendingToolCall] = {}
    continued_turn_ids: set[str] = set()
    completed_call_ids_after_cutoff: set[str] = set()
    legacy_commands: list[LegacyCommand] = []
    running_commands: dict[str, str] = {}
    compaction_item_count = 0
    legacy_compaction_event_times_ms: list[float] = []
    excluded_legacy_replay_task_count = 0
    snapshot_at = ""
    snapshot_ms = 0.0
    legacy_history_start_line = (
        _legacy_history_start_line(path, session_id)
        if parent_session_id is not None and history_start_ordinal is None
        else None
    )

    with path.open(encoding="utf-8") as handle:
        for line_number, line in enumerate(handle):
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                continue
            ordinal = record.get("ordinal")
            payload = record.get("payload")
            if (
                legacy_history_start_line is not None
                and line_number <= legacy_history_start_line
            ):
                continue
            if (
                history_start_ordinal is not None
                and isinstance(ordinal, int)
                and ordinal < history_start_ordinal
            ):
                continue
            timestamp = record.get("timestamp")
            if not isinstance(timestamp, str):
                continue
            at_ms = _timestamp_ms(timestamp)
            if not isinstance(payload, dict):
                continue
            record_type = record.get("type")
            if at_ms > cutoff_ms:
                # Completed-item records carry their own start/end timestamps. When an
                # item straddles a retrospective cutoff, retain only the portion through
                # that cutoff so subtracting two snapshots clips timing at both interval
                # boundaries. Completion-emitted counters remain completion-attributed.
                if retrospective_cutoff and record_type == "event_msg":
                    future_event_type = payload.get("type")
                    future_turn_id = payload.get("turn_id")
                    if isinstance(future_turn_id, str) and future_event_type in {
                        "item_completed",
                        "task_complete",
                    }:
                        continued_turn_ids.add(future_turn_id)
                    if future_event_type == "item_completed":
                        _parse_completed_item(
                            payload,
                            streams,
                            intervals,
                            commands,
                            cutoff_ms=cutoff_ms,
                            include_completion=False,
                        )
                elif retrospective_cutoff and record_type == "response_item":
                    if payload.get("type") in {
                        "custom_tool_call_output",
                        "function_call_output",
                    }:
                        future_call_id = payload.get("call_id")
                        if isinstance(future_call_id, str):
                            completed_call_ids_after_cutoff.add(future_call_id)
                continue
            if at_ms >= snapshot_ms:
                snapshot_at = timestamp
                snapshot_ms = at_ms

            if record_type == "turn_context":
                turn_id = payload.get("turn_id")
                if isinstance(turn_id, str):
                    contexts.append(
                        TurnContext(
                            turn_id=turn_id,
                            at_ms=at_ms,
                            model=str(payload.get("model") or UNKNOWN_MODEL),
                            thinking_level=str(payload.get("effort") or UNKNOWN_THINKING_LEVEL),
                        )
                    )
                continue

            if record_type == "event_msg":
                event_type = payload.get("type")
                turn_id = payload.get("turn_id")
                if event_type == "task_started" and isinstance(turn_id, str):
                    for pending_turn_id, pending_start_ms in tuple(task_starts.items()):
                        task_windows.append(
                            TaskWindow(
                                turn_id=pending_turn_id,
                                start_ms=pending_start_ms,
                                end_ms=at_ms,
                                completed=False,
                                state="interrupted",
                            )
                        )
                        task_starts.pop(pending_turn_id)
                    task_starts[turn_id] = at_ms
                elif event_type == "task_complete" and isinstance(turn_id, str):
                    start_ms = task_starts.pop(turn_id, at_ms)
                    task_windows.append(
                        TaskWindow(
                            turn_id=turn_id,
                            start_ms=start_ms,
                            end_ms=at_ms,
                            completed=True,
                            state="completed",
                            client_duration_ms=_nonnegative_milliseconds(
                                payload.get("duration_ms")
                            ),
                            client_time_to_first_token_ms=_nonnegative_milliseconds(
                                payload.get("time_to_first_token_ms")
                            ),
                        )
                    )
                elif event_type == "token_count":
                    tokens.append(TokenEvent(at_ms, _usage(payload)))
                elif event_type == "context_compacted":
                    legacy_compaction_event_times_ms.append(at_ms)
                elif event_type == "item_completed":
                    _parse_completed_item(
                        payload,
                        streams,
                        intervals,
                        commands,
                        cutoff_ms=cutoff_ms,
                    )
                    item = payload.get("item")
                    if isinstance(item, dict) and item.get("type") == "ContextCompaction":
                        compaction_item_count += 1
                continue

            if record_type == "response_item":
                item_type = payload.get("type")
                call_id = payload.get("call_id")
                if not isinstance(call_id, str):
                    continue
                if item_type in {"custom_tool_call", "function_call"}:
                    pending_calls[call_id] = PendingToolCall(
                        start_ms=at_ms,
                        name=str(payload.get("name") or "unknown"),
                        input_value=payload.get("input", payload.get("arguments")),
                    )
                elif item_type in {"custom_tool_call_output", "function_call_output"}:
                    pending = pending_calls.pop(call_id, None)
                    if pending is not None:
                        category = _tool_call_category(pending.name, pending.input_value)
                        intervals.append(
                            Interval(
                                pending.start_ms,
                                at_ms,
                                category,
                            )
                        )
                        if category == "command":
                            raw_input = str(pending.input_value or "")
                            is_poll = "tools.write_stdin(" in raw_input
                            input_session_ids = _embedded_session_ids(pending.input_value)
                            command_text = _legacy_command_text(pending.input_value)
                            if is_poll:
                                command_text = next(
                                    (
                                        running_commands[process_id]
                                        for process_id in input_session_ids
                                        if process_id in running_commands
                                    ),
                                    command_text,
                                )
                            output_session_ids = _embedded_session_ids(payload.get("output"))
                            if is_poll:
                                for process_id in input_session_ids - output_session_ids:
                                    running_commands.pop(process_id, None)
                            else:
                                for process_id in output_session_ids:
                                    running_commands[process_id] = command_text
                            legacy_commands.append(
                                LegacyCommand(
                                    start_ms=pending.start_ms,
                                    duration_ms=max(0.0, at_ms - pending.start_ms),
                                    input_value=command_text,
                                    invocation_start=not is_poll,
                                )
                            )

    for call_id, pending in pending_calls.items():
        if call_id in completed_call_ids_after_cutoff and pending.start_ms < cutoff_ms:
            intervals.append(
                Interval(
                    pending.start_ms,
                    cutoff_ms,
                    _tool_call_category(pending.name, pending.input_value),
                )
            )
    for turn_id, start_ms in task_starts.items():
        end_ms = (
            cutoff_ms if retrospective_cutoff and turn_id in continued_turn_ids else snapshot_ms
        )
        task_windows.append(
            TaskWindow(
                turn_id=turn_id,
                start_ms=start_ms,
                end_ms=end_ms,
                completed=False,
                state="live",
            )
        )
    task_windows.sort(key=lambda item: (item.start_ms, item.turn_id))
    contexts.sort(key=lambda item: (item.at_ms, item.turn_id))
    if parent_session_id is not None and history_start_ordinal is None:
        # Legacy subagent logs can replay compressed parent turns even after the
        # best available history marker. Owned turns carry a turn_context;
        # replayed parent turns do not. Keep only the former so near-zero-time
        # token snapshots cannot inflate the child's model totals.
        owned_turn_ids = {context.turn_id for context in contexts}
        candidates = [task for task in task_windows if task.turn_id in owned_turn_ids]
        task_windows = [task for task in candidates if _native_duration_matches_interval(task)]
        excluded_legacy_replay_task_count = len(candidates) - len(task_windows)
    tokens.sort(key=lambda item: item.at_ms)
    streams.sort(key=lambda item: (item.start_ms, item.item_type))
    if not commands:
        commands = _legacy_command_events(legacy_commands, task_windows)
    compaction_intervals = [
        interval for interval in intervals if interval.category == "compaction"
    ]
    unmatched_legacy_compactions = sum(
        not any(
            interval.start_ms <= at_ms <= interval.end_ms for interval in compaction_intervals
        )
        for at_ms in legacy_compaction_event_times_ms
    )
    return ParsedSession(
        session_id=session_id,
        path=path,
        parent_session_id=parent_session_id,
        agent_path=agent_path,
        source_kind=source_kind,
        snapshot_at=snapshot_at,
        snapshot_ms=snapshot_ms,
        tasks=task_windows,
        contexts=contexts,
        tokens=tokens,
        streams=streams,
        explicit_intervals=intervals,
        commands=commands,
        compaction_event_count=compaction_item_count + unmatched_legacy_compactions,
        compaction_item_count=compaction_item_count,
        legacy_compaction_event_count=len(legacy_compaction_event_times_ms),
        excluded_legacy_replay_task_count=excluded_legacy_replay_task_count,
    )


def _legacy_command_text(input_value: Any) -> str:
    if isinstance(input_value, dict):
        return _command_text(input_value.get("cmd", input_value))
    text = str(input_value or "")
    try:
        decoded = json.loads(text)
    except json.JSONDecodeError:
        decoded = None
    if isinstance(decoded, dict) and "cmd" in decoded:
        return _command_text(decoded["cmd"])
    encoded_commands = re.findall(r'(?:"cmd"|\bcmd)\s*:\s*("(?:\\.|[^"\\])*")', text)
    commands: list[str] = []
    for encoded in encoded_commands:
        try:
            command = json.loads(encoded)
        except json.JSONDecodeError:
            continue
        if isinstance(command, str):
            commands.append(command)
    return " && ".join(commands) if commands else text


def _legacy_command_events(
    legacy_commands: Sequence[LegacyCommand],
    tasks: Sequence[TaskWindow],
) -> list[CommandEvent]:
    events: list[CommandEvent] = []
    for command in legacy_commands:
        task = _task_for(tasks, command.start_ms)
        if task is None:
            continue
        normalized = _normalized_command(_legacy_command_text(command.input_value))
        events.append(
            CommandEvent(
                turn_id=task.turn_id,
                duration_ms=command.duration_ms,
                normalized=normalized,
                display=_command_display(normalized),
                category=_command_category(normalized),
                invocation_start=command.invocation_start,
            )
        )
    return events


def _parse_completed_item(
    payload: dict[str, Any],
    streams: list[StreamItem],
    intervals: list[Interval],
    commands: list[CommandEvent],
    *,
    cutoff_ms: float | None = None,
    include_completion: bool = True,
) -> None:
    item = payload.get("item")
    if not isinstance(item, dict):
        return
    item_type = item.get("type")
    turn_id = payload.get("turn_id")
    started_at = payload.get("started_at_ms")
    completed_at = payload.get("completed_at_ms")
    if not isinstance(item_type, str) or not isinstance(started_at, int | float):
        return
    if not isinstance(completed_at, int | float):
        return
    start_ms = float(started_at)
    end_ms = float(completed_at)
    if cutoff_ms is not None:
        end_ms = min(end_ms, cutoff_ms)
    if end_ms <= start_ms:
        return
    if item_type in MODEL_ITEM_TYPES and isinstance(turn_id, str):
        streams.append(StreamItem(turn_id, item_type, start_ms, end_ms))
        return
    category = TOOL_ITEM_CATEGORIES.get(item_type)
    if item_type == "ContextCompaction":
        category = "compaction"
    if item_type == "CollabAgentToolCall" and item.get("tool") == "wait":
        category = "agent_wait"
    if category is not None:
        intervals.append(Interval(start_ms, end_ms, category))
    if (
        not include_completion
        or item_type != "CommandExecution"
        or not isinstance(turn_id, str)
    ):
        return
    normalized = _normalized_command(item.get("command"))
    commands.append(
        CommandEvent(
            turn_id=turn_id,
            duration_ms=max(0.0, end_ms - start_ms),
            normalized=normalized,
            display=_command_display(normalized),
            category=_command_category(normalized),
            invocation_start=True,
        )
    )


def _task_for(tasks: Sequence[TaskWindow], at_ms: float) -> TaskWindow | None:
    matching = [task for task in tasks if task.start_ms <= at_ms <= task.end_ms]
    return matching[-1] if matching else None


def _model_key(context: TurnContext) -> tuple[str, str]:
    return context.model, context.thinking_level


def _model_accumulators(
    parsed: ParsedSession,
    tasks: Sequence[TaskWindow],
    explicit_ranges: Sequence[tuple[float, float]],
) -> dict[tuple[str, str], ModelAccumulator]:
    accumulators: dict[tuple[str, str], ModelAccumulator] = defaultdict(ModelAccumulator)
    for task in tasks:
        task_context = _context_for(parsed.contexts, task.turn_id, task.start_ms)
        task_accumulator = accumulators[_model_key(task_context)]
        if task.completed:
            task_accumulator.completed_turn_count += 1
        if task.client_duration_ms is not None:
            task_accumulator.native_duration_samples_ms.append(task.client_duration_ms)
            task_accumulator.native_interval_samples_ms.append(
                max(0.0, task.end_ms - task.start_ms)
            )
        if task.client_time_to_first_token_ms is not None:
            task_accumulator.first_token_samples_ms.append(task.client_time_to_first_token_ms)
        task_contexts = [
            context for context in parsed.contexts if context.turn_id == task.turn_id
        ]
        boundaries = sorted(
            {
                task.start_ms,
                task.end_ms,
                *(
                    context.at_ms
                    for context in task_contexts
                    if task.start_ms < context.at_ms < task.end_ms
                ),
            }
        )
        for start_ms, end_ms in pairwise(boundaries):
            context = _context_for(parsed.contexts, task.turn_id, start_ms)
            explicit_ms = _intersection_measure(explicit_ranges, start_ms, end_ms)
            accumulators[_model_key(context)].response_envelope_ms += max(
                0.0, end_ms - start_ms - explicit_ms
            )

        task_tokens = [
            token for token in parsed.tokens if task.start_ms <= token.at_ms <= task.end_ms
        ]
        previous_ms = task.start_ms
        for token in task_tokens:
            context = _context_for(parsed.contexts, task.turn_id, token.at_ms)
            accumulator = accumulators[_model_key(context)]
            explicit_ms = _intersection_measure(explicit_ranges, previous_ms, token.at_ms)
            accumulator.latencies_ms.append(max(0.0, token.at_ms - previous_ms - explicit_ms))
            accumulator.calls += 1
            accumulator.input_tokens += token.usage.get("input", 0)
            accumulator.cached_input_tokens += token.usage.get("cached_input", 0)
            accumulator.output_tokens += token.usage.get("output", 0)
            accumulator.reasoning_output_tokens += token.usage.get("reasoning_output", 0)
            previous_ms = token.at_ms

    task_turn_ids = {task.turn_id for task in tasks}
    for stream in parsed.streams:
        if stream.turn_id not in task_turn_ids:
            continue
        context = _context_for(parsed.contexts, stream.turn_id, stream.start_ms)
        accumulator = accumulators[_model_key(context)]
        duration_ms = max(0.0, stream.end_ms - stream.start_ms)
        accumulator.stream_item_count += 1
        if stream.item_type == "Reasoning":
            accumulator.streamed_reasoning_ms += duration_ms
        elif stream.item_type == "AgentMessage":
            accumulator.streamed_message_ms += duration_ms
    return accumulators


def _quantile(values: Sequence[float], fraction: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    position = (len(ordered) - 1) * fraction
    lower = int(position)
    upper = min(lower + 1, len(ordered) - 1)
    weight = position - lower
    return ordered[lower] * (1 - weight) + ordered[upper] * weight


def _timing_distribution(samples_ms: Sequence[float]) -> dict[str, int | float]:
    if not samples_ms:
        return {
            "count": 0,
            "total": 0.0,
            "min": 0.0,
            "p50": 0.0,
            "p95": 0.0,
            "max": 0.0,
        }
    return {
        "count": len(samples_ms),
        "total": _seconds(sum(samples_ms)),
        "min": _seconds(min(samples_ms)),
        "p50": _seconds(statistics.median(samples_ms)),
        "p95": _seconds(_quantile(samples_ms, 0.95)),
        "max": _seconds(max(samples_ms)),
    }


def _native_turn_timing(
    completed_turn_count: int,
    duration_samples_ms: Sequence[float],
    matching_interval_samples_ms: Sequence[float],
    first_token_samples_ms: Sequence[float],
) -> dict[str, Any]:
    duration_count = len(duration_samples_ms)
    first_token_count = len(first_token_samples_ms)
    denominator = completed_turn_count or 1
    return {
        "completed_turn_count": completed_turn_count,
        "duration_available_count": duration_count,
        "time_to_first_token_available_count": first_token_count,
        "duration_coverage": round(duration_count / denominator, 3),
        "time_to_first_token_coverage": round(first_token_count / denominator, 3),
        "reported_duration_seconds": _timing_distribution(duration_samples_ms),
        "time_to_first_token_seconds": _timing_distribution(first_token_samples_ms),
        "matching_interval_seconds": _seconds(sum(matching_interval_samples_ms)),
        "reported_minus_interval_seconds": _seconds(
            sum(duration_samples_ms) - sum(matching_interval_samples_ms)
        ),
        "_duration_samples_ms": list(duration_samples_ms),
        "_matching_interval_samples_ms": list(matching_interval_samples_ms),
        "_first_token_samples_ms": list(first_token_samples_ms),
    }


def _native_turn_timing_for_tasks(tasks: Sequence[TaskWindow]) -> dict[str, Any]:
    duration_tasks = [task for task in tasks if task.client_duration_ms is not None]
    return _native_turn_timing(
        completed_turn_count=sum(task.completed for task in tasks),
        duration_samples_ms=[
            task.client_duration_ms
            for task in duration_tasks
            if task.client_duration_ms is not None
        ],
        matching_interval_samples_ms=[
            max(0.0, task.end_ms - task.start_ms) for task in duration_tasks
        ],
        first_token_samples_ms=[
            task.client_time_to_first_token_ms
            for task in tasks
            if task.client_time_to_first_token_ms is not None
        ],
    )


def _merge_native_turn_timings(summaries: Iterable[dict[str, Any]]) -> dict[str, Any]:
    completed_turn_count = 0
    durations: list[float] = []
    intervals: list[float] = []
    first_tokens: list[float] = []
    for summary in summaries:
        completed_turn_count += int(summary["completed_turn_count"])
        durations.extend(float(value) for value in summary["_duration_samples_ms"])
        intervals.extend(float(value) for value in summary["_matching_interval_samples_ms"])
        first_tokens.extend(float(value) for value in summary["_first_token_samples_ms"])
    return _native_turn_timing(
        completed_turn_count,
        durations,
        intervals,
        first_tokens,
    )


def _serialized_models(
    accumulators: dict[tuple[str, str], ModelAccumulator],
) -> list[dict[str, Any]]:
    serialized: list[dict[str, Any]] = []
    for (model, thinking_level), accumulator in sorted(accumulators.items()):
        latencies = accumulator.latencies_ms
        timed_stream_ms = accumulator.streamed_reasoning_ms + accumulator.streamed_message_ms
        first_token_ms = sum(accumulator.first_token_samples_ms)
        serialized.append(
            {
                "model": model,
                "thinking_level": thinking_level,
                "model_response_count": accumulator.calls,
                "response_envelope_seconds": _seconds(accumulator.response_envelope_ms),
                "timed_model_stream_seconds": _seconds(timed_stream_ms),
                "timed_reasoning_seconds": _seconds(accumulator.streamed_reasoning_ms),
                "timed_message_seconds": _seconds(accumulator.streamed_message_ms),
                "unattributed_response_seconds": _seconds(
                    max(0.0, accumulator.response_envelope_ms - timed_stream_ms)
                ),
                "recorded_first_token_wait_seconds": _seconds(first_token_ms),
                "residual_response_seconds": _seconds(
                    max(
                        0.0,
                        accumulator.response_envelope_ms - timed_stream_ms - first_token_ms,
                    )
                ),
                "native_turn_timing": _native_turn_timing(
                    accumulator.completed_turn_count,
                    accumulator.native_duration_samples_ms,
                    accumulator.native_interval_samples_ms,
                    accumulator.first_token_samples_ms,
                ),
                "stream_timing_available": accumulator.stream_item_count > 0,
                "response_interval_seconds": {
                    "min": _seconds(min(latencies)) if latencies else 0.0,
                    "p50": _seconds(statistics.median(latencies)) if latencies else 0.0,
                    "p95": _seconds(_quantile(latencies, 0.95)) if latencies else 0.0,
                    "max": _seconds(max(latencies)) if latencies else 0.0,
                },
                "tokens": {
                    "input": accumulator.input_tokens,
                    "cached_input": accumulator.cached_input_tokens,
                    "output": accumulator.output_tokens,
                    "reasoning_output": accumulator.reasoning_output_tokens,
                },
            }
        )
    return serialized


def _top_commands(commands: Sequence[CommandEvent]) -> list[dict[str, Any]]:
    grouped: dict[str, list[CommandEvent]] = defaultdict(list)
    for command in commands:
        grouped[command.normalized].append(command)
    rows: list[dict[str, Any]] = [
        {
            "category": entries[0].category,
            "display": entries[0].display,
            "invocation_count": sum(entry.invocation_start for entry in entries),
            "timing_segment_count": len(entries),
            "total_seconds": _seconds(sum(entry.duration_ms for entry in entries)),
            "max_seconds": _seconds(max(entry.duration_ms for entry in entries)),
        }
        for entries in grouped.values()
    ]
    return sorted(
        rows,
        key=lambda row: (
            -row["total_seconds"],
            -row["invocation_count"],
            row["display"],
        ),
    )[:20]


def _command_categories(commands: Sequence[CommandEvent]) -> list[dict[str, Any]]:
    grouped: dict[str, list[CommandEvent]] = defaultdict(list)
    for command in commands:
        grouped[command.category].append(command)
    rows = [
        {
            "category": category,
            "invocation_count": sum(entry.invocation_start for entry in entries),
            "timing_segment_count": len(entries),
            "total_seconds": _seconds(sum(entry.duration_ms for entry in entries)),
            "max_seconds": _seconds(max(entry.duration_ms for entry in entries)),
        }
        for category, entries in grouped.items()
    ]
    return sorted(rows, key=lambda row: (-row["total_seconds"], row["category"]))


def _own_summary(parsed: ParsedSession) -> dict[str, Any]:
    active_ranges = [(task.start_ms, task.end_ms) for task in parsed.tasks]
    partitioned = _partition_intervals(parsed.explicit_intervals, active_ranges)
    explicit_ranges = [item for ranges in partitioned.values() for item in ranges]
    active_ms = _range_measure(active_ranges)
    explicit_ms = _range_measure(explicit_ranges)
    models = _model_accumulators(parsed, parsed.tasks, explicit_ranges)
    response_envelope_ms = max(0.0, active_ms - explicit_ms)
    timed_stream_ms = sum(
        (model.streamed_reasoning_ms + model.streamed_message_ms) for model in models.values()
    )
    first_token_ms = sum(task.client_time_to_first_token_ms or 0.0 for task in parsed.tasks)
    turns = [
        _turn_summary(parsed, task, partitioned)
        for task in sorted(parsed.tasks, key=lambda item: item.start_ms)
    ]
    wall_start = min((task.start_ms for task in parsed.tasks), default=parsed.snapshot_ms)
    wall_end = max((task.end_ms for task in parsed.tasks), default=parsed.snapshot_ms)
    wall_span_ms = max(0.0, wall_end - wall_start)
    return {
        "snapshot_at": parsed.snapshot_at,
        "snapshot_incomplete": any(task.state == "live" for task in parsed.tasks),
        "task_count": len(parsed.tasks),
        "completed_task_count": sum(task.completed for task in parsed.tasks),
        "interrupted_task_count": sum(task.state == "interrupted" for task in parsed.tasks),
        "wall_span_seconds": _seconds(wall_span_ms),
        "active_seconds": _seconds(active_ms),
        "inactive_gap_seconds": _seconds(max(0.0, wall_span_ms - active_ms)),
        "response_envelope_seconds": _seconds(response_envelope_ms),
        "timed_model_stream_seconds": _seconds(timed_stream_ms),
        "unattributed_response_seconds": _seconds(
            max(0.0, response_envelope_ms - timed_stream_ms)
        ),
        "recorded_first_token_wait_seconds": _seconds(first_token_ms),
        "residual_response_seconds": _seconds(
            max(0.0, response_envelope_ms - timed_stream_ms - first_token_ms)
        ),
        "native_turn_timing": _native_turn_timing_for_tasks(parsed.tasks),
        "stream_timing_available": any(
            model.stream_item_count > 0 for model in models.values()
        ),
        "tool_seconds_by_category": {
            category: _seconds(_range_measure(ranges))
            for category, ranges in sorted(partitioned.items())
            if category != "compaction"
        },
        "compaction_seconds": _seconds(_range_measure(partitioned.get("compaction", []))),
        "compaction_event_count": parsed.compaction_event_count,
        "compaction_item_count": parsed.compaction_item_count,
        "legacy_compaction_event_count": parsed.legacy_compaction_event_count,
        "excluded_legacy_replay_task_count": (parsed.excluded_legacy_replay_task_count),
        "models": _serialized_models(models),
        "turns": turns,
        "command_categories": _command_categories(parsed.commands),
        "top_commands": _top_commands(parsed.commands),
    }


def _turn_summary(
    parsed: ParsedSession,
    task: TaskWindow,
    partitioned: dict[str, list[tuple[float, float]]],
) -> dict[str, Any]:
    active_ranges = [(task.start_ms, task.end_ms)]
    turn_partitioned = {
        category: [
            (max(start, task.start_ms), min(end, task.end_ms))
            for start, end in ranges
            if start < task.end_ms and end > task.start_ms
        ]
        for category, ranges in partitioned.items()
    }
    explicit_ranges = [item for ranges in turn_partitioned.values() for item in ranges]
    models = _model_accumulators(parsed, [task], explicit_ranges)
    active_ms = _range_measure(active_ranges)
    explicit_ms = _range_measure(explicit_ranges)
    response_envelope_ms = max(0.0, active_ms - explicit_ms)
    timed_stream_ms = sum(
        (model.streamed_reasoning_ms + model.streamed_message_ms) for model in models.values()
    )
    first_token_ms = task.client_time_to_first_token_ms or 0.0
    return {
        "turn_id": task.turn_id,
        "completed": task.completed,
        "state": task.state,
        "active_seconds": _seconds(active_ms),
        "response_envelope_seconds": _seconds(response_envelope_ms),
        "timed_model_stream_seconds": _seconds(timed_stream_ms),
        "unattributed_response_seconds": _seconds(
            max(0.0, response_envelope_ms - timed_stream_ms)
        ),
        "recorded_first_token_wait_seconds": _seconds(first_token_ms),
        "residual_response_seconds": _seconds(
            max(0.0, response_envelope_ms - timed_stream_ms - first_token_ms)
        ),
        "client_duration_seconds": (
            _seconds(task.client_duration_ms) if task.client_duration_ms is not None else None
        ),
        "client_time_to_first_token_seconds": (
            _seconds(task.client_time_to_first_token_ms)
            if task.client_time_to_first_token_ms is not None
            else None
        ),
        "stream_timing_available": any(
            model.stream_item_count > 0 for model in models.values()
        ),
        "tool_seconds_by_category": {
            category: _seconds(_range_measure(ranges))
            for category, ranges in sorted(turn_partitioned.items())
            if category != "compaction" and ranges
        },
        "compaction_seconds": _seconds(_range_measure(turn_partitioned.get("compaction", []))),
        "models": _serialized_models(models),
    }


def _merge_model_rows(rows: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    accumulators: dict[tuple[str, str], ModelAccumulator] = defaultdict(ModelAccumulator)
    for row in rows:
        key = (str(row["model"]), str(row["thinking_level"]))
        accumulator = accumulators[key]
        accumulator.calls += int(row["model_response_count"])
        accumulator.response_envelope_ms += (
            float(row["response_envelope_seconds"]) * MILLISECONDS_PER_SECOND
        )
        accumulator.streamed_reasoning_ms += (
            float(row["timed_reasoning_seconds"]) * MILLISECONDS_PER_SECOND
        )
        accumulator.streamed_message_ms += (
            float(row["timed_message_seconds"]) * MILLISECONDS_PER_SECOND
        )
        accumulator.stream_item_count += int(bool(row["stream_timing_available"]))
        native_timing = row["native_turn_timing"]
        accumulator.completed_turn_count += int(native_timing["completed_turn_count"])
        accumulator.native_duration_samples_ms.extend(
            float(value) for value in native_timing["_duration_samples_ms"]
        )
        accumulator.native_interval_samples_ms.extend(
            float(value) for value in native_timing["_matching_interval_samples_ms"]
        )
        accumulator.first_token_samples_ms.extend(
            float(value) for value in native_timing["_first_token_samples_ms"]
        )
        tokens = row["tokens"]
        accumulator.input_tokens += int(tokens["input"])
        accumulator.cached_input_tokens += int(tokens["cached_input"])
        accumulator.output_tokens += int(tokens["output"])
        accumulator.reasoning_output_tokens += int(tokens["reasoning_output"])
    merged = _serialized_models(accumulators)
    for row in merged:
        row["response_interval_seconds"] = None
    return merged


def _node_intervals(node: dict[str, Any]) -> list[tuple[float, float]]:
    ranges = list(node.pop("_active_ranges"))
    for child in node["children"]:
        ranges.extend(_node_intervals(child))
    return ranges


def _build_node(
    parsed_by_id: dict[str, ParsedSession],
    children_by_parent: dict[str, list[str]],
    session_id: str,
    ancestors: frozenset[str],
) -> dict[str, Any]:
    if session_id in ancestors:
        raise ValueError(f"cycle in Codex session tree at {session_id}")
    parsed = parsed_by_id[session_id]
    own = _own_summary(parsed)
    children = [
        _build_node(parsed_by_id, children_by_parent, child_id, ancestors | {session_id})
        for child_id in sorted(children_by_parent.get(session_id, []))
        if child_id in parsed_by_id
    ]
    own_ranges = [(task.start_ms, task.end_ms) for task in parsed.tasks]
    child_ranges = [item for child in children for item in child["_active_ranges"]]
    subtree_ranges = own_ranges + child_ranges
    all_nodes = [own, *(child["subtree"] for child in children)]
    agent_active_seconds = sum(float(item["agent_active_seconds"]) for item in all_nodes[1:])
    agent_active_seconds += float(own["active_seconds"])
    model_rows = list(own["models"])
    for child in children:
        model_rows.extend(child["subtree"]["models"])
    start_ms = min((start for start, _ in subtree_ranges), default=parsed.snapshot_ms)
    end_ms = max((end for _, end in subtree_ranges), default=parsed.snapshot_ms)
    active_union_seconds = _seconds(_range_measure(subtree_ranges))
    subtree = {
        "session_count": 1 + sum(int(child["subtree"]["session_count"]) for child in children),
        "agent_active_seconds": round(agent_active_seconds, 3),
        "elapsed_envelope_seconds": _seconds(max(0.0, end_ms - start_ms)),
        "active_union_seconds": active_union_seconds,
        "parallel_overlap_seconds": round(
            max(0.0, agent_active_seconds - active_union_seconds), 3
        ),
        "response_envelope_seconds": round(
            float(own["response_envelope_seconds"])
            + sum(float(child["subtree"]["response_envelope_seconds"]) for child in children),
            3,
        ),
        "timed_model_stream_seconds": round(
            float(own["timed_model_stream_seconds"])
            + sum(float(child["subtree"]["timed_model_stream_seconds"]) for child in children),
            3,
        ),
        "unattributed_response_seconds": round(
            float(own["unattributed_response_seconds"])
            + sum(
                float(child["subtree"]["unattributed_response_seconds"]) for child in children
            ),
            3,
        ),
        "recorded_first_token_wait_seconds": round(
            float(own["recorded_first_token_wait_seconds"])
            + sum(
                float(child["subtree"]["recorded_first_token_wait_seconds"])
                for child in children
            ),
            3,
        ),
        "residual_response_seconds": round(
            float(own["residual_response_seconds"])
            + sum(float(child["subtree"]["residual_response_seconds"]) for child in children),
            3,
        ),
        "native_turn_timing": _merge_native_turn_timings(
            [own["native_turn_timing"]]
            + [child["subtree"]["native_turn_timing"] for child in children]
        ),
        "compaction_event_count": int(own["compaction_event_count"])
        + sum(int(child["subtree"]["compaction_event_count"]) for child in children),
        "compaction_item_count": int(own["compaction_item_count"])
        + sum(int(child["subtree"]["compaction_item_count"]) for child in children),
        "legacy_compaction_event_count": int(own["legacy_compaction_event_count"])
        + sum(int(child["subtree"]["legacy_compaction_event_count"]) for child in children),
        "excluded_legacy_replay_task_count": int(own["excluded_legacy_replay_task_count"])
        + sum(int(child["subtree"]["excluded_legacy_replay_task_count"]) for child in children),
        "models": _merge_model_rows(model_rows),
    }
    return {
        "session_id": parsed.session_id,
        "parent_session_id": parsed.parent_session_id,
        "agent_path": parsed.agent_path,
        "source_kind": parsed.source_kind,
        "log_path": str(parsed.path),
        "own": own,
        "subtree": subtree,
        "children": children,
        "_active_ranges": subtree_ranges,
    }


def build_rollup(
    sessions_root: Path,
    root_ids: Sequence[str],
    *,
    through: str | None = None,
    retrospective_cutoff: bool = False,
) -> dict[str, Any]:
    """Build a recursive, deterministic rollup for the requested Codex task ids."""

    scan_started_at = _utc_now()
    cutoff_at = through or scan_started_at
    try:
        cutoff_ms = _timestamp_ms(cutoff_at)
    except ValueError as error:
        raise ValueError(f"invalid --through timestamp: {cutoff_at}") from error
    discovered = _discover_sessions(sessions_root)
    missing = sorted(set(root_ids) - discovered.keys())
    if missing:
        raise ValueError(
            f"Codex session ids not found under {sessions_root}: {', '.join(missing)}"
        )
    relevant: set[str] = set(root_ids)
    changed = True
    while changed:
        changed = False
        for session_id, (_, parent_id, _, _, _) in discovered.items():
            if parent_id in relevant and session_id not in relevant:
                relevant.add(session_id)
                changed = True
    all_parsed_by_id = {
        session_id: _parse_session(
            discovered[session_id][0],
            session_id=session_id,
            parent_session_id=discovered[session_id][1],
            agent_path=discovered[session_id][2],
            source_kind=discovered[session_id][3],
            history_start_ordinal=discovered[session_id][4],
            cutoff_ms=cutoff_ms,
            retrospective_cutoff=retrospective_cutoff,
        )
        for session_id in sorted(relevant)
    }
    parsed_by_id = {
        session_id: parsed
        for session_id, parsed in all_parsed_by_id.items()
        if parsed.snapshot_at or session_id in root_ids
    }
    children_by_parent: dict[str, list[str]] = defaultdict(list)
    for session_id, parsed in parsed_by_id.items():
        if parsed.parent_session_id:
            children_by_parent[parsed.parent_session_id].append(session_id)
    roots = [
        _build_node(parsed_by_id, children_by_parent, root_id, frozenset())
        for root_id in root_ids
    ]
    for root in roots:
        _remove_private_fields(root)
    snapshot_at = max(
        (parsed.snapshot_at for parsed in parsed_by_id.values() if parsed.snapshot_at),
        default="",
    )
    return {
        "schema": ROLLUP_SCHEMA,
        "scan_started_at": scan_started_at,
        "scan_completed_at": _utc_now(),
        "cutoff_at": cutoff_at,
        "snapshot_at": snapshot_at,
        "sessions_root": str(sessions_root),
        "semantics": {
            "response_envelope_seconds": (
                "Upper-bound client response envelope: active task time after explicit tool "
                "and context-compaction intervals are removed. It includes model generation, "
                "API latency, client dispatch, and any uninstrumented or suspended gaps; it is "
                "not server-side inference latency."
            ),
            "timed_model_stream_seconds": (
                "Lower-bound time covered by explicit Reasoning and AgentMessage item timing. "
                "Legacy logs may not expose these item timings."
            ),
            "unattributed_response_seconds": (
                "Response-envelope time not covered by timed model-stream items. Do not assign "
                "it wholly to model inference. This compatibility field still includes the "
                "recorded first-token wait."
            ),
            "recorded_first_token_wait_seconds": (
                "Sum of client-observed time_to_first_token_ms values on completed turns. "
                "This measures only the first response in each turn and is not a server-phase "
                "breakdown."
            ),
            "residual_response_seconds": (
                "Response-envelope time left after explicit Reasoning and AgentMessage item "
                "timing and recorded first-token wait are removed. It can include later model "
                "startup, API and client latency, and uninstrumented or suspended gaps."
            ),
            "native_turn_timing": (
                "Coverage and distributions from task_complete.duration_ms and "
                "task_complete.time_to_first_token_ms. Event timestamps remain the basis for "
                "overlap-safe interval accounting."
            ),
            "excluded_legacy_replay_task_count": (
                "Legacy subagent task records excluded because a client-reported duration "
                "differed from the local event interval by more than max(1 second, 5%). Such "
                "records are compressed parent-history replays, not child execution."
            ),
            "compaction_event_count": (
                "Count of current ContextCompaction item records plus legacy "
                "context_compacted events that do not coincide with a timed item. "
                "Source-specific item and legacy record counts are also reported."
            ),
            "model_response_count": (
                "Count of token-usage response events. This is the most stable client-log "
                "proxy for model responses, not a provider-side request counter."
            ),
            "agent_active_seconds": (
                "Sum of active task time across a session subtree. Parallel children add "
                "agent-seconds "
                "without extending the parent wall clock by the same amount."
            ),
            "active_union_seconds": (
                "Union of active parent and child intervals, used to expose overlap without "
                "double counting."
            ),
            "live_logs": (
                "The scan-start time is the default cutoff, or --through supplies an explicit "
                "cutoff. Ordinary live snapshots end incomplete tasks at their last included "
                "event. A retrospective cutoff may clip tasks and timed items to the cutoff "
                "only when a later record proves they straddled it. Completion-emitted "
                "counters can still arrive later, so a live snapshot is a lower bound for "
                "those counters."
            ),
        },
        "roots": roots,
    }


def _remove_private_fields(node: dict[str, Any]) -> None:
    node.pop("_active_ranges", None)
    for summary in (node["own"], node["subtree"]):
        _remove_private_timing_fields(summary["native_turn_timing"])
        for model in summary["models"]:
            _remove_private_timing_fields(model["native_turn_timing"])
    for child in node["children"]:
        _remove_private_fields(child)


def _remove_private_timing_fields(timing: dict[str, Any]) -> None:
    for key in (
        "_duration_samples_ms",
        "_matching_interval_samples_ms",
        "_first_token_samples_ms",
    ):
        timing.pop(key, None)


def _format_duration(seconds: float) -> str:
    if seconds >= SECONDS_PER_HOUR:
        hours = int(seconds // SECONDS_PER_HOUR)
        minutes = int((seconds % SECONDS_PER_HOUR) // SECONDS_PER_MINUTE)
        return f"{hours}h {minutes}m"
    if seconds >= SECONDS_PER_MINUTE:
        minutes = int(seconds // SECONDS_PER_MINUTE)
        remainder = round(seconds % SECONDS_PER_MINUTE)
        return f"{minutes}m {remainder}s"
    return f"{seconds:.1f}s"


def _format_native_duration(row: dict[str, Any], statistic: str = "total") -> str:
    seconds = float(row["native_turn_timing"]["reported_duration_seconds"][statistic])
    return _format_duration(seconds)


def _render_tree(
    node: dict[str, Any],
    indent: int = 0,
    *,
    include_turns: bool = False,
) -> list[str]:
    prefix = "  " * indent
    own = node["own"]
    path = f" ({node['agent_path']})" if node["agent_path"] else ""
    marker = " [live]" if own["snapshot_incomplete"] else ""
    lines = [
        (
            f"{prefix}- `{node['session_id']}`{path}{marker}: "
            f"{_format_duration(own['active_seconds'])} active; "
            f"{_format_duration(own['response_envelope_seconds'])} response envelope; "
            f"{_format_duration(own['recorded_first_token_wait_seconds'])} "
            "first-token wait; "
            f"{_format_duration(own['timed_model_stream_seconds'])} timed model stream; "
            f"{_format_duration(own['residual_response_seconds'])} residual response"
        )
    ]
    if include_turns:
        for turn in own["turns"]:
            turn_marker = f" [{turn['state']}]" if turn["state"] != "completed" else ""
            lines.append(
                f"{prefix}  - turn `{turn['turn_id']}`{turn_marker}: "
                f"{_format_duration(turn['active_seconds'])} active"
            )
            lines.extend(
                (
                    f"{prefix}    - `{model['model']}` / "
                    f"`{model['thinking_level']}`: "
                    f"{model['model_response_count']} responses; "
                    f"{_format_duration(model['response_envelope_seconds'])} envelope; "
                    f"{_format_duration(model['recorded_first_token_wait_seconds'])} "
                    "first-token wait; "
                    f"{_format_duration(model['timed_model_stream_seconds'])} "
                    "timed stream; "
                    f"{_format_native_duration(model)} "
                    "native turn duration; "
                    f"{model['tokens']['reasoning_output']} reasoning tokens"
                )
                for model in turn["models"]
            )
    else:
        lines.extend(
            (
                f"{prefix}  - `{model['model']}` / `{model['thinking_level']}`: "
                f"{model['model_response_count']} responses; "
                f"{_format_duration(model['response_envelope_seconds'])} envelope; "
                f"{_format_duration(model['recorded_first_token_wait_seconds'])} "
                "first-token wait; "
                f"{_format_duration(model['timed_model_stream_seconds'])} timed stream; "
                f"{_format_native_duration(model)} "
                "native turn duration; "
                f"{model['tokens']['reasoning_output']} reasoning tokens"
            )
            for model in own["models"]
        )
    for child in node["children"]:
        lines.extend(_render_tree(child, indent + 1, include_turns=include_turns))
    return lines


def render_markdown(rollup: dict[str, Any], *, include_turns: bool = False) -> str:
    """Render the stable rollup as a compact human-readable report."""

    lines = [
        "# Codex Efficiency Rollup",
        "",
        f"**Cutoff:** {rollup['cutoff_at']}",
        "",
        f"**Log snapshot:** {rollup['snapshot_at']}",
        "",
        "The response envelope is active client time after explicit tools and context",
        "compaction are removed; it is an upper bound, not server inference latency.",
        "Native first-token wait covers only the first response in each completed turn.",
        "Timed model streaming is a lower bound and is unavailable in some legacy logs.",
        "Parent wall time and recursive agent-time are reported separately because child",
        "agents can overlap.",
        "",
        "## Recursive task tree",
        "",
    ]
    for root in rollup["roots"]:
        lines.extend(_render_tree(root, include_turns=include_turns))
    lines.extend(["", "## Root rollups", ""])
    for root in rollup["roots"]:
        subtree = root["subtree"]
        lines.extend(
            [
                f"### `{root['session_id']}`",
                "",
                "| Metric | Value |",
                "| --- | ---: |",
                f"| Parent active time | {_format_duration(root['own']['active_seconds'])} |",
                (
                    "| Parent response envelope | "
                    f"{_format_duration(root['own']['response_envelope_seconds'])} |"
                ),
                (
                    "| Parent timed model stream | "
                    f"{_format_duration(root['own']['timed_model_stream_seconds'])} |"
                ),
                (
                    "| Parent recorded first-token wait | "
                    f"{_format_duration(root['own']['recorded_first_token_wait_seconds'])} |"
                ),
                (
                    "| Parent residual response | "
                    f"{_format_duration(root['own']['residual_response_seconds'])} |"
                ),
                (
                    "| Parent native completed-turn duration | "
                    f"{_format_native_duration(root['own'])} |"
                ),
                (
                    "| Parent native duration coverage | "
                    f"{root['own']['native_turn_timing']['duration_available_count']} / "
                    f"{root['own']['native_turn_timing']['completed_turn_count']} |"
                ),
                (
                    "| Recursive agent-time | "
                    f"{_format_duration(subtree['agent_active_seconds'])} |"
                ),
                f"| Active union | {_format_duration(subtree['active_union_seconds'])} |",
                (
                    "| Parallel overlap | "
                    f"{_format_duration(subtree['parallel_overlap_seconds'])} |"
                ),
                f"| Sessions | {subtree['session_count']} |",
                "",
                (
                    "| Model | Thinking | Responses | Native turn duration | Turn p50 | "
                    "Response envelope | First-token wait | Timed stream | Residual | Input | "
                    "Cached input | Output | Reasoning output |"
                ),
                (
                    "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | "
                    "---: | ---: | ---: | ---: |"
                ),
            ]
        )
        for model in subtree["models"]:
            tokens = model["tokens"]
            lines.append(
                f"| `{model['model']}` | `{model['thinking_level']}` | "
                f"{model['model_response_count']} | "
                f"{_format_native_duration(model)} | "
                f"{_format_native_duration(model, 'p50')} | "
                f"{_format_duration(model['response_envelope_seconds'])} | "
                f"{_format_duration(model['recorded_first_token_wait_seconds'])} | "
                f"{_format_duration(model['timed_model_stream_seconds'])} | "
                f"{_format_duration(model['residual_response_seconds'])} | "
                f"{tokens['input']} | {tokens['cached_input']} | {tokens['output']} | "
                f"{tokens['reasoning_output']} |"
            )
        commands = root["own"]["top_commands"][:10]
        if commands:
            lines.extend(
                [
                    "",
                    "Top parent commands:",
                    "",
                    "| Category | Invocations | Segments | Total | Max segment | Command |",
                    "| --- | ---: | ---: | ---: | ---: | --- |",
                ]
            )
            for command in commands:
                display = str(command["display"]).replace("|", "\\|")
                lines.append(
                    f"| {command['category']} | {command['invocation_count']} | "
                    f"{command['timing_segment_count']} | "
                    f"{_format_duration(command['total_seconds'])} | "
                    f"{_format_duration(command['max_seconds'])} | `{display}` |"
                )
        lines.append("")
    lines.extend(
        [
            "<!-- This document follows common-doc-guidelines.md.",
            "See github.com/jlevy/practical-prose and review guidelines before editing.",
            "-->",
            "",
        ]
    )
    return "\n".join(lines)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Recursively roll up timing and model usage from Codex JSONL logs."
    )
    parser.add_argument(
        "--sessions-root",
        type=Path,
        default=Path.home() / ".codex" / "sessions",
        help="Codex sessions directory to scan (default: ~/.codex/sessions).",
    )
    parser.add_argument(
        "--root-id",
        action="append",
        required=True,
        help="Root Codex task id. Repeat to compare several task trees.",
    )
    parser.add_argument(
        "--format",
        choices=("json", "markdown"),
        default="markdown",
        help="Output format (default: markdown).",
    )
    parser.add_argument(
        "--through",
        help=(
            "Include records at or before this ISO-8601 timestamp. By default the scan-start "
            "time freezes live logs."
        ),
    )
    parser.add_argument(
        "--include-turns",
        action="store_true",
        help="Include every turn below each session in Markdown output.",
    )
    return parser


def main(arguments: Sequence[str] | None = None) -> int:
    """Run the Codex efficiency rollup CLI."""

    options = _parser().parse_args(arguments)
    try:
        rollup = build_rollup(
            options.sessions_root,
            options.root_id,
            through=options.through,
        )
    except ValueError as error:
        print(f"error: {error}", file=sys.stderr)
        return 2
    if options.format == "json":
        print(json.dumps(rollup, indent=2, sort_keys=True))
    else:
        print(render_markdown(rollup, include_turns=options.include_turns), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
