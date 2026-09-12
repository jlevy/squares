#!/usr/bin/env python3
"""Does the workbench's blind physics rediscover a known-best packing, and how often?

    uv run --frozen --group dev python -m devtools.bench_annealing --n 11 17 --seeds 40
    uv run --frozen --group dev python -m devtools.bench_annealing --n 11 --seeds 200
    uv run --frozen --group dev python -m devtools.bench_annealing --replay results/....jsonl

The page's physics is a search. In blind mode it is told nothing about where the squares
are meant to end up: it starts from the packing of n in an inflated container, drops the
new square into the emptiest place a coarse grid finds, and closes the walls in with
contacts, walls and a decaying jiggle. Whether it lands on the record is a question with
a number for an answer, and this is where the number comes from.

**One trial is one (n, seed, parameter set).** Before `setSeed` existed there was exactly
one trial per n, because every generator on the page was seeded from n alone -- so a rate
was 0 or 1 and meant nothing. The seed is what makes a rate a rate.

**What it reports, and why each part is there.** The success rate alone hides the shape of
the failures: a method that lands 0.1% above the record every time is a different thing
from one that scatters, and only the distribution says which. Cost is reported beside the
rate because a parameter set that wins by running ten times longer has not won. And every
trial carries its seed, so any claim here can be re-run rather than believed.

**It finishes.** `check_revision6.py` runs a blind sweep over 323 pairs and has never
completed -- 57 minutes without finishing, measured, and still going at 30 on an idle
machine. This one samples the n it is given, streams each trial to disk as it lands, and
stops at `--budget` seconds with a partial result rather than a lost one.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import statistics
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PAGE = PROJECT_ROOT / "site/workbench/index.html"
RESULTS = PROJECT_ROOT / "campaign/results/annealing"

#: How close a run's container side has to come to the record to count as having found it.
#:
#: Argued rather than picked. The record's own poses, replayed through the same measurement,
#: score 0 to 1.3e-5 of a unit side of summed overlap -- the float precision of the stored
#: poses -- so anything looser than that is measuring the tolerance and not the search. The
#: three reported here bracket it: `exact` is at the noise floor, `close` is a tenth of a
#: per cent, and `near` is one per cent, which is about the gap between the best known
#: packing and the grid it improves on at these n.
TOLERANCES = {"exact": 0.0001, "close": 0.1, "near": 1.0}

#: The metric the accept rule scores, and it is NOT the raw excess.
#:
#: `miss.excess` is `(side / record - 1) * 100` -- the percentage the run's container exceeds
#: the best known one by -- and it cannot be compared across n, because the room between the
#: record and the trivial grid differs at every n. At n = 29 the grid is 1.1% above the record
#: and at n = 5 it is 10.8%, so an excess of 1% is nearly a failure at the first and a strong
#: result at the second.
#:
#: `closed` normalises it: 1 means the run reached the record, 0 means it got no further than
#: the grid `ceil(sqrt(n))`, and a negative number means it ended worse than the grid.
#: Measured over 1200 trials at six n it sits at 0.47 with a range of 0.33 to 0.70 -- which is
#: what turned "n = 11 is easy and n = 17 is hard" into "the method closes about half the gap
#: wherever it is pointed, and the two only looked different because their gaps differ".
OUTCOME = "closed"

#: The k at which best-of-k is reported. A trial costs a fraction of a millisecond, so the
#: question is never "what does one run give" but "what does the best of a budget give", and
#: the ladder is what shows whether more budget is still buying anything.
BEST_OF = (1, 10, 100, 1000, 10_000)

#: How deep two squares may overlap in the final arrangement before the trial is INVALID
#: rather than merely poor.
#:
#: This is the guard, and it is the reason the first sweep's headline was wrong. Thirty cells
#: reported a best-of-k `closed` above 1 -- a container BELOW the known-best side, which is
#: either a new record or a run whose squares are inside each other. It is the second: the
#: side is the bounding box of the final poses, and a box can be made arbitrarily small by
#: letting the squares intersect. A search that is allowed to cheat reports cheating as
#: progress.
#:
#: **The number is measured, not chosen.** Run the same check over the SNAPPED trajectory,
#: which ends on the record's own poses by construction, and the deepest pair overlap is
#: 5.5e-7 at n = 5, 1.0e-6 at n = 11 and 7.3e-7 at n = 17 -- the float noise the stored poses
#: carry. A blind run at the same n scores 0.091, 0.035 and 0.095. Two orders of magnitude
#: separate the noise from the smallest real overlap, so 1e-5 refuses overlaps without
#: refusing arithmetic, and the control is what says so rather than a guess about precision.
VALID_OVERLAP = 1e-5


def gap_closed(n: int, record: float, excess: float) -> float:
    """How much of the record-to-grid gap a run closed: 1 reached the record, 0 the grid.

    `ceil(sqrt(n))` is the trivial grid and no best known packing exceeds it, checked over the
    whole corpus. It is the honest zero for this search: the blind run has to beat the grid
    before it has done anything at all.
    """
    grid = math.ceil(math.sqrt(n))
    gap = (grid / record - 1) * 100
    if gap <= 0:
        return float("nan")
    return 1 - excess / gap


@dataclass
class Trial:
    """One blind run: what it was asked, and what came back."""

    n: int
    seed: int
    style: str
    excess: float
    side: float
    record: float
    closed: float
    overlap: float
    resolved_side: float
    resolved_closed: float
    resolved_overlap: float
    steps: int
    ms: float
    centre: float
    angle: float
    params: dict[str, Any] = field(default_factory=dict)

    def row(self) -> dict[str, Any]:
        return {
            "n": self.n,
            "seed": self.seed,
            "style": self.style,
            "excess": self.excess,
            "closed": self.closed,
            "overlap": self.overlap,
            "resolved_side": self.resolved_side,
            "resolved_closed": self.resolved_closed,
            "resolved_overlap": self.resolved_overlap,
            "side": self.side,
            "record": self.record,
            "steps": self.steps,
            "ms": self.ms,
            "centre": self.centre,
            "angle": self.angle,
            **({"params": self.params} if self.params else {}),
        }


#: Runs one blind trial in the page and returns its miss record. Kept here rather than in a
#: probe file because this tool is the only caller and the probe directory belongs to the
#: workbench's own checkers.
TRIAL_JS = """
(o) => {
  const A = window.atlasTransitions;
  A.setSeed(o.seed);
  if (o.inflate !== null) { A.setBlindInflate(o.inflate); }
  if (o.anneal !== null) { A.setAnneal(o.anneal); }
  const index = A.pairs().findIndex((q) => q.n + 1 === o.n);
  if (index < 0) { return { error: `the page carries no pair into n = ${o.n}` }; }
  const started = performance.now();
  const r = A.physics(index, o.style, "blind");

  // **The validity check, written here rather than read off the simulation.**
  //
  // The deepest overlap between any two squares in the FINAL arrangement, by the separating
  // axis theorem: two convex polygons are disjoint exactly when some edge normal separates
  // them, and for squares the four candidate axes are the two edge directions of each. The
  // depth is the smallest overlap across those axes, and it is zero the moment one separates.
  //
  // It is computed from the poses the run ended on, with none of the page's own bookkeeping,
  // because the thing being checked is whether the page's answer is a packing at all. The
  // simulation reports `maxPenetration` over the whole trajectory, which says how deep the
  // squares went at any instant and nothing about where they stopped.
  const poses = r.final;
  const N = poses.length;
  const axesOf = (a) => {
    const t = (a * Math.PI) / 180;
    return [[Math.cos(t), Math.sin(t)], [-Math.sin(t), Math.cos(t)]];
  };
  const cornersOf = (p) => {
    const t = (p[2] * Math.PI) / 180;
    const c = Math.cos(t) / 2, s = Math.sin(t) / 2;
    return [
      [p[0] + c - s, p[1] + s + c],
      [p[0] - c - s, p[1] - s + c],
      [p[0] - c + s, p[1] - s - c],
      [p[0] + c + s, p[1] + s - c],
    ];
  };
  const spanOn = (pts, ax) => {
    let lo = Infinity, hi = -Infinity;
    for (const q of pts) {
      const v = q[0] * ax[0] + q[1] * ax[1];
      if (v < lo) { lo = v; }
      if (v > hi) { hi = v; }
    }
    return [lo, hi];
  };
  let deepest = 0;
  const corners = poses.map(cornersOf);
  for (let i = 0; i < N; i++) {
    for (let j = i + 1; j < N; j++) {
      if (Math.hypot(poses[i][0] - poses[j][0], poses[i][1] - poses[j][1]) > 1.4143) {
        continue;
      }
      let depth = Infinity;
      for (const ax of [...axesOf(poses[i][2]), ...axesOf(poses[j][2])]) {
        const [al, ah] = spanOn(corners[i], ax);
        const [bl, bh] = spanOn(corners[j], ax);
        const over = Math.min(ah, bh) - Math.max(al, bl);
        if (over <= 0) { depth = 0; break; }
        if (over < depth) { depth = over; }
      }
      if (depth > deepest) { deepest = depth; }
    }
  }

  // **The resolution phase: what container does this arrangement actually need?**
  //
  // A run that ends overlapping has not found a container, it has found a number. Pushing
  // the squares apart until no pair overlaps -- translation only, angles held, each pair
  // separated along its own minimum-penetration axis -- turns that number into one about a
  // packing. The box that fits the separated arrangement is the honest answer.
  //
  // This is a projection rather than a search: it never improves an arrangement, it only
  // stops it cheating. `resolvedSide` is therefore always at least the raw side, and the
  // difference between them is how much of the raw result was overlap.
  const rp = poses.map((q) => [q[0], q[1], q[2]]);
  let unresolved = true;
  let sweeps = 0;
  for (; sweeps < 400 && unresolved; sweeps++) {
    unresolved = false;
    const cs = rp.map(cornersOf);
    for (let i = 0; i < N; i++) {
      for (let j = i + 1; j < N; j++) {
        if (Math.hypot(rp[i][0] - rp[j][0], rp[i][1] - rp[j][1]) > 1.4143) { continue; }
        let depth = Infinity, best = null, sign = 1;
        for (const ax of [...axesOf(rp[i][2]), ...axesOf(rp[j][2])]) {
          const [al, ah] = spanOn(cs[i], ax);
          const [bl, bh] = spanOn(cs[j], ax);
          const over = Math.min(ah, bh) - Math.max(al, bl);
          if (over <= 0) { depth = 0; break; }
          if (over < depth) {
            depth = over;
            best = ax;
            sign = ah - bh > 0 ? 1 : -1;
          }
        }
        if (depth > 1e-9 && best !== null) {
          unresolved = true;
          const push = (depth / 2 + 1e-9) * sign;
          rp[i][0] += best[0] * push; rp[i][1] += best[1] * push;
          rp[j][0] -= best[0] * push; rp[j][1] -= best[1] * push;
          cs[i] = cornersOf(rp[i]); cs[j] = cornersOf(rp[j]);
        }
      }
    }
  }
  let rx0 = Infinity, rx1 = -Infinity, ry0 = Infinity, ry1 = -Infinity;
  for (const q of rp) {
    for (const c of cornersOf(q)) {
      if (c[0] < rx0) { rx0 = c[0]; }
      if (c[0] > rx1) { rx1 = c[0]; }
      if (c[1] < ry0) { ry0 = c[1]; }
      if (c[1] > ry1) { ry1 = c[1]; }
    }
  }
  const resolvedSide = Math.max(rx1 - rx0, ry1 - ry0);
  let resolvedOverlap = 0;
  const rcs = rp.map(cornersOf);
  for (let i = 0; i < N; i++) {
    for (let j = i + 1; j < N; j++) {
      let depth = Infinity;
      for (const ax of [...axesOf(rp[i][2]), ...axesOf(rp[j][2])]) {
        const [al, ah] = spanOn(rcs[i], ax);
        const [bl, bh] = spanOn(rcs[j], ax);
        const over = Math.min(ah, bh) - Math.max(al, bl);
        if (over <= 0) { depth = 0; break; }
        if (over < depth) { depth = over; }
      }
      if (depth > resolvedOverlap) { resolvedOverlap = depth; }
    }
  }

  return {
    excess: r.miss.excess,
    side: r.miss.side,
    record: r.miss.record,
    centre: r.miss.centre,
    angle: r.miss.angle,
    overlap: deepest,
    resolvedSide,
    resolvedOverlap,
    sweeps,
    steps: r.steps,
    ms: performance.now() - started,
  };
}
"""

#: Asserts the instrument was measuring something before any of its numbers are believed.
#: Six runs in another campaign were taken in a 0x0 browser pane and produced plausible
#: timings measured against nothing; the guard here is the same idea -- a page with no API,
#: no pairs, or a record of zero is not a page this tool may report on.
GUARD_JS = """
() => {
  const A = window.atlasTransitions;
  if (!A || typeof A.physics !== "function") { return { ok: false, why: "no page API" }; }
  if (typeof A.setSeed !== "function") { return { ok: false, why: "the page has no seed" }; }
  const pairs = A.pairs();
  if (!pairs || pairs.length === 0) { return { ok: false, why: "the page carries no pairs" }; }
  return { ok: true, pairs: pairs.length, seed: A.seed() };
}
"""


def _launch(playwright: Any) -> Any:
    """The pinned headless shell if the environment names one, else Playwright's own."""
    return playwright.chromium.launch(executable_path=os.environ.get("SQPACK_CHROMIUM"))


@dataclass(frozen=True)
class Run:
    """What one invocation of the harness is asked for.

    A record rather than seven positional arguments, because every one of these is part of
    the regime a result is evidence about -- they belong together in the artifact too.
    """

    sizes: list[int]
    seeds: list[int]
    style: str
    inflate: float | None
    anneal: int | None
    budget: float
    out: Path

    @property
    def params(self) -> dict[str, Any]:
        """The parameter overrides, for the row each trial writes."""
        return {
            key: value
            for key, value in (("inflate", self.inflate), ("anneal", self.anneal))
            if value is not None
        }


def run_trials(run: Run) -> list[Trial]:
    """Every (n, seed) in the grid, streamed to `out` as each lands."""
    from playwright.sync_api import sync_playwright  # noqa: PLC0415

    trials: list[Trial] = []
    started = time.monotonic()
    stopped_early = False
    with sync_playwright() as driver:
        browser = _launch(driver)
        page = browser.new_page(viewport={"width": 1920, "height": 1080})
        failures: list[str] = []
        page.on("pageerror", lambda e: failures.append(str(e)))
        page.goto(PAGE.as_uri())
        page.wait_for_function("window.atlasTransitions !== undefined", timeout=60_000)
        guard = page.evaluate(GUARD_JS)
        if not guard["ok"]:
            msg = f"the instrument is not measuring anything: {guard['why']}"
            raise RuntimeError(msg)
        print(f"# page: {guard['pairs']} pairs, seed {guard['seed']}, {PAGE}")
        with run.out.open("w", encoding="utf-8") as sink:
            for n in run.sizes:
                for seed in run.seeds:
                    if time.monotonic() - started > run.budget:
                        stopped_early = True
                        break
                    got = page.evaluate(
                        TRIAL_JS,
                        {
                            "n": n,
                            "seed": seed,
                            "style": run.style,
                            "inflate": run.inflate,
                            "anneal": run.anneal,
                        },
                    )
                    if "error" in got:
                        print(f"# skipped n = {n}: {got['error']}")
                        break
                    trial = Trial(
                        n=n,
                        seed=seed,
                        style=run.style,
                        excess=got["excess"],
                        closed=gap_closed(n, got["record"], got["excess"]),
                        overlap=got["overlap"],
                        resolved_side=got["resolvedSide"],
                        resolved_closed=gap_closed(
                            n, got["record"], (got["resolvedSide"] / got["record"] - 1) * 100
                        ),
                        resolved_overlap=got["resolvedOverlap"],
                        side=got["side"],
                        record=got["record"],
                        steps=got["steps"],
                        ms=got["ms"],
                        centre=got["centre"],
                        angle=got["angle"],
                        params=run.params,
                    )
                    trials.append(trial)
                    sink.write(json.dumps(trial.row()) + "\n")
                    sink.flush()
                if stopped_early:
                    break
        if failures:
            print(f"# {len(failures)} page error(s), first: {failures[0][:120]}")
        browser.close()
    if stopped_early:
        print(f"# budget of {run.budget:g}s spent; {len(trials)} trial(s) recorded")
    return trials


def valid(trials: list[Trial]) -> list[Trial]:
    """The trials whose final arrangement is a packing.

    A run whose squares end up inside each other has not found a smaller container, it has
    found a smaller number. Refused here rather than annotated, because an invalid run is not
    a poor result -- it is not a result.
    """
    return [t for t in trials if not (t.resolved_overlap > VALID_OVERLAP)]


def report(trials: list[Trial]) -> int:
    """Per n: the rate at each tolerance, the shape of the failures, and the cost."""
    if not trials:
        print("no trials")
        return 1
    kept = valid(trials)
    refused = len(trials) - len(kept)
    if refused:
        worst = max(t.resolved_overlap for t in trials if t.resolved_overlap > VALID_OVERLAP)
        print(
            f"\n  REFUSED {refused} of {len(trials)} trials as invalid: squares overlapping by "
            f"up to {worst:.4f}\n  of a unit side. They are not poor results, they are not "
            "results."
        )
    if not kept:
        print("  every trial was invalid")
        return 1
    trials = kept
    by_n: dict[int, list[Trial]] = {}
    for t in trials:
        by_n.setdefault(t.n, []).append(t)

    names = list(TOLERANCES)
    head = "    n  trials  " + "  ".join(f"{name:>7}" for name in names)
    print(f"\n{head}   closed      best    median     worst   ms/trial")
    print("  " + "-" * (len(head) + 44))
    for n in sorted(by_n):
        rows = by_n[n]
        # The RESOLVED excess, so every column in this table is about the same arrangement.
        # Scoring the tolerances on the raw side while scoring `closed` on the resolved one
        # would put two different arrangements in one row.
        excess = sorted((t.resolved_side / t.record - 1) * 100 for t in rows)
        rates = []
        for name in names:
            hits = sum(1 for e in excess if e <= TOLERANCES[name])
            rates.append(f"{hits / len(excess):>6.1%} ")
        closed = statistics.median(t.resolved_closed for t in rows)
        print(
            f"  {n:>3}  {len(rows):>6}  "
            + "  ".join(rates)
            + f"  {closed:>7.3f}  {excess[0]:>8.4f}  {statistics.median(excess):>8.4f}  "
            f"{excess[-1]:>8.4f}  {statistics.median(t.ms for t in rows):>9.1f}"
        )
    # **Best-of-k, which is the number that matters and the one nobody was reporting.**
    # The median says the method closes about half the gap; the best of a thousand trials at
    # n = 5 closes 98.7% of it. Those are both true and only the second is a result about
    # what the search can reach -- a run costs a fraction of a millisecond, so k is free and
    # the tail is the product.
    print(f"\n{'    n':>5}" + "".join(f"{'best-of-' + str(k):>12}" for k in BEST_OF))
    for n in sorted(by_n):
        ordered = sorted(by_n[n], key=lambda t: t.seed)
        line = f"{n:>5}"
        for k in BEST_OF:
            if k > len(ordered):
                line += f"{'-':>12}"
                continue
            line += f"{max(t.resolved_closed for t in ordered[:k]):>12.3f}"
        print(line)
    print("  (closed at the best trial of the first k seeds)")

    every = sorted(t.resolved_closed for t in trials)
    print(
        "\n  closed is the fraction of the record-to-grid gap the run closed: 1 reached the "
        "record,\n  0 got no further than ceil(sqrt(n)). It is the only column that compares "
        "across n.\n  excess is (side / record - 1) x 100. Tolerances: "
        + ", ".join(f"{k} <= {v:g}%" for k, v in TOLERANCES.items())
    )
    print(
        f"\n  over all {len(every)} trials: closed median {statistics.median(every):.3f}, "
        f"range {every[0]:.3f} to {every[-1]:.3f}"
    )
    return 0


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n", type=int, nargs="+", default=[11, 17], help="the n to benchmark")
    parser.add_argument("--seeds", type=int, default=20, help="trials per n")
    parser.add_argument("--seed-from", type=int, default=0, help="first seed")
    parser.add_argument("--style", default="bodies", choices=["physics", "bodies"])
    parser.add_argument("--inflate", type=float, default=None, help="BLIND.inflate override")
    parser.add_argument("--anneal", type=int, default=None, help="the shake dial, 0..10")
    parser.add_argument(
        "--budget",
        type=float,
        default=900.0,
        help="seconds before stopping with a partial result",
    )
    parser.add_argument("--out", type=Path, default=None, help="where the raw trials go")
    parser.add_argument("--replay", type=Path, default=None, help="report an existing jsonl")
    parser.add_argument(
        "--sweep",
        nargs="+",
        default=None,
        metavar="KEY=V,V,V",
        help="parameter grid, e.g. --sweep anneal=0,3,6,10 inflate=1.05,1.12,1.25",
    )
    return parser.parse_args(argv)


def parse_grid(spec: list[str]) -> list[dict[str, float | int]]:
    """`["anneal=0,3", "inflate=1.1,1.2"]` into the four cells it names.

    A grid rather than one axis at a time, because the interesting question is almost never
    what one parameter does alone -- a shake that helps at a tight container may hurt at a
    loose one, and only the cross says so.
    """
    axes: list[tuple[str, list[float | int]]] = []
    for entry in spec:
        key, _, values = entry.partition("=")
        if not values:
            msg = f"a sweep axis needs values: {entry!r}"
            raise ValueError(msg)
        axes.append(
            (
                key,
                [int(v) if key == "anneal" else float(v) for v in values.split(",")],
            )
        )
    cells: list[dict[str, float | int]] = [{}]
    for key, values in axes:
        cells = [{**cell, key: value} for cell in cells for value in values]
    return cells


def sweep(args: argparse.Namespace, seeds: list[int], stamp: str) -> int:
    """One run per cell of the grid, reported as one table of best-of-k."""
    cells = parse_grid(args.sweep)
    print(f"# {len(cells)} cell(s) x {len(args.n)} n x {len(seeds)} seeds")
    table: list[tuple[dict[str, float | int], int, list[Trial]]] = []
    for cell in cells:
        label = "-".join(f"{k}{v}" for k, v in cell.items())
        out = RESULTS / f"{stamp}-sweep-{label}.jsonl"
        trials = run_trials(
            Run(
                sizes=args.n,
                seeds=seeds,
                style=args.style,
                inflate=float(cell["inflate"]) if "inflate" in cell else args.inflate,
                anneal=int(cell["anneal"]) if "anneal" in cell else args.anneal,
                budget=args.budget,
                out=out,
            )
        )
        by_n: dict[int, list[Trial]] = {}
        for trial in trials:
            by_n.setdefault(trial.n, []).append(trial)
        table.extend((cell, n, by_n[n]) for n in sorted(by_n))
    if not table:
        print("no trials")
        return 1
    keys = list(cells[0])
    head = "  " + "".join(f"{k:>9}" for k in keys) + f"{'n':>5}{'trials':>8}{'median':>9}"
    print(f"\n{head}" + "".join(f"{'best-' + str(k):>11}" for k in BEST_OF if k <= len(seeds)))
    print("  " + "-" * (len(head) + 11 * len(BEST_OF)))
    for cell, n, rows in table:
        ordered = sorted(rows, key=lambda t: t.seed)
        line = "  " + "".join(f"{cell[k]:>9}" for k in keys)
        line += (
            f"{n:>5}{len(rows):>8}{statistics.median(t.resolved_closed for t in rows):>9.3f}"
        )
        for k in BEST_OF:
            if k > len(seeds):
                continue
            line += f"{max(t.resolved_closed for t in ordered[:k]):>11.3f}"
        print(line)
    print("\n  median and best-of-k are both `closed`: 1 is the record, 0 the grid.")
    return 0


def _trial_of(row: dict[str, Any]) -> Trial:
    """One recorded row as a `Trial`.

    Rows written before `closed` existed are still readable: the fraction is derived from n
    and the record, both of which every row has always carried. The record is corrected,
    not rewritten, so an old file keeps its numbers and gains the new column here.
    """
    n = int(row["n"])
    record = float(row["record"])
    excess = float(row["excess"])
    return Trial(
        n=n,
        seed=int(row["seed"]),
        style=str(row["style"]),
        excess=excess,
        side=float(row["side"]),
        record=record,
        closed=float(row["closed"]) if "closed" in row else gap_closed(n, record, excess),
        overlap=float(row.get("overlap", float("nan"))),
        resolved_side=float(row.get("resolved_side", float("nan"))),
        resolved_closed=float(row.get("resolved_closed", float("nan"))),
        resolved_overlap=float(row.get("resolved_overlap", float("nan"))),
        steps=int(row["steps"]),
        ms=float(row["ms"]),
        centre=float(row["centre"]),
        angle=float(row["angle"]),
        params=dict(row.get("params", {})),
    )


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    if args.replay is not None:
        rows = [
            json.loads(line) for line in args.replay.read_text(encoding="utf-8").splitlines()
        ]
        return report([_trial_of(row) for row in rows])
    if not PAGE.is_file():
        print(f"no built page at {PAGE}; run `python -m devtools.build_workbench_site` first")
        return 1
    RESULTS.mkdir(parents=True, exist_ok=True)
    stamp = time.strftime("%Y%m%dT%H%M%S")
    if args.sweep is not None:
        return sweep(args, list(range(args.seed_from, args.seed_from + args.seeds)), stamp)
    label = "-".join(str(n) for n in args.n)
    out = args.out or RESULTS / f"{stamp}-n{label}-{args.style}.jsonl"
    seeds = list(range(args.seed_from, args.seed_from + args.seeds))
    trials = run_trials(
        Run(
            sizes=args.n,
            seeds=seeds,
            style=args.style,
            inflate=args.inflate,
            anneal=args.anneal,
            budget=args.budget,
            out=out,
        )
    )
    print(f"# {len(trials)} trial(s) -> {out}")
    return report(trials)


if __name__ == "__main__":
    sys.exit(main())
