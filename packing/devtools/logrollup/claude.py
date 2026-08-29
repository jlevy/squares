"""The Claude Code reader.

Faithful to what Claude Code's transcript actually records, in its own terms. The shared
skeleton is `devtools.logrollup.model`; everything here is the half that is specific to
this harness.

The shell shapes exist to make `OR-1` checkable. "Never leave a measurement in one-off
code" is a rule about heredocs and `python -c`, and a rule nobody counts is a rule nobody
keeps.
"""

from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path
from typing import Any

from devtools.logrollup.model import (
    Elapsed,
    SessionRollup,
    SourceLog,
    Span,
    ToolCall,
    Turn,
    instant,
)
from devtools.logrollup.shell import Invocation, invocations, primary

CONTRACT = "packing.squares:ClaudeEfficiencyRollup/v1"
SCHEMA = "../schemas/claude-efficiency-rollup.schema.yaml"
TOP_TOOLS = 25
TOP_COMMANDS = 30

HEREDOC = re.compile(r"<<-?\s*['\"]?\w+['\"]?")
PYTHON = re.compile(r"\bpython3?\b")
PYTHON_INLINE = re.compile(r"\bpython3?\b[^|;&]*\s-c\b")
SEQUENCING = re.compile(r"&&|\|\||;")
PIPE = re.compile(r"(?<!\|)\|(?!\|)")
REDIRECT = re.compile(r"(?<![<>0-9])>{1,2}(?!&)")
SUBSHELL = re.compile(r"\$\(")
BACKGROUNDED = re.compile(r"&\s*$")


class Shape(StrEnum):
    """The structural shape of a shell command.

    Values are lower_snake_case because they are literal keys in a stored record, and a
    reader of that record should see the same token the code uses.
    """

    python_heredoc = "python_heredoc"
    python_inline = "python_inline"
    heredoc = "heredoc"
    compound = "compound"
    pipeline = "pipeline"
    simple = "simple"
    empty = "empty"

    @classmethod
    def of(cls, command: object) -> Shape:
        """Classify one command against `PRIORITY`, first match winning."""
        if not isinstance(command, str) or not command.strip():
            return cls.empty
        return next(
            (shape for shape, matches in PRIORITY if matches(command)),
            cls.simple,
        )

    @property
    def is_one_off_code(self) -> bool:
        """Whether this shape is what `OR-1` calls a measurement left in one-off code."""
        return self in {Shape.python_heredoc, Shape.python_inline}


# Priority order, and the order is what makes the classification useful rather than
# merely descriptive: a Python heredoc that also pipes is a Python heredoc, because that
# is the fact `OR-1` is about and the piping is incidental. As data rather than a chain
# of returns so the precedence is readable in one place.
PRIORITY: tuple[tuple[Shape, Callable[[str], bool]], ...] = (
    (Shape.python_heredoc, lambda c: bool(HEREDOC.search(c)) and bool(PYTHON.search(c))),
    (Shape.python_inline, lambda c: bool(PYTHON_INLINE.search(c))),
    (Shape.heredoc, lambda c: bool(HEREDOC.search(c))),
    (Shape.compound, lambda c: bool(SEQUENCING.search(c))),
    (Shape.pipeline, lambda c: bool(PIPE.search(c))),
)


TRAITS = (
    ("redirects_output", REDIRECT),
    ("pipes", PIPE),
    ("substitutes", SUBSHELL),
    ("backgrounded", BACKGROUNDED),
)


def traits_of(command: object) -> tuple[str, ...]:
    """Non-exclusive structural features, counted alongside the shape."""
    if not isinstance(command, str):
        return ()
    return tuple(name for name, pattern in TRAITS if pattern.search(command))


def token_counts(usage: Mapping[str, Any]) -> dict[str, int]:
    """The token counters one turn reports, flattened to one level."""
    counted = {
        field: usage[field]
        for field in (
            "input_tokens",
            "output_tokens",
            "cache_creation_input_tokens",
            "cache_read_input_tokens",
        )
        if isinstance(usage.get(field), int)
    }
    details = usage.get("output_tokens_details") or {}
    if isinstance(details.get("thinking_tokens"), int):
        counted["thinking_tokens"] = details["thinking_tokens"]
    creation = usage.get("cache_creation") or {}
    for field in ("ephemeral_1h_input_tokens", "ephemeral_5m_input_tokens"):
        if isinstance(creation.get(field), int):
            counted[field] = creation[field]
    return counted


def read_records(path: Path) -> list[dict[str, Any]]:
    """Every well-formed JSON record in the log, in file order.

    A truncated final line is how a live transcript normally ends, so it is skipped
    rather than treated as a corrupt file.
    """
    records: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        if not line.strip():
            continue
        try:
            parsed = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(parsed, dict):
            records.append(parsed)
    return records


@dataclass(frozen=True, slots=True)
class Session:
    """One parsed transcript, before it is reduced to a record."""

    records: tuple[dict[str, Any], ...]
    turns: tuple[Turn, ...]
    calls: tuple[ToolCall, ...]
    invoked: Mapping[str, int]
    """Every tool invoked, counted across all segments of every command.

    Counts and not elapsed, on purpose. Most commands here run several tools and the
    transcript times the call rather than the pipeline, so how often a CLI was reached
    for is knowable and its share of the clock is not.
    """

    invoked_families: Mapping[str, int]
    traits: Mapping[str, int]
    errors: int
    denials: int
    unpaired: int
    outstanding: int


@dataclass(frozen=True, slots=True)
class _Issued:
    """A tool call in flight, awaiting its result."""

    tool: str
    at: float | None
    thinking_level: str
    command: Invocation | None
    shape: Shape | None


def parse(records: Sequence[dict[str, Any]]) -> Session:
    """Turns and completed tool calls, paired by `tool_use_id`."""
    by_uuid = {r["uuid"]: r for r in records if isinstance(r.get("uuid"), str)}
    turns: list[Turn] = []
    issued: dict[str, _Issued] = {}
    traits: Counter[str] = Counter()
    invoked: Counter[str] = Counter()
    invoked_families: Counter[str] = Counter()

    for record in records:
        if record.get("type") != "assistant":
            continue
        message = record.get("message") or {}
        level = str(record.get("effort"))
        at = instant(record.get("timestamp"))
        parent = by_uuid.get(str(record.get("parentUuid")))
        started = instant(parent.get("timestamp")) if parent else None
        turns.append(
            Turn(
                model=str(message.get("model")),
                thinking_level=level,
                branch=str(record.get("gitBranch")),
                sidechain=bool(record.get("isSidechain")),
                tokens=token_counts(message.get("usage") or {}),
                latency_seconds=(
                    at - started
                    if at is not None and started is not None and at >= started
                    else None
                ),
            )
        )
        for block in message.get("content") or []:
            if not isinstance(block, dict) or block.get("type") != "tool_use":
                continue
            command = (block.get("input") or {}).get("command")
            traits.update(traits_of(command))
            for call in invocations(command):
                invoked[call.name] += 1
                invoked_families[str(call.family)] += 1
            if isinstance(block.get("id"), str):
                issued[block["id"]] = _Issued(
                    tool=str(block.get("name")),
                    at=at,
                    thinking_level=level,
                    command=primary(command),
                    shape=Shape.of(command) if command is not None else None,
                )

    calls: list[ToolCall] = []
    errors = unpaired = denials = 0
    for record in records:
        if record.get("type") != "user":
            continue
        denials += bool(record.get("toolDenialKind"))
        for block in (record.get("message") or {}).get("content") or []:
            if not isinstance(block, dict) or block.get("type") != "tool_result":
                continue
            errors += bool(block.get("is_error"))
            key = block.get("tool_use_id")
            if not isinstance(key, str) or key not in issued:
                unpaired += 1
                continue
            pending = issued.pop(key)
            done = instant(record.get("timestamp"))
            if pending.at is None or done is None:
                continue
            calls.append(
                ToolCall(
                    tool=pending.tool,
                    seconds=done - pending.at,
                    thinking_level=pending.thinking_level,
                    command=pending.command.name if pending.command else None,
                    family=str(pending.command.family) if pending.command else None,
                    shape=str(pending.shape) if pending.shape else None,
                )
            )

    return Session(
        records=tuple(records),
        turns=tuple(turns),
        calls=tuple(calls),
        invoked=dict(invoked.most_common()),
        invoked_families=dict(invoked_families.most_common()),
        traits=dict(traits.most_common()),
        errors=errors,
        denials=denials,
        unpaired=unpaired,
        outstanding=len(issued),
    )


def _ranked(
    calls: Sequence[ToolCall],
    key: Any,
    limit: int | None = None,
) -> dict[str, Any]:
    """Elapsed summaries per group, heaviest first."""
    grouped: dict[str, list[float]] = defaultdict(list)
    for call in calls:
        name = key(call)
        if name is not None:
            grouped[name].append(call.seconds)
    ordered = sorted(grouped.items(), key=lambda item: -sum(item[1]))
    return {name: Elapsed.of(values).payload() for name, values in ordered[:limit]}


SEMANTICS: Mapping[str, str] = {
    "wall_seconds": (
        "First to last timestamped record. It is elapsed session time and includes every "
        "interval in which nothing was running, so it is an upper bound on work and never "
        "a measure of it."
    ),
    "tool_call_seconds": (
        "From the assistant record issuing a tool_use to the user record carrying its "
        "tool_result. It therefore includes harness scheduling and any permission wait, "
        "not only the tool's own execution."
    ),
    "model_seconds": (
        "UNAVAILABLE for this harness. Claude Code's transcript records no timed "
        "model-stream items and no first-token latency, so model time cannot be separated "
        "from the interval before a turn's record is written. It is absent rather than "
        "zero, and a consumer that sums it with a harness that does report it must carry "
        "the gap forward."
    ),
    "turns.latency": (
        "From a turn's parent record to the turn itself. It is the closest thing here to "
        "model time and is NOT model time: it also carries queueing, the user's own "
        "thinking time before a reply, and any wait for a permission prompt. Read the "
        "median, not the maximum."
    ),
    "share_of_wall": (
        "tool_call_seconds over wall_seconds. Concurrent calls are summed independently, "
        "so on a session that backgrounds work this can exceed one and is a load figure, "
        "not an occupancy figure."
    ),
    "tokens": (
        "As the harness reported them per turn, summed. Cache creation and cache read are "
        "distinct from input tokens and are not double-counted here, but no cost is "
        "derived: pricing is not this record's and a stored price goes stale silently."
    ),
    "tokens_by_thinking_level": (
        "The same counters split by the effort the harness recorded for each turn. This is "
        "what makes OR-2's 'matched to the task' claim answerable rather than asserted."
    ),
    "by_shell_shape": (
        "Structural classification of shell commands in a fixed priority order, so a "
        "Python heredoc that also pipes counts as a Python heredoc. `python_heredoc` and "
        "`python_inline` are the shapes OR-1 calls one-off code; a session with many of "
        "them was writing scripts where it should have been building a tool."
    ),
    "by_command": (
        "The tool a shell command actually runs, named as it was invoked: the runner "
        "prefix is kept because `uv run foo.py` is not `foo.py`, a Python call is named "
        "by its module or script, and a subcommanded tool keeps its subcommand. Peeling "
        "matters more than it sounds: keyed on the leading word instead, `cd` led 524 of "
        "882 commands in this session and the figure said nothing. A command no single "
        "tool owns is `(pipeline)` rather than attributed to whichever ran first."
    ),
    "invoked": (
        "Every tool reached for, counted across all segments of every command, not just "
        "the one a call's time was attributed to. Counts and never elapsed: most commands "
        "here run several tools and the transcript times the call rather than the "
        "pipeline, so how often a CLI was used is knowable and its share of the clock is "
        "not. This is the table that answers which instruments a session actually uses; "
        "`by_command` answers where its measured time went."
    ),
    "by_command_family": (
        "Our own instruments against everything else. `project` is this repository's "
        "CLIs and modules, `toolchain` the language tooling, `inspection` the reading "
        "and searching a session does to orient itself. Time in `packing-validate` and "
        "time in `grep` are both real and are not the same kind of cost."
    ),
    "errors": (
        "tool_result blocks the harness marked is_error. A failed call still spends its "
        "elapsed time, and the count is here so a rising failure rate is visible rather "
        "than hidden inside the total."
    ),
    "unpaired_results": (
        "tool_result blocks whose tool_use was not seen, which is normal for a log that "
        "begins mid-session after a compaction. A large count means the elapsed figures "
        "cover less than the session does."
    ),
    "session_events.queue_operations": (
        "Messages queued and withdrawn while a turn was running. An enqueue is an "
        "interjection, which is a signal about the session's pacing rather than about any "
        "tool."
    ),
    "excluded": (
        "Every prose body: assistant text, thinking text, user messages, tool stdout and "
        "stderr, file contents, and diffs. This record is not a transcript and cannot be "
        "read as one."
    ),
}


@dataclass(frozen=True, slots=True)
class ClaudeCodeReader:
    """Reads Claude Code JSONL transcripts."""

    harness: str = "claude-code"

    def detects(self, path: Path) -> bool:
        """A Claude Code transcript carries `sessionId` and `uuid` on its records.

        Read by content rather than by filename: a transcript that has been copied or
        renamed is still a Claude Code transcript.
        """
        for line in path.read_text(encoding="utf-8", errors="replace").splitlines()[:40]:
            if not line.strip():
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                continue
            if isinstance(record, dict) and "sessionId" in record and "uuid" in record:
                return True
        return False

    def read(self, path: Path) -> SessionRollup:
        records = read_records(path)
        session = parse(records)
        span = Span.of(records)
        calls = session.calls
        tool_seconds = sum(call.seconds for call in calls)

        tokens: Counter[str] = Counter()
        by_level: dict[str, Counter[str]] = defaultdict(Counter)
        for turn in session.turns:
            tokens.update(turn.tokens)
            by_level[turn.thinking_level].update(turn.tokens)

        latencies = [t.latency_seconds for t in session.turns if t.latency_seconds is not None]
        system = [r for r in records if r.get("type") == "system"]
        one_off = [c for c in calls if c.shape and Shape(c.shape).is_one_off_code]

        extra: dict[str, Any] = {
            "turns": {
                "assistant": len(session.turns),
                "sidechain": sum(t.sidechain for t in session.turns),
                "by_model": dict(Counter(t.model for t in session.turns).most_common()),
                "by_thinking_level": dict(
                    Counter(t.thinking_level for t in session.turns).most_common()
                ),
                "by_model_and_thinking_level": dict(
                    Counter(
                        f"{t.model} @ {t.thinking_level}" for t in session.turns
                    ).most_common()
                ),
                "by_branch": dict(Counter(t.branch for t in session.turns).most_common()),
                "latency": Elapsed.of(latencies).payload(),
            },
            "tokens": dict(sorted(tokens.items())),
            "tokens_by_thinking_level": {
                level: dict(sorted(counter.items()))
                for level, counter in sorted(by_level.items())
            },
            "tool_calls": {
                "total": len(calls),
                "total_seconds": round(tool_seconds, 3),
                "share_of_wall": (
                    round(tool_seconds / span.wall_seconds, 4) if span.wall_seconds else None
                ),
                "errors": session.errors,
                "denied": session.denials,
                "unpaired_results": session.unpaired,
                "outstanding_at_snapshot": session.outstanding,
                "one_off_code": Elapsed.of([c.seconds for c in one_off]).payload(),
                "by_tool": _ranked(calls, lambda c: c.tool, TOP_TOOLS),
                "by_command": _ranked(calls, lambda c: c.command, TOP_COMMANDS),
                "by_command_family": _ranked(calls, lambda c: c.family),
                "invoked": dict(list(session.invoked.items())[:TOP_COMMANDS]),
                "invoked_families": dict(session.invoked_families),
                "by_shell_shape": _ranked(calls, lambda c: c.shape),
                "by_thinking_level": _ranked(calls, lambda c: c.thinking_level),
                "shell_traits": dict(session.traits),
            },
            "session_events": {
                "compact_boundaries": sum(
                    r.get("subtype") == "compact_boundary" for r in system
                ),
                "stop_hook_summaries": sum(
                    r.get("subtype") == "stop_hook_summary" for r in system
                ),
                "queue_operations": dict(
                    Counter(
                        str(r.get("operation"))
                        for r in records
                        if r.get("type") == "queue-operation"
                    ).most_common()
                ),
            },
        }

        return SessionRollup(
            contract=CONTRACT,
            schema=SCHEMA,
            source=SourceLog.of(path, harness=self.harness, records=records),
            span=span,
            semantics=SEMANTICS,
            extra=extra,
        )
