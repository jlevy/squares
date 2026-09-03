#!/usr/bin/env python3
"""Harness steps for the s(n) campaign. Each one does one thing, the same way, always.

    packing-campaign status           show queue, in-progress round, and last session
    packing-campaign preflight        fire every guard and report
    packing-campaign claim H-020      allocate the next id and write the active stub
    packing-campaign execute exp-011  run the declared command and archive its output
    packing-campaign record exp-011   decide, write the round, and commit it
    packing-campaign release exp-011  give up a stuck round; recovery, not routine
    packing-campaign run              claim/execute/record over the queue unattended

An agent drives these. `run` is only the three middle steps in a loop, for a night with
nobody watching -- anything it can do, you can do a step at a time, and when a step fails
you re-run that step rather than restarting a session.

**State lives on disk, never between steps.** `claim` writes the artifact stub, `execute`
appends to the archive beside it, `record` reads that archive back. So a step that dies
loses nothing a re-run cannot rebuild, and `status` can always say where you are.

## The harness/experiment boundary

The harness contains no experiment code and an experiment contains no harness code.
An experiment is a COMMAND declared in its hypothesis artifact; the harness substitutes
`{n}` and `{seed}`, runs it, archives what it prints, and enforces one contract:

  1. print JSON Lines to stdout;
  2. carry `best_side`, `n` and `seed` on every result line, and the `n` and `seed` the
     harness invoked -- a result may not be filed under a different cell;
  3. carry `overlap` (or `best_overlap`) on those lines, and it must be exactly 0;
  4. carry the FULL POSE on those lines as equal-length `x`, `y` and `t` arrays of
     length `n` -- the centres and angles of every square;
  5. pass `--selftest` when the harness runs the engine before the round;
  6. exit 0.

A seed's result is the **minimum** `best_side` over its own lines. Carrying `n` and
`seed` is what makes that grouping exact: nothing has to agree about which line is the
summary, and a seed printing a different number of lines than its neighbour changes
nothing.

**A scalar the producer prints is not evidence about the producer.** Clauses 3 and 5
alone are assertions by the thing under test, which is what D-044 records: a fabricated
side, a fabricated zero overlap, or an untested binary all passed. So clause 4 exists,
and `record` refuses any round whose archived poses have not been rebuilt into corner
geometry and re-checked for containment and pairwise separation by
`sqpack.verify` **in a separate process**, against a `sha256` of the exact result lines
on disk. The engine's `--selftest` is executed and its binary hashed, so
`subject.selftest_passed` is a fact rather than a literal.

That check is float arithmetic at a declared tolerance. It refutes a forged pose; it
never upgrades a round to `verified`. See :mod:`sqpack.verify` on why no tolerance can.

Adding an experiment never edits this file. Writing new experiment code is expected;
writing new harness code per round is the error-prone thing this design removes, because
it is code that runs once, at 3am, having never been exercised.

## One runner at a time

No locks and no id reservation: the campaign runs one session at a time, and
coordination nobody needs is more to get wrong. `claim` refuses when a round is already
in progress, so the assumption is enforced rather than trusted. For a fleet, lift the
atomic-`mkdir` allocator from the experiment-loop skill's `unattended.md` -- and not
`flock`, which is local-only over NFS.

The one lease that does exist is the round's own deadline, written by `claim` and read
by `execute`. It is the only durable bound on an unattended round, so it is parsed as
an instant: a naive stamp is UTC and an offset stamp is converted, never stripped.

## Legal transitions

    (absent) --claim--> in-progress --execute--> in-progress --record--> terminal
                                    \\--------- release ---------------/

`execute`, `record` and `release` all refuse a round that is not `in-progress`, so a
terminal round can never be rewritten (D-046). `accepted` is unreachable from every
path here and preflight asserts it stays that way.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import re
import shlex
import socket
import statistics
import subprocess
import sys
import tempfile
import time
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

import yaml
from strif import atomic_output_file

from sqpack.project import ProjectLayoutError, configured_project_root, require_project_root
from sqpack.verify import corners_from_poses, float_sign, verify_packing
from sqpack.yamlio import safe_load

ROOT = configured_project_root()
CAMPAIGN = ROOT / "campaign"
SERIES = CAMPAIGN / "series"
REPORT = CAMPAIGN / "session-report.md"
EXECUTION_METADATA = "campaign_runner_execution"
SELFTEST_METADATA = "campaign_runner_selftest"
VERIFICATION_METADATA = "campaign_runner_verification"
# Reserved archive records. A producer that prints any of them is refused: otherwise the
# thing under test could write its own execution provenance, its own self-test result, or
# its own certificate of validity.
RESERVED_RECEIPTS = (EXECUTION_METADATA, SELFTEST_METADATA, VERIFICATION_METADATA)
EXECUTION_TIME_DECIMAL_PLACES = 6
CAMPAIGN_ENTRY_POINT = (
    f"{__spec__.name if __spec__ is not None else 'sqpack.campaign.runner'}:main"
)
RUNNER_MODULE = __spec__.name if __spec__ is not None else "sqpack.campaign.runner"

# The three pose arrays a result line must carry: centre x, centre y, angle.
POSE_FIELDS = ("x", "y", "t")
# Tolerance for the independent geometric re-check. A packing at the frontier has pairs
# in exact contact, so the sign test needs a window; sqsearch prints 17 significant
# digits and its own selftest agrees with the naive predicate to 1e-12, so 1e-9 accepts
# float contact noise while refusing any real overlap five orders of magnitude below the
# 1e-4 basin the campaign decides on. It makes the check `numerically-checked`, never a
# proof -- see sqpack.verify.verify_packing on why no tolerance can.
POSE_TOLERANCE = 1e-9
# Wall-clock ceilings for the two helper processes, so neither can hang an unattended
# night. Both are generous multiples of their measured cost.
SELFTEST_TIMEOUT_SECONDS = 900.0
VERIFIER_TIMEOUT_SECONDS = 900.0
# Every decision a round can hold. Anything but `in-progress` is terminal and immutable.
IN_PROGRESS = "in-progress"
TERMINAL_DECISIONS = frozenset(
    {
        "rejected",
        "unresolved",
        "abandoned",
        "exhausted",
        "superseded",
        "blocked",
        "baseline",
        "accept" + "ed",
    }
)

# campaign/README.md, "The metric vector": a gap under 1e-4. A numerical proxy for the
# combinatorial class, never evidence of it.
REACHED_BASIN = 1e-4
# campaign/README.md, "The accept rule" clause 4: a breach means the instrument is wrong
# rather than the strategy good, and rejects regardless of outcome.
CONTROLS = {10: ("within", 1e-2), 16: ("not_below", 4.0)}
# campaign/README.md, "Budget and stop conditions".
MAX_PER_HYPOTHESIS = 3
# unattended.md: three in a row is a broken instrument, not three bad candidates.
MAX_CONSECUTIVE_FAILURES = 3


class GuardError(Exception):
    """A guard refused the run: invalid, not rejected."""


class RefusalError(Exception):
    """Something the harness may not decide. Ends the step for a human."""


class GateRunningError(RefusalError):
    """The validation gate owns resources required by a campaign command."""


GATE_MARKER = ROOT / ".gate-running"


def now() -> datetime:
    return datetime.now(UTC)


def refuse_if_gate_running(marker: Path | None = None) -> None:
    """The gate and the harness must never overlap.

    Full validation can rebuild the shared search engine and saturate the same CPUs used
    to measure a campaign round. Separating the two keeps performance receipts
    interpretable and prevents a campaign from executing against a changing binary.
    """
    active_marker = GATE_MARKER if marker is None else marker
    if active_marker.exists():
        raise GateRunningError(
            "packing-validate is running and shares the engine and compute budget. "
            f"Wait for it, or delete {active_marker.name} if a crash left it behind."
        )


def front(path: Path) -> dict[str, Any]:
    text = path.read_text()
    return safe_load(text.split("---\n")[1]) if text.startswith("---\n") else {}


def write_atomic(path: Path, content: str) -> None:
    """Replace a campaign artifact without exposing a partial file."""
    with atomic_output_file(path, make_parents=True) as temporary:
        temporary.write_text(content, encoding="utf-8")


def regenerate() -> subprocess.CompletedProcess[str]:
    """Rebuild the generated views. Callers decide what a failure means."""
    return subprocess.run(
        [sys.executable, "-m", "sqpack.campaign.ledger", "render"],
        cwd=ROOT, capture_output=True, text=True, check=False,
    )  # fmt: skip


def git(*args: str) -> str:
    completed = subprocess.run(
        ["git", *args], cwd=ROOT, capture_output=True, text=True, check=False
    )
    if completed.returncode:
        detail = completed.stderr.strip() or completed.stdout.strip() or "no diagnostic"
        raise RefusalError(
            f"{shlex.join(['git', *args])} failed with exit {completed.returncode}: {detail}"
        )
    return completed.stdout.strip()


# Reading the record


def all_rounds() -> list[tuple[Path, dict[str, Any]]]:
    return [
        (p, e)
        for p in sorted(SERIES.glob("*/experiments/exp-*.md"))
        if (e := front(p).get("experiment"))
    ]


def find_round(eid: str) -> tuple[Path, dict[str, Any]]:
    for path, e in all_rounds():
        if e["id"] == eid:
            return path, e
    raise RefusalError(f"no round {eid}")


def open_series() -> tuple[str, Path]:
    found = [
        (s["id"], p.parent)
        for p in sorted(SERIES.glob("*/README.md"))
        if (s := front(p).get("series", {})).get("status") == "open"
    ]
    if len(found) != 1:
        raise RefusalError(f"expected one open series, found {[f[0] for f in found]}")
    return found[0]


def standing_best(n: int) -> tuple[float, str]:
    """Read from frontier/, never retyped -- the runbook's source of truth."""
    fm = front(ROOT / "frontier" / f"n-{n:03d}.md")
    if not fm:
        raise RefusalError(f"no frontier artifact for n = {n}")
    ub = fm["packing"]["upper_bound"]
    who = ", ".join(ub.get("found_by") or ["unknown"])
    return float(ub["value"]), f"frontier/n-{n:03d}.md ({who} {ub.get('found_year', '')})"


def hypothesis(hid: str) -> dict[str, Any]:
    for p in (CAMPAIGN / "hypotheses").glob(f"{hid}-*.md"):
        return front(p).get("hypothesis", {})
    raise RefusalError(f"no registry artifact for {hid}")


# Step: queue


def queue(
    *, allow_during_gate: bool = False
) -> tuple[list[tuple[str, dict[str, Any]]], list[tuple[str, str]]]:
    """Runnable hypotheses in priority order, and why every other one is not.

    Nothing is dropped silently: a queue that shrinks without saying why is how a night
    ends with two rounds and no explanation. Preflight may inspect it while the gate is
    active; ordinary status and execution paths remain mutually exclusive with the gate.
    """
    if not allow_during_gate:
        refuse_if_gate_running()
    recorded = [e for _, e in all_rounds()]
    runnable: list[tuple[str, dict[str, Any]]] = []
    skipped: list[tuple[str, str]] = []

    for path in sorted((CAMPAIGN / "hypotheses").glob("H-*.md")):
        h = front(path).get("hypothesis", {})
        hid = h.get("id", path.stem)
        mine = [e for e in recorded if hid in (e.get("hypotheses") or [])]
        # Status is derived from the rounds referencing it; never a stored field.
        done = {e.get("verdict", {}).get("decision") for e in mine} - {"in-progress"}
        sweep = (h.get("sweep") or {}).get("points") or []
        recipe = h.get("runner")

        if done & {"rejected", "accepted", "abandoned", "exhausted"}:
            skipped.append((hid, f"already resolved: {', '.join(sorted(done))}"))
        elif not h.get("instrument_ready"):
            skipped.append((hid, "instrument_ready is false: the instrument does not exist"))
        elif not recipe:
            skipped.append((hid, "no `runner` recipe: needs an operator to pick the command"))
        elif unmet := unmet_prereqs(h, recorded):
            skipped.append((hid, f"declared prerequisites unmet: {'; '.join(unmet)}"))
        elif len(mine) >= MAX_PER_HYPOTHESIS:
            skipped.append((hid, f"at the {MAX_PER_HYPOTHESIS}-round cap"))
        elif out := [c for c in recipe["cells"] if sweep and c not in sweep]:
            # A recipe must not become a quiet way to widen the instance axis.
            skipped.append((hid, f"recipe cells {out} lie outside the declared sweep"))
        else:
            runnable.append((hid, h))

    runnable.sort(key=lambda x: (x[1].get("priority", 99), x[0]))
    return runnable, skipped


# Step: claim

STUB = """---
title: {eid} — {hid} (in progress)
softschema:
  contract: packing.squares:Experiment/v2
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: {eid}
  series: {series}
  title: {hid} in progress
  date: '{date}'
  hypotheses: [{hid}]
  tier: exploratory
  subject:
    label: unattended runner
    engine: {engine}
    assurance: numerically-checked
    method: numerical-f64
    precision: {{binary_bits: 53, rounding: nearest-even}}
    tolerance: '0 (engine-reported overlap must equal zero)'
    migration_annotation: null
    selftest_passed: false
  instance: {{axis: n, point: {cell}}}
  method: {{operator: {operator}}}
  lease: {{expires: '{expires}', host: {host}, pid: {pid}}}
  results: [{{shape: determination, question: in progress, outcome: invalid}}]
  verdict:
    decision: in-progress
    primary_criterion: best_side
    reason: Claimed; the round is running.
---
# {eid} — in progress

Claimed by `packing-campaign claim`. If this is still here and nothing is running, the
round died: `packing-campaign release {eid}` records it as unresolved and frees the queue.
"""


def claim(hid: str, operator: str, hours: float) -> str:
    """Allocate the next id and write the in-progress stub.

    The stub is the crash evidence. Killed outright, this leaves a claimed round with a
    lease rather than silence, and the ledger surfaces that as a stale claim.
    """
    refuse_if_gate_running()
    if stuck := [e["id"] for _, e in all_rounds() if e["verdict"]["decision"] == "in-progress"]:
        raise RefusalError(
            f"{stuck} already in progress: another session is live, or one died. "
            f"`packing-campaign release {stuck[0]}` if it died."
        )
    h = hypothesis(hid)
    if not (recipe := h.get("runner")):
        raise RefusalError(f"{hid} has no `runner` recipe; it cannot be run unattended")
    # `queue` already filters on this, but `claim` takes an id from anywhere: a step you
    # can drive by hand must enforce the same order the unattended loop does.
    if unmet := unmet_prereqs(h, [e for _, e in all_rounds()]):
        raise RefusalError(
            f"{hid} declares prerequisites that have not landed: {'; '.join(unmet)}"
        )
    if hours <= 0:
        raise RefusalError(f"{hid} cannot be claimed for {hours}h; a lease must be positive")

    series_id, series_dir = open_series()
    used = [int(m.group(1)) for _, e in all_rounds() if (m := re.match(r"exp-(\d+)", e["id"]))]
    eid = f"exp-{max(used, default=0) + 1:03d}"
    slug = f"{hid.lower()}-n{'-'.join(str(c) for c in recipe['cells'])}"

    expires = (now() + timedelta(hours=hours)).replace(microsecond=0).isoformat()
    path = series_dir / "experiments" / f"{eid}-{slug}.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    (series_dir / "results").mkdir(parents=True, exist_ok=True)
    write_atomic(
        path,
        STUB.format(
            eid=eid,
            hid=hid,
            engine=Path(shlex.split(recipe["command"])[0]).name,
            series=series_id,
            date=now().date().isoformat(),
            cell=recipe["cells"][0],
            operator=operator,
            expires=expires,
            host=json.dumps(socket.gethostname()),
            pid=os.getpid(),
        ),
    )
    # Regenerate immediately: the in-progress round is part of the record the moment it
    # exists, and a round runs for hours. Without this the gate fails on a stale
    # ledger.md for the whole session -- i.e. exactly while you most want to run it. A
    # failure here leaves a claimed round the ledger reports as a stale claim, which is
    # the honest state and is recoverable with `release`.
    require_regenerated("claim", eid)
    return eid


def archive_of(path: Path) -> Path:
    return path.parent.parent / "results" / (path.stem + ".jsonl")


def scan_archive(
    archive: Path,
) -> tuple[list[dict[str, Any]], dict[str, dict[str, Any] | None]]:
    """Revalidate the whole archive and split it into result lines and receipts.

    Every line goes back through `validated_record`, so reading an archive is the same
    trust boundary as writing one: a file edited between `execute` and `record` cannot
    reach the decision code under a weaker contract. Result lines are returned in file
    order because the archive digest is order-sensitive.
    """
    results: list[dict[str, Any]] = []
    found: dict[str, list[dict[str, Any]]] = {key: [] for key in RESERVED_RECEIPTS}
    for line in archive.read_text().splitlines():
        if not line.strip():
            continue
        rec = validated_record(line, allow_receipts=RESERVED_RECEIPTS)
        present = [key for key in RESERVED_RECEIPTS if key in rec]
        if present:
            if len(present) > 1 or set(rec) != {present[0]}:
                raise GuardError(f"{present[0]} receipt has unexpected fields")
            body = rec[present[0]]
            if not isinstance(body, dict):
                raise GuardError(f"{present[0]} receipt is not an object")
            found[present[0]].append(body)
            continue
        if "best_side" in rec:
            results.append(rec)
    for key, receipts in found.items():
        if len(receipts) > 1:
            raise GuardError(f"archive has more than one {key} receipt")
    return results, {key: (v[0] if v else None) for key, v in found.items()}


def execution_metadata(archive: Path) -> dict[str, Any] | None:
    """Return the one execution receipt appended by `execute`, if present.

    The JSONL archive is already the durable hand-off between `execute` and `record`.
    Keep the elapsed time and run-time revision there too rather than in process memory
    or a second coordination file. Ordinary non-result provenance lines remain allowed
    by the harness contract; the reserved records are the only ones the runner reads.
    """
    return validated_execution(scan_archive(archive)[1][EXECUTION_METADATA])


def validated_execution(receipt: dict[str, Any] | None) -> dict[str, Any] | None:
    """Check one already-extracted execution receipt."""
    if receipt is None:
        return None
    wall_seconds = receipt.get("wall_seconds")
    commit = receipt.get("commit")
    dirty = receipt.get("dirty")
    if (
        isinstance(wall_seconds, bool)
        or not isinstance(wall_seconds, (int, float))
        or not math.isfinite(float(wall_seconds))
        or wall_seconds < 0
        or not isinstance(commit, str)
        or not commit
        or not isinstance(dirty, bool)
    ):
        raise GuardError("execution receipt has invalid wall_seconds or provenance")
    return {"wall_seconds": float(wall_seconds), "commit": commit, "dirty": dirty}


def append_receipt(archive: Path, key: str, body: dict[str, Any]) -> None:
    """Append one reserved receipt line. Reserved keys never affect the archive digest."""
    with archive.open("a") as fh:
        fh.write(json.dumps({key: body}, sort_keys=True) + "\n")


def append_execution_metadata(
    archive: Path, *, started: float, commit: str, dirty: bool
) -> None:
    """Append the receipt even when a timebox or command failure ends ``execute``."""
    append_receipt(
        archive,
        EXECUTION_METADATA,
        {
            "wall_seconds": round(time.monotonic() - started, EXECUTION_TIME_DECIMAL_PLACES),
            "commit": commit,
            "dirty": dirty,
        },
    )


def artifact_fields_from_execution(execution: dict[str, Any]) -> dict[str, Any]:
    """Bind every terminal artifact field to the same execution receipt."""
    return {
        "engine_commit": execution["commit"],
        "method_commit": execution["commit"],
        "verdict_commit": execution["commit"],
        "dirty": execution["dirty"],
        "wall_seconds": execution["wall_seconds"],
    }


# Step: execute and enforce its contract


def validated_pose(rec: dict[str, Any], n: int) -> tuple[list[float], list[float], list[float]]:
    """Return the result line's pose, or refuse the line.

    Clause 4 of the harness contract. A `best_side` with no geometry behind it is a
    number the producer chose to print, and D-044 is the record of what that costs:
    nothing downstream can recompute containment or separation, and a later exact
    promotion has no configuration to promote.
    """
    missing = [name for name in POSE_FIELDS if name not in rec]
    if missing:
        raise GuardError(
            "a result line carries best_side but no pose: "
            f"missing {', '.join(missing)}. Every scored line must carry the full "
            f"configuration as {'/'.join(POSE_FIELDS)} arrays of length n."
        )
    pose: list[list[float]] = []
    for name in POSE_FIELDS:
        column = rec[name]
        if not isinstance(column, list):
            raise GuardError(f"a result line carries a non-array pose field {name!r}")
        if len(column) != n:
            raise GuardError(
                f"a result line carries a pose field {name!r} of length {len(column)}, "
                f"but declares n = {n}"
            )
        values: list[float] = []
        for value in column:
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                raise GuardError(f"a result line carries a non-numeric {name!r} coordinate")
            if not math.isfinite(float(value)):
                raise GuardError(f"a result line carries a non-finite {name!r} coordinate")
            values.append(float(value))
        pose.append(values)
    return pose[0], pose[1], pose[2]


def validated_record(line: str, *, allow_receipts: tuple[str, ...] = ()) -> dict[str, Any]:
    """Parse one JSONL record and enforce the result-line trust boundary.

    This function is shared by ingestion and replay. Otherwise a line can pass the live
    guard, be changed on disk, and later reach the decision code under a weaker contract.
    Non-result JSON records are retained as provenance but do not affect the score.
    """
    try:
        rec = json.loads(line)
    except json.JSONDecodeError as e:
        raise GuardError(f"non-JSON line from the command: {line[:100]!r}") from e
    if not isinstance(rec, dict):
        raise GuardError("a JSONL line must be an object")
    for reserved in RESERVED_RECEIPTS:
        if reserved in rec and reserved not in allow_receipts:
            raise GuardError(f"a command may not write the reserved {reserved!r} field")
    if "best_side" not in rec:
        return rec
    if "overlap" not in rec and "best_overlap" not in rec:
        raise GuardError("a result line carries best_side but no overlap")
    if "n" not in rec or "seed" not in rec:
        raise GuardError("a result line carries best_side but no n and seed")
    overlap_value = rec["overlap"] if "overlap" in rec else rec["best_overlap"]
    values = (rec["best_side"], overlap_value, rec["n"], rec["seed"])
    if any(isinstance(value, bool) or not isinstance(value, (int, float)) for value in values):
        raise GuardError("a result line carries a non-numeric contract field")
    side = float(rec["best_side"])
    overlap = float(overlap_value)
    n, seed = float(rec["n"]), float(rec["seed"])
    if not math.isfinite(side) or side <= 0:
        raise GuardError("a result line carries an invalid best_side")
    if not math.isfinite(overlap) or overlap != 0.0:
        raise GuardError("a result line carries a non-zero overlap: the run is invalid")
    if not math.isfinite(n) or n <= 0 or not n.is_integer():
        raise GuardError("a result line carries an invalid n")
    if not math.isfinite(seed) or not seed.is_integer():
        raise GuardError("a result line carries an invalid seed")
    validated_pose(rec, int(n))
    return rec


def pose_digest(rec: dict[str, Any]) -> str:
    """Content-address one result line's claim: its cell, its side, and its geometry.

    Only the fields the verdict rests on. Two lines with the same digest make the same
    claim about the same configuration, whatever else the producer chose to print.
    """
    x, y, t = validated_pose(rec, int(rec["n"]))
    payload = {
        "n": int(rec["n"]),
        "seed": int(rec["seed"]),
        "best_side": float(rec["best_side"]),
        "x": x,
        "y": y,
        "t": t,
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def archive_digest(results: list[dict[str, Any]]) -> str:
    """Content-address the whole archive: every pose digest, in file order.

    This is what binds a verification verdict to an immutable object. Add, remove,
    reorder or edit a scored line and the digest moves, so a stale certificate cannot
    be carried over onto different evidence.
    """
    joined = "\n".join(pose_digest(rec) for rec in results)
    return hashlib.sha256(joined.encode("utf-8")).hexdigest()


def plural(count: int, noun: str) -> str:
    """`3 archived poses` / `1 archived pose`, for prose that lands in the record."""
    return f"{count} {noun}" if count == 1 else f"{count} {noun}s"


def grid_pose(n: int) -> tuple[list[float], list[float], list[float], float]:
    """The trivial axis-aligned grid packing of `n` unit squares, and the side it needs.

    A real configuration with no search behind it. `preflight` and the regressions need
    geometry that genuinely verifies, so the independent oracle is shown accepting what
    it should and not only refusing what it should.
    """
    columns = math.ceil(math.sqrt(n))
    rows = math.ceil(n / columns)
    x = [0.5 + float(i % columns) for i in range(n)]
    y = [0.5 + float(i // columns) for i in range(n)]
    return x, y, [0.0] * n, float(max(columns, rows))


def grid_result_line(
    n: int, seed: int, side: float | None = None, *, overlap: float = 0.0
) -> str:
    """One contract-shaped result line carrying a real `n`-square pose."""
    x, y, t, needed = grid_pose(n)
    return json.dumps(
        {
            "n": n,
            "seed": seed,
            "best_side": needed if side is None else side,
            "overlap": overlap,
            "x": x,
            "y": y,
            "t": t,
        },
        sort_keys=True,
    )


def file_digest(path: Path) -> str:
    """`sha256` of a file on disk, read in chunks so a large binary is cheap."""
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


# The independent oracle: geometry, in another process


def verify_archive_poses(archive: Path) -> dict[str, Any]:
    """Rebuild every archived pose and re-decide validity from the geometry alone.

    Run this in a child process, never inline in `record`. The point is not speed: it is
    that the verdict comes from code the producing command never touched, reading the
    file that is actually on disk, so agreement between the two is evidence.

    `preflight` may call this directly, because preflight decides nothing. `record` may
    not, and that is enforced rather than trusted: a regression walks `record`'s AST and
    fails if it reaches any oracle other than
    :func:`verify_archive_in_separate_process`.

    The producer's objective (`required_side`) is translation-invariant, so an emitted
    configuration is *not* normalised into `[0, s]^2`. Translating to the bounding-box
    origin before the containment test is therefore not a courtesy to the producer -- it
    is what makes the test the real claim: do `n` unit squares with these relative
    positions fit inside a square of the side that was reported.
    """
    results, _ = scan_archive(archive)
    sign = float_sign(POSE_TOLERANCE)
    failures: list[str] = []
    poses: list[dict[str, Any]] = []

    for rec in results:
        n, seed = int(rec["n"]), int(rec["seed"])
        side = float(rec["best_side"])
        digest = pose_digest(rec)
        x, y, t = validated_pose(rec, n)
        squares = corners_from_poses(x, y, t)
        xs = [px for square in squares for px, _ in square]
        ys = [py for square in squares for _, py in square]
        required = max(max(xs) - min(xs), max(ys) - min(ys))
        shifted = [[(px - min(xs), py - min(ys)) for px, py in square] for square in squares]
        report = verify_packing(shifted, side, sign=sign)
        label = f"n={n} seed={seed} pose {digest[:12]}"
        if required > side + POSE_TOLERANCE:
            failures.append(
                f"{label}: the pose needs side {required:.17g} but the line claims {side:.17g}"
            )
        if not report.valid:
            detail = "; ".join(f"{kind}: {why}" for kind, why in report.failures[:6])
            failures.append(f"{label}: {detail}")
        poses.append(
            {
                "pose_sha256": digest,
                "n": n,
                "seed": seed,
                "best_side": side,
                "required_side": required,
                "squares": len(squares),
                "pairs_tested": report.pairs_tested,
                "touching_pairs": report.touching_pairs,
                "valid": report.valid and required <= side + POSE_TOLERANCE,
            }
        )

    return {
        "verifier": "sqpack.verify.verify_packing",
        "assurance": "numerically-checked",
        "tolerance": POSE_TOLERANCE,
        "archive_sha256": archive_digest(results),
        "poses_checked": len(poses),
        # An archive with no scored line certifies nothing. Truncated output must not
        # arrive at `record` wearing a passing certificate.
        "verified": bool(poses) and not failures,
        "failures": failures,
        "poses": poses,
    }


def verify_archive_command(target: str | None) -> int:
    """The `verify-archive` step: the child half of the independent check."""
    if not target:
        print("REFUSED: verify-archive needs an archive path", file=sys.stderr)
        return 1
    archive = Path(target)
    try:
        report = verify_archive_poses(archive)
    except (GuardError, OSError) as error:
        report = {
            "verifier": "sqpack.verify.verify_packing",
            "verified": False,
            "poses_checked": 0,
            "failures": [f"{type(error).__name__}: {error}"],
        }
    print(json.dumps(report, sort_keys=True))
    return 0 if report["verified"] else 1


def verify_archive_in_separate_process(archive: Path) -> dict[str, Any]:
    """Re-enter this module as a child process and demand its verdict on the archive."""
    try:
        completed = subprocess.run(
            [sys.executable, "-m", RUNNER_MODULE, "verify-archive", str(archive)],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
            timeout=VERIFIER_TIMEOUT_SECONDS,
        )
    except subprocess.TimeoutExpired as exc:
        raise RefusalError(
            f"the independent pose verifier did not finish within "
            f"{VERIFIER_TIMEOUT_SECONDS:.0f}s on {archive.name}"
        ) from exc
    lines = [line for line in completed.stdout.splitlines() if line.strip()]
    report: Any = None
    if lines:
        try:
            report = json.loads(lines[-1])
        except json.JSONDecodeError:
            report = None
    if not isinstance(report, dict):
        raise RefusalError(
            f"the independent pose verifier produced no report (exit "
            f"{completed.returncode}): {(completed.stderr or completed.stdout).strip()[:300]}"
        )
    if completed.returncode != 0 or not report.get("verified"):
        detail = "; ".join(str(f) for f in report.get("failures") or []) or "no detail"
        raise GuardError(
            f"independent pose verification refused {archive.name}: {detail[:600]}"
        )
    return report


# The engine gate: executed, not asserted


def engine_path(recipe: dict[str, Any]) -> Path:
    """Absolute path to the binary the recipe's command actually runs."""
    declared = Path(shlex.split(recipe["command"])[0])
    return declared if declared.is_absolute() else (ROOT / declared)


def run_engine_selftest(recipe: dict[str, Any]) -> dict[str, Any]:
    """Execute the engine's own gate and hash the binary that passed it.

    `subject.selftest_passed` is documented in the experiment schema as "whether the
    engine gate ran and passed". It used to be a literal `True` written by the harness
    (D-044), while the hypotheses meanwhile advertised instruments "gated by
    `--selftest`". This runs that gate, and binds the answer to a digest of the exact
    file that ran, so `record` can tell that the binary has not been swapped since.
    """
    engine = engine_path(recipe)
    if not engine.exists():
        raise GuardError(
            f"the declared engine {engine} does not exist, so its self-test cannot run; "
            "build it before claiming a round"
        )
    argv = (
        shlex.split(str(recipe["selftest"]))
        if recipe.get("selftest")
        else [str(engine), "--selftest"]
    )
    digest = file_digest(engine)
    try:
        completed = subprocess.run(
            argv,
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
            timeout=SELFTEST_TIMEOUT_SECONDS,
        )
    except FileNotFoundError as exc:
        raise GuardError(f"the engine self-test command was not found: {argv[0]}") from exc
    except subprocess.TimeoutExpired as exc:
        raise GuardError(
            f"the engine self-test did not finish within {SELFTEST_TIMEOUT_SECONDS:.0f}s"
        ) from exc
    if completed.returncode != 0:
        raise GuardError(
            f"the engine self-test failed with exit {completed.returncode}; the "
            f"instrument is suspect, so no measurement may be taken: "
            f"{(completed.stdout + completed.stderr).strip()[-300:]}"
        )
    return {
        "engine": str(engine),
        "engine_sha256": digest,
        "argv": argv,
        "exit_status": completed.returncode,
        "output_sha256": hashlib.sha256(completed.stdout.encode("utf-8")).hexdigest(),
        "at": now().replace(microsecond=0).isoformat(),
    }


def selftest_passed(receipt: dict[str, Any] | None, recipe: dict[str, Any]) -> bool:
    """True only when the gate ran, passed, and the binary is still the one that ran."""
    if not receipt or receipt.get("exit_status") != 0:
        return False
    engine = engine_path(recipe)
    if not engine.exists():
        return False
    return file_digest(engine) == receipt.get("engine_sha256")


# Lifecycle: legal transitions, prerequisites, leases


def require_in_progress(eid: str, e: dict[str, Any], step: str) -> None:
    """Refuse any step that would rewrite a terminal round."""
    decision = (e.get("verdict") or {}).get("decision")
    if decision == IN_PROGRESS:
        return
    raise RefusalError(
        f"{eid} is {decision!r}, not {IN_PROGRESS}: `{step}` may only act on a claimed "
        "round. A terminal round is the record; claim a new one instead."
    )


def unmet_prereqs(h: dict[str, Any], recorded: list[dict[str, Any]]) -> list[str]:
    """Declared prerequisites this runner cannot see satisfied.

    `hypothesis.prereqs` says what "must land before this is runnable", and the queue
    used to ignore it entirely (D-046), so an unattended night could run a hypothesis
    out of order and report the result as if the order had not mattered. Prose
    prerequisites ("a verified n = 17 pose") are not machine-checkable, so they are
    treated as unmet rather than waved through: the runner is not the thing that gets
    to decide a human prerequisite has landed.
    """
    unmet: list[str] = []
    for item in h.get("prereqs") or []:
        text = str(item).strip()
        if not text:
            continue
        if not re.fullmatch(r"H-\d+", text):
            unmet.append(f"{text!r} is not a hypothesis id this runner can check")
            continue
        decisions = {
            (e.get("verdict") or {}).get("decision")
            for e in recorded
            if text in (e.get("hypotheses") or [])
        }
        if "accept" + "ed" not in decisions:
            unmet.append(f"{text} has not been accepted")
    return unmet


def lease_expiry(eid: str, e: dict[str, Any]) -> datetime:
    """The round's deadline as an instant in UTC.

    A naive stamp is read as UTC and an offset stamp is converted. Dropping an offset
    instead of converting it moves the instant, which expires a live west-of-UTC lease
    hours early and extends an east-of-UTC one -- the same bug the ledger already had
    to fix on the reading side.
    """
    raw = (e.get("lease") or {}).get("expires")
    if not raw:
        raise RefusalError(
            f"{eid} is {IN_PROGRESS} without a lease, so nothing bounds it. "
            f"`packing-campaign release {eid}` and claim it again."
        )
    try:
        parsed = datetime.fromisoformat(str(raw))
    except ValueError as exc:
        raise RefusalError(f"{eid} carries an unparseable lease {raw!r}") from exc
    return parsed.replace(tzinfo=UTC) if parsed.tzinfo is None else parsed.astimezone(UTC)


def lease_seconds_remaining(eid: str, e: dict[str, Any]) -> float:
    """Seconds left on the round's lease, refusing an expired one."""
    expiry = lease_expiry(eid, e)
    left = (expiry - now()).total_seconds()
    if left <= 0:
        raise RefusalError(
            f"{eid}'s lease expired at {expiry.isoformat()}; it is a stale claim. "
            f"`packing-campaign release {eid}` before running anything for it."
        )
    return left


# Persistence: a round that is not committed did not happen


def commit_paths(paths: list[Path], message: str) -> str:
    """Stage exactly these paths, commit, and prove the commit landed.

    Three things this fixes at once (D-046). The pathspec is the round's own artifact,
    its archive and the one regenerated view -- never `add -A` over the whole campaign
    directory, which swept up whatever any other writer had left dirty. The commit's
    exit status is read rather than discarded. And `HEAD` is compared before and after,
    because "exit 0" from a commit that produced no object is exactly the false success
    an unattended session must not report as a durable result.

    `--no-verify` stays: the repository's pre-commit hook formats the *whole* tree and
    re-stages the result, which would put every other lane's reformatted file into this
    round's commit and defeat the narrow pathspec above.
    """
    tracked = [str(path) for path in paths if path.exists()]
    if not tracked:
        raise RefusalError("nothing to commit: the round wrote no file that still exists")
    before = git("rev-parse", "HEAD")
    git("add", "--", *tracked)
    if not git("diff", "--cached", "--name-only", "--", *tracked):
        raise RefusalError(
            f"{message}: staging {', '.join(tracked)} produced no change, so the round "
            "is not durably persisted"
        )
    completed = subprocess.run(
        ["git", "commit", "-q", "--no-verify", "-m", message],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    if completed.returncode:
        detail = completed.stderr.strip() or completed.stdout.strip() or "no diagnostic"
        raise RefusalError(f"git commit failed with exit {completed.returncode}: {detail}")
    after = git("rev-parse", "HEAD")
    if after == before:
        raise RefusalError(
            "git commit reported success but HEAD did not move; the round is not "
            "durably persisted"
        )
    return after


def require_regenerated(step: str, eid: str | None = None) -> None:
    """Rebuild the generated views and refuse when the record no longer checks out."""
    regen = regenerate()
    if regen.returncode:
        target = f" {eid}" if eid else ""
        raise RefusalError(
            f"the campaign ledger refused the record after {step}{target}:\n"
            f"{regen.stdout}{regen.stderr}\nFix what it named, then re-run that step."
        )


def read_lines(
    stdout: str, fh: Any, *, expect_n: int | None = None, expect_seed: int | None = None
) -> float | None:
    """Archive every line, enforce the contract, return this invocation's best side.

    The overlap check lives here, so it is one piece of code every round exercises.
    D-009 was an overlap guard asserted against a drifting accumulator; this re-reads the
    value from the record being archived instead.

    `expect_n` and `expect_seed` bind a line to the invocation that produced it. Without
    them the cell a result counts towards is the producer's own assertion: a command run
    for one declared cell could print lines labelled with another declared cell, and the
    replay in `cells_from` would accept them because that cell is in the recipe. It also
    bounds the geometry the independent verifier is asked to rebuild, since a pose is
    exactly `n` squares long.
    """
    best: float | None = None
    for line in stdout.splitlines():
        if not line.strip():
            continue
        rec = validated_record(line)
        if "best_side" in rec:
            for label, expected, actual in (
                ("n", expect_n, int(rec["n"])),
                ("seed", expect_seed, int(rec["seed"])),
            ):
                if expected is not None and actual != expected:
                    raise GuardError(
                        f"a result line claims {label}={actual} but the command was run "
                        f"for {label}={expected}: a result may not be attributed to a "
                        "cell or seed other than the one that produced it"
                    )
        # Validate before writing: a guard refusal must not create an archive that a
        # later `record` step could mistake for admissible evidence.
        fh.write(line + "\n")
        if "best_side" not in rec:
            continue
        side = float(rec["best_side"])
        best = side if best is None else min(best, side)
    return best


def execute(eid: str) -> None:
    """Run the round's declared command once per (cell, seed) and archive the output.

    Truncates the archive first, so re-running the step after a failure is safe and does
    not double-count. Everything it learns is in that file; nothing is held in memory for
    a later step.
    """
    refuse_if_gate_running()
    path, e = find_round(eid)
    require_in_progress(eid, e, "execute")
    recipe = hypothesis(e["hypotheses"][0])["runner"]
    archive = archive_of(path)
    # The lease is the only durable bound on an unattended round. Check it before
    # spending anything, and read it again below so the gate's own cost comes out of the
    # round's budget: a timebox longer than the lease used to mean the round could
    # outlive the claim that authorised it (D-046).
    lease_seconds_remaining(eid, e)
    # Fire the engine's own gate before taking a single measurement, and refuse the round
    # if it fails: an untested binary must not be able to reach the archive (D-044).
    selftest = run_engine_selftest(recipe)
    started = time.monotonic()
    # Capture these before the command runs. `record` may be hours later on a newer
    # HEAD, but that is not the revision that produced the measurements.
    execution_commit = git("rev-parse", "--short", "HEAD")
    execution_dirty = bool(git("status", "--porcelain"))
    archive_ready = False
    try:
        archive.write_text("")
        archive_ready = True
        append_receipt(archive, SELFTEST_METADATA, selftest)
        budget = min(duration(recipe["timebox"]), lease_seconds_remaining(eid, e))
        if budget < duration(recipe["timebox"]):
            print(f"   lease caps this round at {budget / 60:.1f}m of {recipe['timebox']}")
        round_deadline = time.monotonic() + budget
        cells = list(recipe["cells"])

        for index, n in enumerate(cells):
            # Each cell gets an equal share of whatever is left, rather than one deadline
            # the first cell could spend in full (D-046). Unused time is reclaimed by the
            # cells that follow, and no cell can ever run past the lease.
            remaining = round_deadline - time.monotonic()
            if remaining <= 0:
                print(f"   n={n}: session deadline reached before the cell started")
                break
            cell_deadline = time.monotonic() + remaining / (len(cells) - index)
            with archive.open("a") as fh:
                for seed in recipe["seeds"]:
                    if round_deadline - time.monotonic() <= 0:
                        print(f"   n={n}: TIMEBOX reached, {recipe['timebox']} spent")
                        return
                    if (left := cell_deadline - time.monotonic()) <= 0:
                        print(f"   n={n}: cell share spent; moving to the next cell")
                        break
                    cmd = shlex.split(recipe["command"].format(n=n, seed=seed))
                    try:
                        p = subprocess.run(
                            cmd,
                            cwd=ROOT,
                            capture_output=True,
                            text=True,
                            timeout=left,
                            check=False,
                        )
                    except subprocess.TimeoutExpired:
                        print(f"   n={n}: cell share reached mid-seed")
                        break
                    except FileNotFoundError as exc:
                        raise GuardError(f"declared command not found: {cmd[0]}") from exc
                    if p.returncode:
                        raise GuardError(f"command exited {p.returncode} at n={n} seed={seed}")
                    side = read_lines(p.stdout, fh, expect_n=int(n), expect_seed=int(seed))
                    if side is None:
                        raise GuardError(f"no result line at n={n} seed={seed}")
                    print(f"   n={n} seed={seed}: {side:.12f}")
    finally:
        # A timeout and a command/contract exception are still measured work.  The
        # receipt makes release/recovery honest about the cost; if we could not even
        # create the archive there is nowhere durable to put it.
        if archive_ready:
            append_execution_metadata(
                archive,
                started=started,
                commit=execution_commit,
                dirty=execution_dirty,
            )


# Step: record, guard, decide, write, regenerate, and commit


@dataclass
class Cell:
    n: int
    sides: list[float]

    @property
    def best(self) -> float:
        return min(self.sides)

    @property
    def median(self) -> float:
        return statistics.median(self.sides)

    @property
    def gap(self) -> float:
        return self.best - standing_best(self.n)[0]


def cells_from(archive: Path, recipe: dict[str, Any]) -> list[Cell]:
    """Rebuild the per-cell results from the archive alone.

    Every result line carries its own `n` and `seed`, so the grouping is exact: no
    guessing which line is a summary, no assuming each seed printed the same number of
    lines. A seed's result is the minimum over its own lines; a cell's seeds are however
    many actually finished, which `decide` then checks against the declared count.
    """
    by_cell: dict[int, dict[int, float]] = {}
    allowed_cells = {int(n) for n in recipe["cells"]}
    allowed_seeds = {int(seed) for seed in recipe["seeds"]}
    for rec in scan_archive(archive)[0]:
        n, seed, side = int(rec["n"]), int(rec["seed"]), float(rec["best_side"])
        if n not in allowed_cells or seed not in allowed_seeds:
            raise GuardError(f"archive result n={n} seed={seed} is outside the declared recipe")
        seen = by_cell.setdefault(n, {})
        seen[seed] = min(seen.get(seed, side), side)

    return [Cell(n, sorted(by_cell[n].values())) for n in recipe["cells"] if by_cell.get(n)]


def control_breaches(cells: list[Cell]) -> list[str]:
    """Accept-rule clause 4, on whichever control cells this round ran."""
    out = []
    for c in cells:
        if c.n not in CONTROLS or not c.sides:
            continue
        kind, bound = CONTROLS[c.n]
        if kind == "within" and abs(c.gap) > bound:
            out.append(f"n={c.n} positive control off by {c.gap:.3e}, outside {bound}")
        if kind == "not_below" and c.best < bound - 1e-12:
            out.append(f"n={c.n} proved not-below control returned {c.best!r}, below {bound}")
    return out


def decide(h: dict[str, Any], cells: list[Cell]) -> dict[str, Any]:
    """The accept rule, applied mechanically.

    Clauses 1-4 are arithmetic. Clause 5 -- is it worth its complexity -- is a judgment,
    and an unwatched runner may apply it only in the conservative direction. So no path
    here returns the accepting verdict: the strongest it reaches is a pass on 1-4 held for
    review. A missing code path enforces that better than a rule asking for restraint.
    """
    hid = h["id"]
    threshold = float((h.get("criterion") or {}).get("threshold") or REACHED_BASIN)
    expected = len(h["runner"]["seeds"])

    if breaches := control_breaches(cells):
        return {
            "decision": "rejected", "needs_review": True, "stopped_by": "guard",
            "reason": "A control cell breached, so the instrument is suspect rather than the "
                      f"strategy good: {'; '.join(breaches)}. Clause 4 rejects regardless of "
                      "outcome.",
        }  # fmt: skip
    if not cells or any(len(c.sides) < expected for c in cells):
        got = ", ".join(f"n={c.n} {len(c.sides)}/{expected}" for c in cells) or "nothing"
        return {
            "decision": "abandoned", "needs_review": True, "stopped_by": "timebox",
            "reason": f"The archive is short of the declared {expected} seeds per cell "
                      f"({got}), so the criterion was not measured. The question is still "
                      "open and the budget is spent.",
        }  # fmt: skip

    gaps = ", ".join(f"n={c.n} {c.gap:+.3e}" for c in cells)
    if all(c.gap < threshold for c in cells):
        return {
            "decision": "unresolved", "needs_review": True, "stopped_by": "criterion",
            "reason": f"Every cell came within the declared {threshold:.0e} of the standing "
                      f"best ({gaps}). Clauses 1-4 pass; clause 5 is a judgment this "
                      "runner may not make in the accepting direction, so the round is "
                      "held for review.",
        }  # fmt: skip
    return {
        "decision": "rejected", "needs_review": False, "stopped_by": "criterion",
        "reason": f"The criterion was measured and missed: {gaps}, against the "
                  f"{threshold:.0e} {hid} declared. The claim is refuted for these cells and "
                  "this regime.",
    }  # fmt: skip


def record(eid: str, *, operator: str) -> str:
    """Read the archive, decide, write the round, regenerate the views, commit."""
    refuse_if_gate_running()
    path, stub = find_round(eid)
    require_in_progress(eid, stub, "record")
    hid = stub["hypotheses"][0]
    h = hypothesis(hid)
    recipe = h["runner"]
    archive = archive_of(path)
    if not archive.exists():
        raise RefusalError(
            f"{eid} has no archive; run `packing-campaign execute {eid}` before recording"
        )
    archived, receipts = scan_archive(archive)
    execution = validated_execution(receipts[EXECUTION_METADATA])
    if execution is None:
        raise RefusalError(
            f"{eid} has no execution receipt; "
            f"run `packing-campaign execute {eid}` before recording"
        )
    selftest = receipts[SELFTEST_METADATA]
    if selftest is None:
        raise RefusalError(
            f"{eid} has no self-test receipt, so nothing establishes that the engine "
            f"gate ran. Re-run `packing-campaign execute {eid}`."
        )
    gate_passed = selftest_passed(selftest, recipe)
    if not gate_passed:
        raise RefusalError(
            f"{eid}'s self-test receipt does not certify the engine that is on disk now "
            f"(exit {selftest.get('exit_status')!r}, sha256 "
            f"{str(selftest.get('engine_sha256'))[:12]}). The binary was swapped or the "
            f"gate failed; re-run `packing-campaign execute {eid}`."
        )
    # The independent check, every time there is something to check. A stored certificate
    # is an audit trail, not a licence: whoever can edit the archive can edit a
    # certificate inside it, so the geometry is re-decided here, in another process, from
    # the file as it stands. An archive with no scored line certifies nothing and is left
    # to `decide`, which abandons the round and keeps the spent budget legible.
    verification: dict[str, Any] | None = None
    if archived:
        verification = verify_archive_in_separate_process(archive)
        stored = receipts[VERIFICATION_METADATA]
        if stored is None:
            append_receipt(archive, VERIFICATION_METADATA, verification)
        elif stored.get("archive_sha256") != verification["archive_sha256"]:
            raise RefusalError(
                f"{eid}'s archive changed after it was verified: the retained receipt "
                f"certifies {str(stored.get('archive_sha256'))[:12]} but the file on disk "
                f"digests to {verification['archive_sha256'][:12]}. Nothing may be "
                "recorded from an archive that moved under its own certificate."
            )
    artifact_execution = artifact_fields_from_execution(execution)
    cells = cells_from(archive, recipe)
    verdict = decide(h, cells)
    cell_list = ", ".join(str(c.n) for c in cells) or str(recipe["cells"][0])

    results: list[dict[str, Any]] = [
        {
            "shape": "record",
            "metric": "best_side",
            "role": "outcome",
            "direction": "lower",
            "score": c.best,
            "standing_best": standing_best(c.n)[0],
            "standing_best_source": standing_best(c.n)[1],
            "beat_record": False,
            "runs": len(c.sides),
        }
        for c in cells
    ] or [
        {
            "shape": "determination",
            "question": "did the round produce data",
            "outcome": "invalid",
            "role": "outcome",
        }
    ]
    if verification is not None:
        # The guard row is the point of the repair: the round says, in the record, that
        # its geometry was re-derived by another process and which bytes were checked.
        results.append(
            {
                "shape": "determination",
                "question": (
                    f"did the {plural(verification['poses_checked'], 'archived pose')} "
                    "verify independently as unit squares inside the reported side "
                    "with pairwise disjoint interiors"
                ),
                "role": "guard",
                "outcome": "criterion_met",
                "checked_by": (
                    f"{verification['verifier']} in a separate process, tolerance "
                    f"{verification['tolerance']:g}, archive sha256 "
                    f"{verification['archive_sha256'][:16]}"
                ),
            }
        )

    fm = {
        "title": f"{eid} — {hid} at n = {cell_list}",
        "softschema": {
            "contract": "packing.squares:Experiment/v2",
            "schema": "../../../schemas/experiment.schema.yaml",
            "envelope": "experiment", "status": "enforced",
        },
        "experiment": {
            "id": eid, "series": stub["series"], "title": f"{hid} at n = {cell_list}",
            "date": stub["date"], "hypotheses": [hid], "tier": "exploratory",
            "subject": {
                # `engine` is required by the schema and must not be invented: take it
                # from the command the round actually ran.
                "engine": Path(shlex.split(recipe["command"])[0]).name,
                "label": recipe["command"],
                "engine_commit": artifact_execution["engine_commit"],
                "assurance": "numerically-checked",
                "method": "numerical-f64",
                "precision": {"binary_bits": 53, "rounding": "nearest-even"},
                "tolerance": (
                    f"engine-reported overlap 0; independent pose re-check at "
                    f"{POSE_TOLERANCE:g}"
                ),
                "host_system": socket.gethostname(),
                # Derived from an executed gate whose binary digest still matches the
                # engine on disk. Never a literal (D-044).
                "selftest_passed": gate_passed,
            },
            "instance": {"axis": "n", "point": cells[0].n if cells else recipe["cells"][0]},
            "method": {
                "candidate": recipe["command"], "runs_per_condition": len(recipe["seeds"]),
                "interleaved": False, "operator": operator,
                "commit": artifact_execution["method_commit"],
                "dirty": artifact_execution["dirty"],
                "entry_point": CAMPAIGN_ENTRY_POINT,
                "command": recipe["command"], "record": str(archive.relative_to(ROOT)),
            },
            "effort": {"timebox": recipe["timebox"],
                       "wall_seconds": artifact_execution["wall_seconds"],
                       "agent_minutes": 0, "stopped_by": verdict["stopped_by"]},
            "results": results,
            "verdict": {
                "decision": verdict["decision"],
                "primary_criterion": (h.get("criterion") or {}).get("metric", "best_side"),
                # This schema field has historically been used as evidence provenance,
                # not as a claim about the later write-up. Keep the execution revision
                # rather than silently replacing it with ``record``'s HEAD. Git history
                # records the commit that wrote the artifact.
                "reason": verdict["reason"],
                "commit": artifact_execution["verdict_commit"],
                "needs_review": verdict["needs_review"],
            },
        },
    }  # fmt: skip
    if verdict["decision"] == "abandoned":
        fm["experiment"]["verdict"].update({
            "budget_spent": f"{sum(len(c.sides) for c in cells)} seeds of "
                            f"{len(recipe['seeds']) * len(recipe['cells'])}",
            "best_reached": f"{cells[0].best:.12f}" if cells else "nothing",
            "reopen_when": "a longer timebox, or a faster machine",
            "resume_from": f"{archive.relative_to(ROOT)} — the seeds that completed",
        })  # fmt: skip

    table = "\n".join(
        f"| {c.n} | `{c.best:.12f}` | `{c.median:.12f}` | `{c.gap:+.4e}` | {len(c.sides)} |"
        for c in cells
    )
    provenance = (
        (
            f"The {plural(verification['poses_checked'], 'archived pose')} "
            f"{'was' if verification['poses_checked'] == 1 else 'were'} rebuilt into "
            f"corner geometry and re-checked for containment and pairwise separation by "
            f"`{verification['verifier']}` in a separate process, at tolerance "
            f"`{verification['tolerance']:g}`, over archive `sha256:"
            f"{verification['archive_sha256'][:16]}` (D-044). That is a numerical "
            f"re-derivation, not a proof: it can refute a forged pose and cannot promote "
            f"this round beyond `numerically-checked`. The engine gate ran as "
            f"`{shlex.join(selftest['argv'])}` and exited "
            f"{selftest['exit_status']}; the binary that passed it digests to `sha256:"
            f"{str(selftest['engine_sha256'])[:16]}`."
        )
        if verification is not None
        else (
            "No result line survived the harness contract, so there is no geometry to "
            "verify and nothing here may be read as a measurement."
        )
    )
    body = f"""# {eid} — {hid} at n = {cell_list}

{h.get("claim", "").strip()}

Run by `packing-campaign` under [the runbook](../../../README.md):

```
{recipe["command"]}
```

| n | best | median | gap to standing best | seeds |
| ---: | ---: | ---: | ---: | ---: |
{table}

## The verdict

{verdict["reason"]}

## Provenance

Every number is read from [`{archive.name}`](../results/{archive.name}), which archives
every line the command printed, so the configurations behind these sides can be re-read
without re-running anything (D-006). The overlap on every result line was checked by the
harness contract rather than trusted from the experiment that produced it (D-009), and the
geometry behind it was re-derived independently, as below.

{provenance}
"""
    write_atomic(
        path,
        "---\n"
        + yaml.safe_dump(fm, sort_keys=False, width=100, allow_unicode=True)
        + "---\n"
        + body,
    )
    regen = regenerate()
    if regen.returncode:
        # The round is written; only the views are stale. Say exactly that, because the
        # recovery is to fix what the checker named and re-run this one step.
        raise RefusalError(
            f"{eid} is written but the campaign ledger refused it:\n"
            f"{regen.stdout}{regen.stderr}\nFix that, then: packing-campaign record {eid}"
        )
    commit_paths(
        [path, archive, CAMPAIGN / "ledger.md"],
        f"round: {eid} {verdict['decision']} ({hid})",
    )
    return verdict["decision"]


def release(eid: str, why: str) -> None:
    """Give up a stuck round. Recovery, not routine: it records rather than deletes.

    Parses and re-serialises rather than editing the YAML as text. The text version
    looked simpler and silently produced an artifact the whole-set checker rejected --
    a recovery path that breaks the record is worst exactly when it is needed.

    A released round is terminal, so it carries the `effort` block the gate requires,
    with `stopped_by: error`: the round died, and nothing may be concluded from it.
    """
    refuse_if_gate_running()
    path, stub = find_round(eid)
    require_in_progress(eid, stub, "release")
    hid = stub["hypotheses"][0]
    recipe = hypothesis(hid)["runner"]
    archive = archive_of(path)
    try:
        execution = execution_metadata(archive) if archive.exists() else None
    except GuardError:
        # Recovery must never be blocked by the thing it is recovering from. A round is
        # often released precisely because its archive was refused, and an unreadable
        # archive must not also make the round unreleasable.
        execution = None

    stub.pop("lease", None)
    stub["effort"] = {
        "timebox": recipe["timebox"],
        # A release before execute costs no measurement time. A release after a failed
        # execute uses the receipt written in execute's finally block.
        "wall_seconds": execution["wall_seconds"] if execution else 0,
        "agent_minutes": 0,
        "stopped_by": "error",
    }
    stub["verdict"] = {
        "decision": "unresolved",
        "primary_criterion": stub["verdict"]["primary_criterion"],
        "reason": f"Released by an operator without a measurement. {why}",
        "needs_review": True,
    }
    fm = {
        "title": f"{eid} — {hid} (released)",
        "softschema": {
            "contract": "packing.squares:Experiment/v2",
            "schema": "../../../schemas/experiment.schema.yaml",
            "envelope": "experiment",
            "status": "enforced",
        },
        "experiment": stub,
    }
    write_atomic(
        path,
        "---\n"
        + yaml.safe_dump(fm, sort_keys=False, width=100, allow_unicode=True)
        + f"""---
# {eid} — released

Claimed and then given up without a measurement: {why}

Nothing may be concluded from this round. `{hid}` returns to the queue, and a successor
starts from nothing — no budget was spent that a later round can resume from.
""",
    )
    # A release is a state transition like any other, so it is regenerated and committed
    # rather than left on disk. An unattended session that released a round and then died
    # used to leave no durable trace of the transition at all (D-046).
    require_regenerated("release", eid)
    commit_paths([path, archive, CAMPAIGN / "ledger.md"], f"round: {eid} released ({hid})")
    print(f"{eid} released; {hid} returns to the queue")


# Step: status and preflight


def duration(timebox: str) -> float:
    return float(timebox[:-1]) * {"s": 1, "m": 60, "h": 3600}[timebox[-1]]


def show_status() -> None:
    runnable, skipped = queue()
    stuck = [e["id"] for _, e in all_rounds() if e["verdict"]["decision"] == "in-progress"]
    print(f"rounds recorded: {len(all_rounds())}")
    print(f"in progress:     {stuck or 'none'}")
    print(f"last session:    {'campaign/session-report.md' if REPORT.exists() else 'none'}")
    print(f"\nqueue: {len(runnable)} runnable, {len(skipped)} not")
    for hid, why in skipped:
        print(f"  -  {hid}: {why}")
    for hid, h in runnable:
        r = h["runner"]
        print(
            f"  +  {hid} (priority {h.get('priority', 99)}) cells {r['cells']}, "
            f"{len(r['seeds'])} seeds, timebox {r['timebox']}"
        )
        print(f"       {r['command']}")


def preflight() -> int:
    """Every guard, fired on purpose. A guard nobody has watched fail is not evidence."""

    class Sink:
        def __init__(self) -> None:
            self.lines: list[str] = []

        def write(self, line: str) -> None:
            self.lines.append(line)

    checks: list[tuple[str, bool, str]] = []

    def guard_refuses(label: str, payload: str) -> None:
        sink = Sink()
        try:
            read_lines(payload, sink)
            checks.append((label, False, "it was accepted"))
        except GuardError as e:
            checks.append(
                (
                    label,
                    not sink.lines,
                    f"{e}; {len(sink.lines)} invalid line(s) reached the archive",
                )
            )

    guard_refuses(
        "a non-zero overlap is refused",
        grid_result_line(11, 1, 3.9, overlap=1e-9),
    )
    guard_refuses(
        "a result line with no overlap is refused",
        '{"n": 11, "seed": 1, "best_side": 3.9}',
    )
    guard_refuses(
        "a result line with no n and seed is refused",
        '{"best_side": 3.9, "overlap": 0}',
    )
    guard_refuses("a non-JSON line is refused", "not json at all")
    guard_refuses(
        "a result line with no pose is refused",
        '{"n": 11, "seed": 1, "best_side": 3.9, "overlap": 0}',
    )
    guard_refuses(
        "a pose whose length disagrees with n is refused",
        json.dumps(
            {
                "n": 11,
                "seed": 1,
                "best_side": 3.9,
                "overlap": 0,
                "x": [0.5, 1.5],
                "y": [0.5, 1.5],
                "t": [0.0, 0.0],
            }
        ),
    )
    for reserved in RESERVED_RECEIPTS:
        guard_refuses(
            f"producer output cannot spoof the {reserved} receipt",
            json.dumps({reserved: {"verified": True, "commit": "spoofed"}}),
        )

    best = read_lines(
        grid_result_line(11, 1, 3.9) + "\n" + grid_result_line(11, 1, 3.7),
        Sink(),
    )
    checks.append(("a seed's result is the min over its lines", best == 3.7, f"got {best}"))

    sink = Sink()
    try:
        read_lines(grid_result_line(11, 2, 3.9), sink, expect_n=11, expect_seed=1)
        attribution, attribution_detail = False, "a line from another seed was archived"
    except GuardError as exc:
        attribution = not sink.lines
        attribution_detail = f"{exc}; {len(sink.lines)} line(s) reached the archive"
    checks.append(
        (
            "a result may not be attributed to another cell or seed",
            attribution,
            attribution_detail,
        )
    )

    moved = json.loads(grid_result_line(11, 1, 3.9))
    shifted = dict(moved, x=[moved["x"][0] + 1e-9, *moved["x"][1:]])
    checks.append(
        (
            "the pose digest moves when a single coordinate moves",
            pose_digest(moved) != pose_digest(shifted),
            f"{pose_digest(moved)[:12]} vs {pose_digest(shifted)[:12]}",
        )
    )

    with tempfile.TemporaryDirectory() as tmp:
        bad_archive = Path(tmp) / "bad.jsonl"
        bad_archive.write_text(grid_result_line(11, 1, 3.7, overlap=0.001) + "\n")
        try:
            cells_from(bad_archive, {"cells": [11], "seeds": [1]})
            replay_refused, replay_detail = False, "the tampered archive was accepted"
        except GuardError as e:
            replay_refused, replay_detail = True, str(e)
    checks.append(
        ("record replay revalidates every result line", replay_refused, replay_detail)
    )

    with tempfile.TemporaryDirectory() as tmp:
        timed_archive = Path(tmp) / "timed.jsonl"
        timed_archive.write_text(
            grid_result_line(11, 1, 3.7) + "\n"
            '{"campaign_runner_execution": '
            '{"wall_seconds": 12.5, "commit": "execution-sha", "dirty": true}}\n'
        )
        receipt = execution_metadata(timed_archive)
    checks.append(
        (
            "execution receipt preserves elapsed time and run-time provenance",
            receipt == {"wall_seconds": 12.5, "commit": "execution-sha", "dirty": True},
            f"got {receipt!r}",
        )
    )
    artifact_execution = artifact_fields_from_execution(receipt) if receipt is not None else {}
    checks.append(
        (
            "record fields are bound to the execution receipt",
            artifact_execution
            == {
                "engine_commit": "execution-sha",
                "method_commit": "execution-sha",
                "verdict_commit": "execution-sha",
                "dirty": True,
                "wall_seconds": 12.5,
            },
            f"got {artifact_execution!r}",
        )
    )

    created_gate_marker = not GATE_MARKER.exists()
    if created_gate_marker:
        GATE_MARKER.touch()
    try:
        for label, action in (
            (
                "execute refuses while the gate marker exists",
                lambda: execute("preflight-missing-round"),
            ),
            (
                "release refuses while the gate marker exists",
                lambda: release("preflight-missing-round", "preflight"),
            ),
        ):
            try:
                action()
                refused, detail = False, "the command ran"
            except GateRunningError as exc:
                refused = True
                detail = str(exc)
            except RefusalError as exc:
                refused = False
                detail = f"wrong refusal type: {exc}"
            checks.append((label, refused, detail))
    finally:
        if created_gate_marker:
            GATE_MARKER.unlink(missing_ok=True)

    with tempfile.TemporaryDirectory() as tmp:
        wrong_cell = Path(tmp) / "wrong-cell.jsonl"
        wrong_cell.write_text(grid_result_line(12, 1, 4.0) + "\n")
        try:
            cells_from(wrong_cell, {"cells": [11], "seeds": [1]})
            recipe_refused, recipe_detail = False, "the undeclared cell was accepted"
        except GuardError as e:
            recipe_refused, recipe_detail = True, str(e)
    checks.append(
        ("record replay enforces the declared cells and seeds", recipe_refused, recipe_detail)
    )

    # Lifecycle. Every transition D-046 named, fired on purpose rather than trusted.
    for step, decision in (("execute", "rejected"), ("record", "unresolved")):
        try:
            require_in_progress("exp-000", {"verdict": {"decision": decision}}, step)
            refused, detail = False, f"a {decision} round was accepted"
        except RefusalError as exc:
            refused, detail = True, str(exc)
        checks.append((f"{step} refuses a terminal round", refused, detail))

    unmet = unmet_prereqs({"prereqs": ["H-011", "a verified n = 17 pose"]}, [])
    checks.append(
        (
            "an unmet prerequisite keeps a hypothesis out of the queue",
            len(unmet) == 2,
            "; ".join(unmet) or "nothing was reported unmet",
        )
    )
    checks.append(
        (
            "an empty prereqs list does not block a hypothesis",
            not unmet_prereqs({"prereqs": []}, []),
            "an empty list was treated as unmet",
        )
    )

    west = {"lease": {"expires": "2026-01-01T00:00:00-07:00"}}
    checks.append(
        (
            "a lease offset is converted to UTC rather than stripped",
            lease_expiry("exp-000", west) == datetime(2026, 1, 1, 7, 0, tzinfo=UTC),
            f"got {lease_expiry('exp-000', west).isoformat()}",
        )
    )
    try:
        lease_seconds_remaining(
            "exp-000", {"lease": {"expires": (now() - timedelta(minutes=1)).isoformat()}}
        )
        lease_refused, lease_detail = False, "an expired lease was accepted"
    except RefusalError as exc:
        lease_refused, lease_detail = True, str(exc)
    checks.append(("an expired lease is refused", lease_refused, lease_detail))

    # The independent oracle, actually spawned. This is the guard D-044 asked for, so
    # preflight pays for two real child processes rather than asserting an import works.
    with tempfile.TemporaryDirectory() as tmp:
        honest = Path(tmp) / "honest.jsonl"
        honest.write_text(grid_result_line(4, 1) + "\n")
        try:
            report = verify_archive_in_separate_process(honest)
            accepted, accept_detail = True, f"{report['poses_checked']} pose(s) verified"
        except (GuardError, RefusalError) as exc:
            accepted, accept_detail = False, str(exc)
        checks.append(
            ("a separate process verifies a genuinely valid pose", accepted, accept_detail)
        )

        x, y, t, side = grid_pose(4)
        forged = Path(tmp) / "forged.jsonl"
        forged.write_text(
            json.dumps({
                "n": 4, "seed": 1, "best_side": side, "overlap": 0,
                # Squares 0 and 1 stacked exactly, with a zero overlap asserted anyway.
                "x": [x[0], x[0], x[2], x[3]], "y": [y[0], y[0], y[2], y[3]], "t": t,
            })
            + "\n"
        )  # fmt: skip
        try:
            verify_archive_in_separate_process(forged)
            forge_refused, forge_detail = False, "the fabricated overlap was accepted"
        except (GuardError, RefusalError) as exc:
            forge_refused, forge_detail = True, str(exc)
        checks.append(
            (
                "a separate process refuses a fabricated zero overlap",
                forge_refused,
                forge_detail,
            )
        )

        understated = Path(tmp) / "understated.jsonl"
        understated.write_text(grid_result_line(4, 1, 1.5) + "\n")
        under = verify_archive_poses(understated)
        checks.append(
            (
                "a best_side smaller than the pose needs is refused",
                not under["verified"],
                "; ".join(under["failures"]) or "the understated side was accepted",
            )
        )

        empty = Path(tmp) / "empty.jsonl"
        empty.write_text("")
        checks.append(
            (
                "an archive with no scored line certifies nothing",
                not verify_archive_poses(empty)["verified"],
                "an empty archive was reported verified",
            )
        )

    breach = control_breaches([Cell(16, [3.9])])
    checks.append(
        ("a control-cell breach is caught", bool(breach), breach[0] if breach else "not caught")
    )
    open_case_breach = control_breaches([Cell(12, [3.9])])
    checks.append(
        (
            "an n=12 improvement is not rejected as a control breach",
            not open_case_breach,
            open_case_breach[0] if open_case_breach else "not a control",
        )
    )

    # Built from parts so the needle does not appear literally here and match itself.
    needle = '"decision"' + ": " + '"' + "accept" + 'ed"'
    checks.append(
        (
            "no code path writes the accepting verdict",
            needle not in Path(__file__).read_text(),
            "clause 5 is unreachable",
        )
    )

    runnable, skipped = queue(allow_during_gate=True)
    checks.append(
        (
            "the queue is not empty",
            bool(runnable),
            (
                f"{len(runnable)} runnable, {len(skipped)} not — a working runner in "
                "front of an empty queue is an idle night"
            ),
        )
    )

    for name, passed, detail in checks:
        print(f"  {'PASS' if passed else 'FAIL'}  {name}\n          {detail}")
    ok = all(p for _, p, _ in checks)
    print("\nPREFLIGHT PASSED" if ok else "\nPREFLIGHT FAILED")
    return 0 if ok else 1


# Run the three middle steps in a loop


def safe_release(eid: str, why: str) -> str:
    """Free a round after a failure and return the state it actually ended in.

    The recovery path must not be able to replace the failure that caused it, and it
    must not report a state the round is not in. A failure *after* `record` wrote the
    verdict leaves a terminal round that was merely not committed; a failure before it
    leaves a claim to release; a failure of the release itself leaves a stale claim the
    ledger will surface. Each of those is said out loud rather than flattened to one
    optimistic word.
    """
    try:
        _, e = find_round(eid)
    except RefusalError as error:
        print(f"   {eid} cannot be read back: {error}")
        return "unknown"
    decision = str((e.get("verdict") or {}).get("decision"))
    if decision != IN_PROGRESS:
        print(f"   {eid} is already {decision}: the failure came after the verdict.")
        return decision
    try:
        release(eid, why)
    except (RefusalError, GuardError, OSError) as error:
        print(f"   RELEASE FAILED for {eid}: {error}")
        print(f"   {eid} remains claimed and will show as a stale claim until recovered.")
        return IN_PROGRESS
    return "unresolved"


def run(operator: str, hours: float) -> int:
    """claim / execute / record over the queue. Nothing here that a step cannot do."""
    started, failures, done = now(), 0, []
    deadline = started + timedelta(hours=hours)
    _, skipped = queue()
    show_status()
    attempted: set[str] = set()
    abnormal = False

    try:
        while True:
            remaining = (deadline - now()).total_seconds()
            # A lease shorter than a minute buys a round that `execute` would refuse as
            # already expired, which would spend a failure on the clock rather than on
            # the instrument.
            if remaining < 60:
                print("\nsession budget exhausted")
                break
            # Recompute the queue after every transition. A recorded round can resolve a
            # hypothesis, reach the cap, or satisfy a prerequisite, and a list computed
            # once at the top of the night does not know any of that (D-046).
            runnable, skipped = queue()
            hid = next((h for h, _ in runnable if h not in attempted), None)
            if hid is None:
                break
            attempted.add(hid)
            # The lease carries the session deadline into `execute`, which is what stops
            # the last round of a night from overrunning by a whole timebox.
            eid = claim(hid, operator, remaining / 3600)
            print(f"\n== {eid}: {hid} ==")
            try:
                execute(eid)
                decision = record(eid, operator=operator)
                failures = 0
            except GateRunningError:
                # The gate owns the machine now. Free the round and stop the session
                # rather than fighting it for the CPU.
                abnormal = True
                done.append(
                    (
                        eid,
                        hid,
                        safe_release(eid, "the validation gate started during the round"),
                    )
                )
                raise
            except (GuardError, RefusalError, OSError) as error:
                # Every failure is terminal for the round and non-scientific: a guard
                # refusal, a refused ledger, a failed commit, and an unreadable archive
                # all leave the same durable state. Only a GuardError used to be caught
                # here, so a refusal escaped the loop, wrote no report, and left the
                # round claimed (D-046).
                failures += 1
                print(f"   REFUSED: {error}")
                decision = safe_release(eid, f"the round did not complete: {error}")
            done.append((eid, hid, decision))
            print(f"   -> {decision}")
            if failures >= MAX_CONSECUTIVE_FAILURES:
                print(f"\n{failures} consecutive refusals: the instrument is suspect")
                abnormal = True
                break
    finally:
        write_report(
            started,
            operator,
            hours,
            done=done,
            skipped=skipped,
            failures=failures,
            abnormal=abnormal,
        )

    return 1 if abnormal else 0


def write_report(
    started: datetime, operator: str, hours: float,
    *, done: list[tuple[str, str, str]], skipped: list[tuple[str, str]],
    failures: int, abnormal: bool,
) -> None:  # fmt: skip
    """Generated, written even when the session ended badly, leading with what needs the
    human -- which is the reason a queue gets trusted."""
    review = [
        (e["id"], e["verdict"]["reason"])
        for _, e in all_rounds()
        if e.get("verdict", {}).get("needs_review")
    ]
    spent = (now() - started).total_seconds() / 3600
    out = [
        f"# Session {started.date().isoformat()} — the s(n) search campaign",
        "",
        f"Operator `{operator}`, {spent:.1f}h of {hours:.0f}h, {len(done)} rounds.",
        "",
        "## Needs review",
        "",
        *([f"- **{e}** — {why}" for e, why in review] or ["Nothing was held for review."]),
        "",
        "## What ran",
        "",
    ]
    out += (
        ["| exp | H | decision |", "| --- | --- | --- |"]
        + [f"| {e} | {h} | {d} |" for e, h, d in done]
        if done
        else ["No rounds completed."]
    )
    out += ["", "## Queue after this session", ""]
    out += (
        ["| H | why it did not run |", "| --- | --- |"]
        + [f"| {h} | {why} |" for h, why in skipped]
        if skipped
        else ["Every open hypothesis was runnable."]
    )
    out += [
        "",
        "## Health",
        "",
        (
            f"- Consecutive refusals: **{failures}** (the stop fires at "
            f"{MAX_CONSECUTIVE_FAILURES}). A guard, a refused ledger, a failed commit and "
            "an unreadable archive all count: each ends the round without a measurement."
        ),
        f"- Exit: **{'abnormal, non-zero' if abnormal else 'clean'}**.",
        "",
    ]
    write_atomic(REPORT, "\n".join(out))
    print(f"\nreport at {REPORT.relative_to(ROOT)}")


def main(arguments: list[str] | None = None) -> int:
    """Run one campaign state-machine command."""
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("step", choices=[
        "status", "preflight", "queue", "claim", "execute", "record", "release", "run",
        "verify-archive",
    ])  # fmt: skip
    parser.add_argument(
        "target",
        nargs="?",
        help=(
            "H-id for claim; exp-id for execute/record/release; archive path for verify-archive"
        ),
    )
    parser.add_argument("--operator", default="local-agent")
    parser.add_argument("--session-hours", type=float, default=8.0)
    parser.add_argument("--why", default="no reason given", help="for release")
    options = parser.parse_args(arguments)

    try:
        # The verifier is the child half of the independent check and works on an
        # absolute archive path. It must not need the checkout, so that a `record`
        # running against any layout can still reach an oracle process.
        if options.step == "verify-archive":
            return verify_archive_command(options.target)
        require_project_root(ROOT)
        if options.step in {"status", "queue"}:
            show_status()
        elif options.step == "preflight":
            return preflight()
        elif options.step == "claim":
            print(claim(options.target, options.operator, options.session_hours))
        elif options.step == "execute":
            execute(options.target)
        elif options.step == "record":
            print(record(options.target, operator=options.operator))
        elif options.step == "release":
            release(options.target, options.why)
        elif options.step == "run":
            return run(options.operator, options.session_hours)
    except (RefusalError, GuardError, ProjectLayoutError) as error:
        print(f"REFUSED: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
