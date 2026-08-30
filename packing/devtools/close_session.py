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

`--check` verifies without writing, which is what a gate would call. `--update` regenerates
the rollups first. Neither invents an attribution: a sub-agent log is matched to a session
by its `span` against the session's own window, and anything outside every window is
listed rather than guessed at.

Usage, from `packing/`:
    uv run --frozen --all-extras --group dev python -m devtools.close_session --check
    uv run --frozen --all-extras --group dev python -m devtools.close_session \
        --update --session session-047 --log <path-to-session>.jsonl
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from datetime import datetime
from pathlib import Path

from devtools.check_session_rollups import GRANDFATHERED_BEFORE
from sqpack.yamlio import safe_load

ROOT = Path(__file__).resolve().parent.parent
SESSIONS = ROOT / "campaign" / "agent-sessions"
USAGE = ROOT / "campaign" / "resource-usage"

TERMINAL = {"completed", "stopped"}


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

    def parse(value: object) -> datetime | None:
        if not isinstance(value, str):
            return None
        try:
            return datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError:
            return None

    return parse(span.get("started_at")), parse(span.get("ended_at"))


def totals(path: Path) -> dict[str, object]:
    document = safe_load(path.read_text(encoding="utf-8"))
    rollup = document.get("rollup") or document
    turns = rollup.get("turns") or {}
    calls = rollup.get("tool_calls") or {}
    span = rollup.get("span") or {}
    return {
        "turns": turns.get("assistant"),
        "calls": calls.get("total"),
        "errors": calls.get("errors"),
        "one_off": (calls.get("one_off_code") or {}).get("count"),
        "hours": round((span.get("wall_seconds") or 0) / 3600, 2) or None,
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


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--session", help="report on one session in full")
    parser.add_argument("--log", type=Path, help="the session's harness log, to regenerate")
    parser.add_argument("--agent-logs", type=Path, nargs="*", default=[])
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true", help="verify without writing")
    mode.add_argument("--update", action="store_true", help="regenerate rollups first")
    args = parser.parse_args(argv)

    if args.update:
        if args.log is None:
            print("--update needs --log")
            return 2
        written = regenerate(args.log, list(args.agent_logs))
        print(f"wrote {len(written)} rollups: {', '.join(written) if written else 'none new'}")
        print()

    return report(args.session)


if __name__ == "__main__":
    sys.exit(main())
