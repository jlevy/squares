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
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import TypedDict

from devtools.check_session_rollups import GRANDFATHERED_BEFORE
from devtools.render_pr_rollup import current_branch
from devtools.render_pr_rollup import render as render_branch_cost
from sqpack.yamlio import safe_load

ROOT = Path(__file__).resolve().parent.parent
SESSIONS = ROOT / "campaign" / "agent-sessions"
USAGE = ROOT / "campaign" / "resource-usage"
REPORT = ROOT / "campaign" / "session-close-report.yaml"
SYNOPSIS = ROOT.parent / "SYNOPSIS.md"

TERMINAL = {"completed", "stopped"}
CLAUDE_CONTRACT = "packing.squares:ClaudeEfficiencyRollup/v1"
CODEX_CONTRACT = "packing.squares:CodexTaskTreeDelta/v1"


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
            return datetime.fromisoformat(value.replace("Z", "+00:00"))
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
    rollup = document["rollup"]
    delta = rollup["delta"]
    source = rollup["source"]
    responses = sum(int(model["model_response_count"]) for model in delta["models"])
    started = datetime.fromisoformat(str(source["start_cutoff_at"]).replace("Z", "+00:00"))
    ended = datetime.fromisoformat(str(source["end_cutoff_at"]).replace("Z", "+00:00"))
    return {
        "path": path.relative_to(ROOT.parent).as_posix(),
        "model_responses": responses,
        "agent_hours": round(float(delta["agent_active_seconds"]) / 3600, 2),
        "active_union_hours": round(float(delta["active_union_seconds"]) / 3600, 2),
        "wall_hours": round(max(0.0, (ended - started).total_seconds()) / 3600, 2),
        "snapshot_incomplete": bool(rollup["completeness"]["snapshot_incomplete"]),
    }


def sum_rollups(names: set[str]) -> dict[str, int | float]:
    """Add up a set of rollups, once each.

    Taking a set rather than a list is the whole safeguard. Sessions 045, 046 and 047 all
    declare the same harness log, so summing the per-session figures counted 37 hours three
    times and reported 117.9 for a campaign that had spent 43.7 -- an error in the
    flattering direction, which is the direction to build against.
    """
    each = [
        totals(USAGE / name)
        for name in sorted(names)
        if (USAGE / name).exists() and contract_of(USAGE / name) == CLAUDE_CONTRACT
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
        written.append(target.name)
    return written


def report(session_id: str | None) -> int:
    sessions = load_sessions()
    declared_all: set[str] = set()
    for payload in sessions.values():
        declared_all.update(Path(r).name for r in (payload.get("resource_rollups") or []))

    problems: list[str] = []

    targets = [session_id] if session_id else sorted(sessions)
    for ident in targets:
        payload = sessions.get(ident)
        if payload is None:
            print(f"no such session: {ident}")
            return 1
        if payload.get("status") not in TERMINAL and session_id is None:
            continue

        declared = [Path(r).name for r in (payload.get("resource_rollups") or [])]
        missing = [name for name in declared if not (USAGE / name).exists()]
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
        for name in declared:
            path = USAGE / name
            if not path.exists():
                print(f"    MISSING  {name}")
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

    orphans = sorted({p.name for p in USAGE.glob("*.yaml")} - declared_all)
    if orphans:
        print(
            f"{len(orphans)} rollups no session declares "
            "(pre-field sessions do this legitimately):"
        )
        for name in orphans:
            started, _ = rollup_span(USAGE / name)
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
    owners: dict[str, list[str]] = {}
    for ident, payload in sessions.items():
        for ref in payload.get("resource_rollups") or []:
            owners.setdefault(Path(ref).name, []).append(ident)

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
    attributed = {name for name in owners if (USAGE / name).exists()}
    orphaned = {path.name for path in USAGE.glob("*.yaml")} - attributed
    codex_attributed = sum(contract_of(USAGE / name) == CODEX_CONTRACT for name in attributed)
    codex_unattributed = sum(contract_of(USAGE / name) == CODEX_CONTRACT for name in orphaned)
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
        declared = [str(r) for r in (payload.get("resource_rollups") or [])]
        declared_codex = [
            USAGE / Path(ref).name
            for ref in declared
            if (USAGE / Path(ref).name).exists()
            and contract_of(USAGE / Path(ref).name) == CODEX_CONTRACT
        ]
        summed = {"turns": 0, "calls": 0, "errors": 0, "one_off": 0, "hours": 0.0}
        present = False
        claude_present = False
        for ref in declared:
            path = USAGE / Path(ref).name
            if not path.exists():
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
    owners: dict[str, list[str]] = {}
    for ident, payload in sessions.items():
        for ref in payload.get("resource_rollups") or []:
            owners.setdefault(Path(ref).name, []).append(ident)
    attributed = {name for name in owners if (USAGE / name).exists()}
    orphaned = {path.name for path in USAGE.glob("*.yaml")} - attributed
    measured_ids = sorted({ident for ids in owners.values() for ident in ids})
    codex_names = {
        path.name for path in USAGE.glob("*.yaml") if contract_of(path) == CODEX_CONTRACT
    }
    claude_names = {path.name for path in USAGE.glob("*.yaml")} - codex_names

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
        declared = {Path(r).name for r in (payload.get("resource_rollups") or [])}
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
    for name in [*declared_codex, *orphaned_codex]:
        receipt = codex_receipt_summary(USAGE / name)
        claimants = ", ".join(owners.get(name, [])) or "unattributed"
        lines.append(
            f"| `{name}` | {claimants} | {receipt['model_responses']:,} "
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


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--session", help="report on one session in full")
    parser.add_argument("--log", type=Path, help="the session's harness log, to regenerate")
    parser.add_argument("--agent-logs", type=Path, nargs="*", default=[])
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true", help="verify without writing")
    mode.add_argument("--update", action="store_true", help="regenerate rollups first")
    mode.add_argument("--render", action="store_true", help="write the measured-cost view")
    args = parser.parse_args(argv)

    if args.render:
        REPORT.write_text(render_report(), encoding="utf-8")
        SYNOPSIS.write_text(
            splice_synopsis(SYNOPSIS.read_text(encoding="utf-8")), encoding="utf-8"
        )
        print(f"wrote {REPORT.relative_to(ROOT.parent)} and the {SYNOPSIS.name} view")
        status = report(args.session)
        # Printed here rather than left to a second command anyone can forget. `OR-9` says
        # the pull request leads with what the branch cost, and the moment that block is
        # correct is the moment the rollups are written -- which is now.
        print()
        print("=" * 78)
        print("Paste the block below at the top of the pull request (OR-9).")
        print("=" * 78)
        print()
        print(render_branch_cost(current_branch(), args.session), end="")
        return status

    if args.update:
        if args.log is None:
            print("--update needs --log")
            return 2
        written = regenerate(args.log, list(args.agent_logs))
        print(f"wrote {len(written)} rollups: {', '.join(written) if written else 'none new'}")
        print()

    if args.check:
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

    return report(args.session)


if __name__ == "__main__":
    sys.exit(main())
