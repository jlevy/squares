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
import re
import sys
from collections.abc import Iterable, Mapping

import yaml

from devtools.codex_task_tree_delta import validate_delta_document
from sqpack.yamlio import safe_load

ROOT = pathlib.Path(__file__).resolve().parent.parent
SESSIONS = ROOT / "campaign" / "agent-sessions"
REPO = ROOT.parent
ROLLUP_REFERENCE = re.compile(
    r"packing/campaign/resource-usage/[A-Za-z0-9][A-Za-z0-9._-]*\.yaml"
)

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


def canonical_resource_rollup_reference(reference: object) -> str | None:
    """Return one canonical repository-relative receipt reference, or refuse it."""
    if not isinstance(reference, str) or not ROLLUP_REFERENCE.fullmatch(reference):
        return None
    return reference


def resource_rollup_path(reference: object) -> pathlib.Path | None:
    """Resolve one canonical receipt reference against the repository root."""
    canonical = canonical_resource_rollup_reference(reference)
    return REPO / canonical if canonical is not None else None


def unique_resource_rollups(session: Mapping[str, object]) -> list[str]:
    """Return declarations once each, preserving their recorded order."""
    declared = session.get("resource_rollups")
    if not isinstance(declared, list):
        return []
    return list(dict.fromkeys(str(reference) for reference in declared))


def codex_branch_claims(
    session_records: Iterable[Mapping[str, object]], codex_references: set[str]
) -> dict[str, dict[str, set[str]]]:
    """Index operator declarations without inventing branch telemetry."""
    claims: dict[str, dict[str, set[str]]] = {}
    for session in session_records:
        identifier = session.get("id")
        branch = session.get("branch")
        if not isinstance(identifier, str) or not isinstance(branch, str) or not branch:
            continue
        for reference in unique_resource_rollups(session):
            if reference not in codex_references:
                continue
            claims.setdefault(reference, {}).setdefault(branch, set()).add(identifier)
    return claims


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
            elif meta.get("contract") == "packing.squares:CodexTaskTreeDelta/v1":
                semantic_problems = validate_delta_document(document)
                if semantic_problems:
                    problem = "fails semantic validation: " + "; ".join(semantic_problems[:3])
    return problem


def main() -> int:
    problems: list[str] = []
    grandfathered: list[str] = []
    checked = 0
    rollups = 0
    records = sessions()
    codex_references: set[str] = set()
    for path, session in records:
        identifier = str(session.get("id", path.stem))
        if str(session.get("status")) not in TERMINAL:
            continue
        raw_declared = session.get("resource_rollups") or []
        declared = unique_resource_rollups(session)
        if isinstance(raw_declared, list) and len(raw_declared) != len(declared):
            problems.append(f"{path.name}: resource_rollups contains duplicate entries")
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
        codex_declared = False
        for relative in declared:
            rollup_path = resource_rollup_path(relative)
            if rollup_path is None:
                problems.append(
                    f"{path.name}: resource_rollups entry is not a canonical receipt path: "
                    f"{relative!r}"
                )
                continue
            if not rollup_path.is_file():
                problems.append(f"{path.name}: declared rollup is missing: {relative}")
            else:
                rollups += 1
                problem = rollup_problem(rollup_path)
                if problem:
                    problems.append(f"{path.name}: declared rollup {relative} {problem}")
                else:
                    document = safe_load(rollup_path.read_text(encoding="utf-8"))
                    meta = document.get("softschema")
                    if meta.get("contract") == "packing.squares:CodexTaskTreeDelta/v1":
                        codex_declared = True
                        codex_references.add(relative)
        if codex_declared and not session.get("branch"):
            problems.append(
                f"{path.name}: terminal session declares a Codex task-tree receipt but no "
                "operator-attributed branch"
            )

    claims = codex_branch_claims((session for _, session in records), codex_references)
    for reference, branches in sorted(claims.items()):
        if len(branches) > 1:
            problems.append(f"Codex rollup {reference} is attributed to more than one branch")

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
    raise SystemExit(main())
