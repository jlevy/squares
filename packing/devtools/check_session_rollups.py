#!/usr/bin/env python3
"""Every terminal session names the resource rollups it produced, and they exist.

A session record says what was attempted and what came back. What it never said is what it
cost, and not for want of the data: `campaign/resource-usage/` holds enforced
harness-specific receipts. Nothing joined the two. Claude rollups are named by harness log
id and Codex task-tree intervals by their retained receipt, while sessions use their own
sequence numbers.

**This exists because a reminder was the wrong fix.** Session-045 ran twenty-three phases
without the rollup being written once, and the omission was invisible: no field was empty,
no check failed, and the session closed clean. `OR-1` says the answer to a recurring
measurement gap is a tool rather than a better memory, so the link is now a required field
at terminal state and this checks both its existence and its enforced contract.

Sessions that closed before the field existed are listed as **grandfathered** rather than
silently skipped. A checker that hides what it is not checking is the same failure one level
up.

Usage:
    uv run --frozen python -m devtools.check_session_rollups
"""

from __future__ import annotations

import pathlib
import sys

import yaml

from sqpack.yamlio import safe_load

ROOT = pathlib.Path(__file__).resolve().parent.parent
SESSIONS = ROOT / "campaign" / "agent-sessions"
REPO = ROOT.parent

TERMINAL = {"completed", "stopped"}
SUPPORTED_ROLLUP_CONTRACTS = {
    "packing.squares:ClaudeEfficiencyRollup/v1",
    "packing.squares:CodexTaskTreeDelta/v1",
}

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


def rollup_problem(path: pathlib.Path) -> str | None:
    """Return why a declared resource receipt is not one of the enforced contracts."""
    try:
        document = safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as error:
        return f"cannot be read as YAML: {error}"
    problem: str | None = None
    if not isinstance(document, dict):
        problem = "is not a mapping"
    else:
        meta = document.get("softschema")
        if not isinstance(meta, dict):
            problem = "has no softschema declaration"
        elif meta.get("contract") not in SUPPORTED_ROLLUP_CONTRACTS:
            problem = f"declares unsupported contract {meta.get('contract')!r}"
        elif meta.get("status") != "enforced":
            problem = f"declares status {meta.get('status')!r}, expected 'enforced'"
        else:
            envelope = meta.get("envelope")
            if not isinstance(envelope, str) or not isinstance(document.get(envelope), dict):
                problem = f"declares missing or invalid envelope {envelope!r}"
    return problem


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
            rollup_path = REPO / relative
            if not rollup_path.is_file():
                problems.append(f"{path.name}: declared rollup is missing: {relative}")
            else:
                rollups += 1
                if problem := rollup_problem(rollup_path):
                    problems.append(f"{path.name}: declared rollup {relative} {problem}")

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
