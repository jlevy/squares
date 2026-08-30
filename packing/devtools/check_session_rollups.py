#!/usr/bin/env python3
"""Every terminal session names the resource rollups it produced, and they exist.

A session record says what was attempted and what came back. What it never said is what it
cost, and not for want of the data: `campaign/resource-usage/` holds one
`ClaudeEfficiencyRollup` per agent log. Nothing joined the two. Rollups are named by harness
log id and sessions by their own sequence number, so going from `session-045` to its usage
meant knowing the UUID by heart.

**This exists because a reminder was the wrong fix.** Session-045 ran twenty-three phases
without the rollup being written once, and the omission was invisible: no field was empty,
no check failed, and the session closed clean. `OR-1` says the answer to a recurring
measurement gap is a tool rather than a better memory, so the link is now a required field
at terminal state and this is what enforces it.

Sessions that closed before the field existed are listed as **grandfathered** rather than
silently skipped. A checker that hides what it is not checking is the same failure one level
up.

Usage:
    uv run --frozen python -m devtools.check_session_rollups
"""

from __future__ import annotations

import pathlib
import sys

from sqpack.yamlio import safe_load

ROOT = pathlib.Path(__file__).resolve().parent.parent
SESSIONS = ROOT / "campaign" / "agent-sessions"
REPO = ROOT.parent

TERMINAL = {"completed", "stopped"}

GRANDFATHERED_BEFORE = "session-045"
"""Sessions numbered below this closed before `resource_rollups` existed.

Named as a boundary rather than a list so the exemption cannot quietly grow: a new session
is above it by construction, and moving it is a visible edit.
"""


def sessions() -> list[tuple[pathlib.Path, dict]]:
    found = []
    for path in sorted(SESSIONS.glob("session-*.md")):
        text = path.read_text(encoding="utf-8")
        if not text.startswith("---\n"):
            continue
        payload = safe_load(text.split("---\n")[1])
        if isinstance(payload, dict) and "session" in payload:
            found.append((path, payload["session"]))
    return found


def main() -> int:
    problems: list[str] = []
    grandfathered: list[str] = []
    checked = 0
    rollups = 0
    for path, session in sessions():
        identifier = str(session.get("id", path.stem))
        if str(session.get("status")) not in TERMINAL:
            continue
        declared = session.get("resource_rollups") or []
        if identifier < GRANDFATHERED_BEFORE and not declared:
            grandfathered.append(identifier)
            continue
        if not declared:
            problems.append(
                f"{path.name}: terminal session declares no resource_rollups; run "
                "`python -m devtools.log_rollup <log>.jsonl --out campaign/resource-usage` "
                "for the session log and every sub-agent transcript, then list them here"
            )
            continue
        checked += 1
        for relative in declared:
            if not (REPO / relative).is_file():
                problems.append(f"{path.name}: declared rollup is missing: {relative}")
            else:
                rollups += 1

    for line in problems:
        print(f"FAIL {line}", file=sys.stderr)
    if problems:
        return 1
    print(f"  {checked} terminal sessions declare {rollups} resource rollups, all present")
    if grandfathered:
        print(
            f"  {len(grandfathered)} closed before the field existed and are not checked: "
            + ", ".join(grandfathered)
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
