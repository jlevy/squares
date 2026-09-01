#!/usr/bin/env python3
"""Render the cost of the work behind a pull request, for the pull request itself.

A reviewer looking at a branch can see what changed and cannot see what it took. Two
harness-specific receipts can supply that view without pretending their telemetry is the
same: Claude records Git branches in each log, while Codex can produce a privacy-reduced
task-tree delta over the interval an AgentSession explicitly declares.

**The attribution is a bound, not a figure, and saying so is the point.** `turns.by_branch`
is the only branch-aware field in the record: tokens and tool calls are counted per log,
not per branch. So a log whose turns are entirely on this branch contributes exactly, and
a log that straddles branches contributes somewhere between nothing and all of itself.
Reporting the first as the answer would understate by whatever the straddling logs did
here; reporting the sum would charge this branch for work done elsewhere. Both are printed,
and the honest total is the interval between them.

Usage, from `packing/`:
    uv run --frozen --all-extras --group dev python -m devtools.render_pr_rollup \
        --branch claude/my-branch

For Codex, also pass the declaring session. The renderer will not infer attribution from
the task tree because Codex exposes no Git-branch field:
    uv run --frozen --all-extras --group dev python -m devtools.render_pr_rollup \
        --branch codex/my-branch --session session-062
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

from sqpack.yamlio import safe_load

ROOT = Path(__file__).resolve().parent.parent
USAGE = ROOT / "campaign" / "resource-usage"
SESSIONS = ROOT / "campaign" / "agent-sessions"
CLAUDE_CONTRACT = "packing.squares:ClaudeEfficiencyRollup/v1"
CODEX_CONTRACT = "packing.squares:CodexTaskTreeDelta/v1"


def current_branch() -> str:
    result = subprocess.run(
        ["git", "rev-parse", "--abbrev-ref", "HEAD"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout.strip()


def resource_documents() -> list[tuple[str | None, dict, Path]]:
    """Load retained resource receipts without pretending their shapes are unified."""
    found = []
    for path in sorted(USAGE.glob("*.yaml")):
        document = safe_load(path.read_text(encoding="utf-8"))
        if not isinstance(document, dict):
            continue
        meta = document.get("softschema") or {}
        rollup = document.get("rollup") or document
        if not isinstance(rollup, dict):
            continue
        found.append((meta.get("contract"), rollup, path))
    return found


def rollups() -> list[dict]:
    """Claude records retain harness-observed branch attribution."""
    found = []
    for contract, rollup, path in resource_documents():
        if contract != CLAUDE_CONTRACT:
            continue
        rollup["_name"] = path.name
        found.append(rollup)
    return found


def session_payload(session_id: str) -> dict | None:
    matches = sorted(SESSIONS.glob(f"{session_id}-*.md"))
    if len(matches) != 1:
        return None
    text = matches[0].read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return None
    document = safe_load(text.split("---\n")[1])
    payload = document.get("session") if isinstance(document, dict) else None
    return payload if isinstance(payload, dict) else None


def codex_receipts(session_id: str | None) -> list[dict]:
    """Codex intervals are eligible only through an explicit AgentSession declaration."""
    if session_id is None or (payload := session_payload(session_id)) is None:
        return []
    declared = {Path(str(ref)).name for ref in payload.get("resource_rollups") or []}
    return [
        rollup
        for contract, rollup, path in resource_documents()
        if contract == CODEX_CONTRACT and path.name in declared
    ]


def thousands(value: float) -> str:
    return f"{value:,.0f}"


def hours(seconds: float) -> str:
    return f"{seconds / 3600:,.1f} h"


def duration(seconds: float) -> str:
    """A unit that shows the number. Twenty tools round to `0 m` and none of them took none."""
    if seconds >= 3600:
        return f"{seconds / 3600:,.1f} h"
    if seconds >= 60:
        return f"{seconds / 60:,.0f} m"
    return f"{seconds:,.1f} s"


def tokens_of(rollup: dict) -> dict[str, int]:
    return {k: int(v) for k, v in (rollup.get("tokens") or {}).items()}


def add(into: Counter, values: dict) -> None:
    """Sum the integer fields of an untyped mapping, skipping anything that is not one."""
    for key, value in values.items():
        if isinstance(value, int) and not isinstance(value, bool):
            into[key] += value


def section_headline(exact: list[dict], mixed: list[dict], branch: str) -> list[str]:
    """Floor, estimate, ceiling -- in that order, because only the first two are honest.

    A log that straddles branches has a branch-aware turn count and nothing else, so its
    tokens and calls can be excluded (understating by whatever it did here), charged in full
    (overstating by whatever it did elsewhere), or prorated by its turn share. The third is
    an estimate and is labelled as one; it is the only column a reader should quote, and the
    other two are what make it checkable.
    """
    # Weighted sums are floats by construction -- a turn share is not an integer -- so
    # these are float accumulators rather than Counters, which type as int-valued.
    floor: dict[str, float] = defaultdict(float)
    share_of: dict[str, float] = defaultdict(float)
    ceiling: dict[str, float] = defaultdict(float)

    def fold(into: dict[str, float], record: dict, weight: float) -> None:
        calls = record.get("tool_calls") or {}
        into["turns"] += (record["turns"].get("by_branch") or {}).get(branch, 0)
        into["calls"] += (calls.get("total") or 0) * weight
        into["wall"] += ((record.get("span") or {}).get("wall_seconds") or 0) * weight
        tokens = tokens_of(record)
        into["generated"] += (
            tokens.get("output_tokens", 0) + tokens.get("thinking_tokens", 0)
        ) * weight
        into["cache_read"] += tokens.get("cache_read_input_tokens", 0) * weight

    for record in exact:
        for target in (floor, share_of, ceiling):
            fold(target, record, 1.0)
    for record in mixed:
        turns = record["turns"]
        weight = (turns.get("by_branch") or {}).get(branch, 0) / max(turns["assistant"], 1)
        fold(floor, record, 0.0)
        fold(share_of, record, weight)
        fold(ceiling, record, 1.0)

    rows = (
        ("agent turns", "turns", thousands),
        ("tool calls", "calls", thousands),
        ("generated tokens", "generated", thousands),
        ("cache reads", "cache_read", thousands),
        ("wall time", "wall", hours),
    )
    lines = [
        "| | on-branch logs only | **by turn share** | every log that touched it |",
        "| --- | ---: | ---: | ---: |",
    ]
    for label, key, fmt in rows:
        middle = fmt(share_of[key])
        lines.append(f"| {label} | {fmt(floor[key])} | **{middle}** | {fmt(ceiling[key])} |")
    lines += [
        "",
        (
            f"**Turn counts are exact; everything else is bounded.** {len(exact)} logs sit "
            f"entirely on `{branch}` and contribute exactly. {len(mixed)} straddle branches, "
            "and `ClaudeEfficiencyRollup` counts tokens and tool calls per log rather than "
            "per branch — so the first column drops them, the last charges this branch for "
            "all of their work including what happened elsewhere, and the middle prorates "
            "them by the share of their turns spent here. **The middle is an estimate**, "
            "the outer two are measurements, and the record cannot do better than this "
            "without a branch-aware token count."
        ),
    ]
    return lines


def section_models(records: list[dict]) -> list[str]:
    turns: Counter = Counter()
    for record in records:
        add(turns, record["turns"].get("by_model_and_thinking_level") or {})

    by_level: Counter = Counter()
    levels: dict[str, Counter] = {}
    for record in records:
        for level, values in (record.get("tokens_by_thinking_level") or {}).items():
            bucket = levels.setdefault(level, Counter())
            add(bucket, {k: v for k, v in values.items() if isinstance(v, int | float)})
        add(by_level, record["turns"].get("by_thinking_level") or {})

    lines = [
        "| model @ thinking | turns | output | thinking | cache read |",
        "| --- | ---: | ---: | ---: | ---: |",
    ]
    for name, count in sorted(turns.items(), key=lambda pair: -pair[1]):
        level = name.split(" @ ")[-1]
        bucket = levels.get(level, Counter())
        share = count / by_level[level] if by_level[level] else 0.0
        lines.append(
            f"| `{name}` | {thousands(count)} "
            f"| {thousands(bucket['output_tokens'] * share)} "
            f"| {thousands(bucket['thinking_tokens'] * share)} "
            f"| {thousands(bucket['cache_read_input_tokens'] * share)} |"
        )
    lines += [
        "",
        (
            "Over every log that touched this branch, including the other-branch work of the "
            "straddling ones \u2014 the third column above, not the second. Token columns are "
            "recorded per thinking level rather than per model, so a level that ran more than "
            "one model is split by that level's turn share; where each level ran one model the "
            "split is the identity and the figures are the record's own."
        ),
    ]
    return lines


def section_tools(records: list[dict]) -> list[str]:
    counts: Counter = Counter()
    seconds: Counter = Counter()
    errors = denied = one_off = 0
    one_off_seconds = 0.0
    for record in records:
        calls = record.get("tool_calls") or {}
        errors += calls.get("errors") or 0
        denied += calls.get("denied") or 0
        one_off += (calls.get("one_off_code") or {}).get("count") or 0
        one_off_seconds += (calls.get("one_off_code") or {}).get("total_seconds") or 0
        for tool, stats in (calls.get("by_tool") or {}).items():
            counts[tool] += stats.get("count") or 0
            seconds[tool] += stats.get("total_seconds") or 0

    total = sum(counts.values())
    total_seconds = sum(seconds.values())
    lines = [
        "| tool | calls | share | time | share of tool time |",
        "| --- | ---: | ---: | ---: | ---: |",
    ]
    for tool, count in sorted(counts.items(), key=lambda pair: (-pair[1], pair[0])):
        lines.append(
            f"| `{tool}` | {thousands(count)} | {count / total:.1%} "
            f"| {duration(seconds[tool])} | {seconds[tool] / total_seconds:.1%} |"
        )
    lines += [
        (
            f"| **{len(counts)} tools** | **{thousands(total)}** | | "
            f"**{total_seconds / 3600:,.1f} h** | |"
        ),
        "",
        (
            "Same scope as the model table: every log that touched this branch. "
            f"**{thousands(errors)} calls returned an error and {denied} were denied.** "
            f"{thousands(one_off)} of the calls ran code written for a single measurement "
            f"({one_off_seconds / 3600:,.1f} h) — `OR-1` says a measurement worth repeating "
            "belongs in a tool rather than in a heredoc, so this is the number that says how "
            "often that rule was not followed."
        ),
    ]
    return lines


def _window_seconds(source: dict) -> float:
    start = datetime.fromisoformat(str(source["start_cutoff_at"]).replace("Z", "+00:00"))
    end = datetime.fromisoformat(str(source["end_cutoff_at"]).replace("Z", "+00:00"))
    return max(0.0, (end - start).total_seconds())


def section_codex(records: list[dict], session_id: str, branch: str) -> list[str]:
    """Render declared intervals separately from Claude's observed branch accounting."""
    lines = [
        f"### Codex task-tree interval (declared by `{session_id}`)",
        "",
        (
            f"Codex logs expose no Git-branch field. `{session_id}` declares these task-tree "
            f"intervals as work for `{branch}`; that association is operator-recorded, not "
            "harness-observed. The receipt retains additive aggregates only and excludes "
            "prompts, reasoning prose, private paths, descendant and turn identifiers, and "
            "commands."
        ),
        "",
    ]
    for index, record in enumerate(records, start=1):
        source = record["source"]
        delta = record["delta"]
        models = delta["models"]
        responses = sum(int(model["model_response_count"]) for model in models)
        tokens: Counter = Counter()
        for model in models:
            add(tokens, model["tokens"])
        live = bool(record["completeness"]["snapshot_incomplete"])
        lines += [
            f"#### Interval {index}",
            "",
            "| metric | value |",
            "| --- | ---: |",
            f"| declared wall window | {duration(_window_seconds(source))} |",
            f"| recursive agent time | {duration(delta['agent_active_seconds'])} |",
            f"| active union | {duration(delta['active_union_seconds'])} |",
            f"| parallel overlap | {duration(delta['parallel_overlap_seconds'])} |",
            f"| model responses | {responses:,} |",
            f"| output tokens | {tokens['output']:,} |",
            f"| reasoning-output tokens | {tokens['reasoning_output']:,} |",
            f"| cached-input tokens | {tokens['cached_input']:,} |",
            "",
            "| model @ thinking | responses | output | reasoning output | cached input |",
            "| --- | ---: | ---: | ---: | ---: |",
        ]
        for model in models:
            model_tokens = model["tokens"]
            lines.append(
                f"| `{model['model']} @ {model['thinking_level']}` "
                f"| {model['model_response_count']:,} | {model_tokens['output']:,} "
                f"| {model_tokens['reasoning_output']:,} "
                f"| {model_tokens['cached_input']:,} |"
            )
        tools = delta["tool_seconds_by_category"]
        if tools:
            lines += [
                "",
                "| tool-time category | overlap-safe time |",
                "| --- | ---: |",
            ]
            ordered_tools = sorted(tools.items(), key=lambda item: (-item[1], item[0]))
            for category, seconds in ordered_tools:
                lines.append(f"| `{category}` | {duration(seconds)} |")
        lines += [
            "",
            (
                "**Lower bound:** the after-snapshot still contained a live task, so later "
                "work in that task is absent."
                if live
                else "The after-snapshot contained no live task in this measured tree."
            ),
            (
                "Events emitted on completion can straddle an interval boundary; the receipt "
                "states that boundary limitation rather than reallocating them."
            ),
            "",
        ]
    return lines


def render(branch: str, session_id: str | None = None) -> str:
    exact, mixed = [], []
    for record in rollups():
        by_branch = record["turns"].get("by_branch") or {}
        here = by_branch.get(branch, 0)
        if not here:
            continue
        (exact if here == record["turns"]["assistant"] else mixed).append(record)

    codex = codex_receipts(session_id)
    if not exact and not mixed and not codex:
        return f"No rollup records any turn on `{branch}`.\n"

    versions = sorted(
        {
            v
            for r in exact + mixed
            for v in (r.get("source") or {}).get("harness_versions") or []
        }
    )
    lines = [
        "## What this branch cost",
        "",
    ]
    if exact or mixed:
        lines += [
            "### Claude branch-derived rollups",
            "",
            *section_headline(exact, mixed, branch),
            "",
            "#### Model use",
            "",
            *section_models(exact + mixed),
            "",
            "#### Every tool used",
            "",
            *section_tools(exact + mixed),
            "",
            (
                f"Generated from {len(exact) + len(mixed)} Claude rollups, harness "
                f"{', '.join(versions) or 'unrecorded'}."
            ),
            "",
        ]
    if codex and session_id is not None:
        lines += section_codex(codex, session_id, branch)
    command = f"devtools.render_pr_rollup --branch {branch}"
    if session_id:
        command += f" --session {session_id}"
    lines += [
        (
            f"Generated by `{command}` from `packing/campaign/resource-usage/`. "
            "Session-by-session figures are in "
            "[`session-close-report.yaml`](packing/campaign/session-close-report.yaml)."
        ),
        "",
    ]
    return "\n".join(lines) + "\n"


def branches() -> list[str]:
    """Every branch any rollup has turns on, so `--check` exercises the real shapes."""
    found: set[str] = set()
    for record in rollups():
        found.update((record["turns"].get("by_branch") or {}).keys())
    return sorted(found)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--branch", help="branch to attribute (default: the checked-out one)")
    parser.add_argument(
        "--session",
        help="AgentSession that explicitly declares any Codex interval receipts",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="render for every branch in the records without printing, as a smoke test",
    )
    args = parser.parse_args(argv)

    if args.check:
        # Rendering every branch is the check. Each has a different shape -- one wholly-owned
        # log, several straddling ones, a branch with no exclusive log at all -- and a
        # renderer that divides by a turn count fails on exactly those edges.
        names = branches()
        for name in names:
            render(name)
        render("a-branch-no-rollup-mentions")
        print(f"  the branch cost rollup renders for {len(names)} branches, and for none")
        return 0

    print(render(args.branch or current_branch(), args.session), end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())
