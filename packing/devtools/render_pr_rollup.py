#!/usr/bin/env python3
"""Render the cost and checked closeout of work behind a pull request.

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

For Codex, the renderer discovers every AgentSession that explicitly declares the branch.
The command above is therefore the cumulative branch-cost entry point. Pass `--session`
only to inspect one declaration:
    uv run --frozen --all-extras --group dev python -m devtools.render_pr_rollup \
        --branch codex/my-branch --session session-062

For a terminal research agenda, add `--agenda agenda-NNN`. The cost block remains first;
the result, stop-reason, disposition, grouped-change, validation, documentation, and
replanning sections come from the agenda's checked W10 closeout rather than from a
hand-written PR chronology.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

import yaml

from devtools.check_session_rollups import codex_branch_claims
from devtools.codex_task_tree_delta import validate_delta_document
from sqpack.yamlio import safe_load

ROOT = Path(__file__).resolve().parent.parent
USAGE = ROOT / "campaign" / "resource-usage"
SESSIONS = ROOT / "campaign" / "agent-sessions"
AGENDAS = ROOT / "campaign" / "agendas"
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


def resource_reference(path: Path) -> str:
    """Canonical identity for a receipt enumerated directly from the usage directory."""
    if path.parent != USAGE:
        raise ValueError("resource receipt is outside the usage directory")
    return f"packing/campaign/resource-usage/{path.name}"


def rollups() -> list[dict]:
    """Claude records retain harness-observed branch attribution."""
    found = []
    for contract, rollup, path in resource_documents():
        if contract != CLAUDE_CONTRACT:
            continue
        rollup["_name"] = path.name
        found.append(rollup)
    return found


def session_payloads() -> list[dict]:
    """Load declarations once; malformed records remain the schema gate's responsibility."""
    found = []
    for path in sorted(SESSIONS.glob("session-*.md")):
        text = path.read_text(encoding="utf-8")
        if not text.startswith("---\n"):
            continue
        document = safe_load(text.split("---\n")[1])
        payload = document.get("session") if isinstance(document, dict) else None
        if isinstance(payload, dict):
            found.append(payload)
    return found


def codex_receipts(session_id: str | None, branch: str) -> list[dict]:
    """Return distinct intervals declared for a branch, with their session claimants."""
    payloads = session_payloads()
    if session_id is not None:
        matches = [payload for payload in payloads if payload.get("id") == session_id]
        if len(matches) != 1 or matches[0].get("branch") != branch:
            return []

    documents = {
        resource_reference(path): (rollup, path)
        for contract, rollup, path in resource_documents()
        if contract == CODEX_CONTRACT
    }
    claims = codex_branch_claims(payloads, set(documents))
    conflicts = [reference for reference, branches in claims.items() if len(branches) > 1]
    if conflicts:
        name = Path(sorted(conflicts)[0]).name
        raise ValueError(f"{name} is attributed to more than one branch")

    retained = []
    for reference, branches in sorted(claims.items()):
        claimants = sorted(branches.get(branch, set()))
        if not claimants or (session_id is not None and session_id not in claimants):
            continue
        rollup, path = documents[reference]
        document = safe_load(path.read_text(encoding="utf-8"))
        if problems := validate_delta_document(document):
            raise ValueError(f"{path.name} fails semantic validation: {problems[0]}")
        record = dict(rollup)
        record["_name"] = path.name
        record["_claimants"] = claimants
        retained.append(record)
    return retained


def _claimant_label(record: dict) -> str:
    claimants = [f"`{identifier}`" for identifier in record["_claimants"]]
    return ", ".join(claimants)


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


def section_codex(records: list[dict], branch: str) -> list[str]:
    """Render declared intervals separately from Claude's observed branch accounting."""
    lines = [
        "### Codex task-tree intervals declared by AgentSessions",
        "",
        (
            f"Codex logs expose no Git-branch field. AgentSessions declare these task-tree "
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
            (
                f"#### Interval {index}: `{record['_name']}` — declared by "
                f"{_claimant_label(record)}"
            ),
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

    codex = codex_receipts(session_id, branch)
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
    if codex:
        lines += section_codex(codex, branch)
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


def _cell(value: object) -> str:
    """One plain Markdown table cell from prose-shaped YAML."""
    return " ".join(str(value).split()).replace("|", "\\|")


def agenda_payload(agenda_id: str) -> dict:
    """Load exactly one agenda by stable id and require its W10 closeout."""
    matches = []
    for path in sorted(AGENDAS.glob(f"{agenda_id}-*.md")):
        text = path.read_text(encoding="utf-8")
        if not text.startswith("---\n"):
            continue
        document = safe_load(text.split("---\n")[1])
        agenda = document.get("agenda") if isinstance(document, dict) else None
        if isinstance(agenda, dict) and agenda.get("id") == agenda_id:
            matches.append(agenda)
    if len(matches) != 1:
        raise ValueError(f"{agenda_id} does not identify exactly one agenda")
    agenda = matches[0]
    if agenda.get("status") not in {"completed", "superseded"}:
        raise ValueError(f"{agenda_id} is not terminal")
    if not isinstance(agenda.get("closeout"), dict):
        raise TypeError(f"{agenda_id} has no W10 closeout")
    return agenda


STOP_EXPLANATIONS = {
    "achieved": "Frozen exit met",
    "bounded-negative": "Declared search scope exhausted without a qualifying result",
    "time-limited": "External wall arrived before the declared scope completed",
    "guard-refused": "A correct admission, provenance, validity, or safety guard refused",
    "technical-failure": "Unintended tooling or validation failure prevented completion",
    "never-opened": "An upstream dependency never authorized execution",
    "inconclusive": "The full valid protocol ran, but its frozen criterion did not decide",
}


def render_agenda_closeout(agenda: dict) -> str:
    """Render reviewer-facing facts from one checked terminal agenda."""
    closeout = agenda["closeout"]
    lines = [
        "## Results and Dispositions",
        "",
        (
            "| Work or result | What was established | Evidence | Why it stopped "
            "| Disposition and follow-up |"
        ),
        "| --- | --- | --- | --- | --- |",
    ]
    classifications = []
    for item in agenda["items"]:
        for outcome in item["outcomes"]:
            classification = outcome["classification"]
            classifications.append(classification)
            follow_up = outcome.get("follow_up")
            disposition = f"`{outcome['disposition']}`"
            if follow_up:
                disposition += f" via `{follow_up}`"
            evidence = "<br>".join(_cell(item) for item in outcome["evidence"])
            lines.append(
                f"| `{item['id']}` — {_cell(outcome['scope'])} "
                f"| {_cell(outcome['result'])} "
                f"| {evidence} "
                f"| `{classification}` — {STOP_EXPLANATIONS[classification]} "
                f"| {disposition} |"
            )

    if "bounded-negative" not in classifications:
        lines += [
            "",
            (
                "**No completed bounded-negative search is claimed.** Partial prefixes, "
                "guard refusals, technical failures, and unopened routes are reported "
                "under their own classes rather than made to look like negative results."
            ),
        ]

    lines += [
        "",
        "## Changes by Purpose",
        "",
        "| Area | Result | Principal files or interfaces |",
        "| --- | --- | --- |",
    ]
    for change in closeout["changes"]:
        paths = "<br>".join(f"`{path}`" for path in change["paths"])
        lines.append(f"| `{change['name']}` | {_cell(change['result'])} | {paths} |")

    lines += ["", "## Validation", ""]
    for check in closeout["validation"]:
        lines.append(
            f"- **{_cell(check['scope'])}: {check['status']}.** {_cell(check['evidence'])}"
        )

    lines += [
        "",
        "## Documentation and Replanning",
        "",
        "| Document | Decision | Reason |",
        "| --- | --- | --- |",
    ]
    for review in closeout["documentation_review"]:
        lines.append(
            f"| `{review['path']}` | `{review['decision']}` | {_cell(review['reason'])} |"
        )

    replanning = closeout["replanning"]
    operator = replanning["operator_input"]
    lines += [
        "",
        (f"Operator input: **{operator['status']}** — {_cell(operator['note'])}"),
        "",
        "| Priority | Candidate | Workflow | Why it remains |",
        "| ---: | --- | --- | --- |",
    ]
    for candidate in sorted(
        replanning["candidates"], key=lambda value: (value["priority"], value["bead"])
    ):
        lines.append(
            f"| {candidate['priority']} | `{candidate['bead']}` "
            f"| `{candidate['workflow']}` | {_cell(candidate['rationale'])} |"
        )
    selected = replanning["selected"]
    lines += [
        "",
        (
            f"**Selected next entry:** `{selected['bead']}` under "
            f"`{selected['workflow']}` — {_cell(selected['rationale'])}"
        ),
        "",
        "## Limits",
        "",
        (
            f"This closeout reports only the claims and scopes recorded by "
            f"`{agenda['id']}`. A continued or deferred item requires its named follow-up "
            "and a fresh prospective contract where the original record is immutable."
        ),
        "",
    ]
    return "\n".join(lines) + "\n"


def render_description(branch: str, agenda_id: str, session_id: str | None = None) -> str:
    """The complete cost-first PR description for a terminal agenda."""
    if session_id is not None:
        # Validate the explicit Codex declaration without narrowing the PR's cumulative
        # branch receipt to that one session.
        render(branch, session_id)
    return render(branch) + render_agenda_closeout(agenda_payload(agenda_id))


def branches() -> list[str]:
    """Every branch any rollup has turns on, so `--check` exercises the real shapes."""
    found: set[str] = set()
    for record in rollups():
        found.update((record["turns"].get("by_branch") or {}).keys())
    for payload in session_payloads():
        branch = payload.get("branch")
        if isinstance(branch, str) and branch:
            found.add(branch)
    return sorted(found)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--branch", help="branch to attribute (default: the checked-out one)")
    parser.add_argument(
        "--session",
        help="AgentSession that explicitly declares any Codex interval receipts",
    )
    parser.add_argument(
        "--agenda",
        help="terminal agenda whose checked W10 closeout follows the cost block",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="render for every branch in the records without printing, as a smoke test",
    )
    args = parser.parse_args(argv)

    checked_names: list[str] | None = None
    rendered: str | None = None
    try:
        if args.check:
            # Rendering every branch exercises both harness records and the retained corpus.
            checked_names = branches()
            for name in checked_names:
                render(name)
            render("a-branch-no-rollup-mentions")
            for path in sorted(AGENDAS.glob("agenda-*.md")):
                document = safe_load(path.read_text(encoding="utf-8").split("---\n")[1])
                agenda = document.get("agenda") if isinstance(document, dict) else None
                if isinstance(agenda, dict) and isinstance(agenda.get("closeout"), dict):
                    render_agenda_closeout(agenda)
        else:
            branch = args.branch or current_branch()
            rendered = (
                render_description(branch, args.agenda, args.session)
                if args.agenda
                else render(branch, args.session)
            )
    except ValueError as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    except (
        AttributeError,
        IndexError,
        KeyError,
        OSError,
        TypeError,
        yaml.YAMLError,
        subprocess.CalledProcessError,
    ):
        print("error: unable to render branch-cost rollup", file=sys.stderr)
        return 1
    if checked_names is not None:
        print(
            f"  the branch cost rollup renders for {len(checked_names)} branches, and for none"
        )
    else:
        assert rendered is not None
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())
