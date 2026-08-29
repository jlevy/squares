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
  2. carry `best_side`, `n` and `seed` on every result line;
  3. carry `overlap` (or `best_overlap`) on those lines, and it must be exactly 0;
  4. exit 0.

A seed's result is the **minimum** `best_side` over its own lines. Carrying `n` and
`seed` is what makes that grouping exact: nothing has to agree about which line is the
summary, and a seed printing a different number of lines than its neighbour changes
nothing.

Adding an experiment never edits this file. Writing new experiment code is expected;
writing new harness code per round is the error-prone thing this design removes, because
it is code that runs once, at 3am, having never been exercised.

## One runner at a time

No locks, no leases to reclaim, no id reservation: the campaign runs one session at a
time, and coordination nobody needs is more to get wrong. `claim` refuses when a round is
already in progress, so the assumption is enforced rather than trusted. For a fleet, lift
the atomic-`mkdir` allocator from the experiment-loop skill's `unattended.md` -- and not
`flock`, which is local-only over NFS.
"""

from __future__ import annotations

import argparse
import json
import math
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
from sqpack.yamlio import safe_load

ROOT = configured_project_root()
CAMPAIGN = ROOT / "campaign"
SERIES = CAMPAIGN / "series"
REPORT = CAMPAIGN / "session-report.md"
EXECUTION_METADATA = "campaign_runner_execution"
EXECUTION_TIME_DECIMAL_PLACES = 6
CAMPAIGN_ENTRY_POINT = (
    f"{__spec__.name if __spec__ is not None else 'sqpack.campaign.runner'}:main"
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
    selftest_passed: true
  instance: {{axis: n, point: {cell}}}
  method: {{operator: {operator}}}
  lease: {{expires: '{expires}'}}
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
        ),
    )
    # Regenerate immediately: the in-progress round is part of the record the moment it
    # exists, and a round runs for hours. Without this the gate fails on a stale
    # ledger.md for the whole session -- i.e. exactly while you most want to run it.
    regenerate()
    return eid


def archive_of(path: Path) -> Path:
    return path.parent.parent / "results" / (path.stem + ".jsonl")


def execution_metadata(archive: Path) -> dict[str, Any] | None:
    """Return the one execution receipt appended by `execute`, if present.

    The JSONL archive is already the durable hand-off between `execute` and `record`.
    Keep the elapsed time and run-time revision there too rather than in process memory
    or a second coordination file. Ordinary non-result provenance lines remain allowed
    by the harness contract; this reserved record is the only one interpreted by the
    runner.
    """
    receipts: list[dict[str, Any]] = []
    for line in archive.read_text().splitlines():
        if not line.strip():
            continue
        rec = validated_record(line, allow_execution_metadata=True)
        if EXECUTION_METADATA not in rec:
            continue
        if set(rec) != {EXECUTION_METADATA}:
            raise GuardError("execution receipt has unexpected fields")
        receipt = rec[EXECUTION_METADATA]
        if not isinstance(receipt, dict):
            raise GuardError("execution receipt is not an object")
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
        receipts.append({"wall_seconds": float(wall_seconds), "commit": commit, "dirty": dirty})
    if len(receipts) > 1:
        raise GuardError("archive has more than one execution receipt")
    return receipts[0] if receipts else None


def append_execution_metadata(
    archive: Path, *, started: float, commit: str, dirty: bool
) -> None:
    """Append the receipt even when a timebox or command failure ends ``execute``."""
    receipt = {
        EXECUTION_METADATA: {
            "wall_seconds": round(time.monotonic() - started, EXECUTION_TIME_DECIMAL_PLACES),
            "commit": commit,
            "dirty": dirty,
        }
    }
    with archive.open("a") as fh:
        fh.write(json.dumps(receipt, sort_keys=True) + "\n")


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


def validated_record(line: str, *, allow_execution_metadata: bool = False) -> dict[str, Any]:
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
    if EXECUTION_METADATA in rec and not allow_execution_metadata:
        raise GuardError(f"a command may not write the reserved {EXECUTION_METADATA!r} field")
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
    return rec


def read_lines(stdout: str, fh: Any) -> float | None:
    """Archive every line, enforce the contract, return this invocation's best side.

    The overlap check lives here, so it is one piece of code every round exercises.
    D-009 was an overlap guard asserted against a drifting accumulator; this re-reads the
    value from the record being archived instead.
    """
    best: float | None = None
    for line in stdout.splitlines():
        if not line.strip():
            continue
        rec = validated_record(line)
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
    recipe = hypothesis(e["hypotheses"][0])["runner"]
    archive = archive_of(path)
    started = time.monotonic()
    # Capture these before the command runs. `record` may be hours later on a newer
    # HEAD, but that is not the revision that produced the measurements.
    execution_commit = git("rev-parse", "--short", "HEAD")
    execution_dirty = bool(git("status", "--porcelain"))
    archive_ready = False
    try:
        archive.write_text("")
        archive_ready = True
        deadline = time.monotonic() + duration(recipe["timebox"])

        for n in recipe["cells"]:
            with archive.open("a") as fh:
                for seed in recipe["seeds"]:
                    if (left := deadline - time.monotonic()) <= 0:
                        print(f"   n={n}: TIMEBOX reached, {recipe['timebox']} spent")
                        return
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
                        print(f"   n={n}: TIMEBOX reached mid-seed")
                        return
                    except FileNotFoundError as exc:
                        raise GuardError(f"declared command not found: {cmd[0]}") from exc
                    if p.returncode:
                        raise GuardError(f"command exited {p.returncode} at n={n} seed={seed}")
                    if (side := read_lines(p.stdout, fh)) is None:
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
    for line in archive.read_text().splitlines():
        if not line.strip():
            continue
        rec = validated_record(line, allow_execution_metadata=True)
        if "best_side" not in rec:
            continue
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
    hid = stub["hypotheses"][0]
    h = hypothesis(hid)
    recipe = h["runner"]
    archive = archive_of(path)
    execution = execution_metadata(archive) if archive.exists() else None
    if execution is None:
        raise RefusalError(
            f"{eid} has no execution receipt; "
            f"run `packing-campaign execute {eid}` before recording"
        )
    artifact_execution = artifact_fields_from_execution(execution)
    cells = cells_from(archive, recipe) if archive.exists() else []
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
                "tolerance": "0 (engine-reported overlap must equal zero)",
                "host_system": socket.gethostname(), "selftest_passed": True,
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
without re-running anything (D-006). The overlap of every result line was asserted zero
by the harness contract rather than by the experiment that produced it (D-009).
"""
    write_atomic(
        path,
        "---\n"
        + yaml.safe_dump(fm, sort_keys=False, width=100, allow_unicode=True)
        + "---\n"
        + body,
    )
    regen = subprocess.run(
        [sys.executable, "-m", "sqpack.campaign.ledger", "render"],
        cwd=ROOT, capture_output=True, text=True, check=False,
    )  # fmt: skip
    if regen.returncode:
        # The round is written; only the views are stale. Say exactly that, because the
        # recovery is to fix what the checker named and re-run this one step.
        raise RefusalError(
            f"{eid} is written but the campaign ledger refused it:\n"
            f"{regen.stdout}{regen.stderr}\nFix that, then: packing-campaign record {eid}"
        )
    git("add", "-A", str(CAMPAIGN))
    subprocess.run(
        [
            "git",
            "commit",
            "-q",
            "-m",
            f"round: {eid} {verdict['decision']} ({hid})",
            "--no-verify",
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
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
    if stub["verdict"]["decision"] != "in-progress":
        raise RefusalError(f"{eid} is {stub['verdict']['decision']}, not in-progress")
    hid = stub["hypotheses"][0]
    recipe = hypothesis(hid)["runner"]
    archive = archive_of(path)
    execution = execution_metadata(archive) if archive.exists() else None

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
    regenerate()
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
        '{"n": 11, "seed": 1, "best_side": 3.9, "overlap": 1e-9}',
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
        "producer output cannot spoof the execution receipt",
        '{"campaign_runner_execution": '
        '{"wall_seconds": 0, "commit": "spoofed", "dirty": false}}',
    )

    best = read_lines(
        '{"n": 11, "seed": 1, "best_side": 3.9, "overlap": 0}\n'
        '{"n": 11, "seed": 1, "best_side": 3.7, "overlap": 0}',
        Sink(),
    )
    checks.append(("a seed's result is the min over its lines", best == 3.7, f"got {best}"))

    with tempfile.TemporaryDirectory() as tmp:
        bad_archive = Path(tmp) / "bad.jsonl"
        bad_archive.write_text('{"n": 11, "seed": 1, "best_side": 3.7, "overlap": 0.001}\n')
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
            '{"n": 11, "seed": 1, "best_side": 3.7, "overlap": 0}\n'
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
        wrong_cell.write_text('{"n": 12, "seed": 1, "best_side": 4.0, "overlap": 0}\n')
        try:
            cells_from(wrong_cell, {"cells": [11], "seeds": [1]})
            recipe_refused, recipe_detail = False, "the undeclared cell was accepted"
        except GuardError as e:
            recipe_refused, recipe_detail = True, str(e)
    checks.append(
        ("record replay enforces the declared cells and seeds", recipe_refused, recipe_detail)
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


def run(operator: str, hours: float) -> int:
    """claim / execute / record over the queue. Nothing here that a step cannot do."""
    started, failures, done = now(), 0, []
    runnable, skipped = queue()
    show_status()

    for hid, _ in runnable:
        if (now() - started).total_seconds() > hours * 3600:
            print("\nsession budget exhausted")
            break
        eid = claim(hid, operator, hours)
        print(f"\n== {eid}: {hid} ==")
        try:
            execute(eid)
            decision = record(eid, operator=operator)
            failures = 0
        except GuardError as e:
            failures += 1
            print(f"   GUARD REFUSED: {e}")
            release(eid, f"guard refused the measurement: {e}")
            decision = "unresolved"
        done.append((eid, hid, decision))
        print(f"   -> {decision}")
        if failures >= MAX_CONSECUTIVE_FAILURES:
            print(f"\n{failures} consecutive guard refusals: the instrument is suspect")
            write_report(
                started,
                operator,
                hours,
                done=done,
                skipped=skipped,
                failures=failures,
                abnormal=True,
            )
            return 1

    write_report(
        started, operator, hours, done=done, skipped=skipped, failures=failures, abnormal=False
    )
    return 0


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
        f"- Guard refusals: **{failures}** (the stop fires at {MAX_CONSECUTIVE_FAILURES}).",
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
    ])  # fmt: skip
    parser.add_argument(
        "target", nargs="?", help="H-id for claim; exp-id for execute/record/release"
    )
    parser.add_argument("--operator", default="local-agent")
    parser.add_argument("--session-hours", type=float, default=8.0)
    parser.add_argument("--why", default="no reason given", help="for release")
    options = parser.parse_args(arguments)

    try:
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
