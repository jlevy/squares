#!/usr/bin/env python3
"""Render the cost of the work behind a pull request, for the pull request itself.

A reviewer looking at a branch can see what changed and cannot see what it took. That
number exists -- `campaign/resource-usage/` holds one `ClaudeEfficiencyRollup` per agent
log, with turns by model and thinking level, tokens, and every tool call -- and it has
never been in front of the person deciding whether to merge.

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
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path

from sqpack.yamlio import safe_load

ROOT = Path(__file__).resolve().parent.parent
USAGE = ROOT / "campaign" / "resource-usage"


def current_branch() -> str:
    result = subprocess.run(
        ["git", "rev-parse", "--abbrev-ref", "HEAD"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout.strip()


def rollups() -> list[dict]:
    found = []
    for path in sorted(USAGE.glob("*.yaml")):
        document = safe_load(path.read_text(encoding="utf-8"))
        rollup = document.get("rollup") or document
        rollup["_name"] = path.name
        found.append(rollup)
    return found


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


def render(branch: str) -> str:
    exact, mixed = [], []
    for record in rollups():
        by_branch = record["turns"].get("by_branch") or {}
        here = by_branch.get(branch, 0)
        if not here:
            continue
        (exact if here == record["turns"]["assistant"] else mixed).append(record)

    if not exact and not mixed:
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
        *section_headline(exact, mixed, branch),
        "",
        "### Model use",
        "",
        *section_models(exact + mixed),
        "",
        "### Every tool used",
        "",
        *section_tools(exact + mixed),
        "",
        (
            f"Generated by `devtools.render_pr_rollup --branch {branch}` from "
            f"{len(exact) + len(mixed)} rollups in `packing/campaign/resource-usage/`, "
            f"harness {', '.join(versions) or 'unrecorded'}. "
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

    print(render(args.branch or current_branch()), end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())
