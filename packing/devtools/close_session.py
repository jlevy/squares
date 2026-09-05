#!/usr/bin/env python3
"""Close a session: roll up what it cost, check the record, and print what happened.

Three things were manual and each cost something.

The rollup was manual, and a session can end without it: `session-045` ran twenty-three
phases with no rollup written and closed clean, because nothing linked a session to its
usage. `check_session_rollups` refuses that now, but refusing is not the same as doing.

The sub-agent logs were manual, and they are where delegated cost lives. Reconstructing
the sequence by hand twice on 2026-08-30 produced two different answers -- the second pass
found two logs the first had missed -- which is `OR-1`'s argument exactly.

And there was no report. The rollup is a large YAML holding real numbers that nobody reads
as prose, and the session record holds outcomes with no costs beside them. What a reader
wants at the end of a session is one page saying what it did, what that took, and whether
the record is complete. This prints that, and prints it from the artifacts rather than
from anybody's recollection.

`--render` writes both views of that join: `campaign/session-close-report.yaml`, one
validated entry per session, and the tables spliced into `SYNOPSIS.md`. `--check` compares
both against a fresh render without writing, which is what the gate calls. `--update`
regenerates Claude rollups from logs first, and is also the whole of Claude backfill. Codex
uses `devtools.codex_task_tree_delta` first because its recursive task tree and declared
interval are not a one-log/one-record shape.

**No attribution is ever inferred.** A session owns the receipts its own record declares
and nothing else. A receipt that no session declares is listed as such rather than assigned
to the session whose window happens to contain it -- the spans overlap heavily, so that
guess would look right and be unfalsifiable. Claude totals and Codex intervals remain
separate because they can overlap and count different units.

Usage, from `packing/`:
    uv run --frozen --all-extras --group dev python -m devtools.close_session --check
    uv run --frozen --all-extras --group dev python -m devtools.close_session --render
    uv run --frozen --all-extras --group dev python -m devtools.close_session \
        --update --session session-047 --log <path-to-session>.jsonl
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import TypedDict

import yaml

from devtools.check_session_rollups import (
    GRANDFATHERED_BEFORE,
    canonical_resource_rollup_reference,
    unique_resource_rollups,
)
from devtools.codex_task_tree_delta import validate_delta_document
from devtools.render_pr_rollup import agenda_payload, current_branch
from devtools.render_pr_rollup import render as render_branch_cost
from devtools.render_pr_rollup import render_description as render_pr_description
from sqpack.yamlio import safe_load

ROOT = Path(__file__).resolve().parent.parent
SESSIONS = ROOT / "campaign" / "agent-sessions"
USAGE = ROOT / "campaign" / "resource-usage"
REPORT = ROOT / "campaign" / "session-close-report.yaml"
SYNOPSIS = ROOT.parent / "SYNOPSIS.md"

TERMINAL = {"completed", "stopped"}
CLAUDE_CONTRACT = "packing.squares:ClaudeEfficiencyRollup/v1"
CODEX_CONTRACT = "packing.squares:CodexTaskTreeDelta/v1"


def receipt_path(reference: object) -> Path | None:
    """Resolve only the canonical repository-relative receipt contract."""
    canonical = canonical_resource_rollup_reference(reference)
    return ROOT.parent / canonical if canonical is not None else None


def receipt_reference(path: Path) -> str:
    """Name one on-disk usage receipt without collapsing its repository identity."""
    return path.relative_to(ROOT.parent).as_posix()


def usage_references() -> set[str]:
    return {receipt_reference(path) for path in USAGE.glob("*.yaml")}


def load_sessions() -> dict[str, dict]:
    found = {}
    for path in sorted(SESSIONS.glob("session-*.md")):
        payload = safe_load(path.read_text(encoding="utf-8").split("---\n")[1])["session"]
        found[payload["id"]] = payload
    return found


def rollup_span(path: Path) -> tuple[datetime | None, datetime | None]:
    """A rollup's own window, which is how a sub-agent log is attributed to a session."""
    document = safe_load(path.read_text(encoding="utf-8"))
    span = (document.get("rollup") or document).get("span") or {}
    source = (document.get("rollup") or document).get("source") or {}
    if source.get("harness") == "codex":
        span = {
            "started_at": source.get("start_cutoff_at"),
            "ended_at": source.get("end_cutoff_at"),
        }

    def parse(value: object) -> datetime | None:
        if not isinstance(value, str):
            return None
        try:
            return datetime.fromisoformat(value)
        except ValueError:
            return None

    return parse(span.get("started_at")), parse(span.get("ended_at"))


class RollupTotals(TypedDict):
    """One rollup's numbers, already narrowed.

    `safe_load` returns `Any`, and reading five fields off it produced ten type-floor errors
    the first time this summed them. Narrowing once, here, is cheaper than narrowing at every
    caller and is the only place a malformed rollup can turn into a wrong number.
    """

    turns: int
    calls: int
    errors: int
    one_off: int
    hours: float


class CodexReceiptSummary(TypedDict):
    """The additive figures Codex measures, kept separate from Claude totals."""

    path: str
    model_responses: int
    agent_hours: float
    active_union_hours: float
    wall_hours: float
    snapshot_incomplete: bool


def whole(value: object) -> int:
    """A count, or zero. `bool` is excluded because `True` would otherwise count as one."""
    return value if isinstance(value, int) and not isinstance(value, bool) else 0


def totals(path: Path) -> RollupTotals:
    document = safe_load(path.read_text(encoding="utf-8"))
    rollup = document.get("rollup") or document
    turns = rollup.get("turns") or {}
    calls = rollup.get("tool_calls") or {}
    seconds = (rollup.get("span") or {}).get("wall_seconds")
    return {
        "turns": whole(turns.get("assistant")),
        "calls": whole(calls.get("total")),
        "errors": whole(calls.get("errors")),
        "one_off": whole((calls.get("one_off_code") or {}).get("count")),
        "hours": round(seconds / 3600, 2) if isinstance(seconds, int | float) else 0.0,
    }


def contract_of(path: Path) -> str | None:
    document = safe_load(path.read_text(encoding="utf-8"))
    meta = document.get("softschema") if isinstance(document, dict) else None
    return str(meta.get("contract")) if isinstance(meta, dict) else None


def codex_receipt_summary(path: Path) -> CodexReceiptSummary:
    document = safe_load(path.read_text(encoding="utf-8"))
    if problems := validate_delta_document(document):
        raise ValueError(f"{path.name} fails semantic validation: {problems[0]}")
    rollup = document["rollup"]
    delta = rollup["delta"]
    source = rollup["source"]
    responses = sum(int(model["model_response_count"]) for model in delta["models"])
    started = datetime.fromisoformat(str(source["start_cutoff_at"]))
    ended = datetime.fromisoformat(str(source["end_cutoff_at"]))
    return {
        "path": path.relative_to(ROOT.parent).as_posix(),
        "model_responses": responses,
        "agent_hours": round(float(delta["agent_active_seconds"]) / 3600, 2),
        "active_union_hours": round(float(delta["active_union_seconds"]) / 3600, 2),
        "wall_hours": round(max(0.0, (ended - started).total_seconds()) / 3600, 2),
        "snapshot_incomplete": bool(rollup["completeness"]["snapshot_incomplete"]),
    }


def sum_rollups(references: set[str]) -> dict[str, int | float]:
    """Add up a set of rollups, once each.

    Taking a set rather than a list is the whole safeguard. Sessions 045, 046 and 047 all
    declare the same harness log, so summing the per-session figures counted 37 hours three
    times and reported 117.9 for a campaign that had spent 43.7 -- an error in the
    flattering direction, which is the direction to build against.
    """
    paths = [receipt_path(reference) for reference in sorted(references)]
    each = [
        totals(path)
        for path in paths
        if path is not None and path.exists() and contract_of(path) == CLAUDE_CONTRACT
    ]
    return {
        "rollups": len(each),
        "turns": sum(v["turns"] for v in each),
        "tool_calls": sum(v["calls"] for v in each),
        "tool_errors": sum(v["errors"] for v in each),
        "one_off_code": sum(v["one_off"] for v in each),
        "wall_hours": round(sum(v["hours"] for v in each), 2),
    }


def regenerate(log: Path, extra: list[Path]) -> list[str]:
    """Write the session's rollup and any sub-agent rollup not already on disk."""
    written = []
    for source in [log, *extra]:
        target = USAGE / f"{source.stem}.yaml"
        if source is not log and target.exists():
            continue
        subprocess.run(
            [sys.executable, "-m", "devtools.log_rollup", str(source), "--out", str(USAGE)],
            cwd=ROOT,
            check=True,
            capture_output=True,
        )
        written.append(receipt_reference(target))
    return written


def report(session_id: str | None) -> int:
    sessions = load_sessions()
    declared_all: set[str] = set()
    for payload in sessions.values():
        declared_all.update(unique_resource_rollups(payload))

    problems: list[str] = []

    targets = [session_id] if session_id else sorted(sessions)
    for ident in targets:
        payload = sessions.get(ident)
        if payload is None:
            print(f"no such session: {ident}")
            return 1
        if payload.get("status") not in TERMINAL and session_id is None:
            continue

        declared = unique_resource_rollups(payload)
        missing = [
            reference
            for reference in declared
            if (path := receipt_path(reference)) is None or not path.exists()
        ]
        # Same boundary the gate's own checker uses, imported rather than restated: a
        # session that closed before the field existed cannot be faulted for not using it.
        grandfathered = ident < GRANDFATHERED_BEFORE
        if payload.get("status") in TERMINAL and not declared and not grandfathered:
            problems.append(f"{ident}: terminal and declares no rollups")
        problems.extend(f"{ident}: declares {name}, which is not on disk" for name in missing)

        if session_id is None:
            continue

        print(f"# {ident} — {payload.get('title', '')}")
        print(f"  status {payload.get('status')}   primary bead {payload.get('primary_bead')}")
        print()
        phases = payload.get("workflow_phases") or []
        print(f"  {len(phases)} phases")
        for number, phase in enumerate(phases, start=1):
            outcome = " ".join(str(phase.get("outcome", "")).split())
            print(f"    {number}. [{phase.get('status')}] {phase.get('workflow')}")
            print(f"       {outcome[:150]}{'…' if len(outcome) > 150 else ''}")
        print()

        print(f"  {len(declared)} rollups declared")
        for reference in declared:
            path = receipt_path(reference)
            name = Path(reference).name
            if path is None or not path.exists():
                print(f"    MISSING  {reference}")
                continue
            if contract_of(path) == CODEX_CONTRACT:
                c = codex_receipt_summary(path)
                bound = " lower-bound" if c["snapshot_incomplete"] else ""
                print(
                    f"    codex     {name[:38]:<38} responses "
                    f"{c['model_responses']!s:>5}  agent {c['agent_hours']}h  "
                    f"wall {c['wall_hours']}h{bound}"
                )
            else:
                t = totals(path)
                kind = "session" if not name.startswith("agent-") else "sub-agent"
                print(
                    f"    {kind:<9} {name[:38]:<38} "
                    f"turns {t['turns']!s:>5}  calls {t['calls']!s:>5}  "
                    f"errors {t['errors']!s:>3}  {t['hours']}h"
                )
        print()
        print(
            f"  stop reason: {' '.join(str(payload.get('stop_reason') or '—').split())[:160]}"
        )
        print(
            f"  next action: {' '.join(str(payload.get('next_action') or '—').split())[:160]}"
        )
        print()

    orphans = sorted(usage_references() - declared_all)
    if orphans:
        print(
            f"{len(orphans)} rollups no session declares "
            "(pre-field sessions do this legitimately):"
        )
        for reference in orphans:
            path = receipt_path(reference)
            assert path is not None
            started, _ = rollup_span(path)
            name = Path(reference).name
            print(f"    {name[:44]:<44} span starts {started.date() if started else 'unknown'}")
        print()

    if problems:
        print("problems:")
        for problem in problems:
            print(f"  {problem}")
        return 1

    terminal = sum(1 for p in sessions.values() if p.get("status") in TERMINAL)
    print(f"{terminal} terminal sessions, all declaring rollups that exist")
    return 0


def render_report() -> str:
    """Every session, joined to what it cost, as a validated dataset.

    The join is the whole point. A session record carries phases and outcomes; a rollup
    carries turns and tool calls; nothing held both, so "what did this session cost" was
    answered by hand and "what has the campaign cost" was not answered at all.

    Sessions with no measurement appear with `measured: false` and a reason. Skipping them
    would produce a total that reads as the campaign's cost while being a fraction of it,
    which is the flattering direction. When a retained log turns up for one of them,
    `--update` writes its rollup and the entry fills in on the next render -- that is what
    backfill means here, and it needs no change to this file.
    """
    sessions = load_sessions()
    owners: dict[str, set[str]] = {}
    for ident, payload in sessions.items():
        for ref in unique_resource_rollups(payload):
            owners.setdefault(ref, set()).add(ident)

    lines = [
        "# GENERATED by devtools.close_session --render. Do not edit by hand.",
        "#",
        "# One entry per session, joining the record's phases to the rollup's cost. A",
        "# session with no rollup says so and why, rather than being omitted.",
        "softschema:",
        "  contract: packing.squares:SessionCloseReport/v1",
        "  schema: schemas/session-close-report.schema.yaml",
        "  envelope: null",
        "  status: enforced",
        f"count: {len(sessions)}",
        "generated_by: >-",
        "  uv run --frozen --all-extras --group dev python -m devtools.close_session --render",
        "sessions:",
    ]

    measured_ids = {ident for ids in owners.values() for ident in ids}
    attributed = {
        reference
        for reference in owners
        if (path := receipt_path(reference)) is not None and path.exists()
    }
    orphaned = usage_references() - attributed
    codex_attributed = sum(
        contract_of(path) == CODEX_CONTRACT
        for reference in attributed
        if (path := receipt_path(reference)) is not None
    )
    codex_unattributed = sum(
        contract_of(path) == CODEX_CONTRACT
        for reference in orphaned
        if (path := receipt_path(reference)) is not None
    )
    codex_measured = sum(contract_of(path) == CODEX_CONTRACT for path in USAGE.glob("*.yaml"))

    lines[lines.index("sessions:")] = "totals:"
    lines += [
        f"  sessions_measured: {len(measured_ids)}",
        f"  sessions_unmeasured: {len(sessions) - len(measured_ids)}",
        "  attributed:",
        *[f"    {k}: {v}" for k, v in sum_rollups(attributed).items()],
        "  unattributed:",
        *[f"    {k}: {v}" for k, v in sum_rollups(orphaned).items()],
        "  measured:",
        *[f"    {k}: {v}" for k, v in sum_rollups(attributed | orphaned).items()],
        "codex_receipts:",
        f"  attributed: {codex_attributed}",
        f"  unattributed: {codex_unattributed}",
        f"  measured: {codex_measured}",
    ]
    lines += [
        "# Per-session figures below are the logs each session DECLARES. They overlap when",
        "# sessions share a harness log, so they do not sum to `attributed` above.",
        "sessions:",
    ]

    def scalar(value: object) -> str:
        return "null" if value is None else str(value)

    for ident in sorted(sessions):
        payload = sessions[ident]
        declared = unique_resource_rollups(payload)
        declared_codex = [
            path
            for ref in declared
            if (path := receipt_path(ref)) is not None
            and path.exists()
            and contract_of(path) == CODEX_CONTRACT
        ]
        summed = {"turns": 0, "calls": 0, "errors": 0, "one_off": 0, "hours": 0.0}
        present = False
        claude_present = False
        for ref in declared:
            path = receipt_path(ref)
            if path is None or not path.exists():
                continue
            present = True
            if contract_of(path) != CLAUDE_CONTRACT:
                continue
            claude_present = True
            each = totals(path)
            summed["turns"] += each["turns"]
            summed["calls"] += each["calls"]
            summed["errors"] += each["errors"]
            summed["one_off"] += each["one_off"]
            summed["hours"] += each["hours"]

        title = " ".join(str(payload.get("title", "")).split()).replace('"', "'")
        lines += [
            f"- id: {ident}",
            f'  title: "{title}"',
            f"  status: {payload.get('status')}",
            f"  primary_bead: {scalar(payload.get('primary_bead'))}",
            f"  phases: {len(payload.get('workflow_phases') or [])}",
            f"  measured: {str(present).lower()}",
        ]
        if not present:
            reason = (
                "closed before resource_rollups existed; the harness log is not retained, "
                "so its cost cannot be recovered"
                if ident < GRANDFATHERED_BEFORE
                else "declares rollups that are not on disk"
                if declared
                else "declares no rollups"
            )
            lines.append(f"  unmeasured_reason: >-\n    {reason}")
        lines.append("  rollups:" + (" []" if not declared else ""))
        lines += [f"  - {ref}" for ref in declared]
        if present:
            lines += [
                f"  turns: {summed['turns'] if claude_present else 'null'}",
                f"  tool_calls: {summed['calls'] if claude_present else 'null'}",
                f"  tool_errors: {summed['errors'] if claude_present else 'null'}",
                f"  one_off_code: {summed['one_off'] if claude_present else 'null'}",
                f"  wall_hours: {round(summed['hours'], 2) if claude_present else 'null'}",
            ]
        lines.append("  codex_receipts:" + (" []" if not declared_codex else ""))
        for path in declared_codex:
            receipt = codex_receipt_summary(path)
            lines += [
                f"  - path: {receipt['path']}",
                f"    model_responses: {receipt['model_responses']}",
                f"    agent_hours: {receipt['agent_hours']}",
                f"    active_union_hours: {receipt['active_union_hours']}",
                f"    wall_hours: {receipt['wall_hours']}",
                f"    snapshot_incomplete: {str(receipt['snapshot_incomplete']).lower()}",
            ]
    return "\n".join(lines) + "\n"


BEGIN = "<!-- BEGIN GENERATED: session-close-report (devtools.close_session) -->"
END = "<!-- END GENERATED: session-close-report -->"


def render_synopsis_block() -> str:
    """The reader-facing view of the same join, for `SYNOPSIS.md`.

    The dataset is the full report and this is not a second copy of it: it carries the
    campaign totals, the sessions that actually have a measurement, and the size of the gap.
    Forty-four rows of dashes would be the full report and would not be worth reading, which
    is the distinction between complete and clean.

    Tables only, and deliberately. Flowmark formats this repository's prose and rewraps any
    paragraph it finds, so a paragraph emitted here would have two owners: the formatter
    would rewrap it on commit and the drift check would then demand it back. That is not
    hypothetical -- `make format-check` reported `SYNOPSIS.md` would be reformatted on the
    first render that included prose. Everything explanatory lives in the hand-written
    section around this block, where flowmark owns it outright.
    """
    sessions = load_sessions()
    owners: dict[str, set[str]] = {}
    for ident, payload in sessions.items():
        for ref in unique_resource_rollups(payload):
            owners.setdefault(ref, set()).add(ident)
    attributed = {
        reference
        for reference in owners
        if (path := receipt_path(reference)) is not None and path.exists()
    }
    orphaned = usage_references() - attributed
    measured_ids = sorted({ident for ids in owners.values() for ident in ids})
    codex_names = {
        receipt_reference(path)
        for path in USAGE.glob("*.yaml")
        if contract_of(path) == CODEX_CONTRACT
    }
    claude_names = usage_references() - codex_names

    def row(label: str, figures: dict[str, int | float], *, bold: bool = False) -> str:
        mark = "**" if bold else ""
        cells = [
            f"{figures['rollups']:,}",
            f"{figures['turns']:,}",
            f"{figures['tool_calls']:,}",
            f"{figures['tool_errors']:,}",
            f"{figures['one_off_code']:,}",
            f"{figures['wall_hours']:,} h",
        ]
        return (
            f"| {mark}{label}{mark} | " + " | ".join(f"{mark}{c}{mark}" for c in cells) + " |"
        )

    lines = [
        BEGIN,
        "",
        "| Rollups | count | turns | tool calls | errors | one-off code | wall |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: |",
        row("claimed by a session", sum_rollups(attributed)),
        row("claimed by none", sum_rollups(orphaned)),
        row("measured", sum_rollups(attributed | orphaned), bold=True),
        "",
        "| Session | Phases | Rollups | Turns | Tool calls | Errors | Wall |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    # A rollup declared by several sessions is charged to none of them. Charging it to each
    # is what turned 43.7 hours into 117.9; charging it to the first would be arbitrary. It
    # gets its own row, so the column adds up to the campaign figure above rather than
    # needing a footnote saying why it does not.
    shared = {name for name, ids in owners.items() if len(ids) > 1} & attributed & claude_names
    claude_measured_ids = sorted(
        {ident for name, ids in owners.items() if name in claude_names for ident in ids}
    )
    for ident in claude_measured_ids:
        payload = sessions[ident]
        declared = set(unique_resource_rollups(payload))
        figures = sum_rollups(declared - shared)
        lines.append(
            f"| [{ident}]({link(ident)}) "
            f"| {len(payload.get('workflow_phases') or [])} "
            f"| {figures['rollups']} | {figures['turns']:,} | {figures['tool_calls']:,} "
            f"| {figures['tool_errors']:,} | {figures['wall_hours']} h |"
        )
    if shared:
        figures = sum_rollups(shared)
        lines.append(
            f"| *shared by {len(claude_measured_ids)} sessions* | — "
            f"| {figures['rollups']} | {figures['turns']:,} | {figures['tool_calls']:,} "
            f"| {figures['tool_errors']:,} | {figures['wall_hours']} h |"
        )
    declared_codex = sorted(codex_names & set(owners))
    orphaned_codex = sorted(codex_names - set(owners))
    lines += [
        "",
        (
            "| Codex interval receipt | declaring sessions | model responses | agent time "
            "| active union | wall window | live lower bound |"
        ),
        "| --- | --- | ---: | ---: | ---: | ---: | --- |",
    ]
    for reference in [*declared_codex, *orphaned_codex]:
        path = receipt_path(reference)
        assert path is not None
        receipt = codex_receipt_summary(path)
        claimants = ", ".join(sorted(owners.get(reference, set()))) or "unattributed"
        lines.append(
            f"| `{Path(reference).name}` | {claimants} | {receipt['model_responses']:,} "
            f"| {receipt['agent_hours']} h | {receipt['active_union_hours']} h "
            f"| {receipt['wall_hours']} h "
            f"| {'yes' if receipt['snapshot_incomplete'] else 'no'} |"
        )
    lines += [
        "",
        "| Coverage | sessions |",
        "| --- | ---: |",
        f"| measured | {len(measured_ids)} |",
        (
            f"| closed before `resource_rollups` existed, logs not retained "
            f"| {len(sessions) - len(measured_ids)} |"
        ),
        f"| **total** | **{len(sessions)}** |",
        "",
        END,
    ]
    return "\n".join(lines)


def link(ident: str) -> str:
    """The session record's path, found rather than assumed: filenames carry a slug."""
    matches = sorted(SESSIONS.glob(f"{ident}-*.md"))
    target = matches[0] if matches else SESSIONS / f"{ident}.md"
    return target.relative_to(ROOT.parent).as_posix()


def splice_synopsis(text: str) -> str:
    """Replace the generated block in place, refusing rather than guessing if it is absent."""
    start, stop = text.find(BEGIN), text.find(END)
    if start < 0 or stop < 0:
        raise SystemExit(f"{SYNOPSIS.name} has no session-close-report block to fill")
    return text[:start] + render_synopsis_block() + text[stop + len(END) :]


def finalize_agenda_views(agenda_id: str) -> None:
    """Regenerate every derived campaign and reader view at a W10 boundary."""
    subprocess.run(
        [sys.executable, "-m", "sqpack.campaign.ledger", "check"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )

    # Live tbd is the queue authority. Synchronize it before accepting the checked
    # candidate ranking, then prove every retained candidate still exists at the priority
    # W10 assigned and that the selected one is actually ready.
    subprocess.run(
        ["tbd", "sync"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    agenda = agenda_payload(agenda_id)
    replanning = agenda["closeout"]["replanning"]
    candidates = {candidate["bead"]: candidate for candidate in replanning["candidates"]}
    shown = subprocess.run(
        ["tbd", "show", *candidates, "--json"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    shown_payload = json.loads(shown.stdout)
    shown_issues = shown_payload if isinstance(shown_payload, list) else [shown_payload]
    issues = {issue["displayId"]: issue for issue in shown_issues}
    missing = sorted(candidates.keys() - issues.keys())
    if missing:
        raise ValueError(f"W10 candidates are missing from live tbd: {missing}")
    for bead, candidate in candidates.items():
        issue = issues[bead]
        if issue.get("status") not in {"open", "in_progress"}:
            raise ValueError(f"W10 candidate {bead} is {issue.get('status')}, not live")
        if issue.get("priority") != candidate["priority"]:
            raise ValueError(
                f"W10 candidate {bead} has tbd priority "
                f"{issue.get('priority')}, expected {candidate['priority']}"
            )
    ready = subprocess.run(
        ["tbd", "ready", "--json"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    ready_ids = {item["id"] for item in json.loads(ready.stdout)}
    selected = replanning["selected"]["bead"]
    if selected not in ready_ids:
        raise ValueError(f"W10 selected bead {selected} is not ready in live tbd")

    for arguments in (
        ("sqpack.campaign.ledger", "render"),
        ("devtools.render_agenda_map",),
    ):
        subprocess.run(
            [sys.executable, "-m", *arguments],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )


def _run(options: argparse.Namespace) -> int:
    """Execute one parsed close operation so the CLI can contain receipt failures."""
    if options.render:
        pr_description = (
            render_pr_description(current_branch(), options.agenda, options.session)
            if options.agenda
            else render_branch_cost(current_branch())
        )
        if options.agenda:
            finalize_agenda_views(options.agenda)
        report_text = render_report()
        synopsis_text = splice_synopsis(SYNOPSIS.read_text(encoding="utf-8"))
        REPORT.write_text(report_text, encoding="utf-8")
        SYNOPSIS.write_text(synopsis_text, encoding="utf-8")
        if options.agenda:
            subprocess.run(
                [sys.executable, "-m", "devtools.render_document_map"],
                cwd=ROOT,
                check=True,
                capture_output=True,
                text=True,
            )
        print(f"wrote {REPORT.relative_to(ROOT.parent)} and the {SYNOPSIS.name} view")
        status = report(options.session)
        # Printed here rather than left to a second command anyone can forget. `OR-9` says
        # the pull request leads with what the branch cost, and the moment that block is
        # correct is the moment the rollups are written -- which is now.
        print()
        print("=" * 78)
        print("Use the generated description below for the pull request (OR-9/OR-11).")
        print("=" * 78)
        print()
        print(pr_description, end="")
        return status

    if options.update:
        if options.log is None:
            print("--update needs --log")
            return 2
        written = regenerate(options.log, list(options.agent_logs))
        print(f"wrote {len(written)} rollups: {', '.join(written) if written else 'none new'}")
        print()

    if options.check:
        drifted = [
            name
            for name, current, wanted in (
                (
                    REPORT.relative_to(ROOT.parent).as_posix(),
                    REPORT.read_text(encoding="utf-8") if REPORT.exists() else "",
                    render_report(),
                ),
                (
                    SYNOPSIS.relative_to(ROOT.parent).as_posix(),
                    SYNOPSIS.read_text(encoding="utf-8"),
                    splice_synopsis(SYNOPSIS.read_text(encoding="utf-8")),
                ),
            )
            if current != wanted
        ]
        if drifted:
            for name in drifted:
                print(f"{name} has drifted; run devtools.close_session --render")
            return 1
        count = len(load_sessions())
        print(f"  the close report and its synopsis view agree with {count} sessions")

    return report(options.session)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--session", help="report on one session in full")
    parser.add_argument("--log", type=Path, help="the session's harness log, to regenerate")
    parser.add_argument("--agent-logs", type=Path, nargs="*", default=[])
    parser.add_argument(
        "--agenda",
        help="terminal agenda to reconcile, validate against live tbd, and render for the PR",
    )
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true", help="verify without writing")
    mode.add_argument("--update", action="store_true", help="regenerate rollups first")
    mode.add_argument("--render", action="store_true", help="write the measured-cost view")
    options = parser.parse_args(argv)
    try:
        return _run(options)
    except subprocess.CalledProcessError as error:
        command = error.cmd
        rendered_command = (
            command if isinstance(command, str) else " ".join(str(part) for part in command)
        )
        print(
            f"error: command failed with exit {error.returncode}: {rendered_command}",
            file=sys.stderr,
        )
        detail = error.stderr or error.stdout
        if isinstance(detail, str) and detail.strip():
            print(detail.strip(), file=sys.stderr)
        return 1
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
    ):
        print("error: unable to close or report the session", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
