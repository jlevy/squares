#!/usr/bin/env python3
"""How often does the workbench's blind physics improve a previous packing toward the record?

    squares-workbench-benchmark --n 11 17 --seeds 40
    squares-workbench-benchmark --n 11 --seeds 200
    squares-workbench-benchmark --replay results/....jsonl

The page's blind physics is an incremental, record-conditioned search. It starts from the
retained packing for n - 1, withholds only the destination poses for n, places the added
square with a coarse-grid proposal, and runs the contact dynamics while contracting toward
the reference side, which the run is given; in the default `bodies` style it also welds
squares into blocks matched from the two records. So the question this answers is narrower
than rediscovering a packing from nothing: can this proposal and physics, under a stated
budget and seed schedule, repair to a packing that comes near the known reference?

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
machine. This one samples the n it is given, streams each attempt to disk as it lands, and
stops at `--budget` seconds with a partial result, reported as partial, rather than a lost one.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import math
import os
import platform
import statistics
import subprocess
import sys
import time
from collections import Counter
from collections.abc import Callable, Iterable, Sequence
from dataclasses import dataclass
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import TYPE_CHECKING, TextIO, cast

from workbench_tools.probes import probe
from workbench_tools.trial_records import (
    AttemptFailure,
    AttemptFailureReason,
    ReferenceLookup,
    SourceReceipt,
    Trial,
    attempt_from_json,
    attempt_to_json,
    canonical_reference,
    check_success_band,
    partition_trials,
    trial_from_probe,
    trial_from_row,
    valid,
)

if TYPE_CHECKING:
    from playwright.sync_api import Browser, Playwright

__all__ = ["Trial", "trial_from_row", "valid"]

REPO = Path(__file__).resolve().parents[4]
PROJECT_ROOT = REPO / "packing"
PAGE = PROJECT_ROOT / "site/workbench/index.html"
RESULTS = PROJECT_ROOT / "campaign/results/annealing"
WORKBENCH_PACKAGE = REPO / "packages/workbench"
BUILD_ASSETS = WORKBENCH_PACKAGE / "tools/build-assets.ts"
BENCHMARK_SOURCE = WORKBENCH_PACKAGE / "probes/bench-annealing.ts"
VIEWPORT_WIDTH = 1920
VIEWPORT_HEIGHT = 1080

#: Success bands: how far above the record, in per cent of it, an admitted side may sit.
#:
#: Chosen, not measured. Admission already requires the repaired arrangement to pass the
#: validity contract at 1e-9 and refuses a side below the record (`below-record`), so a band
#: only says how near counts as reaching it. `report` refuses any band finer than the contract
#: can resolve at that record (`check_success_band`): `exact` is 1e-6 of the record, 2.7e-6 to
#: 4.7e-6 of a unit side for n = 5..17. `close` (a tenth of a per cent) and `near` (one per
#: cent) are descriptive; neither comes from the record-to-grid gap, which is zero at n = 6..9
#: and 12..16 and 10.8 per cent at n = 5.
TOLERANCES = {"exact": 0.0001, "close": 0.1, "near": 1.0}

# `closed`, the normalized metric reported beside absolute side and relative excess,
# describes where a result falls inside that case's record-to-grid interval: 1 is
# the record, 0 is `ceil(sqrt(n))`, and a negative number is worse than the grid. It is
# undefined for cases where the record and grid coincide. The report retains side and excess
# because the three scales answer different descriptive questions.

#: The k at which best-of-k is reported for prefixes of the exact recorded seed order.
BEST_OF = (1, 10, 100, 1000, 10_000)


#: The page-side calls, as probe files under `probes/benchmark/`, not JavaScript strings here.
BENCHMARK_PROBES = {
    "ready": "benchmark/page-api-ready",
    "guard": "benchmark/guard",
    "trial": "benchmark/run-trial",
}


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


class ProbeCallError(RuntimeError):
    """The browser call behind one attempt failed; it is recorded and the run goes on."""


type ProbeCall = Callable[[dict[str, object]], object]


@dataclass(frozen=True)
class RunResult:
    """Every planned (n, seed) of a run and what became of it.

    `planned` is the exact order the run would have attempted. An attempt either produced a
    trial (admitted or refused later) or a counted failure; a planned slot with neither was
    not attempted because the budget ran out.
    """

    planned: list[tuple[int, int]]
    trials: list[Trial]
    failures: list[AttemptFailure]
    stopped_early: bool

    @property
    def attempted(self) -> int:
        """How many planned slots produced a trial or a failure."""
        return len(self.trials) + len(self.failures)


def run_attempts(
    evaluate: ProbeCall,
    run: Run,
    source: SourceReceipt,
    sink: TextIO,
    *,
    clock: Callable[[], float] = time.monotonic,
    reference_for: ReferenceLookup = canonical_reference,
) -> RunResult:
    """Attempt every planned (n, seed) in order, recording a failure instead of aborting.

    A malformed or non-finite probe result, a missing witness and a failed browser call each
    become an `AttemptFailure` for that slot. A probe error for an n (the page carries no pair
    into it) is recorded once per remaining seed of that n without calling the probe again.
    Every trial and failure is written to `sink` as it lands.
    """
    planned = [(n, seed) for n in run.sizes for seed in run.seeds]
    trials: list[Trial] = []
    failures: list[AttemptFailure] = []
    started = clock()
    probe_errors: dict[int, str] = {}

    def fail(n: int, seed: int, reason: AttemptFailureReason, detail: str) -> None:
        failure = AttemptFailure(
            n=n,
            seed=seed,
            style=run.style,
            params=run.params,
            reason=reason.value,
            detail=detail,
            source=source,
        )
        failures.append(failure)
        sink.write(attempt_to_json(failure) + "\n")
        sink.flush()

    for n, seed in planned:
        if clock() - started > run.budget:
            return RunResult(planned, trials, failures, stopped_early=True)
        if n in probe_errors:
            fail(n, seed, AttemptFailureReason.PROBE_ERROR, probe_errors[n])
            continue
        options: dict[str, object] = {
            "n": n,
            "seed": seed,
            "style": run.style,
            "inflate": run.inflate,
            "anneal": run.anneal,
        }
        try:
            got = evaluate(options)
        except ProbeCallError as error:
            fail(n, seed, AttemptFailureReason.BROWSER_ERROR, str(error))
            continue
        if isinstance(got, dict):
            message = cast(dict[str, object], got).get("error")
            if isinstance(message, str):
                probe_errors[n] = message
                fail(n, seed, AttemptFailureReason.PROBE_ERROR, message)
                continue
        try:
            trial = trial_from_probe(
                got,
                n=n,
                seed=seed,
                style=run.style,
                params=run.params,
                source=source,
                reference_for=reference_for,
            )
        except OSError as error:
            fail(n, seed, AttemptFailureReason.REFERENCE_UNAVAILABLE, str(error))
            continue
        except (TypeError, ValueError) as error:
            fail(n, seed, AttemptFailureReason.MALFORMED_RESULT, str(error))
            continue
        trials.append(trial)
        sink.write(attempt_to_json(trial) + "\n")
        sink.flush()
    return RunResult(planned, trials, failures, stopped_early=False)


def run_trials(run: Run) -> RunResult:
    """Every (n, seed) in the grid, streamed to `out` as each lands."""
    from playwright.sync_api import Error as PlaywrightError  # noqa: PLC0415
    from playwright.sync_api import sync_playwright  # noqa: PLC0415

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
            page_errors: list[str] = []
            page.on("pageerror", lambda error: page_errors.append(str(error)))
            page.goto(PAGE.as_uri())
            page.wait_for_function(probe(BENCHMARK_PROBES["ready"]), timeout=60_000)
            page.add_script_tag(path=str(benchmark_bundle))
            guard: object = page.evaluate(probe(BENCHMARK_PROBES["guard"]))
            if not isinstance(guard, dict):
                raise TypeError("the benchmark guard returned a malformed receipt")
            receipt = cast(dict[str, object], guard)
            if receipt.get("ok") is not True:
                why = receipt.get("why")
                raise RuntimeError(f"the instrument is not measuring anything: {why}")
            pairs = receipt.get("pairs")
            initial_seed = receipt.get("seed")
            if not isinstance(pairs, int) or not isinstance(initial_seed, int):
                raise TypeError("the benchmark guard omitted its pair or seed count")
            print(f"# page: {pairs} pairs, seed {initial_seed}, {PAGE}")
            source = _source_receipt(browser)

            def evaluate(options: dict[str, object]) -> object:
                try:
                    return page.evaluate(probe(BENCHMARK_PROBES["trial"]), options)
                except PlaywrightError as error:
                    raise ProbeCallError(str(error)) from error

            with run.out.open("w", encoding="utf-8") as sink:
                result = run_attempts(evaluate, run, source, sink)
            if page_errors:
                print(f"# {len(page_errors)} page error(s), first: {page_errors[0][:120]}")
            browser.close()
    if result.stopped_early:
        print(
            f"# budget of {run.budget:g}s spent after {result.attempted} of "
            f"{len(result.planned)} planned attempts"
        )
    return result


def _counts(reasons: Iterable[str]) -> str:
    tally = Counter(reasons)
    return ", ".join(f"{reason}={count}" for reason, count in sorted(tally.items()))


def _report_refusals(total: int, refused: dict[str, int]) -> None:
    below = refused.get("below-record", 0)
    if below:
        print(
            f"  BELOW RECORD {below} of {total} trials: smaller than the reference side, so "
            "not ranked here; each needs exact verification before any claim"
        )
    others = {reason: count for reason, count in refused.items() if reason != "below-record"}
    if others:
        counts = ", ".join(f"{reason}={count}" for reason, count in sorted(others.items()))
        print(f"  REFUSED {sum(others.values())} of {total} trials: {counts}")


def _best_of(
    ordered_seeds: list[int], attempted: set[int], scores: dict[int, float], k: int
) -> str:
    """Best `closed` over the first k planned seeds, or `-` when any of them was not attempted.

    A seed that was attempted but refused, failed or has no defined score is a miss in its
    slot, so best-of-k is always over exactly k planned seeds.
    """
    prefix = ordered_seeds[:k]
    if len(prefix) < k or any(seed not in attempted for seed in prefix):
        return "-"
    values = [scores[seed] for seed in prefix if seed in scores]
    return f"{max(values):.3f}" if values else "none"


def report(
    trials: list[Trial],
    failures: Sequence[AttemptFailure] = (),
    *,
    planned: Sequence[tuple[int, int]] | None = None,
    stopped_early: bool = False,
) -> int:
    """Per n: counts, each band's rate per attempted seed, the failures' shape and the cost.

    `planned` is the run's (n, seed) order; a replay, which has no plan, treats the seeds it
    holds as planned. The report fails on a partial run, and when nothing was admitted.
    """
    if not trials and not failures:
        print("no trials")
        return 1
    kept, refused = partition_trials(trials)
    _report_refusals(len(trials), refused)
    if failures:
        print(f"  FAILED {len(failures)} attempts: {_counts(f.reason for f in failures)}")
    if planned is None:
        planned = sorted({(t.n, t.seed) for t in trials} | {(f.n, f.seed) for f in failures})
    attempted = {(t.n, t.seed) for t in trials} | {(f.n, f.seed) for f in failures}
    if stopped_early:
        print(
            f"  PARTIAL: the budget stopped the run after {len(attempted)} of "
            f"{len(planned)} planned attempts"
        )
    for record in sorted({t.record for t in kept}):
        for band in TOLERANCES.values():
            check_success_band(band, record)

    sizes = list(dict.fromkeys(n for n, _seed in planned))
    names = list(TOLERANCES)
    head = "    n  " + "  ".join(f"{name:>7}" for name in names)
    print(f"\n{head}   closed      best    median     worst   ms/trial")
    print("  " + "-" * (len(head) + 44))
    for n in sizes:
        seeds = [seed for size, seed in planned if size == n]
        tried = {seed for seed in seeds if (n, seed) in attempted}
        rows = [t for t in kept if t.n == n]
        failed = [f for f in failures if f.n == n]
        print(
            f"  n = {n}: planned {len(seeds)}, attempted {len(tried)}, admitted {len(rows)}"
            + (
                f", failed {len(failed)} ({_counts(f.reason for f in failed)})"
                if failed
                else ""
            )
        )
        if not rows:
            print(
                f"  {n:>3}  " + "  ".join(f"{'-':>7}" for _name in names) + "  (none admitted)"
            )
            continue
        # The RESOLVED excess, so every column in this table is about the same arrangement.
        excess = sorted((t.resolved_side / t.record - 1) * 100 for t in rows)
        rates = []
        for name in names:
            hits = sum(1 for e in excess if e <= TOLERANCES[name])
            rates.append(f"{hits / len(tried):>6.1%} ")
        normalized = [value for t in rows if (value := t.resolved_closed) is not None]
        closed = f"{statistics.median(normalized):.3f}" if normalized else "-"
        print(
            f"  {n:>3}  "
            + "  ".join(rates)
            + f"  {closed:>7}  {excess[0]:>8.4f}  {statistics.median(excess):>8.4f}  "
            f"{excess[-1]:>8.4f}  {statistics.median(t.ms for t in rows):>9.1f}"
        )
    print(
        "  (rates per attempted seed: a refused or failed attempt is a miss; excess, closed and"
        " ms are over admitted trials)"
    )
    # Prefixes keep best-of-k reproducible without treating different random orderings as the
    # same work allocation.
    print(f"\n{'    n':>5}" + "".join(f"{'best-of-' + str(k):>12}" for k in BEST_OF))
    for n in sizes:
        seeds = [seed for size, seed in planned if size == n]
        tried = {seed for seed in seeds if (n, seed) in attempted}
        scores = {
            t.seed: value for t in kept if t.n == n and (value := t.resolved_closed) is not None
        }
        print(f"{n:>5}" + "".join(f"{_best_of(seeds, tried, scores, k):>12}" for k in BEST_OF))
    print(
        "  (closed at the best admitted trial of the first k planned seeds; - where fewer than"
        " k were attempted, none where no admitted trial has a score)"
    )

    every = sorted(value for t in kept if (value := t.resolved_closed) is not None)
    print(
        "\n  closed is the fraction of the record-to-grid gap the run closed: 1 reached the "
        "record,\n  0 got no further than ceil(sqrt(n)); it is undefined when that gap is "
        "zero.\n  excess is the relative side excess, (side / record - 1) x 100; the side "
        "column is the absolute container side. Tolerances: "
        + ", ".join(f"{k} <= {v:g}%" for k, v in TOLERANCES.items())
    )
    if every:
        print(
            f"\n  over all {len(every)} defined scores: closed median "
            f"{statistics.median(every):.3f}, range {every[0]:.3f} to {every[-1]:.3f}"
        )
    elif kept:
        print("\n  closed is undefined for every zero reference-gap control in this report")
    if not kept:
        print("  every trial was invalid or failed")
        return 1
    return 1 if stopped_early else 0


def _group_key(attempt: Trial | AttemptFailure) -> str:
    source = attempt.source
    identity = None if source is None else (source.commit, source.page_sha256, source.benchmark)
    return json.dumps(
        [attempt.style, attempt.params, identity], sort_keys=True, separators=(",", ":")
    )


def replay_groups(
    attempts: Sequence[Trial | AttemptFailure],
) -> list[tuple[list[Trial], list[AttemptFailure]]]:
    """Split replayed rows into like runs; refuse a duplicate (n, seed) or mixed configuration.

    Rows are like when they share style, parameter overrides and source (commit, page and
    probe); within a group every trial must also carry one effective configuration apart from
    its seed, as `block_report` requires of a cohort.
    """
    groups: dict[str, tuple[list[Trial], list[AttemptFailure]]] = {}
    for attempt in attempts:
        trials, failures = groups.setdefault(_group_key(attempt), ([], []))
        if isinstance(attempt, Trial):
            trials.append(attempt)
        else:
            failures.append(attempt)
    for trials, failures in groups.values():
        seen: set[tuple[int, int]] = set()
        for slot in [(t.n, t.seed) for t in trials] + [(f.n, f.seed) for f in failures]:
            if slot in seen:
                raise ValueError(f"duplicate attempt for n = {slot[0]}, seed {slot[1]}")
            seen.add(slot)
        configurations = {
            json.dumps(
                {key: value for key, value in t.configuration.row().items() if key != "seed"},
                sort_keys=True,
            )
            for t in trials
            if t.configuration is not None
        }
        if len(configurations) > 1:
            raise ValueError("a replay group mixes effective configurations")
    return list(groups.values())


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n", type=int, nargs="+", default=[11, 17], help="the n to benchmark")
    parser.add_argument("--seeds", type=int, default=20, help="trials per n")
    parser.add_argument("--seed-from", type=int, default=0, help="first seed")
    parser.add_argument("--style", default="bodies", choices=["physics", "bodies"])
    parser.add_argument("--inflate", type=_inflate, default=None, help="BLIND.inflate override")
    parser.add_argument(
        "--anneal", type=int, choices=range(21), default=None, help="the shake dial, 0..20"
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
            if any(not 0 <= value <= 20 for value in parsed):
                raise ValueError("anneal sweep values must be integers from 0 through 20")
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
    """One run per cell of the grid, reported as one table of best-of-k.

    Every planned (cell, n) gets a row, with planned, attempted and admitted counts. Best-of-k
    is printed only where the first k planned seeds were all attempted, and a sweep any of whose
    cells the budget stopped fails.
    """
    cells = parse_grid(args.sweep)
    print(f"# {len(cells)} cell(s) x {len(args.n)} n x {len(seeds)} seeds")
    table: list[tuple[dict[str, float | int], int, list[int], set[int], list[Trial]]] = []
    partial = False
    for cell in cells:
        label = "-".join(f"{k}{v}" for k, v in cell.items())
        out = RESULTS / f"{stamp}-sweep-{label}.jsonl"
        result = run_trials(
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
        partial |= result.stopped_early
        admitted, refused = partition_trials(result.trials)
        _report_refusals(len(result.trials), refused)
        if result.failures:
            reasons = _counts(failure.reason for failure in result.failures)
            print(f"  FAILED {len(result.failures)} attempts: {reasons}")
        attempted = {(t.n, t.seed) for t in result.trials} | {
            (f.n, f.seed) for f in result.failures
        }
        for n in dict.fromkeys(size for size, _seed in result.planned):
            planned = [seed for size, seed in result.planned if size == n]
            tried = {seed for seed in planned if (n, seed) in attempted}
            rows = [trial for trial in admitted if trial.n == n]
            table.append((cell, n, planned, tried, rows))
    if not table:
        print("no trials")
        return 1
    keys = list(cells[0])
    head = (
        "  "
        + "".join(f"{k:>9}" for k in keys)
        + f"{'n':>5}{'planned':>9}{'tried':>7}{'admitted':>10}{'median':>9}"
    )
    print(f"\n{head}" + "".join(f"{'best-' + str(k):>11}" for k in BEST_OF if k <= len(seeds)))
    print("  " + "-" * (len(head) + 11 * len(BEST_OF)))
    for cell, n, planned, tried, rows in table:
        line = "  " + "".join(f"{cell[k]:>9}" for k in keys)
        scores = {t.seed: value for t in rows if (value := t.resolved_closed) is not None}
        median = f"{statistics.median(scores.values()):.3f}" if scores else "-"
        line += f"{n:>5}{len(planned):>9}{len(tried):>7}{len(rows):>10}{median:>9}"
        for k in BEST_OF:
            if k <= len(seeds):
                line += f"{_best_of(planned, tried, scores, k):>11}"
        print(line)
    print(
        "\n  median and best-of-k are both `closed`: 1 is the record, 0 the grid; best-of-k is"
        " over the first k planned seeds, - where fewer were attempted."
    )
    if partial:
        print("  PARTIAL: the budget stopped at least one cell before its planned attempts")
        return 1
    return 0


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    if args.replay is not None:
        attempts = [
            attempt_from_json(line)
            for line in args.replay.read_text(encoding="utf-8").splitlines()
        ]
        try:
            groups = replay_groups(attempts)
        except ValueError as error:
            print(f"replay refused: {error}")
            return 2
        status = 0
        for index, (trials, failures) in enumerate(groups, 1):
            key = _group_key(trials[0] if trials else failures[0])
            print(f"\n== group {index} of {len(groups)}: {key}")
            status = max(status, report(trials, failures))
        return status
    if not PAGE.is_file():
        print(f"no built page at {PAGE}; run `squares-workbench-build` first")
        return 1
    RESULTS.mkdir(parents=True, exist_ok=True)
    stamp = time.strftime("%Y%m%dT%H%M%S")
    if args.sweep is not None:
        return sweep(args, list(range(args.seed_from, args.seed_from + args.seeds)), stamp)
    label = "-".join(str(n) for n in args.n)
    out = args.out or RESULTS / f"{stamp}-n{label}-{args.style}.jsonl"
    seeds = list(range(args.seed_from, args.seed_from + args.seeds))
    result = run_trials(
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
    print(f"# {len(result.trials)} trial(s), {len(result.failures)} failure(s) -> {out}")
    return report(
        result.trials,
        result.failures,
        planned=result.planned,
        stopped_early=result.stopped_early,
    )


if __name__ == "__main__":
    sys.exit(main())
