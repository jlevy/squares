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
import hashlib
import importlib.metadata
import math
import os
import platform
import statistics
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import TYPE_CHECKING

from workbench_tools.trial_records import (
    SourceReceipt,
    Trial,
    partition_trials,
    trial_from_json,
    trial_from_probe,
    trial_from_row,
    trial_to_json,
    valid,
)

if TYPE_CHECKING:
    from playwright.sync_api import Browser, Playwright

__all__ = ["Trial", "trial_from_row", "valid"]

PROJECT_ROOT = Path(__file__).resolve().parent.parent
REPO = PROJECT_ROOT.parent
PAGE = PROJECT_ROOT / "site/workbench/index.html"
RESULTS = PROJECT_ROOT / "campaign/results/annealing"
WORKBENCH_PACKAGE = REPO / "packages/workbench"
BUILD_ASSETS = WORKBENCH_PACKAGE / "tools/build-assets.ts"
BENCHMARK_SOURCE = WORKBENCH_PACKAGE / "probes/bench-annealing.ts"
VIEWPORT_WIDTH = 1920
VIEWPORT_HEIGHT = 1080

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


PROBE_EXPRESSION = "(options) => SquaresWorkbenchBench.runTrial(options)"
GUARD_EXPRESSION = "() => SquaresWorkbenchBench.guard()"


def _launch(playwright: Playwright) -> Browser:
    """The pinned headless shell if the environment names one, else Playwright's own."""
    return playwright.chromium.launch(executable_path=os.environ.get("SQPACK_CHROMIUM"))


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _git(*arguments: str) -> str:
    return subprocess.check_output(
        ["git", *arguments], cwd=REPO, text=True, encoding="utf-8"
    ).strip()


def _source_receipt(browser: Browser) -> SourceReceipt:
    executable = os.environ.get("SQPACK_CHROMIUM") or browser.browser_type.executable_path
    return SourceReceipt(
        commit=_git("rev-parse", "HEAD"),
        dirty=bool(_git("status", "--porcelain", "--untracked-files=all")),
        page=PAGE.relative_to(REPO).as_posix(),
        page_sha256=_sha256(PAGE),
        benchmark=BENCHMARK_SOURCE.relative_to(REPO).as_posix(),
        browser=browser.browser_type.name,
        browser_version=browser.version,
        browser_executable=str(Path(executable).resolve()),
        playwright_version=importlib.metadata.version("playwright"),
        python_version=platform.python_version(),
        platform=platform.platform(),
        viewport_width=VIEWPORT_WIDTH,
        viewport_height=VIEWPORT_HEIGHT,
    )


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
    def params(self) -> dict[str, float | int]:
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
    with TemporaryDirectory(prefix="squares-workbench-bench-") as asset_directory:
        subprocess.run(
            ["node", str(BUILD_ASSETS), asset_directory],
            check=True,
            cwd=REPO,
        )
        benchmark_bundle = Path(asset_directory) / "bench-annealing.js"
        with sync_playwright() as driver:
            browser = _launch(driver)
            page = browser.new_page(
                viewport={"width": VIEWPORT_WIDTH, "height": VIEWPORT_HEIGHT}
            )
            failures: list[str] = []
            page.on("pageerror", lambda error: failures.append(str(error)))
            page.goto(PAGE.as_uri())
            page.wait_for_function("window.atlasTransitions !== undefined", timeout=60_000)
            page.add_script_tag(path=str(benchmark_bundle))
            guard: object = page.evaluate(GUARD_EXPRESSION)
            if not isinstance(guard, dict):
                raise TypeError("the benchmark guard returned a malformed receipt")
            if guard.get("ok") is not True:
                why = guard.get("why")
                raise RuntimeError(f"the instrument is not measuring anything: {why}")
            pairs = guard.get("pairs")
            initial_seed = guard.get("seed")
            if not isinstance(pairs, int) or not isinstance(initial_seed, int):
                raise TypeError("the benchmark guard omitted its pair or seed count")
            print(f"# page: {pairs} pairs, seed {initial_seed}, {PAGE}")
            source = _source_receipt(browser)
            with run.out.open("w", encoding="utf-8") as sink:
                for n in run.sizes:
                    for seed in run.seeds:
                        if time.monotonic() - started > run.budget:
                            stopped_early = True
                            break
                        got: object = page.evaluate(
                            PROBE_EXPRESSION,
                            {
                                "n": n,
                                "seed": seed,
                                "style": run.style,
                                "inflate": run.inflate,
                                "anneal": run.anneal,
                            },
                        )
                        if isinstance(got, dict) and isinstance(got.get("error"), str):
                            print(f"# skipped n = {n}: {got['error']}")
                            break
                        trial = trial_from_probe(
                            got,
                            n=n,
                            seed=seed,
                            style=run.style,
                            params=run.params,
                            source=source,
                        )
                        trials.append(trial)
                        sink.write(trial_to_json(trial) + "\n")
                        sink.flush()
                    if stopped_early:
                        break
            if failures:
                print(f"# {len(failures)} page error(s), first: {failures[0][:120]}")
            browser.close()
    if stopped_early:
        print(f"# budget of {run.budget:g}s spent; {len(trials)} trial(s) recorded")
    return trials


def _report_refusals(total: int, refused: dict[str, int]) -> None:
    if refused:
        counts = ", ".join(f"{reason}={count}" for reason, count in sorted(refused.items()))
        print(f"  REFUSED {sum(refused.values())} of {total} trials: {counts}")


def report(trials: list[Trial]) -> int:
    """Per n: the rate at each tolerance, the shape of the failures, and the cost."""
    if not trials:
        print("no trials")
        return 1
    kept, refused = partition_trials(trials)
    _report_refusals(len(trials), refused)
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
        normalized = [value for t in rows if (value := t.resolved_closed) is not None]
        closed = f"{statistics.median(normalized):.3f}" if normalized else "-"
        print(
            f"  {n:>3}  {len(rows):>6}  "
            + "  ".join(rates)
            + f"  {closed:>7}  {excess[0]:>8.4f}  {statistics.median(excess):>8.4f}  "
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
            prefix = [value for t in ordered[:k] if (value := t.resolved_closed) is not None]
            line += f"{max(prefix):>12.3f}" if prefix else f"{'-':>12}"
        print(line)
    print("  (closed at the best trial of the first k seeds)")

    every = sorted(value for t in trials if (value := t.resolved_closed) is not None)
    print(
        "\n  closed is the fraction of the record-to-grid gap the run closed: 1 reached the "
        "record,\n  0 got no further than ceil(sqrt(n)). It is the only column that compares "
        "across n.\n  excess is (side / record - 1) x 100. Tolerances: "
        + ", ".join(f"{k} <= {v:g}%" for k, v in TOLERANCES.items())
    )
    if every:
        print(
            f"\n  over all {len(every)} defined scores: closed median "
            f"{statistics.median(every):.3f}, range {every[0]:.3f} to {every[-1]:.3f}"
        )
    else:
        print("\n  closed is undefined for every zero reference-gap control in this report")
    return 0


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n", type=int, nargs="+", default=[11, 17], help="the n to benchmark")
    parser.add_argument("--seeds", type=int, default=20, help="trials per n")
    parser.add_argument("--seed-from", type=int, default=0, help="first seed")
    parser.add_argument("--style", default="bodies", choices=["physics", "bodies"])
    parser.add_argument("--inflate", type=_inflate, default=None, help="BLIND.inflate override")
    parser.add_argument(
        "--anneal", type=int, choices=range(11), default=None, help="the shake dial, 0..10"
    )
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
    args = parser.parse_args(argv)
    if any(n < 1 for n in args.n):
        parser.error("every n must be positive")
    if args.seeds < 1:
        parser.error("seeds must be positive")
    if args.seed_from < 0 or args.seed_from + args.seeds - 1 > 0xFFFF_FFFF:
        parser.error("the requested seed interval must fit uint32")
    if not math.isfinite(args.budget) or args.budget <= 0:
        parser.error("budget must be finite and positive")
    return args


def _inflate(value: str) -> float:
    number = float(value)
    if not 1 <= number <= 2:
        raise argparse.ArgumentTypeError("inflate must be between 1 and 2")
    return number


def parse_grid(spec: list[str]) -> list[dict[str, float | int]]:
    """`["anneal=0,3", "inflate=1.1,1.2"]` into the four cells it names.

    A grid rather than one axis at a time, because the interesting question is almost never
    what one parameter does alone -- a shake that helps at a tight container may hurt at a
    loose one, and only the cross says so.
    """
    axes: list[tuple[str, list[float | int]]] = []
    seen: set[str] = set()
    for entry in spec:
        key, _, values = entry.partition("=")
        if not values:
            msg = f"a sweep axis needs values: {entry!r}"
            raise ValueError(msg)
        if key not in {"anneal", "inflate"}:
            raise ValueError(f"unsupported sweep axis {key!r}")
        if key in seen:
            raise ValueError(f"duplicate sweep axis {key!r}")
        seen.add(key)
        parsed: list[float | int]
        if key == "anneal":
            parsed = [int(value) for value in values.split(",")]
            if any(not 0 <= value <= 10 for value in parsed):
                raise ValueError("anneal sweep values must be integers from 0 through 10")
        else:
            parsed = [_inflate(value) for value in values.split(",")]
        axes.append(
            (
                key,
                parsed,
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
        admitted, refused = partition_trials(trials)
        _report_refusals(len(trials), refused)
        for trial in admitted:
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
        normalized = [value for t in rows if (value := t.resolved_closed) is not None]
        median = f"{statistics.median(normalized):.3f}" if normalized else "-"
        line += f"{n:>5}{len(rows):>8}{median:>9}"
        for k in BEST_OF:
            if k > len(seeds):
                continue
            prefix = [value for t in ordered[:k] if (value := t.resolved_closed) is not None]
            line += f"{max(prefix):>11.3f}" if prefix else f"{'-':>11}"
        print(line)
    print("\n  median and best-of-k are both `closed`: 1 is the record, 0 the grid.")
    return 0


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    if args.replay is not None:
        trials = [
            trial_from_json(line)
            for line in args.replay.read_text(encoding="utf-8").splitlines()
        ]
        return report(trials)
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
