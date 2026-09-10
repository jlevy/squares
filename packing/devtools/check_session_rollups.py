#!/usr/bin/env python3
"""Every terminal session names its resource measurement, and every receipt exists.

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
silently skipped. A stopped session may explicitly say native harness data is unavailable,
but only by naming the reason and the bead that dispositioned the missing source. This
measurement state is independent of certification: a later gate can clear
``certification_pending`` while the honest unmeasured marker remains. The checker reports
that case as unmeasured; it never turns an absent receipt into a measurement. A checker that
hides what it is not checking is the same failure one level up.

Usage:
    uv run --frozen python -m devtools.check_session_rollups
"""

from __future__ import annotations

import functools
import json
import pathlib
import re
import shutil
import subprocess
import sys
from collections.abc import Iterable, Mapping
from typing import Literal

import yaml

from devtools.codex_task_tree_delta import validate_delta_document
from sqpack.yamlio import safe_load

ROOT = pathlib.Path(__file__).resolve().parent.parent
SESSIONS = ROOT / "campaign" / "agent-sessions"
REPO = ROOT.parent
ROLLUP_REFERENCE = re.compile(
    r"packing/campaign/resource-usage/[A-Za-z0-9][A-Za-z0-9._-]*\.yaml"
)
BEAD_REFERENCE = re.compile(r"think-[a-z0-9]+")

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

UNMEASURED_REASON = "native_harness_data_unavailable"
"""The sole reason that can replace a terminal resource receipt.

The value is deliberately an enum of one rather than free text. A new failure mode must
become an explicit contract change instead of quietly broadening the exception.
"""

UNMEASURED_HANDOFF_ROLES = frozenset({"administrative_closeout", "work_handoff"})
"""Explicit handoff roles; prose and session age never decide this distinction."""

type BeadPresence = Literal["present", "missing", "unresolved"]


@functools.cache
def disposition_bead_presence(reference: str) -> BeadPresence:
    """Resolve a short bead id when tbd can answer, without making it a build dependency."""
    if shutil.which("tbd") is None:
        return "unresolved"
    try:
        shown = subprocess.run(
            ("tbd", "show", reference, "--json"),
            capture_output=True,
            text=True,
            check=False,
            cwd=str(REPO),
            timeout=30,
        )
    except OSError, subprocess.SubprocessError:
        return "unresolved"
    try:
        payload = json.loads(shown.stdout or shown.stderr)
    except ValueError:
        return "unresolved"
    presence: BeadPresence = "unresolved"
    if shown.returncode != 0:
        if isinstance(payload, dict) and payload.get("type") == "NotFoundError":
            presence = "missing"
    else:
        issues = payload if isinstance(payload, list) else [payload]
        if any(
            isinstance(issue, dict) and isinstance(issue.get("status"), str) for issue in issues
        ):
            presence = "present"
    return presence


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


def unmeasured_resource_problems(name: str, session: Mapping[str, object]) -> list[str]:
    """Validate the narrow stopped-session declaration for unavailable native data."""
    if "resource_usage_unmeasured" not in session:
        return []
    problems: list[str] = []
    marker = session.get("resource_usage_unmeasured")
    if not isinstance(marker, Mapping):
        return [f"{name}: resource_usage_unmeasured must be a mapping"]
    expected_fields = {"reason", "detail", "disposition_bead", "handoff_role"}
    if set(marker) != expected_fields:
        problems.append(
            f"{name}: resource_usage_unmeasured fields must be exactly "
            f"{sorted(expected_fields)}"
        )
    if session.get("status") != "stopped":
        problems.append(f"{name}: resource_usage_unmeasured is allowed only when stopped")
    stop_reason = session.get("stop_reason")
    if not isinstance(stop_reason, str) or not stop_reason.strip():
        problems.append(f"{name}: resource_usage_unmeasured requires a nonblank stop_reason")
    if session.get("resource_rollups") != []:
        problems.append(
            f"{name}: resource_usage_unmeasured requires an explicit empty "
            "resource_rollups list"
        )
    reason = marker.get("reason")
    if reason != UNMEASURED_REASON:
        problems.append(
            f"{name}: resource_usage_unmeasured reason must be {UNMEASURED_REASON!r}"
        )
    detail = marker.get("detail")
    if not isinstance(detail, str) or not detail.strip():
        problems.append(f"{name}: resource_usage_unmeasured requires a nonblank detail")
    handoff_role = marker.get("handoff_role")
    if handoff_role not in UNMEASURED_HANDOFF_ROLES:
        problems.append(
            f"{name}: resource_usage_unmeasured handoff_role must be one of "
            f"{sorted(UNMEASURED_HANDOFF_ROLES)}"
        )
    owner = marker.get("disposition_bead")
    if not isinstance(owner, str) or BEAD_REFERENCE.fullmatch(owner) is None:
        problems.append(
            f"{name}: resource_usage_unmeasured disposition_bead must name one well-formed bead"
        )
    elif not problems and disposition_bead_presence(owner) == "missing":
        problems.append(
            f"{name}: resource_usage_unmeasured disposition_bead {owner} does not resolve "
            "in the available tbd store"
        )
    return problems


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
    unmeasured: list[str] = []
    records = sessions()
    codex_references: set[str] = set()
    for path, session in records:
        identifier = str(session.get("id", path.stem))
        if "resource_usage_unmeasured" in session:
            marker_problems = unmeasured_resource_problems(path.name, session)
            problems.extend(marker_problems)
            if not marker_problems:
                unmeasured.append(identifier)
            continue
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
    if unmeasured:
        print(
            f"  {len(unmeasured)} stopped sessions explicitly record unavailable "
            "resource measurement: " + ", ".join(unmeasured)
        )
    if grandfathered:
        print(
            f"  {len(grandfathered)} closed before the field existed and are not checked: "
            + ", ".join(grandfathered)
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
