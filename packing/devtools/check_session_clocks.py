#!/usr/bin/env python3
"""Refuse a session artifact that declares a clock it cannot have read.

`D-358` recorded an unattended run misreading its own clock by a factor of four -- blocks
declared at 150, 180, 180 and 40 minutes that the commit timestamps put at 31, 42, 29 and
23 -- and its `regression` field said, honestly, "None automatic". On 2026-08-30 the same
session family did it again: `session-045` declared two phases starting at `10:16Z` and
`11:10Z` while the clock read `09:52Z`. Twice is a pattern and the second one is what this
file is.

What is refused is only what cannot be true, and the line is drawn deliberately.

**Refused: a start time later than the moment of checking.** A session records what it did,
so a phase cannot have begun after the record of it was written. This is the exact shape of
both occurrences, and it is safe to anchor on the wall clock precisely because the bound is
monotone -- a timestamp in the past stays in the past, so a run that passes today cannot
fail tomorrow for having drifted. A deadline at or before its own start is refused on the
same ground: no run fits in it.

**Reported, never refused: starts that run backwards between consecutive phases.** This
looked like an obvious second refusal and is not. `session-044`'s phase 7 begins thirteen
minutes before phase 6 because it *ran as a delegated lane against a worktree branched from
this branch's head*, and was integrated afterwards. Position in the file is authoring
order, not wall-clock order, and the record carries no field distinguishing the two. So it
is printed with the reason rather than failed, and the day a `delegated` marker exists this
can be tightened.

**Reported, never refused: phases carrying no clock at all.** `started_at` is nullable and
most sessions before 2026-08-29 leave it so. The count of phases actually carrying a clock
is printed, because a check whose coverage is invisible is a check that can quietly stop
covering anything.

**Reported, never refused: elapsed against budget.** A phase's elapsed time is the next
phase's start minus its own, which the record already determines. Printing it beside
`budget_minutes` is what would have made `D-358` visible while it was happening -- that run
declared 150 minutes and its own successive timestamps said 31. A budget is an estimate and
overrunning one is not a defect, so this is output, not a gate.

Usage:
    uv run --frozen --all-extras --group dev python -m devtools.check_session_clocks
"""

from __future__ import annotations

import argparse
import pathlib
import sys
from dataclasses import dataclass
from datetime import UTC, datetime

from sqpack.yamlio import safe_load

ROOT = pathlib.Path(__file__).resolve().parent.parent
SESSIONS = ROOT / "campaign" / "agent-sessions"


@dataclass(frozen=True, slots=True)
class Phase:
    index: int
    workflow: str
    status: str
    started_at: datetime | None
    deadline_at: datetime | None
    budget_minutes: float | None


def _moment(value: object) -> datetime | None:
    if not isinstance(value, str) or not value:
        return None
    return datetime.fromisoformat(value)


def session_record(path: pathlib.Path) -> dict[str, object]:
    """The `session` frontmatter of one artifact."""
    text = path.read_text(encoding="utf-8")
    return safe_load(text.split("---", 2)[1])["session"]


def phases(record: dict[str, object]) -> list[Phase]:
    declared = record.get("workflow_phases") or record.get("phases") or []
    if not isinstance(declared, list):
        return []
    return [
        Phase(
            index=index,
            workflow=str(phase.get("workflow", "?")),
            status=str(phase.get("status", "?")),
            started_at=_moment(phase.get("started_at")),
            deadline_at=_moment(phase.get("deadline_at")),
            budget_minutes=(
                float(phase["budget_minutes"])
                if isinstance(phase.get("budget_minutes"), int | float)
                else None
            ),
        )
        for index, phase in enumerate(declared)
        if isinstance(phase, dict)
    ]


def violations(name: str, record: dict[str, object], now: datetime) -> list[str]:
    """What cannot be true about this artifact's clock. Refusals only; see the reports."""
    found: list[str] = []
    opened = _moment(record.get("started_at"))
    if opened is not None and opened > now:
        found.append(
            f"{name}: session starts at {opened:%Y-%m-%dT%H:%M:%SZ}, which is ahead of now"
        )

    for phase in phases(record):
        label = f"{name} phase {phase.index + 1} ({phase.workflow})"
        if phase.started_at is None:
            continue
        if phase.started_at > now:
            found.append(
                f"{label}: starts at {phase.started_at:%Y-%m-%dT%H:%M:%SZ}, ahead of now -- "
                "a phase cannot have begun after the record of it was written (D-358)"
            )
        if opened is not None and phase.started_at < opened:
            found.append(f"{label}: starts before the session it belongs to")
        if phase.deadline_at is not None and phase.deadline_at <= phase.started_at:
            found.append(f"{label}: deadline is not after its own start, so no run fits it")
    return found


def remarks(name: str, record: dict[str, object]) -> list[str]:
    """Clock oddities that a legitimate record can have. Printed, never failed."""
    found: list[str] = []
    previous: Phase | None = None
    for phase in phases(record):
        if (
            previous is not None
            and previous.started_at is not None
            and phase.started_at is not None
            and phase.started_at < previous.started_at
        ):
            found.append(
                f"{name} phase {phase.index + 1} starts before phase {previous.index + 1}; "
                "a delegated lane run in a worktree does this legitimately"
            )
        previous = phase
    return found


def elapsed_report(record: dict[str, object], now: datetime) -> list[str]:
    """Declared budget against the elapsed time the record's own timestamps imply."""
    lines: list[str] = []
    declared = phases(record)
    for position, phase in enumerate(declared):
        if phase.started_at is None:
            continue
        following = declared[position + 1] if position + 1 < len(declared) else None
        ended = following.started_at if following and following.started_at else now
        minutes = (ended - phase.started_at).total_seconds() / 60
        budget = f"{phase.budget_minutes:.0f}" if phase.budget_minutes else "--"
        marker = "  " if phase.status != "in_progress" else "* "
        lines.append(
            f"    {marker}phase {phase.index + 1:>2} {phase.workflow:<22} "
            f"{minutes:6.0f} min against a budget of {budget:>4}"
        )
    return lines


def audit(*, verbose: bool) -> int:
    now = datetime.now(UTC)
    paths = sorted(SESSIONS.glob("session-[0-9][0-9][0-9]-*.md"))
    if not paths:
        print("  no session artifacts found", file=sys.stderr)
        return 1

    problems: list[str] = []
    notes: list[str] = []
    clocked = 0
    counted = 0
    for path in paths:
        record = session_record(path)
        problems.extend(violations(path.name, record, now))
        notes.extend(remarks(path.name, record))
        declared = phases(record)
        counted += len(declared)
        clocked += sum(1 for phase in declared if phase.started_at is not None)

    if problems:
        for problem in problems:
            print(f"  {problem}", file=sys.stderr)
        return 1

    print(
        f"  {len(paths)} session artifacts, {counted} phases, {clocked} carrying a clock: "
        "every declared start is one that could have been read"
    )
    for note in notes:
        print(f"  note: {note}")
    if verbose:
        latest = paths[-1]
        print(f"  elapsed against budget in {latest.name}:")
        for line in elapsed_report(session_record(latest), now):
            print(line)
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--review", action="store_true", help="also print elapsed against budget"
    )
    return audit(verbose=parser.parse_args().review)


if __name__ == "__main__":
    sys.exit(main())
