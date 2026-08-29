#!/usr/bin/env python3
"""Build a prose-excluding efficiency rollup from one Claude Code JSONL session log.

The sibling of `codex_log_rollup.py`, and deliberately not a generalisation of it.
Codex and Claude Code record genuinely different things, and forcing one shape onto both
means either discarding what one of them knows or inventing fields the other cannot fill.
So this reader is faithful to Claude Code's transcript in its own terms, emits
`ClaudeEfficiencyRollup/v1`, and leaves the mapping into a unified shape to a later step.

**The rollup is the retained artifact, not a pointer to one.** The raw JSONL is large
(8.0 MB for one session here), harness-private, and full of prose this repository has no
reason to keep, so it will not always be archived. What survives has to answer the
questions the efficiency block asks without it.

What is kept: per-tool-call identity and elapsed time, per-turn token accounting, thinking
level, model, and the branch each turn ran against. What is dropped, deliberately and
stated here because a record whose losses are undocumented gets read as complete:
every prose body -- assistant text, thinking text, user messages, tool stdout and stderr,
file contents, and diffs. A Bash command is reduced to its leading executable word, which
is identity rather than content; nothing reconstructs the command line from this file.

Usage:
    uv run --frozen python -m devtools.claude_log_rollup LOG.jsonl
    uv run --frozen python -m devtools.claude_log_rollup LOG.jsonl --out DIR
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shlex
import statistics
import sys
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any

import yaml

ROLLUP_CONTRACT = "packing.squares:ClaudeEfficiencyRollup/v1"
SCHEMA_PATH = "../schemas/claude-efficiency-rollup.schema.yaml"
TOP_TOOLS = 25
TOP_COMMANDS = 30


def _instant(value: object) -> float | None:
    """Seconds since the epoch for one ISO-8601 timestamp, or None."""
    if not isinstance(value, str):
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).timestamp()
    except ValueError:
        return None


def _executable(command: object) -> str:
    """The leading executable word of a shell command.

    Identity, not content. `shlex` rather than a split on whitespace so that a quoted
    path does not become two tokens, and a command that will not lex is reported as such
    instead of guessed at.
    """
    if not isinstance(command, str) or not command.strip():
        return "(none)"
    try:
        tokens = shlex.split(command)
    except ValueError:
        return "(unlexable)"
    for token in tokens:
        if "=" in token and not token.startswith("/"):
            continue  # a leading VAR=value assignment
        return Path(token).name
    return "(none)"


def _summarise(seconds: list[float]) -> dict[str, Any]:
    """Count and distribution for one set of elapsed times."""
    if not seconds:
        return {"count": 0, "total_seconds": 0.0}
    return {
        "count": len(seconds),
        "total_seconds": round(sum(seconds), 3),
        "median_seconds": round(statistics.median(seconds), 3),
        "max_seconds": round(max(seconds), 3),
    }


def read_records(path: Path) -> list[dict[str, Any]]:
    """Every well-formed JSON record in the log, in file order.

    A truncated final line is a normal way for a live transcript to end, so it is skipped
    rather than treated as a corrupt file.
    """
    records = []
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        if not line.strip():
            continue
        try:
            records.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return records


def rollup(path: Path) -> dict[str, Any]:
    """One `ClaudeEfficiencyRollup/v1` payload for one session log."""
    raw = path.read_bytes()
    records = read_records(path)

    instants = [t for record in records if (t := _instant(record.get("timestamp")))]
    turns = [r for r in records if r.get("type") == "assistant"]

    models: Counter[str] = Counter()
    efforts: Counter[str] = Counter()
    branches: Counter[str] = Counter()
    tokens: Counter[str] = Counter()
    block_kinds: Counter[str] = Counter()
    sidechain_turns = 0

    # tool_use id -> (name, issued_at, command executable)
    issued: dict[str, tuple[str, float | None, str | None]] = {}
    for record in turns:
        message = record.get("message") or {}
        models[str(message.get("model"))] += 1
        efforts[str(record.get("effort"))] += 1
        branches[str(record.get("gitBranch"))] += 1
        sidechain_turns += bool(record.get("isSidechain"))

        usage = message.get("usage") or {}
        for field in (
            "input_tokens",
            "output_tokens",
            "cache_creation_input_tokens",
            "cache_read_input_tokens",
        ):
            if isinstance(usage.get(field), int):
                tokens[field] += usage[field]
        details = usage.get("output_tokens_details") or {}
        if isinstance(details.get("thinking_tokens"), int):
            tokens["thinking_tokens"] += details["thinking_tokens"]
        creation = usage.get("cache_creation") or {}
        for field in ("ephemeral_1h_input_tokens", "ephemeral_5m_input_tokens"):
            if isinstance(creation.get(field), int):
                tokens[field] += creation[field]

        at = _instant(record.get("timestamp"))
        for block in message.get("content") or []:
            if not isinstance(block, dict):
                continue
            kind = str(block.get("type"))
            block_kinds[kind] += 1
            if kind == "tool_use" and isinstance(block.get("id"), str):
                command = (block.get("input") or {}).get("command")
                issued[block["id"]] = (str(block.get("name")), at, _executable(command))

    elapsed_by_tool: dict[str, list[float]] = defaultdict(list)
    elapsed_by_executable: dict[str, list[float]] = defaultdict(list)
    unpaired = 0
    for record in records:
        if record.get("type") != "user":
            continue
        for block in (record.get("message") or {}).get("content") or []:
            if not isinstance(block, dict) or block.get("type") != "tool_result":
                continue
            key = block.get("tool_use_id")
            if not isinstance(key, str) or key not in issued:
                unpaired += 1
                continue
            name, at, executable = issued.pop(key)
            done = _instant(record.get("timestamp"))
            if at is None or done is None:
                continue
            seconds = done - at
            elapsed_by_tool[name].append(seconds)
            if executable and executable != "(none)":
                elapsed_by_executable[executable].append(seconds)

    tools = {
        name: _summarise(values)
        for name, values in sorted(elapsed_by_tool.items(), key=lambda item: -sum(item[1]))[
            :TOP_TOOLS
        ]
    }
    commands = {
        name: _summarise(values)
        for name, values in sorted(
            elapsed_by_executable.items(), key=lambda item: -sum(item[1])
        )[:TOP_COMMANDS]
    }
    tool_seconds = sum(sum(v) for v in elapsed_by_tool.values())
    span = (max(instants) - min(instants)) if instants else 0.0

    return {
        "softschema": {
            "contract": ROLLUP_CONTRACT,
            "schema": SCHEMA_PATH,
            "envelope": "rollup",
            "status": "enforced",
        },
        "rollup": {
            "source": {
                "harness": "claude-code",
                "filename": path.name,
                "sha256": hashlib.sha256(raw).hexdigest(),
                "bytes": len(raw),
                "records": len(records),
                "session_id": str(
                    next((r.get("sessionId") for r in records if r.get("sessionId")), "")
                ),
                "harness_versions": sorted(
                    {str(r["version"]) for r in records if r.get("version")}
                ),
            },
            "span": {
                "started_at": min(
                    (r["timestamp"] for r in records if _instant(r.get("timestamp"))),
                    default=None,
                ),
                "ended_at": max(
                    (r["timestamp"] for r in records if _instant(r.get("timestamp"))),
                    default=None,
                ),
                "wall_seconds": round(span, 3),
            },
            "turns": {
                "assistant": len(turns),
                "sidechain": sidechain_turns,
                "by_model": dict(models.most_common()),
                "by_thinking_level": dict(efforts.most_common()),
                "by_branch": dict(branches.most_common()),
                "content_blocks": dict(block_kinds.most_common()),
            },
            "tokens": dict(sorted(tokens.items())),
            "tool_calls": {
                "total": sum(len(v) for v in elapsed_by_tool.values()),
                "total_seconds": round(tool_seconds, 3),
                "share_of_wall": round(tool_seconds / span, 4) if span else None,
                "unpaired_results": unpaired,
                "outstanding_at_snapshot": len(issued),
                "by_tool": tools,
                "by_executable": commands,
            },
            "semantics": {
                "wall_seconds": (
                    "First to last timestamped record. It is elapsed session time and "
                    "includes every interval in which nothing was running, so it is an "
                    "upper bound on work and never a measure of it."
                ),
                "tool_call_seconds": (
                    "From the assistant record issuing a tool_use to the user record "
                    "carrying its tool_result. It therefore includes harness scheduling "
                    "and any permission wait, not only the tool's own execution."
                ),
                "model_seconds": (
                    "UNAVAILABLE for this harness. Claude Code's transcript records no "
                    "timed model-stream items and no first-token latency, so model time "
                    "cannot be separated from the interval before a turn's record is "
                    "written. It is absent rather than zero, and a consumer that sums it "
                    "with a harness that does report it must carry the gap forward."
                ),
                "share_of_wall": (
                    "tool_call_seconds over wall_seconds. Concurrent tool calls are "
                    "summed independently, so on a session that backgrounds work this "
                    "can exceed one and is a load figure, not an occupancy figure."
                ),
                "tokens": (
                    "As the harness reported them per turn, summed. Cache creation and "
                    "cache read are distinct from input tokens and are not double-counted "
                    "here, but no cost is derived from them: pricing is not this record's."
                ),
                "by_executable": (
                    "The leading executable word of a Bash command, which is identity "
                    "rather than content. Nothing reconstructs a command line from this "
                    "file."
                ),
                "unpaired_results": (
                    "tool_result blocks whose tool_use was not seen, which is normal for "
                    "a log that begins mid-session after a compaction. A large count "
                    "means the elapsed figures cover less than the session does."
                ),
                "excluded": (
                    "Every prose body: assistant text, thinking text, user messages, tool "
                    "stdout and stderr, file contents, and diffs. This record is not a "
                    "transcript and cannot be read as one."
                ),
            },
        },
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("log", type=Path, help="a Claude Code session JSONL file")
    parser.add_argument(
        "--out",
        type=Path,
        default=None,
        help="directory to write <session-id>.yaml into; default prints to stdout",
    )
    namespace = parser.parse_args(argv)
    if not namespace.log.is_file():
        print(f"  no such log: {namespace.log}", file=sys.stderr)
        return 1

    payload = rollup(namespace.log)
    text = yaml.safe_dump(payload, sort_keys=False, allow_unicode=True, width=88)
    if namespace.out is None:
        print(text)
        return 0

    namespace.out.mkdir(parents=True, exist_ok=True)
    session = payload["rollup"]["source"]["session_id"] or namespace.log.stem
    destination = namespace.out / f"{session}.yaml"
    destination.write_text(text, encoding="utf-8")
    source = payload["rollup"]["source"]
    calls = payload["rollup"]["tool_calls"]
    print(f"  wrote {destination}")
    print(
        f"  {source['records']} records, {payload['rollup']['turns']['assistant']} turns, "
        f"{calls['total']} tool calls, "
        f"{payload['rollup']['span']['wall_seconds'] / 3600:.2f} h wall"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
