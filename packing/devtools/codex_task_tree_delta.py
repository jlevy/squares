#!/usr/bin/env python3
"""Build a privacy-safe retained delta from two Codex task-tree snapshots."""

from __future__ import annotations

import argparse
import math
import sys
from collections.abc import Callable, Iterable, Mapping
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
MAX_VALIDATION_PROBLEMS = 64

_DOCUMENT_FIELDS = frozenset({"softschema", "rollup"})
_SOFTSCHEMA_FIELDS = frozenset({"contract", "schema", "envelope", "status"})
_ROLLUP_FIELDS = frozenset({"source", "completeness", "before", "after", "delta", "semantics"})
_SOURCE_FIELDS = frozenset(
    {
        "harness",
        "source_schema",
        "root_task_id",
        "start_cutoff_at",
        "end_cutoff_at",
        "before_snapshot_at",
        "after_snapshot_at",
    }
)
_COMPLETENESS_FIELDS = frozenset({"snapshot_incomplete", "live_session_count"})
_METRIC_FIELDS = frozenset(
    {*INTEGER_FIELDS, *NUMBER_FIELDS, "tool_seconds_by_category", "models"}
)
_MODEL_FIELDS = frozenset(
    {"model", "thinking_level", *MODEL_INTEGER_FIELDS, *MODEL_NUMBER_FIELDS, "tokens"}
)
_SEMANTIC_FIELDS = frozenset(
    {"attribution", "delta", "cutoff_boundary", "live_snapshot", "retention"}
)


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
    if (
        not isinstance(value, int | float)
        or isinstance(value, bool)
        or not math.isfinite(value)
        or value < 0
    ):
        raise ValueError(f"{field} is not a nonnegative number")
    return round(float(value), ROUND_DIGITS)


def _semantic_mapping(
    value: object, field: str, problem: Callable[[str], None]
) -> Mapping[object, object] | None:
    if not isinstance(value, Mapping):
        problem(f"{field} is not a mapping")
        return None
    return value


def _semantic_keys(
    value: Mapping[object, object],
    allowed: frozenset[str],
    field: str,
    problem: Callable[[str], None],
) -> None:
    if any(not isinstance(key, str) or key not in allowed for key in value):
        problem(f"{field} contains unexpected fields")


def _semantic_integer(value: object, field: str, problem: Callable[[str], None]) -> int | None:
    if not isinstance(value, int) or isinstance(value, bool) or value < 0:
        problem(f"{field} is not a nonnegative integer")
        return None
    return value


def _semantic_number(value: object, field: str, problem: Callable[[str], None]) -> float | None:
    if (
        not isinstance(value, int | float)
        or isinstance(value, bool)
        or not math.isfinite(value)
        or value < 0
    ):
        problem(f"{field} is not a finite nonnegative number")
        return None
    return round(float(value), ROUND_DIGITS)


def _semantic_instant(
    value: object, field: str, problem: Callable[[str], None]
) -> datetime | None:
    if not isinstance(value, str):
        problem(f"{field} is not an offset-aware timestamp")
        return None
    try:
        instant = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except OverflowError, ValueError:
        problem(f"{field} is not an offset-aware timestamp")
        return None
    if instant.tzinfo is None:
        problem(f"{field} is not an offset-aware timestamp")
        return None
    return instant


def _semantic_models(
    value: object, field: str, problem: Callable[[str], None]
) -> dict[tuple[str, str], dict[str, Any]] | None:
    if not isinstance(value, list):
        problem(f"{field} is not a list")
        return None
    indexed: dict[tuple[str, str], dict[str, Any]] = {}
    for index, raw in enumerate(value):
        row_field = f"{field}[{index}]"
        row = _semantic_mapping(raw, row_field, problem)
        if row is None:
            continue
        _semantic_keys(row, _MODEL_FIELDS, row_field, problem)
        model = row.get("model")
        thinking = row.get("thinking_level")
        if not isinstance(model, str) or not model:
            problem(f"{row_field}.model is not a nonempty string")
        if not isinstance(thinking, str) or not thinking:
            problem(f"{row_field}.thinking_level is not a nonempty string")

        scalars: dict[str, int | float] = {}
        valid = (
            isinstance(model, str)
            and bool(model)
            and isinstance(thinking, str)
            and bool(thinking)
        )
        for name in MODEL_INTEGER_FIELDS:
            parsed = _semantic_integer(row.get(name), f"{row_field}.{name}", problem)
            valid = valid and parsed is not None
            if parsed is not None:
                scalars[name] = parsed
        for name in MODEL_NUMBER_FIELDS:
            parsed = _semantic_number(row.get(name), f"{row_field}.{name}", problem)
            valid = valid and parsed is not None
            if parsed is not None:
                scalars[name] = parsed

        tokens: dict[str, int] = {}
        raw_tokens = _semantic_mapping(row.get("tokens"), f"{row_field}.tokens", problem)
        if raw_tokens is None:
            valid = False
        else:
            _semantic_keys(raw_tokens, frozenset(TOKEN_FIELDS), f"{row_field}.tokens", problem)
            for name in TOKEN_FIELDS:
                parsed = _semantic_integer(
                    raw_tokens.get(name), f"{row_field}.tokens.{name}", problem
                )
                valid = valid and parsed is not None
                if parsed is not None:
                    tokens[name] = parsed

        if not valid:
            continue
        assert isinstance(model, str)
        assert isinstance(thinking, str)
        identity = (model, thinking)
        if identity in indexed:
            problem(f"{field} contains a duplicate model identity")
            continue
        indexed[identity] = {"index": index, "scalars": scalars, "tokens": tokens}
    return indexed


def _semantic_metrics(
    value: object, field: str, problem: Callable[[str], None]
) -> dict[str, Any] | None:
    metrics = _semantic_mapping(value, field, problem)
    if metrics is None:
        return None
    _semantic_keys(metrics, _METRIC_FIELDS, field, problem)

    scalars: dict[str, int | float] = {}
    for name in INTEGER_FIELDS:
        parsed = _semantic_integer(metrics.get(name), f"{field}.{name}", problem)
        if parsed is not None:
            scalars[name] = parsed
    for name in NUMBER_FIELDS:
        parsed = _semantic_number(metrics.get(name), f"{field}.{name}", problem)
        if parsed is not None:
            scalars[name] = parsed

    tools: dict[str, float] | None = None
    raw_tools = _semantic_mapping(
        metrics.get("tool_seconds_by_category"), f"{field}.tool_seconds_by_category", problem
    )
    if raw_tools is not None:
        _semantic_keys(raw_tools, TOOL_CATEGORIES, f"{field}.tool_seconds_by_category", problem)
        tools = {}
        for category in TOOL_CATEGORIES:
            if category not in raw_tools:
                continue
            parsed = _semantic_number(
                raw_tools.get(category),
                f"{field}.tool_seconds_by_category.{category}",
                problem,
            )
            if parsed is not None:
                tools[category] = parsed

    models = _semantic_models(metrics.get("models"), f"{field}.models", problem)
    return {"scalars": scalars, "tools": tools, "models": models}


def _semantic_difference(after: int | float, before: int | float) -> int | float | None:
    if after < before:
        return None
    value = after - before
    return value if isinstance(after, int) and isinstance(before, int) else round(value, 3)


def _compare_metric_delta(
    before: Mapping[str, Any],
    after: Mapping[str, Any],
    delta: Mapping[str, Any],
    problem: Callable[[str], None],
) -> None:
    before_scalars = before["scalars"]
    after_scalars = after["scalars"]
    delta_scalars = delta["scalars"]
    for name in (*INTEGER_FIELDS, *NUMBER_FIELDS):
        if name not in before_scalars or name not in after_scalars or name not in delta_scalars:
            continue
        expected = _semantic_difference(after_scalars[name], before_scalars[name])
        if expected is None:
            problem(f"{name} is non-monotone between before and after")
        elif delta_scalars[name] != expected:
            problem(f"delta.{name} does not equal after minus before")

    before_tools = before["tools"]
    after_tools = after["tools"]
    delta_tools = delta["tools"]
    if before_tools is not None and after_tools is not None and delta_tools is not None:
        expected_categories = set(before_tools) | set(after_tools)
        if set(delta_tools) != expected_categories:
            problem("delta.tool_seconds_by_category keys do not match before and after")
        for category in sorted(expected_categories & set(delta_tools)):
            expected = _semantic_difference(
                after_tools.get(category, 0.0), before_tools.get(category, 0.0)
            )
            if expected is None:
                problem(f"tool_seconds_by_category.{category} is non-monotone")
            elif delta_tools[category] != expected:
                problem(
                    f"delta.tool_seconds_by_category.{category} does not equal "
                    "after minus before"
                )

    before_models = before["models"]
    after_models = after["models"]
    delta_models = delta["models"]
    if before_models is None or after_models is None or delta_models is None:
        return
    expected_identities = set(before_models) | set(after_models)
    if set(delta_models) != expected_identities:
        problem("delta.models identities do not match before and after")
    zero_scalars: dict[str, int | float] = {
        **dict.fromkeys(MODEL_INTEGER_FIELDS, 0),
        **dict.fromkeys(MODEL_NUMBER_FIELDS, 0.0),
    }
    zero_tokens = dict.fromkeys(TOKEN_FIELDS, 0)
    for identity in sorted(expected_identities & set(delta_models)):
        first = before_models.get(identity)
        last = after_models.get(identity)
        observed = delta_models[identity]
        first_scalars = first["scalars"] if first is not None else zero_scalars
        last_scalars = last["scalars"] if last is not None else zero_scalars
        index = observed["index"]
        for name in (*MODEL_INTEGER_FIELDS, *MODEL_NUMBER_FIELDS):
            if (
                name not in first_scalars
                or name not in last_scalars
                or name not in observed["scalars"]
            ):
                continue
            expected = _semantic_difference(last_scalars[name], first_scalars[name])
            if expected is None:
                problem(f"models[{index}].{name} is non-monotone")
            elif observed["scalars"][name] != expected:
                problem(f"delta.models[{index}].{name} does not equal after minus before")
        first_tokens = first["tokens"] if first is not None else zero_tokens
        last_tokens = last["tokens"] if last is not None else zero_tokens
        for name in TOKEN_FIELDS:
            if (
                name not in first_tokens
                or name not in last_tokens
                or name not in observed["tokens"]
            ):
                continue
            expected = _semantic_difference(last_tokens[name], first_tokens[name])
            if expected is None:
                problem(f"models[{index}].tokens.{name} is non-monotone")
            elif observed["tokens"][name] != expected:
                problem(
                    f"delta.models[{index}].tokens.{name} does not equal after minus before"
                )


def validate_delta_document(document: object) -> list[str]:
    """Return bounded, privacy-safe semantic problems in one retained delta document."""

    problems: list[str] = []
    truncated = False

    def problem(message: str) -> None:
        nonlocal truncated
        if len(problems) < MAX_VALIDATION_PROBLEMS:
            problems.append(message)
        else:
            truncated = True

    root = _semantic_mapping(document, "document", problem)
    if root is None:
        return problems
    _semantic_keys(root, _DOCUMENT_FIELDS, "document", problem)
    meta = _semantic_mapping(root.get("softschema"), "softschema", problem)
    if meta is not None:
        _semantic_keys(meta, _SOFTSCHEMA_FIELDS, "softschema", problem)
        if meta.get("contract") != CONTRACT:
            problem("softschema.contract is not the Codex delta contract")
        if meta.get("envelope") != "rollup":
            problem("softschema.envelope is not rollup")
        if meta.get("status") != "enforced":
            problem("softschema.status is not enforced")
        if not isinstance(meta.get("schema"), str) or not meta.get("schema"):
            problem("softschema.schema is not a nonempty string")

    rollup = _semantic_mapping(root.get("rollup"), "rollup", problem)
    if rollup is None:
        return problems
    _semantic_keys(rollup, _ROLLUP_FIELDS, "rollup", problem)

    source = _semantic_mapping(rollup.get("source"), "source", problem)
    if source is not None:
        _semantic_keys(source, _SOURCE_FIELDS, "source", problem)
        if source.get("harness") != "codex":
            problem("source.harness is not codex")
        if source.get("source_schema") != ROLLUP_SCHEMA:
            problem("source.source_schema is not the expected scanner contract")
        if not isinstance(source.get("root_task_id"), str) or not source.get("root_task_id"):
            problem("source.root_task_id is not a nonempty string")
        start = _semantic_instant(
            source.get("start_cutoff_at"), "source.start_cutoff_at", problem
        )
        end = _semantic_instant(source.get("end_cutoff_at"), "source.end_cutoff_at", problem)
        if start is not None and end is not None and end <= start:
            problem("end cutoff must be later than start cutoff")
        for name in ("before_snapshot_at", "after_snapshot_at"):
            if name not in source:
                problem(f"source.{name} is missing")
            elif source.get(name) is not None:
                _semantic_instant(source.get(name), f"source.{name}", problem)

    completeness = _semantic_mapping(rollup.get("completeness"), "completeness", problem)
    if completeness is not None:
        _semantic_keys(completeness, _COMPLETENESS_FIELDS, "completeness", problem)
        incomplete = completeness.get("snapshot_incomplete")
        if not isinstance(incomplete, bool):
            problem("completeness.snapshot_incomplete is not a boolean")
        live_count = _semantic_integer(
            completeness.get("live_session_count"),
            "completeness.live_session_count",
            problem,
        )
        if (
            isinstance(incomplete, bool)
            and live_count is not None
            and incomplete != (live_count > 0)
        ):
            problem("completeness fields disagree")

    before = _semantic_metrics(rollup.get("before"), "before", problem)
    after = _semantic_metrics(rollup.get("after"), "after", problem)
    delta = _semantic_metrics(rollup.get("delta"), "delta", problem)
    if before is not None and after is not None and delta is not None:
        _compare_metric_delta(before, after, delta, problem)

    semantics = _semantic_mapping(rollup.get("semantics"), "semantics", problem)
    if semantics is not None:
        _semantic_keys(semantics, _SEMANTIC_FIELDS, "semantics", problem)
        for name in _SEMANTIC_FIELDS:
            if not isinstance(semantics.get(name), str) or not semantics.get(name):
                problem(f"semantics.{name} is not a nonempty string")

    if truncated:
        problems.append("additional semantic problems omitted")
    return problems


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
    before_rollup = build_rollup(
        sessions_root,
        [root_task_id],
        through=start,
        retrospective_cutoff=True,
    )
    after_rollup = build_rollup(
        sessions_root,
        [root_task_id],
        through=end,
        retrospective_cutoff=True,
    )
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
                    "Task, tool, compaction, and model-stream timings are clipped at both "
                    "cutoffs. Token counts and client-reported first-token waits are emitted "
                    "on completion and can be charged wholly to the interval containing that "
                    "completion."
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
