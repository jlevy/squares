#!/usr/bin/env python3
"""Build a privacy-safe retained delta from two Codex task-tree snapshots."""

from __future__ import annotations

import argparse
import sys
from collections.abc import Iterable, Mapping
from datetime import datetime
from pathlib import Path
from typing import Any

import yaml
from strif import atomic_output_file

from devtools.codex_log_rollup import ROLLUP_SCHEMA, build_rollup

CONTRACT = "packing.squares:CodexTaskTreeDelta/v1"
SCHEMA_REFERENCE = "../schemas/codex-task-tree-delta.schema.yaml"
TOOL_CATEGORIES = frozenset(
    {"agent_wait", "command", "mcp", "agent_control", "file_change", "extension"}
)
INTEGER_FIELDS = (
    "session_count",
    "task_count",
    "completed_task_count",
    "interrupted_task_count",
    "compaction_event_count",
    "compaction_item_count",
    "legacy_compaction_event_count",
    "excluded_legacy_replay_task_count",
)
NUMBER_FIELDS = (
    "agent_active_seconds",
    "elapsed_envelope_seconds",
    "active_union_seconds",
    "parallel_overlap_seconds",
    "timed_model_stream_seconds",
    "recorded_first_token_wait_seconds",
    "compaction_seconds",
)
MODEL_INTEGER_FIELDS = ("model_response_count",)
MODEL_NUMBER_FIELDS = (
    "timed_model_stream_seconds",
    "timed_reasoning_seconds",
    "timed_message_seconds",
    "recorded_first_token_wait_seconds",
)
TOKEN_FIELDS = ("input", "cached_input", "output", "reasoning_output")
ROUND_DIGITS = 3


def _instant(value: str) -> datetime:
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as error:
        raise ValueError(f"invalid cutoff timestamp: {value}") from error
    if parsed.tzinfo is None:
        raise ValueError(f"cutoff timestamp has no UTC offset: {value}")
    return parsed


def _mapping(value: object, field: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise TypeError(f"{field} is not a mapping")
    return value


def _integer(value: object, field: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value < 0:
        raise ValueError(f"{field} is not a nonnegative integer")
    return value


def _number(value: object, field: str) -> float:
    if not isinstance(value, int | float) or isinstance(value, bool) or value < 0:
        raise ValueError(f"{field} is not a nonnegative number")
    return round(float(value), ROUND_DIGITS)


def _nodes(root: Mapping[str, Any]) -> Iterable[Mapping[str, Any]]:
    yield root
    children = root.get("children")
    if not isinstance(children, list):
        raise TypeError("Codex rollup node children is not a list")
    for child in children:
        yield from _nodes(_mapping(child, "Codex rollup child"))


def _root(snapshot: Mapping[str, Any], root_task_id: str) -> Mapping[str, Any]:
    if snapshot.get("schema") != ROLLUP_SCHEMA:
        raise ValueError(f"expected {ROLLUP_SCHEMA}, got {snapshot.get('schema')!r}")
    roots = snapshot.get("roots")
    if not isinstance(roots, list) or len(roots) != 1:
        raise ValueError("Codex delta needs exactly one root task tree")
    root = _mapping(roots[0], "Codex rollup root")
    if root.get("session_id") != root_task_id:
        raise ValueError("Codex rollup root does not match the requested root task id")
    return root


def _sum_own_integer(nodes: Iterable[Mapping[str, Any]], field: str) -> int:
    return sum(
        _integer(_mapping(node.get("own"), "Codex node own").get(field), f"own.{field}")
        for node in nodes
    )


def _sum_own_number(nodes: Iterable[Mapping[str, Any]], field: str) -> float:
    return round(
        sum(
            _number(_mapping(node.get("own"), "Codex node own").get(field), f"own.{field}")
            for node in nodes
        ),
        ROUND_DIGITS,
    )


def _tool_seconds(nodes: Iterable[Mapping[str, Any]]) -> dict[str, float]:
    totals: dict[str, float] = {}
    for node in nodes:
        own = _mapping(node.get("own"), "Codex node own")
        values = _mapping(own.get("tool_seconds_by_category"), "own.tool_seconds_by_category")
        unknown = set(values) - TOOL_CATEGORIES
        if unknown:
            raise ValueError(f"unexpected Codex tool categories: {sorted(unknown)}")
        for category, value in values.items():
            totals[category] = round(
                totals.get(category, 0.0) + _number(value, f"tool.{category}"), ROUND_DIGITS
            )
    return dict(sorted(totals.items()))


def _models(subtree: Mapping[str, Any]) -> list[dict[str, Any]]:
    raw_models = subtree.get("models")
    if not isinstance(raw_models, list):
        raise TypeError("subtree.models is not a list")
    retained: list[dict[str, Any]] = []
    for raw in raw_models:
        model = _mapping(raw, "subtree model")
        name = model.get("model")
        thinking_level = model.get("thinking_level")
        if not isinstance(name, str) or not isinstance(thinking_level, str):
            raise TypeError("Codex model identity is not a string")
        tokens = _mapping(model.get("tokens"), "model.tokens")
        retained.append(
            {
                "model": name,
                "thinking_level": thinking_level,
                **{
                    field: _integer(model.get(field), f"model.{field}")
                    for field in MODEL_INTEGER_FIELDS
                },
                **{
                    field: _number(model.get(field), f"model.{field}")
                    for field in MODEL_NUMBER_FIELDS
                },
                "tokens": {
                    field: _integer(tokens.get(field), f"model.tokens.{field}")
                    for field in TOKEN_FIELDS
                },
            }
        )
    return sorted(retained, key=lambda row: (row["model"], row["thinking_level"]))


def _metrics(snapshot: Mapping[str, Any], root_task_id: str) -> dict[str, Any]:
    root = _root(snapshot, root_task_id)
    tree_nodes = list(_nodes(root))
    subtree = _mapping(root.get("subtree"), "Codex root subtree")
    return {
        "session_count": _integer(subtree.get("session_count"), "subtree.session_count"),
        "task_count": _sum_own_integer(tree_nodes, "task_count"),
        "completed_task_count": _sum_own_integer(tree_nodes, "completed_task_count"),
        "interrupted_task_count": _sum_own_integer(tree_nodes, "interrupted_task_count"),
        **{
            field: _number(subtree.get(field), f"subtree.{field}")
            for field in NUMBER_FIELDS
            if field != "compaction_seconds"
        },
        "tool_seconds_by_category": _tool_seconds(tree_nodes),
        "compaction_seconds": _sum_own_number(tree_nodes, "compaction_seconds"),
        **{
            field: _integer(subtree.get(field), f"subtree.{field}")
            for field in INTEGER_FIELDS
            if field
            not in {
                "session_count",
                "task_count",
                "completed_task_count",
                "interrupted_task_count",
            }
        },
        "models": _models(subtree),
    }


def _difference(after: int | float, before: int | float, field: str) -> int | float:
    if after < before:
        raise ValueError(f"non-monotone Codex delta field {field}: {before} -> {after}")
    value = after - before
    return value if isinstance(after, int) and isinstance(before, int) else round(value, 3)


def _model_index(metrics: Mapping[str, Any]) -> dict[tuple[str, str], Mapping[str, Any]]:
    return {(str(row["model"]), str(row["thinking_level"])): row for row in metrics["models"]}


def _zero_model(model: str, thinking_level: str) -> dict[str, Any]:
    return {
        "model": model,
        "thinking_level": thinking_level,
        **dict.fromkeys(MODEL_INTEGER_FIELDS, 0),
        **dict.fromkeys(MODEL_NUMBER_FIELDS, 0.0),
        "tokens": dict.fromkeys(TOKEN_FIELDS, 0),
    }


def _subtract_metrics(before: Mapping[str, Any], after: Mapping[str, Any]) -> dict[str, Any]:
    delta: dict[str, Any] = {
        field: _difference(after[field], before[field], field)
        for field in (*INTEGER_FIELDS, *NUMBER_FIELDS)
    }
    before_tools = _mapping(before["tool_seconds_by_category"], "before tools")
    after_tools = _mapping(after["tool_seconds_by_category"], "after tools")
    delta["tool_seconds_by_category"] = {
        category: _difference(
            after_tools.get(category, 0.0),
            before_tools.get(category, 0.0),
            f"tool_seconds_by_category.{category}",
        )
        for category in sorted(set(before_tools) | set(after_tools))
    }

    before_models = _model_index(before)
    after_models = _model_index(after)
    model_deltas: list[dict[str, Any]] = []
    for key in sorted(set(before_models) | set(after_models)):
        first = before_models.get(key, _zero_model(*key))
        last = after_models.get(key, _zero_model(*key))
        row = {
            "model": key[0],
            "thinking_level": key[1],
            **{
                field: _difference(last[field], first[field], f"model.{key}.{field}")
                for field in (*MODEL_INTEGER_FIELDS, *MODEL_NUMBER_FIELDS)
            },
            "tokens": {
                field: _difference(
                    last["tokens"][field],
                    first["tokens"][field],
                    f"model.{key}.tokens.{field}",
                )
                for field in TOKEN_FIELDS
            },
        }
        model_deltas.append(row)
    delta["models"] = model_deltas
    return delta


def build_delta(
    sessions_root: Path,
    root_task_id: str,
    *,
    start: str,
    end: str,
) -> dict[str, Any]:
    """Measure the additive change in one Codex task tree between explicit cutoffs."""

    if _instant(end) <= _instant(start):
        raise ValueError("end cutoff must be later than start cutoff")
    before_rollup = build_rollup(sessions_root, [root_task_id], through=start)
    after_rollup = build_rollup(sessions_root, [root_task_id], through=end)
    before = _metrics(before_rollup, root_task_id)
    after = _metrics(after_rollup, root_task_id)
    after_root = _root(after_rollup, root_task_id)
    live_session_count = sum(
        bool(_mapping(node.get("own"), "Codex node own").get("snapshot_incomplete"))
        for node in _nodes(after_root)
    )

    def snapshot_at(rollup: Mapping[str, Any]) -> str | None:
        value = rollup.get("snapshot_at")
        return value if isinstance(value, str) and value else None

    return {
        "softschema": {
            "contract": CONTRACT,
            "schema": SCHEMA_REFERENCE,
            "envelope": "rollup",
            "status": "enforced",
        },
        "rollup": {
            "source": {
                "harness": "codex",
                "source_schema": ROLLUP_SCHEMA,
                "root_task_id": root_task_id,
                "start_cutoff_at": start,
                "end_cutoff_at": end,
                "before_snapshot_at": snapshot_at(before_rollup),
                "after_snapshot_at": snapshot_at(after_rollup),
            },
            "completeness": {
                "snapshot_incomplete": live_session_count > 0,
                "live_session_count": live_session_count,
            },
            "before": before,
            "after": after,
            "delta": _subtract_metrics(before, after),
            "semantics": {
                "attribution": (
                    "Codex logs carry no git-branch telemetry. This task-tree interval is "
                    "not branch-attributed unless an AgentSession explicitly declares it."
                ),
                "delta": (
                    "Delta is after minus before for a fixed whitelist of cumulative additive "
                    "fields; a decrease is rejected rather than hidden."
                ),
                "cutoff_boundary": (
                    "Codex emits some token and timed-item records at completion, so work that "
                    "straddles the start cutoff can be charged wholly to this interval."
                ),
                "live_snapshot": (
                    "When snapshot_incomplete is true, the after snapshot and delta are lower "
                    "bounds on the task tree's eventual totals."
                ),
                "retention": (
                    "The receipt retains aggregate counts, timings, models, efforts, and "
                    "tokens; it drops prose, private paths, agent paths, turn ids, and command "
                    "history."
                ),
            },
        },
    }


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sessions-root", type=Path, required=True)
    parser.add_argument("--root-id", required=True, help="root Codex task id")
    parser.add_argument("--start", required=True, help="inclusive ISO-8601 baseline cutoff")
    parser.add_argument("--end", required=True, help="inclusive ISO-8601 after cutoff")
    parser.add_argument("--out", type=Path, required=True, help="YAML artifact to write")
    return parser


def main(argv: list[str] | None = None) -> int:
    options = _parser().parse_args(argv)
    try:
        document = build_delta(
            options.sessions_root,
            options.root_id,
            start=options.start,
            end=options.end,
        )
        rendered = yaml.safe_dump(document, sort_keys=False, allow_unicode=True, width=96)
        with atomic_output_file(options.out, make_parents=True) as temporary:
            temporary.write_text(rendered, encoding="utf-8")
    except (OSError, TypeError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    print(f"wrote {options.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
