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

#: The metric the accept rule scores. `miss.excess` is `(side / record - 1) * 100`: the
#: percentage by which the run's container exceeds the best known one. Zero is a find.
OUTCOME = "excess"


@dataclass
class Trial:
    """One blind run: what it was asked, and what came back."""

    n: int
    seed: int
    style: str
    excess: float
    side: float
    record: float
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
  return {
    excess: r.miss.excess,
    side: r.miss.side,
    record: r.miss.record,
    centre: r.miss.centre,
    angle: r.miss.angle,
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


def report(trials: list[Trial]) -> int:
    """Per n: the rate at each tolerance, the shape of the failures, and the cost."""
    if not trials:
        print("no trials")
        return 1
    by_n: dict[int, list[Trial]] = {}
    for t in trials:
        by_n.setdefault(t.n, []).append(t)

    names = list(TOLERANCES)
    head = "    n  trials  " + "  ".join(f"{name:>7}" for name in names)
    print(f"\n{head}      best    median       p90     worst   ms/trial")
    print("  " + "-" * (len(head) + 44))
    for n in sorted(by_n):
        rows = by_n[n]
        excess = sorted(t.excess for t in rows)
        rates = []
        for name in names:
            hits = sum(1 for e in excess if e <= TOLERANCES[name])
            rates.append(f"{hits / len(excess):>6.1%} ")
        p90 = excess[min(len(excess) - 1, int(0.9 * len(excess)))]
        print(
            f"  {n:>3}  {len(rows):>6}  "
            + "  ".join(rates)
            + f"  {excess[0]:>8.4f}  {statistics.median(excess):>8.4f}  "
            f"{p90:>8.4f}  {excess[-1]:>8.4f}  {statistics.median(t.ms for t in rows):>9.1f}"
        )
    print(
        "\n  excess is (side / record - 1) x 100: the per cent by which the run's container "
        "exceeds\n  the best known one. 0 is a find. Tolerances: "
        + ", ".join(f"{k} <= {v:g}%" for k, v in TOLERANCES.items())
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
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    if args.replay is not None:
        rows = [
            json.loads(line) for line in args.replay.read_text(encoding="utf-8").splitlines()
        ]
        return report(
            [Trial(**{k: v for k, v in row.items() if k != "params"}) for row in rows]
        )
    if not PAGE.is_file():
        print(f"no built page at {PAGE}; run `python -m devtools.build_workbench_site` first")
        return 1
    RESULTS.mkdir(parents=True, exist_ok=True)
    stamp = time.strftime("%Y%m%dT%H%M%S")
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
