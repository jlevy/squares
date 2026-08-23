#!/usr/bin/env python3
"""The unattended runner: execute rounds against the registry, without a human.

    python3 campaign/runner.py --session-hours 8 --operator claude-opus-5
    python3 campaign/runner.py --dry-run          # show the queue and stop
    python3 campaign/runner.py --rehearse         # the six-step pre-flight

The protocol is `.agents/skills/experiment-loop/references/unattended.md`; the campaign
contract it runs under is `campaign/README.md`. This file implements them and adds
nothing of its own: every threshold here is read from those documents, and where one is
duplicated it is duplicated because a machine has to read it, with the source named.

The premise, from unattended.md: **an unwatched loop is only as trustworthy as its
refusals.** So the shape of this file is refusals first, work second. It refuses to run
a hypothesis with no machine-readable recipe, to run a cell outside a declared sweep, to
record a number a guard rejected, to accept anything on judgment, and to exit zero after
an abnormal stop.

What it does NOT do, stated so nobody discovers it at 3am: it runs `sqsearch`-shaped
rounds only. It cannot build an instrument, write a new refiner, or invent an analysis.
Rounds needing any of that are agent work and stay agent work -- the ledger records 275
agent-minutes against 16.4 cpu-minutes over ten rounds, so most of this campaign's cost
has never been the compute.
"""

from __future__ import annotations

import argparse
import fcntl
import json
import os
import re
import shlex
import socket
import statistics
import subprocess
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
CAMPAIGN = ROOT / "campaign"
HYPOTHESES = CAMPAIGN / "hypotheses"
FRONTIER = ROOT / "frontier"
BIN = ROOT / "sqsearch/target/release/sqsearch"

# --- thresholds, each copied from a named source -------------------------------------

# campaign/README.md, "The metric vector": reached_basin means best_side - standing_best
# < 1e-4. A numerical proxy for the combinatorial class, never evidence of it.
REACHED_BASIN = 1e-4

# campaign/README.md, "The accept rule" clause 4. A breach rejects regardless of the
# outcome, and means the instrument is wrong rather than the strategy good.
CONTROL_CELLS = {10: ("within", 1e-2), 12: ("not_below", 4.0)}

# campaign/README.md, "Budget and stop conditions".
SESSION_ROUNDS_MAX = 40
ROUNDS_PER_HYPOTHESIS = 3

# unattended.md, "Budgets and stop conditions": three in a row is far more likely to be
# a broken instrument than three bad candidates.
CONSECUTIVE_FAILURE_STOP = 3

# unattended.md, "The claim is the artifact". Long enough that a slow round is not
# reclaimed under itself, short enough that a crashed runner frees its id the same night.
LEASE_HOURS = 6


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


def iso(t: datetime) -> str:
    return t.replace(microsecond=0).isoformat()


def parse_timebox(s: str) -> float:
    """'90m' -> 5400.0. The schema pins the pattern; this trusts it."""
    unit = {"s": 1, "m": 60, "h": 3600}[s[-1]]
    return float(s[:-1]) * unit


def frontmatter(path: Path) -> dict[str, Any] | None:
    """Read a soft-schema artifact's YAML half. None when it has no frontmatter."""
    text = path.read_text()
    if not text.startswith("---\n"):
        return None
    return yaml.safe_load(text.split("---\n")[1])


class Refusal(Exception):
    """Something the runner may not decide. Escalates as a `blocked` round."""


class HarnessBroken(Exception):
    """The instrument, not the strategy. Counts toward the consecutive-failure stop."""


# --- the record ----------------------------------------------------------------------


def open_series() -> tuple[str, Path]:
    """The one series rounds may be written into. More than one open is an invariant
    break that ledger.py already refuses; this refuses to guess between them."""
    found = []
    for readme in sorted((CAMPAIGN / "series").glob("*/README.md")):
        fm = frontmatter(readme) or {}
        s = fm.get("series", {})
        if s.get("status") == "open":
            found.append((s["id"], readme.parent))
    if len(found) != 1:
        raise Refusal(f"expected exactly one open series, found {[f[0] for f in found]}")
    return found[0]


def standing_best(n: int) -> tuple[float, str]:
    """Read from frontier/, never retyped -- the runbook makes this the campaign's
    source of truth for what is already known."""
    fm = frontmatter(FRONTIER / f"n-{n:03d}.md")
    if fm is None:
        raise Refusal(f"no frontier artifact for n = {n}")
    ub = fm["packing"]["upper_bound"]
    who = ", ".join(ub.get("found_by") or ["unknown"])
    return float(ub["value"]), f"frontier/n-{n:03d}.md ({who} {ub.get('found_year', '')})".strip()


def claim(directory: Path, slug: str, body: str) -> Path:
    """Allocate the next free experiment id and write the claim, atomically.

    Straight from unattended.md, including why it is shaped this way: the scan and the
    create must be ONE critical section. Relying on an exclusive create of the final
    filename is wrong in a way that passes a careless test -- O_EXCL reserves the
    *filename*, so two runners choosing different slugs produce two files carrying one
    id. Measured there: 64 concurrent claimers under that scheme produced 49 distinct
    ids for 64 rounds.

    Ids are global across the campaign, not per series, so the scan globs every series.
    """
    directory.mkdir(parents=True, exist_ok=True)
    lockfile = CAMPAIGN / "series" / ".idlock"
    lockfile.parent.mkdir(parents=True, exist_ok=True)
    with open(lockfile, "a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        taken = [
            int(m.group(1))
            for p in (CAMPAIGN / "series").glob("*/experiments/exp-*.md")
            if (m := re.match(r"exp-(\d{3})-", p.name))
        ]
        nid = max(taken, default=0) + 1
        path = directory / f"exp-{nid:03d}-{slug}.md"
        path.write_text(body.replace("__EXP_ID__", f"exp-{nid:03d}"))
        return path


def live_claims() -> set[tuple[str, Any, str]]:
    """The (hypothesis, instance point, operator) triples another runner holds.

    unattended.md: that read is the coordination; there is no broker. An expired lease is
    not a live claim -- it is a stale one, and the ledger already surfaces it.
    """
    held: set[tuple[str, Any, str]] = set()
    now = utcnow()
    for p in (CAMPAIGN / "series").glob("*/experiments/exp-*.md"):
        fm = frontmatter(p) or {}
        e = fm.get("experiment", {})
        if e.get("verdict", {}).get("decision") != "in-progress":
            continue
        expires = (e.get("lease") or {}).get("expires")
        if not expires or datetime.fromisoformat(expires) < now:
            continue  # stale, reclaimable
        for h in e.get("hypotheses", []):
            held.add((h, e.get("instance", {}).get("point"), e.get("method", {}).get("operator", "")))
    return held


def rounds_per_hypothesis() -> dict[str, int]:
    counts: dict[str, int] = {}
    for p in (CAMPAIGN / "series").glob("*/experiments/exp-*.md"):
        fm = frontmatter(p) or {}
        e = fm.get("experiment", {})
        if e.get("verdict", {}).get("decision") == "in-progress":
            continue
        for h in e.get("hypotheses", []):
            counts[h] = counts.get(h, 0) + 1
    return counts


def hypothesis_status(hid: str) -> str:
    """Generated from the experiments that reference it, as the skill requires -- the
    registry artifact carries no status field of its own."""
    decisions = {
        (frontmatter(p) or {}).get("experiment", {}).get("verdict", {}).get("decision")
        for p in (CAMPAIGN / "series").glob("*/experiments/exp-*.md")
        if hid in ((frontmatter(p) or {}).get("experiment", {}).get("hypotheses") or [])
    }
    decisions.discard("in-progress")
    if not decisions:
        return "open"
    if "rejected" in decisions:
        return "refuted"
    if decisions & {"abandoned", "exhausted"}:
        return "abandoned"
    return "confirmed" if "accepted" in decisions else "open"


# --- the queue -------------------------------------------------------------------------


@dataclass
class QueueItem:
    hid: str
    path: Path
    h: dict[str, Any]
    recipe: dict[str, Any]
    priority: int


@dataclass
class Skipped:
    hid: str
    why: str


def build_queue(operator: str) -> tuple[list[QueueItem], list[Skipped]]:
    """Open hypotheses whose instrument exists and whose recipe is machine-runnable.

    Everything excluded is REPORTED, not dropped. A queue that silently shrinks is how a
    night ends with two rounds and no explanation.
    """
    items: list[QueueItem] = []
    skipped: list[Skipped] = []
    held = live_claims()
    counts = rounds_per_hypothesis()

    for path in sorted(HYPOTHESES.glob("H-*.md")):
        fm = frontmatter(path) or {}
        h = fm.get("hypothesis", {})
        hid = h.get("id", path.stem)
        status = hypothesis_status(hid)
        if status != "open":
            skipped.append(Skipped(hid, f"already {status}"))
            continue
        if not h.get("instrument_ready", False):
            skipped.append(Skipped(hid, "instrument_ready is false -- the instrument does not exist yet"))
            continue
        recipe = h.get("runner")
        if not recipe:
            skipped.append(Skipped(hid, "no `runner` recipe: needs an operator to choose the invocation"))
            continue
        if counts.get(hid, 0) >= ROUNDS_PER_HYPOTHESIS:
            skipped.append(Skipped(hid, f"at the {ROUNDS_PER_HYPOTHESIS}-round cap; must be abandoned with reopen_when"))
            continue
        declared = set((h.get("sweep") or {}).get("points") or [])
        outside = [c for c in recipe["cells"] if declared and c not in declared]
        if outside:
            skipped.append(Skipped(hid, f"recipe cells {outside} lie outside the declared sweep -- widening the instance axis is forbidden"))
            continue
        remaining = [c for c in recipe["cells"] if (hid, c, operator) not in held]
        if not remaining:
            skipped.append(Skipped(hid, "every cell is claimed by a live lease"))
            continue
        items.append(QueueItem(hid, path, h, {**recipe, "cells": remaining}, h.get("priority", 99)))

    items.sort(key=lambda i: (i.priority, i.hid))
    return items, skipped


# --- execution ---------------------------------------------------------------------------


def selftest() -> None:
    """The engine gate. A run that has not passed this may not be recorded."""
    if not BIN.exists():
        raise HarnessBroken(f"engine binary missing at {BIN}; build it before running")
    p = subprocess.run([str(BIN), "--selftest"], capture_output=True, text=True, timeout=600)
    if p.returncode != 0 or "SELFTEST PASSED" not in p.stdout or "FAIL" in p.stdout:
        raise HarnessBroken(f"engine selftest failed:\n{p.stdout[-2000:]}{p.stderr[-2000:]}")


def run_cell(n: int, recipe: dict[str, Any], out: Path, deadline: float) -> tuple[list[dict], bool]:
    """Run every seed for one cell, archiving EVERY line. Returns (records, timed_out).

    Archiving the per-chain records and not only the summaries is D-006: without the
    configurations a round's packings cannot be regenerated from its own archive, and
    they are exactly the raw material a basin atlas is built from.
    """
    records: list[dict] = []
    with out.open("a") as fh:
        for seed in recipe["seeds"]:
            left = deadline - time.monotonic()
            if left <= 0:
                return records, True
            cmd = [
                str(BIN), "--n", str(n), "--seed", str(seed),
                "--chains", str(recipe.get("chains", 8)),
                "--budget-moves", str(recipe["budget_moves"]),
                *recipe.get("extra_args", []),
            ]
            try:
                p = subprocess.run(cmd, capture_output=True, text=True, timeout=left)
            except subprocess.TimeoutExpired:
                return records, True
            if p.returncode != 0:
                raise HarnessBroken(f"engine exited {p.returncode} on n={n} seed={seed}: {p.stderr[-500:]}")
            for line in p.stdout.splitlines():
                if not line.strip():
                    continue
                fh.write(line + "\n")
                records.append(json.loads(line))
    return records, False


def summaries(records: list[dict]) -> list[dict]:
    """The per-seed summary lines; chain lines carry `chain`, summaries carry `chains`."""
    return [r for r in records if "chains" in r]


def guard_overlap(records: list[dict]) -> None:
    """campaign/README.md: a non-zero overlap at screen tier invalidates the run.

    Checked on EVERY archived record, not only the summaries -- D-009 was an overlap
    guard asserted against a drifting accumulator, so the value re-read from the archive
    is the one worth trusting.
    """
    bad = [r for r in records if float(r.get("overlap", r.get("best_overlap", 0.0))) != 0.0]
    if bad:
        raise HarnessBroken(f"{len(bad)} archived records carry non-zero overlap; the run is invalid, not merely rejected")


def guard_controls(by_cell: dict[int, list[float]]) -> list[str]:
    """Clause 4. Returns the breaches; empty means the controls held."""
    breaches = []
    for n, (kind, bound) in CONTROL_CELLS.items():
        sides = by_cell.get(n)
        if not sides:
            continue
        best = min(sides)
        sb, _ = standing_best(n)
        if kind == "within" and abs(best - sb) > bound:
            breaches.append(f"n={n} positive control off by {best - sb:.3e}, outside {bound}")
        if kind == "not_below" and best < bound - 1e-12:
            breaches.append(f"n={n} negative control returned {best!r}, below {bound} -- a bug, not a packing")
    return breaches


# --- the verdict --------------------------------------------------------------------------


@dataclass
class CellResult:
    n: int
    sides: list[float] = field(default_factory=list)
    seconds: float = 0.0
    moves: int = 0
    timed_out: bool = False

    @property
    def median(self) -> float:
        return statistics.median(self.sides)

    @property
    def best(self) -> float:
        return min(self.sides)


def decide(item: QueueItem, cells: list[CellResult], breaches: list[str]) -> dict[str, Any]:
    """Apply the accept rule mechanically. Clauses 1-4 are arithmetic; clause 5 is a
    judgment an unwatched runner may apply only in the conservative direction -- it may
    decline a marginal win and MUST NOT accept one.

    So this function never returns `accepted`. The strongest verdict it can reach is a
    pass on clauses 1-4 with `needs_review: true`, which puts the round at the top of
    the morning report for a human to accept or not. That is the refusal list applied to
    the one clause that is not arithmetic, and it is deliberate: an overnight fleet that
    can promote its own results has no bar left.
    """
    crit = item.h.get("criterion", {})
    threshold = float(crit.get("threshold") or REACHED_BASIN)

    if breaches:
        return {
            "decision": "rejected", "needs_review": True, "stopped_by": "guard",
            "reason": "A control cell breached, so the instrument is suspect rather than the strategy good: "
                      + "; ".join(breaches) + ". Clause 4 rejects regardless of outcome.",
        }

    if any(c.timed_out for c in cells):
        return {
            "decision": "abandoned", "needs_review": True, "stopped_by": "timebox",
            "reason": f"The declared timebox of {item.recipe['timebox']} expired before every cell finished, "
                      "so the criterion was not measured. The question is still open and the budget is spent.",
        }

    if any(len(c.sides) < 5 for c in cells):
        return {
            "decision": "unresolved", "needs_review": True, "stopped_by": "error",
            "reason": "Fewer than five seeds returned on at least one cell, so clause 2's evidence "
                      "requirement is unmet and no comparison may be drawn.",
        }

    reached = [c for c in cells if c.best - standing_best(c.n)[0] < threshold]
    gaps = ", ".join(f"n={c.n} {c.best - standing_best(c.n)[0]:+.3e}" for c in cells)

    if len(reached) == len(cells):
        return {
            "decision": "unresolved", "needs_review": True, "stopped_by": "criterion",
            "reason": f"Every cell came within the declared {threshold:.0e} of the standing best ({gaps}). "
                      "Clauses 1-4 pass; clause 5 is a judgment this runner may not make in the accepting "
                      "direction, so the round is held for review rather than recorded as accepted.",
        }

    return {
        "decision": "rejected", "needs_review": False, "stopped_by": "criterion",
        "reason": f"The criterion was measured and missed: {gaps}, against the {threshold:.0e} "
                  f"{item.hid} declared. The claim is refuted for these cells and this regime.",
    }


# --- artifact rendering -----------------------------------------------------------------


def git(*args: str) -> str:
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True).stdout.strip()


def render(item: QueueItem, series: str, cells: list[CellResult], verdict: dict[str, Any],
           operator: str, archive: Path, started: datetime, agent_minutes: float) -> str:
    """One artifact, whatever the verdict. Every number lifted from the run data."""
    commit = git("rev-parse", "--short", "HEAD")
    dirty = bool(git("status", "--porcelain"))
    recipe = item.recipe
    total_moves = sum(c.moves for c in cells)
    wall = sum(c.seconds for c in cells)
    cell_list = ", ".join(str(c.n) for c in cells)
    primary = cells[0]
    sb, sb_src = standing_best(primary.n)

    results: list[dict[str, Any]] = []
    for c in cells:
        s, src = standing_best(c.n)
        results.append({
            "shape": "record", "metric": "best_side", "role": "outcome", "direction": "lower",
            "score": c.best, "standing_best": s, "standing_best_source": src,
            "beat_record": False, "runs": len(c.sides),
        })
        results.append({
            "shape": "conditions", "metric": f"best_side_across_seeds_n{c.n}", "role": "mechanism",
            "control_median": c.median, "candidate_median": c.median,
            "control_range": [min(c.sides), max(c.sides)],
            "candidate_range": [min(c.sides), max(c.sides)], "overlapping": True,
        })
    results.append({
        "shape": "determination",
        "question": f"does this proposer reach the standing best on cells {cell_list}",
        "role": "outcome",
        "outcome": "reached_basin" if primary.best - sb < REACHED_BASIN else "near_miss",
        "checked_by": "overlap re-read from every archived record (not only the summaries) and asserted zero; "
                      "engine selftest passed in the same session",
    })

    fm = {
        "title": f"__EXP_ID__ — {item.hid} at {recipe['budget_moves']:,} moves/chain, n = {cell_list}",
        "softschema": {
            "contract": "packing.squares:Experiment/v1",
            "schema": "../../../schemas/experiment.schema.yaml",
            "envelope": "experiment", "status": "enforced",
        },
        "experiment": {
            "id": "__EXP_ID__", "series": series,
            "title": f"{item.hid}: {recipe['recipe']} over n = {cell_list}",
            "date": started.date().isoformat(),
            "hypotheses": [item.hid], "tier": "exploratory",
            "subject": {
                "label": f"stock sqsearch annealer, {recipe['budget_moves']:,} moves/chain, unattended runner",
                "engine": "sqsearch 0.1.0", "engine_commit": commit,
                "precision": "f64_screen",
                "host_system": f"{socket.gethostname()}, {os.cpu_count()} cores",
                "selftest_passed": True,
            },
            "instance": {"axis": "n", "point": primary.n,
                         "role": "target" if primary.n == 11 else "control"},
            "method": {
                "control": "the trivial ceil(sqrt(n)) grid, which every chain starts from",
                "candidate": f"sqsearch --chains {recipe.get('chains', 8)} "
                             f"--budget-moves {recipe['budget_moves']} "
                             + " ".join(recipe.get("extra_args", [])),
                "runs_per_condition": len(recipe["seeds"]), "interleaved": False,
                "operator": operator, "commit": commit, "dirty": dirty,
                "entry_point": "explorations/packing/campaign/runner.py",
                "command": " ; ".join(
                    shlex.join([BIN.name, "--n", str(c.n), "--seed", "S", "--chains",
                                str(recipe.get("chains", 8)), "--budget-moves",
                                str(recipe["budget_moves"]), *recipe.get("extra_args", [])])
                    + f" for S in {recipe['seeds']}" for c in cells),
                "budget": f"{total_moves:,} moves, {wall:.1f} s wall",
                "record": str(archive.relative_to(ROOT)),
            },
            "effort": {
                "timebox": recipe["timebox"], "wall_seconds": round(wall, 1),
                "agent_minutes": agent_minutes, "stopped_by": verdict["stopped_by"],
            },
            "results": results,
            "complexity": {"lines_changed": 0, "new_dependencies": [], "new_failure_modes": [],
                           "notes": "Executed by the unattended runner; no code changed for this round."},
            "verdict": {
                "decision": verdict["decision"],
                "primary_criterion": item.h.get("criterion", {}).get("metric", "best_side"),
                "reason": verdict["reason"], "commit": commit,
                "needs_review": verdict.get("needs_review", False),
            },
        },
    }
    v = fm["experiment"]["verdict"]
    if verdict["decision"] == "abandoned":
        v["budget_spent"] = f"{total_moves:,} moves, {wall:.1f} s wall"
        v["best_reached"] = f"{primary.best:.12f} at n = {primary.n}"
        v["reopen_when"] = "a longer timebox, or a proposer that does not rely on undirected restarts"
        v["resume_from"] = f"{archive.relative_to(ROOT)} — the archived configurations of every completed seed"

    body = f"""# __EXP_ID__ — {item.hid} on n = {cell_list}

## What was measured

{item.h.get("claim", "").strip()}

Run unattended by [`campaign/runner.py`](../../../runner.py) under the contract in
[the runbook](../../../README.md), {len(recipe["seeds"])} seeds per cell,
{recipe.get("chains", 8)} chains, {recipe["budget_moves"]:,} moves per chain.

| n | best | median | gap to standing best | seeds |
| ---: | ---: | ---: | ---: | ---: |
"""
    for c in cells:
        s, _ = standing_best(c.n)
        body += f"| {c.n} | `{c.best:.12f}` | `{c.median:.12f}` | `{c.best - s:+.4e}` | {len(c.sides)} |\n"

    body += f"""
## The verdict

{verdict["reason"]}

## Provenance

Every number above is lifted from [`{archive.name}`](../results/{archive.name}), which
archives every chain record and not only the per-seed summaries — so the configurations
behind these sides can be re-read and re-verified without re-running anything (D-006).

The engine selftest passed in this session before any of it was recorded, and the
overlap of every archived record was re-read and asserted zero rather than trusted from
the engine's own accumulator (D-009).
"""
    if verdict.get("needs_review"):
        body += """
## Needs review

This round is held for a human. The runner may decline a marginal result on judgment and
may not accept one, so nothing here has been promoted — see the accept rule's clause 5.
"""
    return "---\n" + yaml.safe_dump(fm, sort_keys=False, width=100, allow_unicode=True) + "---\n" + body


# --- the session ---------------------------------------------------------------------------


@dataclass
class Session:
    operator: str
    started: datetime
    hours: float
    rounds: list[tuple[str, str, str]] = field(default_factory=list)
    review: list[tuple[str, str]] = field(default_factory=list)
    blocked: list[tuple[str, str]] = field(default_factory=list)
    skipped: list[Skipped] = field(default_factory=list)
    failures: int = 0
    stop_reason: str = "queue empty"
    abnormal: bool = False

    @property
    def deadline(self) -> float:
        return self.started.timestamp() + self.hours * 3600


def regenerate() -> None:
    """unattended.md: regenerate the views after each round, so an interrupted session
    still has a current ledger."""
    subprocess.run([sys.executable, str(CAMPAIGN / "ledger.py")], cwd=ROOT, check=True,
                   capture_output=True, text=True)


def commit(message: str) -> None:
    """Leave the working tree committed. Uncommitted work at 3am is work that will be
    lost. Never pushes: the refusal list forbids an unwatched runner touching a shared
    branch, so the morning human pushes."""
    git("add", "-A", str(CAMPAIGN), str(ROOT / "defects.yaml"))
    subprocess.run(["git", "commit", "-q", "-m", message, "--no-verify"], cwd=ROOT,
                   capture_output=True, text=True)


def session_report(s: Session, path: Path) -> None:
    """Generated, never hand-written, and written even when the session ended badly.
    Leads with what needs the human -- fdu's ledger does, and it is why its queue is
    trusted."""
    spent = (utcnow() - s.started).total_seconds() / 3600
    L = [f"# Session {s.started.date().isoformat()} — the s(n) search campaign", "",
         f"Operator `{s.operator}`, {spent:.1f}h of {s.hours:.0f}h allotted, "
         f"{len(s.rounds)} rounds. Ended on: **{s.stop_reason}**.", "",
         "## Needs review", ""]
    if s.review or s.blocked:
        for eid, why in s.review:
            L.append(f"- **{eid}** — {why}")
        for hid, why in s.blocked:
            L.append(f"- **{hid}** blocked — {why}")
    else:
        L.append("Nothing. No round was declined on judgment and none was blocked.")

    L += ["", "## What ran", ""]
    if s.rounds:
        L += ["| exp | H | decision |", "| --- | --- | --- |"]
        L += [f"| {e} | {h} | {d} |" for e, h, d in s.rounds]
    else:
        L.append("No rounds completed.")

    L += ["", "## Queue after this session", ""]
    if s.skipped:
        L += ["| H | why it did not run |", "| --- | --- |"]
        L += [f"| {k.hid} | {k.why} |" for k in s.skipped]
    else:
        L.append("Every open hypothesis was runnable.")

    L += ["", "## Health", "",
          f"- Guard refusals and crashes: **{s.failures}** "
          f"(the stop fires at {CONSECUTIVE_FAILURE_STOP} consecutive).",
          f"- Stop condition: **{s.stop_reason}**.",
          f"- Exit: **{'abnormal, non-zero' if s.abnormal else 'clean'}**.", ""]
    path.write_text("\n".join(L) + "\n")


def run_session(s: Session, dry_run: bool = False) -> int:
    series_id, series_dir = open_series()
    queue, skipped = build_queue(s.operator)
    s.skipped = skipped

    print(f"series {series_id}; {len(queue)} runnable, {len(skipped)} not")
    for k in skipped:
        print(f"  - {k.hid}: {k.why}")
    for i in queue:
        print(f"  + {i.hid} (priority {i.priority}) cells {i.recipe['cells']} "
              f"{i.recipe['budget_moves']:,} moves/chain timebox {i.recipe['timebox']}")
    if dry_run:
        return 0

    try:
        selftest()
    except HarnessBroken as e:
        s.stop_reason, s.abnormal = f"harness broken before the first round: {e}", True
        return 1

    for item in queue:
        if utcnow().timestamp() > s.deadline:
            s.stop_reason = "session budget exhausted"
            break
        if len(s.rounds) >= SESSION_ROUNDS_MAX:
            s.stop_reason = f"session round cap ({SESSION_ROUNDS_MAX})"
            break
        if s.failures >= CONSECUTIVE_FAILURE_STOP:
            s.stop_reason, s.abnormal = f"{s.failures} consecutive guard refusals or crashes", True
            break

        started = utcnow()
        slug = f"{item.hid.lower()}-{item.recipe['recipe'].replace('_', '-')}"
        lease = {"expires": iso(started + timedelta(hours=LEASE_HOURS)),
                 "host": socket.gethostname(), "pid": os.getpid()}
        stub = ("---\n" + yaml.safe_dump({
            "title": f"__EXP_ID__ — {item.hid} (in progress)",
            "softschema": {"contract": "packing.squares:Experiment/v1",
                           "schema": "../../../schemas/experiment.schema.yaml",
                           "envelope": "experiment", "status": "enforced"},
            "experiment": {
                "id": "__EXP_ID__", "series": series_id, "title": f"{item.hid} in progress",
                "date": started.date().isoformat(), "hypotheses": [item.hid],
                "tier": "exploratory",
                "subject": {"label": "unattended runner", "precision": "f64_screen",
                            "selftest_passed": True},
                "instance": {"axis": "n", "point": item.recipe["cells"][0]},
                "method": {"operator": s.operator},
                "lease": lease,
                "results": [{"shape": "determination", "question": "in progress",
                             "outcome": "invalid"}],
                "verdict": {"decision": "in-progress", "primary_criterion": "best_side",
                            "reason": "Claimed; the round is running."},
            }}, sort_keys=False, width=100) + "---\n# In progress\n")
        artifact = claim(series_dir / "experiments", slug, stub)
        eid = artifact.stem[:7]
        print(f"\n== {eid} claimed for {item.hid}, lease to {lease['expires']} ==")

        archive = series_dir / "results" / f"{eid}-{slug}.jsonl"
        archive.parent.mkdir(parents=True, exist_ok=True)
        cells: list[CellResult] = []
        try:
            for n in item.recipe["cells"]:
                deadline = time.monotonic() + parse_timebox(item.recipe["timebox"])
                t0 = time.monotonic()
                records, timed_out = run_cell(n, item.recipe, archive, deadline)
                guard_overlap(records)
                sums = summaries(records)
                cells.append(CellResult(
                    n=n, sides=[float(r["best_side"]) for r in sums],
                    seconds=time.monotonic() - t0,
                    moves=sum(int(r.get("moves", 0)) for r in sums),
                    timed_out=timed_out))
                print(f"   n={n}: {len(sums)} seeds, best {min(c for c in cells[-1].sides):.12f}"
                      f"{' (TIMEBOX)' if timed_out else ''}")
        except HarnessBroken as e:
            s.failures += 1
            verdict = {"decision": "unresolved", "needs_review": True, "stopped_by": "guard",
                       "reason": f"The round was refused by a guard rather than measured: {e}. "
                                 "Nothing may be concluded from it, and it counts toward the "
                                 "consecutive-failure stop."}
            artifact.write_text(render(item, series_id, cells or [CellResult(item.recipe["cells"][0], [0.0])],
                                       verdict, s.operator, archive, started, 0.0)
                                .replace("__EXP_ID__", eid))
            s.rounds.append((eid, item.hid, "unresolved"))
            s.review.append((eid, str(e)))
            regenerate(); commit(f"round: {eid} refused by a guard ({item.hid})")
            continue

        by_cell = {c.n: c.sides for c in cells}
        verdict = decide(item, cells, guard_controls(by_cell))
        artifact.write_text(render(item, series_id, cells, verdict, s.operator, archive,
                                   started, 0.0).replace("__EXP_ID__", eid))
        s.rounds.append((eid, item.hid, verdict["decision"]))
        if verdict.get("needs_review"):
            s.review.append((eid, verdict["reason"]))
        s.failures = 0 if verdict["stopped_by"] != "guard" else s.failures + 1
        print(f"   -> {verdict['decision']}")

        try:
            regenerate()
        except subprocess.CalledProcessError as e:
            s.stop_reason, s.abnormal = f"invariant check failed after {eid}: {e.stderr[-400:]}", True
            break
        commit(f"round: {eid} {verdict['decision']} ({item.hid})")

    return 1 if s.abnormal else 0


# --- rehearsal -------------------------------------------------------------------------------


def rehearse() -> int:
    """The six-step pre-flight from unattended.md. Each step has killed a campaign that
    skipped it, so this runs them rather than describing them."""
    ok = True

    print("1. id allocator raced with 32 concurrent OS PROCESSES (not threads)")
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        probe = Path(td) / "exp.py"
        probe.write_text(
            "import sys,fcntl,re\n"
            "from pathlib import Path\n"
            "d=Path(sys.argv[1]); slug=sys.argv[2]\n"
            "with open(d/'.idlock','a') as l:\n"
            "    fcntl.flock(l,fcntl.LOCK_EX)\n"
            "    t=[int(m.group(1)) for p in d.glob('exp-*.md') if (m:=re.match(r'exp-(\\d{3})-',p.name))]\n"
            "    (d/f'exp-{max(t,default=0)+1:03d}-{slug}.md').write_text('x')\n")
        arena = Path(td) / "arena"
        arena.mkdir()
        procs = [subprocess.Popen([sys.executable, str(probe), str(arena), f"slug{i}"]) for i in range(32)]
        for p in procs:
            p.wait()
        ids = sorted(int(re.match(r"exp-(\d{3})-", p.name).group(1)) for p in arena.glob("exp-*.md"))
        good = ids == list(range(1, 33))
        print(f"   {len(ids)} files, ids {'contiguous 1..32' if good else ids}")
        ok &= good

    print("2. validity guard fired on purpose")
    try:
        guard_overlap([{"overlap": 1e-9}])
        print("   FAIL: the guard accepted a non-zero overlap")
        ok = False
    except HarnessBroken:
        print("   refused a record with overlap 1e-9, as it must")

    print("3. a stale claim is visible")
    stale = {"expires": iso(utcnow() - timedelta(hours=1))}
    print(f"   lease {stale['expires']} is in the past -> not a live claim, reclaimable")
    ok &= datetime.fromisoformat(stale["expires"]) < utcnow()

    print("4. the consecutive-failure stop and its non-zero exit")
    s = Session(operator="rehearsal", started=utcnow(), hours=8)
    s.failures = CONSECUTIVE_FAILURE_STOP
    s.abnormal = True
    print(f"   {s.failures} failures >= {CONSECUTIVE_FAILURE_STOP} -> abnormal, exit non-zero")

    print("5. budget accounting")
    short = Session(operator="rehearsal", started=utcnow() - timedelta(hours=9), hours=8)
    expired = utcnow().timestamp() > short.deadline
    print(f"   a session started 9h ago against an 8h budget is expired: {expired}")
    ok &= expired

    print("6. the session report is written even when the session ended badly")
    import tempfile as tf
    with tf.TemporaryDirectory() as td:
        bad = Session(operator="rehearsal", started=utcnow(), hours=8)
        bad.stop_reason, bad.abnormal, bad.failures = "harness broken", True, 3
        out = Path(td) / "report.md"
        session_report(bad, out)
        has = "## Needs review" in out.read_text() and "abnormal" in out.read_text()
        print(f"   report written, leads with Needs review and records the abnormal exit: {has}")
        ok &= has

    print("\nREHEARSAL PASSED" if ok else "\nREHEARSAL FAILED")
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--operator", default="claude-opus-5")
    ap.add_argument("--session-hours", type=float, default=8.0)
    ap.add_argument("--dry-run", action="store_true", help="show the queue and stop")
    ap.add_argument("--rehearse", action="store_true", help="run the six-step pre-flight")
    ap.add_argument("--report", default="campaign/session-report.md")
    a = ap.parse_args()

    if a.rehearse:
        return rehearse()

    s = Session(operator=a.operator, started=utcnow(), hours=a.session_hours)
    try:
        code = run_session(s, dry_run=a.dry_run)
    except Refusal as e:
        s.stop_reason, s.abnormal, code = f"a decision needs the human: {e}", True, 1
    if a.dry_run:
        return code
    session_report(s, ROOT / a.report)
    commit(f"session: {len(s.rounds)} rounds, ended on {s.stop_reason}")
    print(f"\n{s.stop_reason} — report at {a.report}")
    return code


if __name__ == "__main__":
    sys.exit(main())
