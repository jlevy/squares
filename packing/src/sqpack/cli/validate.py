"""Run the packing project's refactor, evidence, and infrastructure checks.

The command is read-only. Checks run concurrently, but their captured output is
replayed in the declared order so two runs remain comparable. Use `--edit` while
editing, `--push` before a push (the edit tier plus the behavioral tests reachable from
the change), `--only TEXT` for one named surface, `--skip TEXT` for everything but one,
the default command before a commit, and `--strict` before an unattended research
session or merge.

`--records` exists because of what breaks. Every CI failure on this branch was a
registry, generated view, or declared contract going stale, and none was a test; the
record steps run in about seventy seconds against the fast tier's eight minutes, which
is what made pushing without them the cheaper-looking move.
"""

from __future__ import annotations

import argparse
import fnmatch
import json
import math
import os
import re
import shutil
import signal
import subprocess
import sys
import time
import traceback
from collections.abc import Callable, Iterator, Sequence
from concurrent.futures import ThreadPoolExecutor, as_completed
from contextlib import contextmanager, nullcontext, suppress
from dataclasses import asdict, dataclass, field, replace
from pathlib import Path
from threading import Lock
from typing import Literal, Never, override

from sqpack import gate_budgets
from sqpack.project import (
    ProjectLayoutError,
    add_version_argument,
    configured_project_root,
    require_project_root,
)
from sqpack.yamlio import safe_load

PROJECT_ROOT = configured_project_root()
REPOSITORY_ROOT = PROJECT_ROOT.parent
ENGINE = PROJECT_ROOT / "sqsearch/target/release/sqsearch"
RESULTS = Path("campaign/series/series-000-smoke-and-calibration/results")
ACTIVITY_MARKER = PROJECT_ROOT / ".gate-running"
DEFAULT_CPU_COUNT = 4
INNER_JOB_DIVISOR = 3
NEGATIVE_CONTROL_WORKERS = 2
TOP_TIMING_COUNT = 8
SUPPORTED_PYTHON = (3, 14)
BASIN_EVENT_CONTRACT_PREFIX = "packing.squares:BasinEvent/"
PROCESS_TERMINATION_GRACE_SECONDS = 1.0
DEFAULT_TIMEOUT_SECONDS = 900.0
#: The tiers this command can select as a whole, and therefore the tiers that must
#: carry a declared ceiling in `devtools/gate-budgets.yaml`. `devtools.check_gate_budgets`
#: compares the two sets in both directions, so a tier added here without a ceiling fails
#: the records tier rather than silently running uncapped.
#: The tier-selecting flags, narrowest first: `--records --fast` is the records tier.
#: `test_every_boolean_flag_is_classified` refuses a new `store_true` flag that appears in
#: neither this tuple nor its allow-list, so a tier cannot be added without deciding
#: whether it needs a ceiling.
TIER_FLAGS = ("push", "records", "edit", "suite", "checks", "sweeps", "geometry", "fast")
TIER_IDS = (*TIER_FLAGS, "full")
#: The budget of the whole non-exhaustive suite, read by `fast behavioral tests` and by
#: `--push` when its selector expands to everything (D-432). The two run the same suite
#: through two entry points, so they carry one number; the argument for the number is
#: written beside the `fast behavioral tests` step, where the measurements are.
#:
#: This is the *per-subprocess* cap, and on its own it is not a cost guard: on 2026-08-30
#: the tier it caps cost 499s, and by 2026-09-05 it cost 1369.60s, entirely inside this
#: number. What the tier is allowed to cost is declared in `devtools/gate-budgets.yaml`
#: and enforced by `sqpack.gate_budgets` against each run's own wall.
FAST_SUITE_BUDGET_SECONDS = 1800.0
#: The three behavioural lanes, as pytest marker expressions.
#:
#: They partition the suite: whatever markers a test carries, it satisfies exactly one of
#: the three, so no test can land in two lanes and none can land in none.
#: `test_the_behavioral_lanes_partition_every_test` checks that rather than trusting it.
#:
#: The split is `BC-214`. Before it, one lane ran every non-exhaustive test on every pull
#: request: 1369.60s on CI's two-core runner on 2026-09-05 (run 33982455466), 96.7 per
#: cent of the whole pull-request surface. The eight failures that run caught were all
#: sub-0.15-second tests -- 0.46s of call time between them -- so the wall was not where
#: the detection was, and deferring the whole lane would have thrown away nearly all of
#: the value for nearly none of the cost.
QUICK_TESTS = "not exhaustive_exact and not slow"
SLOW_TESTS = "slow and not exhaustive_exact"
EXHAUSTIVE_TESTS = "exhaustive_exact"
#: The pull-request surface's per-test ceiling, in seconds of pytest `call` time.
#:
#: This is the boundary between `QUICK_TESTS` and `SLOW_TESTS`, and it is a rule rather
#: than a list on purpose: `fast behavioral tests` passes it to pytest as
#: `--durations-min` and fails when any test it ran reports at or above it, naming the
#: test. A hand-kept list of slow tests would rot exactly the way the 499s figure in this
#: module's own docstring rotted -- silently, because nothing read it.
#:
#: Two numbers, deliberately, and the gap between them is runner variance. Tests are
#: *marked* at 2s, which is what keeps the lane inside its budget; the gate *fails* at
#: this ceiling, which leaves the slowest retained test about a factor of two of headroom
#: so an ordinarily loaded runner cannot turn a passing test into a red pull request. A
#: single number would have to be one or the other, and a ceiling that is also the
#: marking threshold is a ceiling that flaps.
#:
#: The `call` phase, not setup or teardown, because a module-scoped fixture bills its
#: whole cost to whichever test happens to trigger it first: `test_every_control_rejects`
#: in `test_n5_local_rigidity.py` reports 13.1s of setup that belongs to the `determination`
#: fixture three other tests in that file also use, and marking that one test would move
#: the cost rather than remove it. A setup phase over the ceiling means the module moves,
#: which is a judgement, not an automatic one.
#:
#: **12s, not the 5s this stood at, and the paragraph above is why it had to move.** That
#: paragraph claims the gap between the 2s marking threshold and the ceiling leaves "about
#: a factor of two of headroom so an ordinarily loaded runner cannot turn a passing test
#: into a red pull request". The claim was right in form and wrong in magnitude: a factor
#: of 2.5 is not enough for this runner.
#:
#: What was measured, over four consecutive CI runs of the same surface. The number of
#: tests reported at or above 5s was 19, then 5, then 1, then 3 -- **a different set each
#: time**, and every one of them a test measuring 1.5s to 3s locally.
#: `test_static_fallback_and_epistemic_labels_are_structural` is 1.55s here and reported
#: 5.68s there, a factor of 3.7, and it is unchanged by its neighbours so it is not a
#: shared build. The tier's own wall moved 191.81s to 290.00s across those runs with no
#: change to what it runs, so roughly half the spread is the runner rather than the load
#: this gate places on it.
#:
#: A guard that fires on a different victim every run is noise, and the repair it invites
#: is worse than the noise: marking whichever test lost, which builds exactly the curated
#: list of slow tests that `SLOW_TESTS` exists to avoid, and does it with tests that are
#: not slow. Three of the four runs above would have had a 1.5s test deferred to the deep
#: surface for having noisy neighbours.
#:
#: So the headroom is six times the marking threshold rather than two and a half. A test
#: genuinely worth deferring does 5s of work and would report near 18s under the inflation
#: measured here, so it is still caught; a 2s test has to lose the lottery six times over
#: before it is. What this does *not* weaken is the aggregate: the lane's total cost is
#: bounded by the tier's own band in `devtools/gate-budgets.yaml`, which is measured, and
#: that is the check that actually stops the lane creeping.
#:
#: The honest fix is to measure something contention-independent -- cpu time rather than
#: wall -- so the threshold means the same thing on a quiet box and a loaded runner.
#: pytest reports wall durations, so that needs a plugin rather than a constant, and it is
#: a cell rather than a number.
QUICK_TEST_CEILING_SECONDS = 12.0
#: The other direction, and it exists because `OR-13` is a floor on coverage rather than a
#: budget on time: a test leaves the pull-request surface by its own measured cost and
#: nothing else, so a `slow` marker on a test that is no longer slow is coverage the
#: pull-request surface has lost for no reason anybody measured. `slow behavioral tests`
#: fails when a test it ran reports a `call` phase below this, naming it, and the fix is to
#: delete the marker.
#:
#: Compared per test *function*, taking its slowest parametrization, because that is the
#: granularity a marker has: a decorator on a `def` defers every case of a parametrized
#: test at once, so one cheap case says nothing about whether the marker is still earned.
#: The ceiling above is compared per node, because there the question is the opposite one
#: -- what the pull-request surface actually pays for a single test it ran.
#:
#: The two numbers leave a band -- 1s to 5s -- where the gate says nothing in either
#: direction, and the band is the point. Marking is done at 2s, in the middle of it, so a
#: test near the boundary can move either way under ordinary runner variance without
#: turning a passing suite red. A single number would make every borderline test a coin
#: toss on every run; the measured distribution has 46 tests between 1s and 2s, which is
#: exactly the population a tight cutoff would flap on.
#:
#: What stops the quick lane creeping upward *in aggregate*, since a test at 4s passes the
#: ceiling, is not this pair but `devtools/gate-budgets.yaml`: the `fast` tier declares a
#: ceiling there that the gate reads and enforces against its own wall. One test getting
#: big is caught here; the tier getting big is caught there; neither is prose. The figure
#: is deliberately not repeated here -- a second copy is the thing that rots.
SLOW_TEST_FLOOR_SECONDS = 1.0
#: The budget of the exhaustive exact tier: every complete finite certificate decision
#: the fast tier defers. Measured on 2026-09-05 at 39 tests: 892s on CI's two-core
#: runner (run 33932095609, eight seconds under the 900s cap it had been inheriting) and
#: 930s on four cores locally, the interval route's five full-net decisions about 370s
#: of it. A 21,600s figure was proposed on a 4,866s exact decision the integer sweep has
#: since made a 30s one.
#:
#: Re-measured on 2026-09-05 at 53 tests, after the tier killed itself on three
#: consecutive merges to main: 2036s on four cores, against 930s at 39 tests when the
#: 1800s figure was written. The budget is a hard kill, not a report -- `_execute_step`
#: hands it to the subprocess as a deadline -- so the 1801.02s the gate printed is
#: 1800s plus `PROCESS_TERMINATION_GRACE_SECONDS`, arithmetic rather than a reading, and
#: the step's output died in an unflushed pipe. The fourteen tests added since cost 837s
#: of the total: `test_verify_claim.py`'s eleven nodes 432s, the D-449 witness walk 321s,
#: `test_minimal_verify` 56s and `test_n11_thirdparty_verify` 28s. Doubling no longer
#: applies to a tier this size -- it would put the budget over an hour -- so this is
#: 1.77x the measurement, the same margin the fast tier carries.
#:
#: One reason recorded against a budget above 1800s does not survive checking. Both the
#: fast tier's note below and D-432 say such a figure "sits above the 1800s CI allows the
#: job". No such limit exists or ever has: `timeout-minutes` appears nowhere in
#: `.github/`, and `git log -S` over that path finds no commit that ever added it. The
#: `validate` job inherits GitHub's 360-minute default. Recorded as D-456.
#:
#: What this does not fix is the trend. The tier has gone 21 to 25 to 39 to 53 nodes in
#: about a week, and over 1500s of the 2036s is single-process work that no core count
#: reduces, so a larger runner does not help. At the recent rate this buys about two
#: weeks. The tier already runs only after merge, so the move that scales is to give it
#: its own job rather than a larger share of this one (think-tr2z).
EXHAUSTIVE_SUITE_BUDGET_SECONDS = 3600.0


class _ProcessRegistry:
    """Process groups owned by one validation run."""

    def __init__(self) -> None:
        self._lock = Lock()
        self._pids: set[int] = set()
        self._stopping = False

    def register(self, pid: int) -> None:
        with self._lock:
            if self._stopping:
                with suppress(ProcessLookupError):
                    os.killpg(pid, signal.SIGKILL)
                raise StepFailureError("validation is stopping; rejected new subprocess")
            self._pids.add(pid)

    def discard(self, pid: int) -> None:
        with self._lock:
            self._pids.discard(pid)

    def stop(self) -> None:
        with self._lock:
            self._stopping = True
            pids = tuple(self._pids)
        if not pids:
            return
        for pid in pids:
            with suppress(ProcessLookupError):
                os.killpg(pid, signal.SIGTERM)
        time.sleep(PROCESS_TERMINATION_GRACE_SECONDS)
        for pid in pids:
            with suppress(ProcessLookupError):
                os.killpg(pid, signal.SIGKILL)


type CommitState = Literal["reachable", "orphaned", "missing"]


class UsageError(ValueError):
    """The requested validation surface is internally inconsistent."""


class StepFailureError(RuntimeError):
    """A check ran and did not establish its contract."""


class StepSkippedError(RuntimeError):
    """A check could not run because an optional local tool is unavailable."""

    def __init__(self, reason: str, *, output: str = "") -> None:
        super().__init__(reason)
        self.output = output


class ParserExitError(Exception):
    """An argparse exit represented as a return value for programmatic callers."""

    def __init__(self, status: int, message: str | None = None) -> None:
        super().__init__(message)
        self.status = status
        self.message = message


class ArgumentParser(argparse.ArgumentParser):
    """Argument parser that never terminates an embedding Python process."""

    @override
    def exit(self, status: int = 0, message: str | None = None) -> Never:
        raise ParserExitError(status, message)

    @override
    def error(self, message: str) -> Never:
        raise UsageError(message)


@dataclass(frozen=True)
class Context:
    """Resolved settings shared by every validation step."""

    deep: bool
    strict: bool
    jobs: int
    inner_jobs: int
    environment: dict[str, str]
    timeout_seconds: float = DEFAULT_TIMEOUT_SECONDS
    timeout_is_explicit: bool = False
    """True when an operator named the cap through `--timeout-seconds` or the
    environment variable, rather than taking the default.

    A step's `budget_seconds` may raise the default cap, because the default is a
    project-wide guess and the whole-suite steps are known to exceed it. It may not
    raise a number a person typed: someone tightening the cap is deliberately bounding
    this run, and a step quietly opting out of that is the bug, not the feature."""

    processes: _ProcessRegistry = field(
        default_factory=_ProcessRegistry, compare=False, repr=False
    )


StepAction = Callable[[Context], str]


@dataclass(frozen=True)
class Step:
    """One independently runnable, read-only validation contract."""

    name: str
    action: StepAction
    fast: bool = False
    needs_engine: bool = False
    records: bool = False
    """Checks the record rather than the mathematics: registries, generated views, and
    declared contracts. Every CI failure on the 2026-08-29 branch was one of these and
    none was a test, so they are selectable without paying for the test step (D-369)."""

    broad: bool = False
    """Excluded from `--edit` because its cost is breadth rather than what it uniquely
    catches.

    What each tier costs is recorded in `devtools/gate-budgets.yaml` and read by the
    gate, not written here. This paragraph used to carry the number -- "measured on
    2026-08-30, `--fast` is 499s and `fast behavioral tests` is 499s of it" -- and six
    days later the tier cost 1369.60s with nothing objecting, because a number a machine
    does not read is a number that drifts. A tier priced at the cost of its widest step
    is a tier people skip, which is the mechanism `D-369` records -- seven CI failures,
    every one a record check, none a behavioural test.

    **The default is the safe direction on purpose.** A new step is in the edit tier
    unless it says otherwise, so forgetting this flag makes the tier slower rather than
    blinder. Marking a step `broad` is the change that needs an argument, and
    `test_the_edit_tier_cannot_under_run` is where it has to be made.

    Being excluded from `--edit` is not being excluded from the gate. Every broad step
    still runs in `--fast` and above, and CI runs the full gate on every push."""

    sweep: bool = False
    """This step re-derives a retained atlas from its witnesses, and it is expensive
    enough that the pull request runs it on its own runner rather than beside the rest.

    `fast` says *whether* a pull request runs a step; this, `suite` and `geometry` say
    *which of the pull request's four jobs* runs it. Every sweep is also `fast`, the four
    selections are complements within `--fast`, and
    `test_the_pull_request_jobs_partition_the_surface` reads the workflow and checks all
    four against what CI actually invokes -- so a step cannot land in no job, and no
    step is paid for twice.

    The boundary is a measurement, not a topic. Four steps carry it, and on CI's
    four-cpu runner (run 34010470187) they cost 313.95s of step time: the
    translation-escape screen at 110.66s, the known-best chunk census at 90.38s, the
    known-best atlas at 75.88s, and the prospective seed at 37.03s. They are also one
    kind of work -- each rebuilds the retained atlas from the hundred-odd witnesses and
    compares it byte for byte -- which is why the split is stable: a step joins this set
    by being measured into it, and
    `test_the_pull_request_runs_its_sweeps_and_its_suite_apart` is where the number has
    to be typed.

    Why its own runner rather than a wider one, and this is the whole arithmetic. Four
    units on four cpus saturates the outer pool, so this job's wall is its longest unit's
    wall and nothing else: 110.66s, against 313.95s if the four had to queue behind the
    rest of the tier. That 110.66s was also the floor under the whole pull-request
    surface, and the lever on it was that step's own cost rather than another job.

    That lever has since been pulled, which is why this job now runs at `--inner-jobs 2`
    rather than 1. `screen_translation_escape` screens 98 independent records and was
    given a process pool on 2026-09-06; the pool reads `PACK_JOBS`, so until the flag
    moved it ran one worker and the parallelism was dormant. Best of five rounds on a
    four-cpu box: 103.94s at one worker, 52.11s at two, 35.40s at three, 27.50s at four.
    Two is what the job asks for, not four -- the outer pool already has four slots on
    four cpus, and a fifth process is the oversubscription that inflated every step of
    `checks` at `--jobs 4`. The blast radius is exactly this step: of the eleven modules
    this tier runs, only `screen_translation_escape` reaches `sqpack.workers`, checked per
    process rather than by eye, so `PACK_JOBS` reaches nothing else here.

    The floor moves with it. Measured whole at the new shape on a four-cpu box the job is
    79.52s: the census 79.51s, the screen 65.27s, the known-best atlas 50.52s, the
    prospective seed 25.07s. The screen costs more than its isolated 52.11s because two
    inner workers beside three other outer steps is not two workers alone, and it is under
    the census either way -- which is the only thing the flag had to achieve.
    `known-best chunk census` at 90.38s on CI is now this job's longest unit and the floor
    under the whole pull-request surface."""

    suite: bool = False
    """This step is the pull request's behavioural lane, and it runs alone on its own
    runner so that xdist can have every cpu.

    One step carries it and the reason is arithmetic rather than kind. `_pytest_workers`
    sizes the lane to `cpus - jobs + 1`, because a lane that asks for every cpu beside
    two other steps oversubscribes the runner and fails ordinary tests against the
    per-test ceiling for having noisy neighbours (`BC-218`). Beside 57 other steps at
    `--jobs 3` that formula gave two workers and the lane cost 142.43s of CI's 221.70s
    `checks` job (run 34010470187) -- the longest single unit anywhere on the surface,
    and a wall no outer parallelism can go below. Alone at `--jobs 1` the same formula
    gives four workers with nothing beside them, which is the one configuration where
    the lane can have the whole runner and the ceiling still measures tests rather than
    contention.

    So this flag buys two things at once that the `sweep` split could not: the lane stops
    setting the `checks` job's wall, and it gets twice the workers while it runs. What it
    does not buy is coverage -- the step runs on every pull request either way, which is
    the distinction `test_the_pull_request_surface_defers_only_what_was_measured` keeps.

    Like `sweep` it defaults to False, so forgetting it makes the `checks` job slower
    rather than leaving a step unrun, and like `sweep` its membership is pinned with a
    measurement in `test_the_pull_request_runs_its_sweeps_and_its_suite_apart`."""

    geometry: bool = False
    """This step runs in the pull request's second half of `checks`, on a fourth runner.

    `sweep` and `suite` were split out on a kind and on a floor. This one is split out on
    a queue, and saying so plainly is the honest description: what was left in `checks`
    after the behavioural lane moved out was 57 steps of pure outer-parallel work with no
    single unit large enough to floor it, and a queue that size is shortened by cpus and
    by nothing else.

    The measurement that forced it, CI run 34016999060 at `--checks --jobs 4
    --inner-jobs 1` on a four-cpu runner: 198.22s of tier wall against a 180s target for
    the whole surface, over roughly 790 worker-seconds of step time. That is the reading
    that also retired `--jobs 4` here. Against the same steps at `--jobs 3` on the run
    before it, every one of them inflated -- the perimeter 60.62s to 84.41s, the type
    floor 40.37s to 72.31s, the SVG renderer 41.30s to 65.36s -- because four outer slots
    on four cpus leaves nothing for the OS, for the pool-backed steps, or for
    `build_n5_identity_pair`, which asks `ProcessPoolExecutor` for the whole machine.
    Four workers over an inflated 790s is not faster than three over 470s; it is the same
    work bought at a worse price. So the split is two jobs at `--jobs 3`, and the second
    core of headroom is the point rather than a rounding error.

    Two rules bound which steps may carry this flag, and the balance is chosen inside
    them rather than over the whole tier:

    * **only a `broad` step**, so `--edit` stays wholly inside `--checks` and a
      contributor's edit loop never spans two selections. `test_the_edit_tier_cannot_
      under_run` is where that is enforced;
    * **no `needs_engine` step and nothing that runs cargo**, so exactly one of the two
      jobs pays the serial `cargo build --release` that `_build_engine` puts in front of
      every step -- about 25s on a cold runner -- and this job needs no Rust toolchain at
      all. That is why the perimeter, the selftest, the differential and the Rust lint
      floor all stay in `checks` even though the perimeter is the largest step there.

    Within those, the boundary is arithmetic: the nine steps below are 275.48s of a local
    545.08s reading (2026-09-06, four cpus, `--checks --jobs 4 --inner-jobs 1`), which
    leaves 269.60s in `checks`. Two halves inside two per cent of each other, and the two
    walls that follow at the reference shape on the same box are 93.27s here and 86.20s
    there. `test_the_pull_request_runs_its_sweeps_and_its_suite_apart` is where a name
    added here has to be typed next to a number.

    Like `sweep` and `suite` it defaults to False, so the failure mode of forgetting it is
    a slower `checks` job rather than a step nobody runs."""

    touches: tuple[str, ...] = ()
    """Repo-relative path globs whose change can affect this step's verdict.

    Empty means *unattributed*, and an unattributed step is selected by every change. The
    default is therefore the safe direction, exactly as `broad` is: forgetting to attribute
    a step costs time, never coverage.

    Selection is conservative on both sides, which is the whole design (`BC-084`):

    - a changed path matching no step's patterns selects the **entire gate**, never the
      empty set, so a file nobody thought about cannot silently skip everything;
    - a step with no patterns is always selected;
    - `test_every_step_is_reachable_from_a_declared_pattern` requires each step to be
      selected by at least one path under `PATTERN_PROBES`, so a pattern set that has
      drifted into selecting nothing is caught rather than trusted.

    **Do not over-trust the first of those.** `fnmatch` crosses separators, so `*.py` and
    `*.md` claim every Python and Markdown file in the repository: measured over the 1312
    tracked files, 953 are claimed and only 359 can still reach the escape hatch. No `.py`
    or `.md` change ever triggers it. For those two extensions the narrow steps' own
    patterns are the *only* protection, and five were measurably too narrow when first
    written -- the SVG step reads every Markdown file in the repo and claimed none of
    them, and `frontier corpus` claimed a module it never runs while missing the one it
    does. The escape hatch is a backstop for unfamiliar file types, not for careless
    attribution of familiar ones.

    This is the commit-boundary instrument, not the edit-loop one. `BC-079` already made
    the edit loop cheap -- `--records` is 5.7s and `--edit` 43s -- so the cost this
    addresses is the full gate, where `D-355` measured a two-file edit to the rigidity
    assessor verified by a 979.79s run whose two reachable steps take 12.06s together.

    Measured on 2026-08-30 over the 42 steps: an edit to the rigidity assessor selects 11,
    one root document 9, one agenda 10, the Rust engine 12, and one unrecognised file
    still selects all 42. Six steps are deliberately unattributed because their true input
    set is the repository's whole path space -- `negative controls` runs 148 declared shell
    commands against a snapshot of nearly everything, `fast behavioral tests` walks
    `REPO.rglob("*")`, and `synopsis`, `README`, `soft-schema validation` and the
    exhaustive test step each resolve or enumerate arbitrary paths. Attributing those would
    make a data file the load-bearing contract, which is the trade this field exists to
    refuse."""

    budget_seconds: float | None = None
    """This step's own declared ceiling, for the rare step that legitimately costs more
    than the shared per-step cap.

    The shared cap exists to stop a hung step consuming the run, and it should stay tight
    for the forty steps that do not need it. `D-366` is the case that motivated an
    exception: the control suite is killed at 900 seconds and completes in about 1270,
    with nothing wrong with it -- it simply grew. Raising the shared cap would have bought
    that one step a pass by weakening the guard on every other step at once, which is the
    trade this field exists to refuse.

    A budget is a declaration, not a waiver. It is per step, it is written next to the
    step that claims it with the measurement that justifies it, and a step that exceeds
    its own budget still fails. An explicit `--timeout-seconds` on the command line still
    wins, so an operator can always tighten what a step asked for."""

    def reachable_from(self, path: str) -> bool:
        """Can a change to `path` affect this step?

        An unattributed step answers yes to everything, which is what makes forgetting to
        attribute one safe.
        """
        if not self.touches:
            return True
        return any(fnmatch.fnmatch(path, pattern) for pattern in self.touches)

    @property
    def tags(self) -> str:
        tags = ["fast" if self.fast else "full"]
        if self.sweep:
            tags.append("sweeps")
        elif self.suite:
            tags.append("suite")
        elif self.geometry:
            tags.append("geometry")
        elif self.fast:
            tags.append("checks")
        if self.fast and not self.broad:
            tags.append("edit")
        if self.records:
            tags.append("records")
        if self.needs_engine:
            tags.append("engine")
        return ", ".join(tags)


@dataclass(frozen=True)
class StepResult:
    """The complete observable outcome of one step."""

    name: str
    status: Literal["passed", "failed", "skipped"]
    seconds: float
    output: str = ""
    reason: str = ""


@dataclass
class RunSummary:
    """Ordered validation results plus setup output."""

    results: list[StepResult]
    wall_seconds: float
    setup_output: str = ""
    selected_count: int = 0
    total_count: int = 0
    partial_pattern: list[str] = field(default_factory=list)
    skipped_pattern: list[str] = field(default_factory=list)
    """The `--skip` patterns, kept apart from `--only` so the closing line can say which
    narrowing produced a partial surface. A run that skipped one named step is not the
    same thing as a tier, and reporting it as one is how a job that quietly stopped
    running something looks exactly like a job that was never meant to."""
    budget: gate_budgets.Verdict | None = None
    """What this run's wall says about the tier it ran, or `None` when the register could
    not be read. Carried on the summary so `--format json` reports the cost verdict to a
    machine, which is the difference between this and the docstring it replaces."""


def _timeout_output(error: subprocess.TimeoutExpired) -> str:
    output = error.output
    if isinstance(output, bytes):
        return output.decode(errors="replace")
    return output or ""


def _stop_process_group(process: subprocess.Popen[str]) -> str:
    """Stop one POSIX group and reap its parent.

    Deliberately detached descendants are outside this group-scoped guarantee.
    """
    grace_deadline = time.monotonic() + PROCESS_TERMINATION_GRACE_SECONDS
    with suppress(ProcessLookupError):
        os.killpg(process.pid, signal.SIGTERM)
    try:
        stdout, _ = process.communicate(timeout=PROCESS_TERMINATION_GRACE_SECONDS)
        output = stdout or ""
    except subprocess.TimeoutExpired as error:
        output = _timeout_output(error)

    # communicate() can return as soon as the parent exits even though a descendant
    # ignores TERM and no longer holds the parent's output pipe. Preserve the complete
    # grace interval before escalating the whole group.
    remaining = grace_deadline - time.monotonic()
    if remaining > 0:
        time.sleep(remaining)
    with suppress(ProcessLookupError):
        os.killpg(process.pid, signal.SIGKILL)

    try:
        stdout, _ = process.communicate(timeout=PROCESS_TERMINATION_GRACE_SECONDS)
    except subprocess.TimeoutExpired as error:
        if process.stdout is not None:
            process.stdout.close()
        try:
            process.wait(timeout=PROCESS_TERMINATION_GRACE_SECONDS)
        except subprocess.TimeoutExpired as reap_error:
            raise StepFailureError(
                "timed-out command did not exit after process-group SIGKILL"
            ) from reap_error
        return _timeout_output(error) or output
    else:
        return stdout or output


def _run(
    context: Context,
    command: Sequence[str],
    *,
    cwd: Path = PROJECT_ROOT,
    timeout_seconds: float | None = None,
) -> str:
    effective_timeout = (
        context.timeout_seconds
        if timeout_seconds is None
        else min(timeout_seconds, context.timeout_seconds)
    )

    if os.name == "nt":
        raise StepFailureError(
            "bounded validation subprocesses require verified process-tree cleanup; "
            "Windows support is not yet implemented"
        )

    process = subprocess.Popen(
        list(command),
        cwd=cwd,
        env=context.environment,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        start_new_session=True,
    )
    try:
        context.processes.register(process.pid)
    except StepFailureError:
        try:
            process.communicate(timeout=PROCESS_TERMINATION_GRACE_SECONDS)
        except subprocess.TimeoutExpired as error:
            if process.stdout is not None:
                process.stdout.close()
            raise StepFailureError(
                "rejected validation subprocess did not exit after SIGKILL"
            ) from error
        raise
    try:
        stdout, _ = process.communicate(timeout=effective_timeout)
    except subprocess.TimeoutExpired:
        output = _stop_process_group(process).rstrip()
        rendered = " ".join(command)
        detail = f"command timed out after {effective_timeout:g} seconds: {rendered}"
        if output:
            detail += f"\n{output}"
        raise StepFailureError(detail) from None
    except BaseException:
        _stop_process_group(process)
        raise
    finally:
        context.processes.discard(process.pid)
    output = (stdout or "").rstrip()
    if process.returncode:
        rendered = " ".join(command)
        detail = f"command exited {process.returncode}: {rendered}"
        if output:
            detail += f"\n{output}"
        raise StepFailureError(detail)
    return output


def _module(context: Context, module: str, *arguments: str) -> str:
    return _run(context, (sys.executable, "-m", module, *arguments))


def _commands(
    context: Context, commands: Sequence[Sequence[str]], *, cwd: Path = PROJECT_ROOT
) -> str:
    outputs = [_run(context, command, cwd=cwd) for command in commands]
    return "\n".join(output for output in outputs if output)


def _require_text(output: str, *needles: str) -> None:
    missing = [needle for needle in needles if needle not in output]
    if missing:
        raise StepFailureError(f"output omitted required text: {missing!r}\n{output}")


def _required_tool(context: Context, name: str) -> str:
    found = shutil.which(name, path=context.environment.get("PATH"))
    if found is None:
        raise StepFailureError(
            f"required development tool is unavailable: {name}; run `uv sync --group dev`"
        )
    return found


def _optional_tool(context: Context, name: str) -> str:
    found = shutil.which(name, path=context.environment.get("PATH"))
    if found is None:
        raise StepSkippedError(f"{name} is unavailable")
    return found


_DURATION_LINE = re.compile(
    r"^(?P<seconds>\d+\.\d+)s\s+(?P<phase>setup|call|teardown)\s+(?P<node>\S+)$"
)
#: pytest prints this header whenever `--durations` is given, even when every test is
#: under the minimum. Requiring it is what makes the ceiling check fail closed: if a
#: future pytest renders durations differently, the check reports that it could not read
#: them rather than silently finding no violations forever.
_DURATION_HEADER = "slowest durations"


def _call_durations(output: str) -> list[tuple[float, str]]:
    """Every test `call` phase pytest's durations section reported, slowest first."""
    calls = [
        (float(match["seconds"]), match["node"])
        for line in output.splitlines()
        if (match := _DURATION_LINE.match(line.strip())) and match["phase"] == "call"
    ]
    return sorted(calls, reverse=True)


#: A node id split into the test function and the parametrization pytest appended to it.
#:
#: The shape is `path::[Class::]function[params]`, and the awkward part is `params`, which
#: pytest writes with `ascii_escaped` and therefore does not escape brackets or colons:
#: `test_param[with[brackets]]`, `TestClass::test_method[z[1]]` and `test_param[x::y]` are
#: all real ids this project's own pytest emits, checked rather than assumed. So neither
#: "cut at the first `[`" nor "split on the last `::`" is safe.
#:
#: What is safe is that a function name is a Python identifier and the parametrization is
#: the whole of the tail. The lazy `.*?::` walks `::`-separated segments from the left and
#: the greedy `\[.*\]$` swallows the tail whole, so the match lands on the last segment
#: that is an identifier followed by either nothing or a bracketed suffix reaching the end
#: of the line -- which is the function, whatever the parameters contain.
_TEST_NODE = re.compile(r"^(?P<function>.*?::[A-Za-z_]\w*)(?:\[.*\])?$")


def _test_function(node: str) -> str:
    """The node id with its parametrization removed, or the node id if it has none.

    An id this cannot parse is returned whole rather than dropped or raised on. That
    degrades to one group per node, which is the behaviour this function replaced, so an
    unfamiliar id makes the floor check stricter than intended rather than blind.
    """
    match = _TEST_NODE.match(node)
    return node if match is None else match["function"]


def _slowest_call_per_function(entries: list[tuple[float, str]]) -> list[tuple[float, str]]:
    """One entry per test function, carrying its slowest parametrization.

    The `slow` marker is per function -- a decorator on a `def`, so a parametrized test
    moves to the deep surface with all of its cases, which is why the registry in
    `test_the_slow_marker_is_declared_only_by_measured_nodes` counts 62 functions and 92
    collected tests. A floor applied per *node* therefore asks a question the marker
    cannot answer: it reports the cheap case of an expensive function as a marker to
    delete, and deleting it would drag the expensive case back onto the pull-request
    surface. The cost of a marker is the cost of its slowest case, so that is what the
    floor compares.

    Ordering is not assumed: the maximum is taken explicitly rather than relying on the
    caller having sorted, and the result is sorted slowest first for rendering.
    """
    slowest: dict[str, tuple[float, str]] = {}
    for seconds, node in entries:
        function = _test_function(node)
        current = slowest.get(function)
        if current is None or seconds > current[0]:
            slowest[function] = (seconds, node)
    return sorted(slowest.values(), reverse=True)


def _require_durations(output: str, lane: str, rule: str) -> None:
    if _DURATION_HEADER not in output:
        raise StepFailureError(
            f"pytest printed no durations section for the {lane} lane, so {rule} went "
            f"unchecked; expected {_DURATION_HEADER!r} in the output"
        )


def _render_durations(entries: list[tuple[float, str]]) -> str:
    return "\n".join(f"    {seconds:7.2f}s  {node}" for seconds, node in entries)


def _pytest_workers(jobs: int) -> int:
    """How many pytest processes the quick behavioural lane asks for.

    Deliberately not `--inner-jobs`. That knob is the worker cap *exported to* every step,
    and the tiers set it to 1 for a good reason: most steps are a single process, the gate
    runs `--jobs` of them at once, and a cap that made each one greedy would just make
    them fight. This lane is the exception, and `BC-218` measured why.

    On CI's own runner (run 33985984585, job 101359470209, commit 88f7e5f8) the `--fast`
    tier's wall was 408.55s and `fast behavioral tests` was 408.09s of it -- 99.9 per
    cent. That is not a tier whose steps are queued behind each other: `--jobs 2` had
    already absorbed the other 37 steps into the second lane, where their whole visible
    cost was 135.17s, and they finished with the wall to spare. So the sequencing was
    never the cost, and no arrangement of GitHub jobs can shorten a wall that is one step
    -- a second job would repeat 11s of checkout, uv install and `uv sync` to run work
    that already costs nothing on the clock. The only parallelism left to buy is inside
    the step.

    The lane is the right shape for it: around 2,000 tests, each held under
    `QUICK_TEST_CEILING_SECONDS` by the ceiling the step itself enforces, none of them
    writing anywhere shared. Measured on a four-core box at `PACK_JOBS=1`: 306.4s in one
    process against 135.04s at `-n 4`, with no failure that appears only under xdist.

    135s is not 306/4, and the gap is where the rest of this lane's cost now is. Two tests
    carry 121s of the serial lane between them -- 93.86s and 26.83s -- so nearly a
    quarter of the work sits in units too big to divide, and at `-n 4` the larger of them
    is 70 per cent of the wall on its own. Neither has grown. Both call a module-level
    cached builder that a test BC-214 deferred used to trigger first, so both are being
    billed for a build rather than for themselves, and this step's own ceiling is failing
    on them today. That is named where the rule lives, in
    `test_the_slow_marker_is_declared_only_by_measured_nodes`, and it is not fixed here:
    marking them moves the failure to the deep surface rather than removing it, because in
    the slow lane the same two tests measure 0.01s and 0.00s. With those 121s gone the
    lane measured 56.61s at `-n 4`, which is what this step is worth once they are.

    The count is what the box has left, not what it has. This lane used to ask for one
    worker per cpu on the grounds that nothing else was waiting behind it, which was true
    while `--jobs 2` hid every other step underneath it. It stopped being true at
    `--jobs 3`: two other steps now run beside this one, so a request for every cpu
    oversubscribes the runner, and the cost lands in a place the tier cannot absorb.

    The measurement that forced this, on GitHub's four-cpu runner. At `--jobs 3` with one
    worker per cpu the tier ran 140.79s once and 192.26s the next time on the same
    configuration -- 37 per cent apart, which is not a tier anyone can set a band around.
    Worse, the second run failed with **19 tests at or above the 5s per-test ceiling**,
    between 5.4s and 8.3s, and not one of them was a shared build or an intrinsically slow
    test: they were ordinary tests inflated by contention. That is the ceiling catching the
    wrong thing. It exists to find a test that is expensive, and under oversubscription it
    finds tests that are merely *contended*, which makes it noise rather than a signal.

    So the lane sizes itself to what is free: `cpus - jobs + 1`, this step being one of the
    `jobs`. At four cpus that is two workers under `--jobs 3` and three under `--jobs 2`,
    and in both cases total concurrency lands at about the cpu count instead of half again
    over it. `-n 1` is not asked for: a single xdist worker is a subprocess and a protocol
    for no concurrency at all, which is slower than not asking, so one worker means running
    in-process.

    The pull request now runs this step alone on its own job at `--jobs 1`, and that is
    the same formula rather than an exception to it: with nothing else in the selection
    the count is `cpus`, and total concurrency is still about the cpu count. The
    difference is who else is asking. That is the whole reason `Step.suite` exists --
    beside 57 other steps the lane could have two workers honestly or four dishonestly,
    and on its own runner four is what is free.

    This trades a little of the lane's own speed for a per-test measurement that means
    something. That is the right trade while the ceiling is the mechanism `OR-13` leans on
    to decide what may leave the pull-request surface: a ceiling measured under contention
    would send tests to the deep surface for the sin of having noisy neighbours.
    """
    cpus = max(1, os.process_cpu_count() or DEFAULT_CPU_COUNT)
    return max(1, cpus - jobs + 1)


def _quick_lane_command(jobs: int) -> tuple[str, ...]:
    workers = _pytest_workers(jobs)
    distribution = () if workers == 1 else ("-n", str(workers))
    return (
        sys.executable,
        "-m",
        "pytest",
        "-q",
        "tests",
        "-m",
        QUICK_TESTS,
        *distribution,
        "--durations=0",
        f"--durations-min={QUICK_TEST_CEILING_SECONDS:g}",
    )


def _fast_tests(context: Context) -> str:
    output = _run(context, _quick_lane_command(context.jobs))
    _require_durations(output, "quick", f"the {QUICK_TEST_CEILING_SECONDS:g}s per-test ceiling")
    over = [
        entry for entry in _call_durations(output) if entry[0] >= QUICK_TEST_CEILING_SECONDS
    ]
    if over:
        raise StepFailureError(
            f"{len(over)} test(s) ran at or above the pull-request surface's "
            f"{QUICK_TEST_CEILING_SECONDS:g}s per-test ceiling:\n{_render_durations(over)}\n"
            "  Make it faster, or mark it `slow` and declare it with its measurement in "
            "test_the_slow_marker_is_declared_only_by_measured_nodes. The marker moves "
            "the test to the deep surface; it does not stop it running."
        )
    return output


#: pytest's exit code for "every test was deselected", which for the slow lane means the
#: ceiling currently defers nothing rather than that anything is wrong.
_PYTEST_NOTHING_SELECTED = "command exited 5:"


def _slow_tests(context: Context) -> str:
    try:
        output = _run(
            context,
            (
                sys.executable,
                "-m",
                "pytest",
                "-q",
                "tests",
                "-m",
                SLOW_TESTS,
                "--durations=0",
                "--durations-min=0",
            ),
        )
    except StepFailureError as error:
        # An empty lane is a lane with no members, not a broken gate. The membership is
        # decided by a ceiling, so it can legitimately fall to zero -- and a deep surface
        # that failed when nothing was slow would teach people to keep a token member in
        # the lane, which is worse than the failure it was meant to report.
        if _PYTEST_NOTHING_SELECTED not in str(error):
            raise
        return "  no test is deferred by the per-test ceiling; the quick lane runs them all"
    _require_durations(output, "slow", f"the {SLOW_TEST_FLOOR_SECONDS:g}s marker floor")
    # Per function, not per node, because the marker is per function. `_fast_tests` keeps
    # the opposite rule for the opposite reason: one node at or above the ceiling is one
    # node the pull-request surface actually pays for, whatever its siblings cost.
    under = [
        entry
        for entry in _slowest_call_per_function(_call_durations(output))
        if entry[0] < SLOW_TEST_FLOOR_SECONDS
    ]
    if under:
        raise StepFailureError(
            f"{len(under)} deferred test(s) ran below the {SLOW_TEST_FLOOR_SECONDS:g}s floor "
            f"a `slow` marker has to earn, each shown at its slowest parametrization:\n"
            f"{_render_durations(under)}\n"
            "  Delete the marker and its registry entry. OR-13 is a floor on coverage: a "
            "test leaves the pull-request surface by its own measured cost, and one that "
            "no longer costs that has to come back."
        )
    return output


def _exhaustive_exact_tests(context: Context) -> str:
    return _run(
        context,
        (
            sys.executable,
            "-m",
            "pytest",
            "-q",
            "tests",
            "-m",
            EXHAUSTIVE_TESTS,
        ),
    )


def _soundness_perimeter(context: Context) -> str:
    output = _module(context, "devtools.check_soundness_perimeter")
    if "skipping engine cells" in output:
        raise StepSkippedError(
            "soundness perimeter did not exercise sqsearch cells",
            output=output,
        )
    return output


_HANDWRITTEN_SKILLS_PATTERN = re.compile(
    r"^HANDWRITTEN_SKILLS\s*:=\s*(?P<names>.*)$", re.MULTILINE
)


def _handwritten_skill_directories() -> tuple[Path, ...]:
    """The hand-written skills under `.agents/skills`, read from the Makefile's
    `HANDWRITTEN_SKILLS` so the lint floor and `make skills-check` share one list.

    Only these are linted. The generated skills beside them are rewritten
    byte-for-byte by their installers, and ruff formats the Python blocks in Markdown
    as well as `.py` files, so pointing it at the whole directory would put the gate
    in conflict with the generators, which is the case `.flowmarkignore` already
    documents. `.claude/skills` is the mirror `make skills-sync` keeps and is not a
    second target.
    """
    makefile = REPOSITORY_ROOT / "Makefile"
    match = _HANDWRITTEN_SKILLS_PATTERN.search(makefile.read_text(encoding="utf-8"))
    if match is None:
        raise StepFailureError(f"{makefile} does not declare HANDWRITTEN_SKILLS")
    names = match.group("names").split()
    if not names:
        raise StepFailureError(f"{makefile} declares HANDWRITTEN_SKILLS as empty")
    directories = tuple(REPOSITORY_ROOT / ".agents" / "skills" / name for name in names)
    missing = [str(path) for path in directories if not path.is_dir()]
    if missing:
        raise StepFailureError(f"HANDWRITTEN_SKILLS names missing directories: {missing}")
    return directories


def _lint_floor(context: Context) -> str:
    """Ruff alone, because it is the half that is instant and the half that caught a
    registry bug: the duplicated declared-consumer key behind one of D-369's CI
    failures was an `F601`. Measured under a second against basedpyright's 36.

    The second target is the hand-written skill assets at the repository root, the one
    place project Python lives outside this directory; basedpyright reaches them
    through its `include` list instead."""
    ruff = _required_tool(context, "ruff")
    skills = [str(path) for path in _handwritten_skill_directories()]
    return _commands(
        context,
        ((ruff, "check", ".", *skills), (ruff, "format", "--check", ".", *skills)),
    )


def _type_floor(context: Context) -> str:
    basedpyright = _required_tool(context, "basedpyright")
    output = _commands(context, ((basedpyright,),))
    _require_text(output, "0 errors, 0 warnings, 0 notes")
    return output


def _basin_atlas(context: Context) -> str:
    return _module(context, "devtools.check_atlas")


def _basin_event_archives(results: Path) -> list[Path]:
    """Discover retained event journals by their versioned record contract."""
    archives: list[Path] = []
    for path in sorted(results.glob("*.jsonl")):
        first_line = next(
            (line for line in path.read_text().splitlines() if line.strip()), None
        )
        if first_line is None:
            continue
        try:
            first_record = json.loads(first_line)
        except json.JSONDecodeError as error:
            message = f"cannot classify malformed result archive {path}"
            raise StepFailureError(message) from error
        contract = first_record.get("contract") if isinstance(first_record, dict) else None
        if isinstance(contract, str) and contract.startswith(BASIN_EVENT_CONTRACT_PREFIX):
            archives.append(path)
    return archives


def _basin_events(context: Context) -> str:
    module = "cases.campaign_smoke.basin_events"
    archives = _basin_event_archives(PROJECT_ROOT / RESULTS)
    if not archives:
        raise StepFailureError(f"no basin-event archives found below {RESULTS}")
    outputs = [_module(context, module, "--selftest")]
    outputs.extend(
        _module(context, module, "replay", str(archive.relative_to(PROJECT_ROOT)))
        for archive in archives
    )
    return "\n".join(outputs)


def _historical_regressions(context: Context) -> str:
    return _module(context, "devtools.check_regressions")


def _small_n(context: Context) -> str:
    commands = (
        (
            sys.executable,
            "-m",
            "cases.small_n.optimal_moduli",
            "--n",
            "3",
            "--replay",
            str(RESULTS / "exp-014-h-032-n3-optimal-moduli.json"),
            "--check-svg",
            "atlas/n-003-optimal-moduli.svg",
        ),
        (
            sys.executable,
            "-m",
            "cases.small_n.optimal_moduli",
            "--n",
            "4",
            "--replay",
            str(RESULTS / "exp-015-h-032-n4-optimal-moduli.json"),
        ),
        (
            sys.executable,
            "-m",
            "cases.small_n.terminal_components",
            "--replay",
            str(RESULTS / "exp-032-h-021-terminal-component-controls.json"),
        ),
        (
            sys.executable,
            "-m",
            "cases.n5.equal_side_face",
            "--replay",
            str(RESULTS / "exp-033-h-023-n5-equal-side-face.json"),
        ),
        (
            sys.executable,
            "-m",
            "cases.n5.angle_sheet",
            "--replay",
            str(RESULTS / "exp-034-h-023-n5-angle-sheet.json"),
        ),
        (
            sys.executable,
            "-m",
            "cases.n5.tangent_cones",
            "--replay",
            str(RESULTS / "exp-035-h-023-n5-tangent-cones.json"),
        ),
        (
            sys.executable,
            "-m",
            "cases.n5.second_order_obstruction",
            "--replay",
            str(RESULTS / "exp-036-h-023-n5-second-order-obstruction.json"),
        ),
        (
            sys.executable,
            "-m",
            "cases.n5.tangent_inventory",
            "--replay",
            str(RESULTS / "exp-038-h-023-n5-tangent-inventory.json"),
        ),
        (
            sys.executable,
            "-m",
            "cases.n5.fixed_angle_polytope",
            "--replay",
            str(RESULTS / "exp-039-h-023-n5-fixed-angle-polytope.json"),
        ),
        (
            sys.executable,
            "-m",
            "cases.n5.rotating_release_paths",
            "--replay",
            str(RESULTS / "exp-042-h-023-n5-endpoint-aware-rotating-paths.json"),
        ),
    )
    return _commands(context, commands)


def _svg_rendering(context: Context) -> str:
    output = _module(context, "devtools.check_svg_rendering", "--check")
    _require_text(output, "SVG RENDERING CHECKS PASSED")
    return output


def _known_best_atlas(context: Context) -> str:
    """The known-best atlas without the chunk census, which is its own step.

    `_commands` runs its list in one process after another, so a step is only as
    schedulable as its longest member and the gate's `--jobs` pool cannot see inside it.
    Measured one subcommand at a time on a four-cpu box at `PACK_JOBS=1`, this step's
    nine members were 133.22s, of which `census_known_best_chunks` alone was 94.85s and
    `build_known_best_atlas` 27.28s; the other seven were 11.09s between them. Against
    the 254.92s the whole step cost on CI that is about 181s in one member, so a step
    declared as one unit put a three-minute serial block in the middle of a tier trying
    to finish in three minutes.

    Splitting at that seam is the only division the measurement supports, and it is
    two steps rather than nine for the same reason: the other seven are noise, and a
    step per subcommand would be seven more names in the register for no wall.
    """
    output = _commands(
        context,
        (
            (sys.executable, "-m", "devtools.build_known_best_atlas", "--check"),
            (sys.executable, "-m", "devtools.build_composite_figure_data", "--check"),
            (sys.executable, "-m", "devtools.render_composite_pdf", "--check"),
            (
                sys.executable,
                "-m",
                "devtools.render_known_best_contact_overlays",
                "--check",
            ),
            (
                sys.executable,
                "-m",
                "devtools.profile_known_best_chunks",
                "--check",
            ),
            (sys.executable, "-m", "devtools.price_contact_enumeration", "--check"),
            (
                sys.executable,
                "-m",
                "devtools.generate_contact_full_cell_control",
                "--check",
            ),
            (
                sys.executable,
                "-m",
                "devtools.generate_contact_structures",
                "--check",
            ),
        ),
    )
    _require_text(
        output,
        "known-best atlas check passed: 100 sources/plans, witnesses, renders, "
        "1 composite, and links",
        "known-best contact overlay check passed: 5 house-rendered calibration strata",
        "known-best chunk evidence profile check passed: 36 non-grid calibration cases",
        "contact enumeration pricing check passed",
        "contact full-cell control check passed",
        "contact structures check passed",
    )
    return output


def _known_best_chunk_census(context: Context) -> str:
    """94.85s of the 133.22s the known-best atlas cost as one step, and about 181s on CI.

    Nothing about the check changed when it was given its own name: it reads the same
    committed documents and compares the same re-derivation. What changed is that the
    gate can now schedule it, and that the step table names it -- which is what `OR-14`
    asks for before anyone tries to make it cheaper. It is the longest single unit in
    the sweeps job, and the second-longest anywhere on the pull-request surface.
    """
    output = _module(context, "devtools.census_known_best_chunks", "--check")
    _require_text(
        output,
        "chunk census check passed: components, contacts, and bounded lattice partitions "
        "for 100 records",
    )
    return output


def _prospective_source_map(context: Context) -> str:
    output = _module(context, "devtools.map_prospective_sources", "--check")
    _require_text(
        output, "prospective source map check passed: 224 cases, availability and SVG"
    )
    return output


def _prospective_atlas(context: Context) -> str:
    """The single longest unit on the pull-request surface: 213.2s of CI's 1,100s.

    Split from the source map it used to share a step with, and the split buys
    attribution rather than time -- the map is 0.39s of the 88.76s the pair cost
    locally. That is the point: `OR-14` says to attribute rather than absorb, and until
    this step carried one subcommand the tier's largest cost was reported under a name
    that also covered a sub-second check.

    That sentence has since been paid off twice and the figure above is the older of the
    two readings: memoizing the frontier took this step to 37.03s, and it is now the
    smallest of the sweeps rather than the largest. What has not changed is the shape of
    the argument. The sweeps job has four units and four cpus, so its outer pool is
    saturated and its wall is its longest unit's wall; the only lever on that unit is the
    unit's own cost. `build_prospective_atlas` still rebuilds 101 witnesses and 101 house
    renderings in one process, each independent of the others, with
    `sqpack.workers.worker_count` unused -- which is what `screen_translation_escape` did
    until it was given a pool and this job was given `--inner-jobs 2`, and it is where
    the next reduction in this job's wall comes from.
    """
    output = _module(context, "devtools.build_prospective_atlas", "--check")
    _require_text(
        output, "prospective atlas seed check passed: 101 witnesses and 101 house renderings"
    )
    return output


def _frontier_rigidity(context: Context) -> str:
    """Every rigidity block still follows from the screen and the tiling argument.

    The counts are pinned because they are the finding: 84 records are NOT rigid on a
    replayable certificate, ten are rigid by an exact tiling with no slack, and four are
    assessed and unsettled. `undetermined` is a result and is not the same as the field
    being null.

    Two records are excluded here because a stronger first-party argument owns them, and
    the exclusion is keyed on the evidence id rather than on a list of n: n=11 from the
    tangent-cone work, and n=5 from `X-007`'s exact first- and second-order certificates.
    n=5 left the assessed bucket while still *reading* `undetermined` -- second-order
    rigidity is not local rigidity -- which is why both numbers here moved by one at once;
    it reads `locally-rigid` since 2026-09-03 (`T-014`), and because the exclusion is by
    evidence id rather than by property, the counts below did not move again with it.

    n=40 moved the same way on 2026-08-30 and for the opposite finding. It is
    infinitesimally *flexible* over `Q(sqrt 2)`, with seven retained directions each refused
    at second order; the property still reads `undetermined` because an infinitesimal flex
    is not a motion and `not-rigid` would assert one. So the counts moved by one again, and
    a record can leave the assessed bucket for having a stronger argument in either
    direction.
    """
    output = _module(context, "devtools.assess_frontier_rigidity", "--check")
    _require_text(output, "frontier rigidity check passed")
    review = _module(context, "devtools.assess_frontier_rigidity", "--review")
    _require_text(
        review,
        "assessed: 10 locally-rigid, 84 not-rigid, 3 undetermined, "
        "3 left to a stronger argument",
    )
    _require_text(review, "left to a stronger argument: n = [5, 11, 40]")
    return output + review


def _translation_escape_screen(context: Context) -> str:
    """The single-square translation screen, rebuilt from the witnesses every run.

    The counts are pinned here because they are the finding: 25 records hold a square
    that can be pushed clear of everything it touches, and the two records whose witness
    geometry is too coarse to read contacts from are excluded rather than reported on.
    A miss is not rigidity, so nothing here may be restated as one.
    """
    output = _module(context, "devtools.screen_translation_escape", "--check")
    _require_text(
        output,
        "translation escape screen check passed: 98 records screened, "
        "25 with a square that separates (76 squares), "
        "84 with a square that translates at all (496 squares), "
        "excluded: n=68, n=69",
    )
    return output


def _contact_scaffold_atlas(context: Context) -> str:
    output = _module(context, "devtools.build_contact_scaffold_atlas", "--check")
    _require_text(
        output,
        "contact scaffold atlas check passed: 21 topologies, 11013 abstract orbits",
    )
    return output


def _negative_controls(context: Context) -> str:
    workers = min(NEGATIVE_CONTROL_WORKERS, context.inner_jobs)
    return _module(
        context,
        "devtools.run_negative_controls",
        "devtools/controls.yaml",
        "-j",
        str(workers),
    )


def _independent_lp(context: Context) -> str:
    output = _module(context, "cases.trump11.independent_lp_cell")
    _require_text(output, "23 variables, 1056 constraints", "ALL CHECKS PASSED")
    return output


def _bead_tree(context: Context) -> str:
    output = _module(context, "devtools.check_bead_tree")
    if output.startswith("SKIP"):
        raise StepSkippedError("no bead store is reachable", output=output)
    return output


def _golden_basins(context: Context) -> str:
    arguments = ("--deep",) if context.deep else ()
    output = _module(context, "devtools.check_golden_basins", *arguments)
    if not context.deep:
        output += "\n  (fast path; `packing-validate --deep` rebuilds and compares the map)"
    return output


def _canonical_identity(context: Context) -> str:
    return _module(context, "devtools.check_canonical")


def _schemas(context: Context) -> str:
    return _commands(
        context,
        (
            (sys.executable, "-m", "devtools.validate_schemas"),
            (sys.executable, "-m", "devtools.check_source_coverage"),
        ),
    )


def _derivation(context: Context) -> str:
    output = _module(context, "cases.trump11.derive_field")
    _require_text(output, "matches cases.trump11.packing.U_MIN_POLY: True")
    return output


def _search_engine(context: Context) -> str:
    if not ENGINE.is_file():
        raise StepSkippedError("sqsearch binary is absent")
    output = _run(context, (str(ENGINE), "--selftest"))
    _require_text(output, "SELFTEST PASSED")
    if "FAIL" in output:
        raise StepFailureError(output)
    return output


def _rust_quality(context: Context) -> str:
    cargo = _optional_tool(context, "cargo")
    output = _commands(
        context,
        (
            (cargo, "clippy", "--release", "--all-targets", "--quiet", "--", "-D", "warnings"),
            (cargo, "fmt", "--check"),
        ),
        cwd=PROJECT_ROOT / "sqsearch",
    )
    return f"{output}\n  clippy clean at warnings-as-errors; rustfmt clean".strip()


def _trump_cones(context: Context) -> str:
    return _module(
        context,
        "cases.trump11.tangent_cones",
        "--replay",
        str(RESULTS / "exp-013-h-026-trump-tangent.json"),
    )


def _stromquist_repair(context: Context) -> str:
    return _module(
        context,
        "cases.stromquist.repaired_cover",
        "--replay",
        str(RESULTS / "exp-017-h-041-stromquist-repaired-figure14.json"),
    )


def _stromquist_rejection(context: Context) -> str:
    return _module(
        context,
        "cases.stromquist.printed_cover",
        "--replay",
        str(RESULTS / "exp-016-h-010-stromquist-printed-figure14.json"),
    )


def _exact_verification(context: Context) -> str:
    output = _commands(
        context,
        (
            (
                sys.executable,
                "-m",
                "devtools.generate_known_best_n011_rational_control",
                "--check",
            ),
            # The exact rational grid replay. It ran inside `soft-schema validation`
            # until D-370, where it was 3.58s of that step and where nobody would look
            # for exact geometry. Same cases, same predicate, same verdict; only the
            # step reporting it changed.
            (sys.executable, "-m", "devtools.check_basic_bounds"),
            (sys.executable, "-m", "cases.trump11.verify_exact"),
            (sys.executable, "-m", "cases.gobel5.verify_exact"),
            (sys.executable, "-m", "cases.gobel10.verify_exact"),
            # n=40 joined the exact cases on 2026-08-30. Its construction is Goebel's
            # published centred-diagonal-block family at a=3, b=4, and its replay also
            # checks agreement with the retained decimal witness to that witness's own
            # truncation, which is the only discrepancy there is.
            (sys.executable, "-m", "cases.gobel40.verify_exact"),
            # n=65 and n=89 joined the same day and by the same route. Goebel's family is
            # exactly the best known at n = 5, 40, 65 and 89; the first two already had
            # constructions, and building the other two took the general form of the rule
            # rather than any new mathematics. Their replay also identifies their retained
            # witnesses: agreement to 5e-33 is not something an independent optimisation
            # reaches, so those decimals are materialisations of this family.
            (sys.executable, "-m", "cases.gobel_family.verify_exact"),
            # n=82 joined on 2026-08-31, the first slice of BC-089's recognition block:
            # the family pose at (4,5) plus the one L DS7 states. Its replay checks the
            # witness's declared side (the exact value rounded up at 32 digits) but not
            # its layout, which matches none of the construction's dihedral images.
            (sys.executable, "-m", "cases.gobel82.verify_exact"),
            # The strip family joined the same day: n = 27, 38, 52, 67 and 84 at
            # a + 1 + sqrt(2)/2 for a = 4..8, with the diamond-count control refusing
            # one more at every size. Five more grid ceilings became exact sides.
            (sys.executable, "-m", "cases.gobel_strip.verify_exact"),
            # And the off-centre family, DS7 section 3's one sentence: n = 26 and 85 at
            # a + 3/2 + b/sqrt(2), with the column-count control refusing square 2a + 2.
            (sys.executable, "-m", "cases.gobel_offcentre.verify_exact"),
            # And the first witness lifts: n = 19 and 66 have published exact sides but
            # no published rule, and their retained decimals lift coordinate by
            # coordinate into Q(sqrt 2) at small height. The lift generates; exact_sign
            # decides.
            (sys.executable, "-m", "cases.lifted_q2.verify_exact"),
            # n = 18 and 86 lift the same way into Q(sqrt 7) -- the first exact
            # verification outside Q(sqrt 2) -- at the tilt DS7 names exactly.
            (sys.executable, "-m", "cases.lifted_q7.verify_exact"),
            (
                sys.executable,
                "-m",
                "sqpack.cli.witness",
                "verify",
                "witnesses/known-best-n011-rational-control.yaml",
            ),
            (
                sys.executable,
                "-m",
                "devtools.check_rational_witness_independent",
                "witnesses/known-best-n011-rational-control.yaml",
            ),
            (
                sys.executable,
                "-m",
                "sqpack.cli.witness",
                "verify",
                "witnesses/schadt-n029-2025-rational.yaml",
            ),
            (
                sys.executable,
                "-m",
                "devtools.check_rational_witness_independent",
                "witnesses/schadt-n029-2025-rational.yaml",
            ),
        ),
    )
    _require_text(
        output,
        "known-best n=11 rational control check passed",
        "VALID: 11 squares, 55 pairs tested",
        "14 separated with zero gap, 41 strictly",
        "20 corner coordinates exactly on the boundary",
        "P(s) == 0 for the published degree-8 polynomial: True",
        "s = 3.87708359002281417730789706010096",
        "VALID: 5 squares, 10 pairs tested",
        "VALID: 10 squares, 45 pairs tested",
        "VERIFIED\n  id: W-known-best-n011-rational",
        "VERIFIED: 11 squares, 55 pairs",
        "VERIFIED\n  id: W-schadt-n029-2025-decimal-rational",
        "VERIFIED: 29 squares, 406 pairs",
    )
    return output


def _verifier_limits(context: Context) -> str:
    output = _module(context, "cases.trump11.verifier_limits")
    _require_text(output, "delta = 1e-100  REJECT", "tol=1e-09")
    if re.search(r"delta = 1e-[0-9]+ +accept", output):
        raise StepFailureError("the exact verifier accepted a perturbed packing")
    line = next((value for value in output.splitlines() if value.startswith("  tol=1e-09")), "")
    _require_text(line, "1e-12: accept")
    return output


def _frontier_corpus(context: Context) -> str:
    files = sorted((PROJECT_ROOT / "frontier").glob("n-*.md"))
    if len(files) != 100:
        raise StepFailureError(f"expected 100 frontier artifacts, found {len(files)}")
    values: set[int] = set()
    formal_open = 0
    reported_open = 0
    nagamochi_count = 0
    for path in files:
        data = safe_load(path.read_text(encoding="utf-8").split("---\n")[1])
        softschema = data["softschema"]
        packing = data["packing"]
        if softschema != {
            "contract": "packing.squares:SquarePackingCase/v2",
            "schema": "square-packing-case.schema.yaml",
            "envelope": "packing",
            "status": "enforced",
        }:
            raise StepFailureError(
                f"unexpected softschema declaration: {path.relative_to(PROJECT_ROOT)}"
            )
        n = int(path.stem.split("-")[1])
        if n != packing["n"] or packing["status"] not in {"proved", "open"}:
            raise StepFailureError(
                f"inconsistent frontier identity: {path.relative_to(PROJECT_ROOT)}"
            )
        if packing["status"] == "open":
            formal_open += 1
            nagamochi_count += (
                "E-nagamochi-lower" in packing["verified_lower_bound"]["evidence"]
            )
        reported_open += packing["reported_status"] == "open"
        values.add(n)
    expected_values = set(range(1, 101))
    if values != expected_values:
        missing = sorted(expected_values - values)
        extra = sorted(values - expected_values)
        raise StepFailureError(
            f"frontier n coverage drifted: missing {missing}, unexpected {extra}"
        )
    # 61 since 2026-08-31: the green17 certificate took over the verified lower
    # bounds at n = 17 and n = 18, so two open cases stopped citing Nagamochi.
    # 60 since 2026-09-03: the adopted Massaccesi certificate took over the verified
    # lower bound at n = 19 by monotonicity (T-016), so a third case stopped citing it.
    # 58 since 2026-09-04: T-020's certificate at 24/5 took n = 20 and n = 21 off the
    # closed form, the first bounds specific to either size. This constant is a
    # tripwire, not a derivation -- check_nagamochi_bounds reads the count from the
    # record; this line exists so the record cannot move without someone saying so.
    if (formal_open, reported_open, nagamochi_count) != (65, 65, 58):
        raise StepFailureError(
            "frontier corpus counts drifted: expected 65 formal-open, 65 reported-open, "
            f"and 58 Nagamochi-bounded; observed {formal_open}, {reported_open}, "
            f"and {nagamochi_count}"
        )

    kingbird = _module(
        context,
        "cases.kingbird29.verify_svg",
        "resources/papers/kingbird-square-29-provenance.svg",
    )
    result = json.loads(kingbird)
    if not (
        result["packing"]["valid"]
        and result["packing"]["n"] == 29
        and result["packing"]["pairs_tested"] == 406
        and result["orientation_class_count"] == 6
        and [item["count"] for item in result["orientation_classes"]] == [15, 1, 9, 1, 2, 1]
        and all(result["selftests"].values())
    ):
        raise StepFailureError("the Kingbird n=29 replay contract changed")
    return (
        f"  100 artifacts, n = 1..100; formal lane: {100 - formal_open} proved, "
        f"{formal_open} open\n"
        f"  reported lane: {100 - reported_open} proved, {reported_open} open; "
        f"{nagamochi_count} formal-open cases use Nagamochi\n"
        "  n=29 source numerically checked: 29 squares, 406 pairs, six classes\n"
        "  named-source reconciliation is enforced by soft-schema validation"
    )


def _generated_tables(context: Context) -> str:
    return _commands(
        context,
        (
            (sys.executable, "-m", "devtools.render_research_tables", "--check"),
            (sys.executable, "-m", "devtools.render_certificate_reach", "--check"),
        ),
    )


def _strategy_catalogues(_context: Context) -> str:
    lines: list[str] = []
    for kind, field_name, expected in (("search", "outcome", 20), ("proof", "status", 30)):
        path = PROJECT_ROOT / "frontier" / f"{kind}-strategies.yaml"
        data = safe_load(path.read_text(encoding="utf-8"))
        strategies = data["strategies"]
        observed_kind = data.get("kind")
        if observed_kind != kind:
            raise StepFailureError(
                f"{kind} catalogue: expected kind {kind!r}, observed {observed_kind!r}"
            )
        declared_count = data.get("count")
        observed_count = len(strategies)
        if declared_count != observed_count or observed_count != expected:
            raise StepFailureError(
                f"{kind} catalogue: expected {expected} strategies; "
                f"declared {declared_count!r}, observed {observed_count} records"
            )
        observed_ids = [item["id"] for item in strategies]
        expected_ids = list(range(1, expected + 1))
        if observed_ids != expected_ids:
            raise StepFailureError(
                f"{kind} catalogue: expected ids {expected_ids}, observed {observed_ids}"
            )
        families = set(data["families"])
        for item in strategies:
            required = (item[field_name], item["name"], item["mechanism"], item["note"])
            if item["family"] not in families or not all(required):
                raise StepFailureError(f"{kind} #{item['id']}: invalid family or empty field")
        lines.append(
            f"  {kind}: {expected} strategies, {len(families)} families, all fields populated"
        )
    return "\n".join(lines)


def _defect_log(context: Context) -> str:
    return _commands(
        context,
        (
            (sys.executable, "-m", "devtools.render_defects", "--check"),
            (sys.executable, "-m", "devtools.check_generated_markdown"),
        ),
    )


def _skills_mirrored(context: Context) -> str:
    make = shutil.which("make", path=context.environment.get("PATH"))
    if make is None:
        raise StepSkippedError("make is unavailable; skill mirrors were not compared")
    return _run(context, (make, "--no-print-directory", "skills-check"), cwd=REPOSITORY_ROOT)


def _synopsis(context: Context) -> str:
    return _commands(
        context,
        (
            (sys.executable, "-m", "devtools.check_documentation"),
            (sys.executable, "-m", "devtools.check_synopsis"),
        ),
    )


def _readme(context: Context) -> str:
    return _module(context, "devtools.check_readme")


def _operating_rules(context: Context) -> str:
    return _module(context, "devtools.render_operating_rules", "--check")


def _agenda_map(context: Context) -> str:
    return _module(context, "devtools.render_agenda_map", "--check")


def _n5_identity_pair(context: Context) -> str:
    # Re-runs the six-seed n=5 census, so ~28s: too slow for --edit and too important to
    # leave unreplayed. D-034's pair is the only prospective control the identity work
    # has, and a census that stopped reproducing it would invalidate the control without
    # changing any file.
    return _module(context, "devtools.build_n5_identity_pair", "--check")


def _exact_construction_price(context: Context) -> str:
    """The decimal route still reproduces neither known contact structure.

    38s, and `broad` for depth rather than breadth: the measurement is a sixty-floor sweep
    at four sizes, and narrowing it would narrow the finding. Kept out of `--edit` for the
    cost and in `--fast` because what it guards is a typed refusal -- if the route ever
    started reproducing `n = 11`'s exact 14-and-20, that would be news either way.
    """
    return _module(context, "devtools.price_exact_construction", "--check")


def _work_accounting(context: Context) -> str:
    """The three work meters still agree on exactly one unit, and no more.

    Runs an LP on a literal three-square structural cell to observe the solver's own
    counters, which is why this is not a records-only check: the number it compares against
    the structural plan has to be measured rather than read.
    """
    return _module(context, "devtools.audit_work_accounting", "--check")


def _assembly_coverage(context: Context) -> str:
    """Every record at `n <= 30` still carries its certificate or its typed limitation.

    Cheap, because it reads the same census the taxonomy does. The value is that the
    contract's `per_record_coverage` block names this record and this replay, so the
    contract and the corpus cannot drift into disagreeing without one of them failing.
    """
    return _module(context, "devtools.certify_assembly_coverage", "--check")


def _chunk_taxonomy(context: Context) -> str:
    """The source-stratified taxonomy still describes the corpus it was drawn from.

    2.6s, which is a third again on top of the records tier and is paid deliberately. The
    record is a generated view over the chunk census and 100 retained witnesses, and
    `D-369` measured that record drift, not mathematics, is what breaks CI -- so a view
    whose drift check sits outside the pre-push tier is a view that drifts.
    """
    return _module(context, "devtools.census_chunk_taxonomy", "--check")


def _session_clocks(context: Context) -> str:
    """No session may declare a start time it could not have read (`D-358`).

    Refuses only what cannot be true, so a delegated lane whose phase legitimately starts
    before the one above it in the file passes with a printed note. The `--review` output
    is the instrument `OR-6` needs: elapsed against budget for every phase of the newest
    session, derived from the record's own successive timestamps.
    """
    output = _module(context, "devtools.check_session_clocks", "--review")
    _require_text(output, "every declared start is one that could have been read")
    return output


def _n5_rigidity_certificates(context: Context) -> str:
    # 0.8s including the scipy import, because the linear programs are 20 rows wide. The
    # certificates are proposed in floating point and re-checked exactly in `Q(sqrt 2)`, so
    # what this replays is the exact check and not the search that proposed it.
    return _module(context, "devtools.assess_n5_rigidity", "--check")


def _session_close(context: Context) -> str:
    # Sub-second: frontmatter plus the span of each rollup. Records tier, and distinct from
    # `_session_rollups` in what it adds -- the reverse direction. That checker asks whether
    # every declared rollup exists; this one also reports rollups no session declares, which
    # is how a measured cost goes unattributed without anything noticing.
    return _module(context, "devtools.close_session", "--check")


def _pr_rollup(context: Context) -> str:
    # Sub-second: it re-reads the rollups the step above already parses and renders each
    # branch shape without printing. Records tier because this block goes on every pull
    # request, so a renderer that raises on a branch with no exclusive log breaks the one
    # place a reviewer sees what the work cost.
    return _module(context, "devtools.render_pr_rollup", "--check")


def _gate_budgets(context: Context) -> str:
    # Sub-second: it reads one register and compares two sets. Records tier because it
    # checks the declaration rather than the clock -- that every tier this command can
    # select carries a ceiling, and that no ceiling has drifted more than the declared
    # headroom above the cost recorded for its tier. The run's own wall is checked
    # separately, by `gate_budgets.judge`, at the end of every whole-tier run.
    output = _module(context, "devtools.check_gate_budgets")
    _require_text(output, "gate budget declaration passed")
    return output


def _control_anchors(context: Context) -> str:
    # Sub-second: it resolves 150 anchors by string containment, running no mutation and no
    # subprocess. Records tier because a control whose anchor has stopped matching is not
    # testing anything, and the suite that would say so runs only in the full gate -- which
    # a pull request never reaches (D-403).
    return _module(context, "devtools.check_control_anchors")


def _nagamochi_bounds(context: Context) -> str:
    # Sub-second: a hundred frontmatter blocks and one closed-form per case. Records tier
    # because it checks the arithmetic of a citation the rest of the register leans on --
    # 88 of the hundred verified lower bounds come from this one external proof, and
    # nothing previously re-derived any of them.
    return _module(context, "devtools.check_nagamochi_bounds")


def _evidence_inventory(context: Context) -> str:
    # Sub-second: it reads one register and re-renders a table. Records tier because it is
    # a generated view of the record, and a generated view that has drifted from its source
    # is the thing this repository logs defects about most often.
    return _module(context, "devtools.render_evidence_inventory", "--check")


def _results_register(context: Context) -> str:
    # Sub-second: re-derives every declared V and C rung from the cited evidence atoms
    # per epistemics.md and refuses unsupported or unexplained-understated declarations,
    # then checks the generated RESULTS.md view against the register.
    first = _module(context, "devtools.check_results")
    second = _module(context, "devtools.render_results", "--check")
    return f"{first}\n{second}"


def _results_headline(context: Context) -> str:
    # Sub-second: one register, one document, one rubric. Records tier because it checks
    # presentation of the record -- that every registered result reaches the section a
    # reader arrives at, in the register's own order. Agenda 016 scored three results and
    # published a synopsis naming none of them, which no other step here would notice.
    return _module(context, "devtools.render_results_headline", "--check")


def _certificate_citations(context: Context) -> str:
    # Sub-second: it ast-parses five modules and reads a hundred frontmatter blocks. Records
    # tier because it checks the record, not the mathematics -- that every exact certificate
    # this repository holds is named by the frontier record it bears on. See D-398, where
    # three records declared a mathematics blocker while their certificate ran in this gate.
    return _module(context, "devtools.check_certificate_citations")


def _rung_figures(context: Context) -> str:
    # Sub-second: it sums a few dozen certificate atoms in exact Fraction arithmetic and
    # regex-scans results.yaml, evidence.yaml, and defects.yaml. Records tier because it
    # checks the record against the artifact, not the mathematics of either -- D-439 found
    # three durable statements describing a rung the ladder had already moved past, every
    # figure exact and real, each simply about the wrong file.
    return _module(context, "devtools.check_rung_figures")


def _case_prose(context: Context) -> str:
    # Sub-second: it regex-scans a hundred case bodies against their own front matter and
    # reuses check_rung_figures's exact-arithmetic rule. Records tier because it checks the
    # record against itself, not the mathematics -- n-017, n-018, and n-019 all stated a
    # verified lower bound in prose that the front matter above it had already moved past,
    # and stayed that way for six hours; check_rung_figures never reads a case body.
    return _module(context, "devtools.check_case_prose")


def _session_rollups(context: Context) -> str:
    # Sub-second: it reads frontmatter and stats files. Records-tier because that is exactly
    # what it checks -- that a terminal session names what it cost and the record is there.
    return _module(context, "devtools.check_session_rollups")


def _session_gate(context: Context) -> str:
    """A terminal session names the gate run that certified its handover (`OR-13`).

    Sub-second: frontmatter, one regex, and two `git` calls per declaration. Records tier
    and therefore on every pull request, which is the point -- `OR-13` says every fast
    check runs in CI, and a rule about the gate that only the gate's slow surface enforces
    is a rule a branch can be green against for its whole life.

    The commit is the load-bearing half. Forty-seven of the first eighty-six terminal
    records mention a gate in `checks` and seven name any commit, so what the corpus mostly
    holds is `full gate: passed` in longer words -- a claim about a tree nobody can now
    identify. Ancestry is checked against the graph and, where the checkout cannot answer,
    reported as uncheckable rather than assumed false (`conventions.md` §6).
    """
    output = _module(context, "devtools.check_session_gate")
    _require_text(output, "name a full-gate run on a commit in their history")
    return output


def _gobel_family(context: Context) -> str:
    # About five seconds: the family is twelve pairs and only the four whose side matches a
    # retained best known are built and verified exactly, the largest being n = 89 at 3916
    # pairs. Cheap enough for the records tier, and it belongs there -- what it checks is
    # that the frontier still says what it said when the coverage was measured.
    return _module(context, "devtools.price_gobel_family", "--check")


def _n40_rigidity_bracket(context: Context) -> str:
    # 4m57s measured 2026-08-30, on a full gate of about sixteen minutes. It re-derives
    # n = 40's whole assessment: the witness and its second-order refusal, six retained
    # rays and theirs, a sweep of the null space, and 144 Farkas searches over the frame.
    # Neither `fast` nor `records` for that reason -- it re-derives the mathematics rather
    # than reading the record, and a three-minute check in the six-second records tier
    # would make that tier one people skip (D-369).
    #
    # It was cut once already: the intersecting-assessor section went from all 120
    # coordinates to the block's 48, which is where the claim lives, saving ninety seconds
    # for a number that said nothing the forty-eight did not. It has since grown again, to
    # 4m57s, with the frame proof, the block-rotation relations and the cone bound.
    #
    # That is a third of the full gate for one step and `D-369` is the standing warning
    # about exactly this. It is left in because every part of it is a claim the record
    # makes and nothing here is a duplicate of anything else; the honest alternative, if
    # the cost bites, is to move the whole step behind a flag rather than to thin the
    # checks until they stop covering what is asserted.
    #
    # The third step the pull-request tier does not carry, and the only one of the three
    # that would have fit: 221.36s on CI. What it re-derives is mathematics, not a
    # record, and a pull request that can change the answer has edited the assessor,
    # which `--since` selects this step for. See the note above `STEPS`.
    return _module(context, "devtools.assess_n40_rigidity", "--check")


def _differential(context: Context) -> str:
    if not ENGINE.is_file():
        raise StepSkippedError(
            "sqsearch binary is absent; differential geometry was not checked"
        )
    return _module(context, "devtools.check_search_differential", "20000")


def _run_returncode(context: Context, command: Sequence[str]) -> int:
    """Run a quiet command through the same bounded process-group path as _run."""
    if os.name == "nt":
        raise StepFailureError(
            "bounded validation subprocesses require verified process-tree cleanup; "
            "Windows support is not yet implemented"
        )
    process = subprocess.Popen(
        list(command),
        cwd=PROJECT_ROOT,
        env=context.environment,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        text=True,
        start_new_session=True,
    )
    try:
        context.processes.register(process.pid)
    except StepFailureError:
        try:
            process.wait(timeout=PROCESS_TERMINATION_GRACE_SECONDS)
        except subprocess.TimeoutExpired as error:
            raise StepFailureError(
                "rejected validation subprocess did not exit after SIGKILL"
            ) from error
        raise
    try:
        process.wait(timeout=context.timeout_seconds)
    except subprocess.TimeoutExpired:
        _stop_process_group(process)
        rendered = " ".join(command)
        raise StepFailureError(
            f"command timed out after {context.timeout_seconds:g} seconds: {rendered}"
        ) from None
    except BaseException:
        _stop_process_group(process)
        raise
    finally:
        context.processes.discard(process.pid)
    return process.returncode


def _commit_state(context: Context, commit: str) -> CommitState:
    available = _run_returncode(
        context,
        ("git", "cat-file", "-e", f"{commit}^{{commit}}"),
    )
    if available != 0:
        return "missing"
    ancestry = _run_returncode(
        context,
        ("git", "merge-base", "--is-ancestor", commit, "HEAD"),
    )
    if ancestry not in {0, 1}:
        raise StepFailureError(
            f"git could not compare engine commit {commit} with HEAD (exit {ancestry})"
        )
    return "reachable" if ancestry == 0 else "orphaned"


def _provenance_line(name: str, commit: str, text: str, state: CommitState) -> str:
    annotation = text.split("## Annotation", 1)[1] if "## Annotation" in text else ""
    loss_is_annotated = commit in annotation and "unreachable" in annotation.lower()
    if state == "reachable":
        return f"  ok          {name} -> {commit}"
    if state == "missing":
        if loss_is_annotated:
            return f"  UNAVAILABLE {name} -> {commit} (historical loss is annotated)"
        raise StepFailureError(
            f"{name}: engine commit {commit} is unavailable in local history; "
            "fetch complete history (`git fetch --unshallow` for a shallow clone, "
            "otherwise `git fetch --all`) and rerun"
        )
    if not loss_is_annotated:
        raise StepFailureError(f"{name}: orphaned engine commit has no explicit annotation")
    return f"  ORPHANED    {name} -> {commit} (historical loss is annotated)"


def _provenance(context: Context) -> str:
    lines: list[str] = []
    checked = 0
    declared = 0
    paths = sorted((PROJECT_ROOT / "campaign/series").glob("*/experiments/*.md"))
    for path in paths:
        text = path.read_text(encoding="utf-8")
        matches = re.findall(r"^[ \t]*engine_commit:[ \t]*(.*)$", text, re.MULTILINE)
        declared += len(matches)
        if not matches:
            continue
        raw = matches[0].split("#", 1)[0]
        commit = raw.strip().strip("'\"").strip()
        if re.fullmatch(r"[0-9a-fA-F]{7,40}", commit) is None:
            raise StepFailureError(f"invalid {path.name} engine_commit: {raw}")
        checked += 1
        state = _commit_state(context, commit)
        lines.append(_provenance_line(path.name, commit, text, state))
    if checked != declared:
        raise StepFailureError(f"checked {checked} of {declared} declared engine commits")
    lines.append(f"  checked all {checked} declared engine commits")
    return "\n".join(lines)


def _campaign_record(context: Context) -> str:
    return _commands(
        context,
        (
            (sys.executable, "-m", "sqpack.campaign.ledger", "check"),
            # A phase's validation_command is its declared falsifier. Nothing checked
            # that the command could run, so two phases once carried a flag that exits
            # 2 (think-ldy8).
            (sys.executable, "-m", "devtools.check_declared_commands"),
        ),
    )


# Attribution groups for `Step.touches`, deliberately generous. A pattern that is too
# wide costs a step that need not have run; one that is too narrow costs a verdict nobody
# checked, and only the second is a soundness failure.
#
# `fnmatch` is not a path glob -- its `*` crosses separators -- so `packing/src/sqpack/*`
# covers the whole subtree, and every pattern here is repo-relative.
_TOOLCHAIN = ("packing/pyproject.toml", "packing/uv.lock", "packing/.python-version")
# `devtools/__init__.py` is imported by every devtools-invoking step and is covered by no
# per-file devtools pattern, so it belongs with the shared core rather than repeated.
_CORE = ("packing/src/sqpack/*", "packing/devtools/__init__.py", *_TOOLCHAIN)
_ENGINE_SRC = ("packing/sqsearch/*",)
_ANY_PYTHON = ("*.py", "*.pyi", *_TOOLCHAIN)
_CASES = ("packing/cases/*",)
# The retained replay archives. Whole subtree, not the named files: several steps
# discover which archives to replay by globbing, so adding one changes what runs.
_RESULTS = ("packing/campaign/series/*",)

# What `fast` means since 2026-09-05: the tier a pull request runs, and therefore the
# tier that has to hold everything a merge would otherwise be the first to check. Since
# 2026-09-06 a pull request runs it as concurrent jobs rather than one -- `--checks`,
# `--geometry`, `--suite` and `--sweeps`, a partition of this tier argued on
# `Step.sweep`, `Step.suite` and `Step.geometry` -- so the tier is unchanged and what a
# pull request waits for is its longest part rather than their sum.
#
# The three-way split was the second cut and it was taken on the two-job surface's own
# measurement (run 34010470187): `checks` 221.70s against `sweeps` 110.66s, badly
# unbalanced, and 142.43s of the longer half was one step -- `fast behavioral tests`,
# which no outer parallelism can divide because a job cannot be shorter than one step.
# Moving that step to a runner of its own does two things at once, and both are
# arithmetic: it takes the largest unit out of the `checks` queue, and it takes the lane
# from two xdist workers (`cpus - jobs + 1` at `--jobs 3`) to four (at `--jobs 1`).
#
# The fourth cut is the one after that, and it says something the first three did not.
# What was left in `checks` was 57 steps of pure outer-parallel work with no single unit
# large enough to floor it, so the obvious move was to spend the freed cpu: `--jobs 4` on
# a four-cpu runner. Run 34016999060 priced that and the answer was no. The tier came in
# at 198.22s -- 23.5s less than the three-worker job that still had the 142.43s
# behavioural lane inside it -- because saturating the runner inflated every step by
# thirty to eighty per cent: the perimeter 60.62s to 84.41s, exact verification 61.75s to
# 79.98s, the type floor 40.37s to 72.31s, the SVG renderer 41.30s to 65.36s. Four
# workers over 790 inflated worker-seconds is the same work at a worse price than three
# over 470, and it is the same lesson `_pytest_workers` already encodes as
# `cpus - jobs + 1`: size to the machine and the neighbours pay for it.
#
# So the fourth job buys cpus rather than schedule. `--checks` and `--geometry` are the
# two halves of that queue, 269.60s and 275.48s of step time on a local four-cpu reading
# of 545.08s, each on its own runner at `--jobs 3` -- eight cpus for work that had four,
# and a core of headroom on each. `Step.geometry` carries the two rules that decide which
# half a step lands in and why only one of the two jobs compiles the engine.
#
# The measurement that forced the first split, CI run at commit `30706bcb`, `--fast
# --jobs 3 --inner-jobs 1` on a four-cpu runner: 501.97s of wall over 1,100s of step time.
# Two steps were 468.11s of it. Three facts follow and all three are arithmetic rather
# than judgement:
#
#   * 1,100s of step time on four cpus cannot finish in under 275s however it is
#     scheduled, so the two-to-three-minute target is not reachable on one runner. Two
#     runners is eight cpus and a 137s floor.
#   * the tier's utilisation was 2.19 of its three workers, so the loss was not only
#     work but queueing: the four longest steps were 826s between them and had to share.
#   * a job cannot be shorter than its longest step, which is why the composite steps
#     were split at their measured seams first. `known-best n=1..100 atlas` was nine
#     subcommands run one after another and one of them was 71 per cent of it.
#
# The contention was the second cost and it was not on the clock. Five ordinary tests
# reported between 5.47s and 6.72s against the quick lane's 5s per-test ceiling on the
# merged tier -- not because they had grown but because 468s of atlas rendering was
# running beside them on the same four cpus. Marking them was tried and is wrong: in the
# slow lane the same tests fall under the 1s marker floor, which then demands the marker
# back. They are contended, not slow, and moving the sweeps to their own runner is what
# removes the contention rather than relabelling it.
# Twenty-four of the sixty-one steps ran only after merge until this date, and two
# defects reached main through that gap in one afternoon and sat there red for nine
# hours -- D-455 caught by `deterministic SVG rendering` and D-456 by the exhaustive
# tier, neither of them reachable from any pull request (think-k4fb).
#
# Twenty-one of the twenty-four are promoted, and what makes that affordable is that a
# tier does not cost the sum of its steps. At `--jobs 2` one worker is inside the
# behavioural suite for the whole run, so the tier costs
# `max(that suite, everything else run serially on the other worker)`. The measurements,
# local at 4 cores and one step at a time under `--only`, with CI about 1.3x slower
# (`type floor` is 45.51s there against 35.62s here):
#
#   115s  the fast tier as it stood, minus the suite
#   538s  the twenty-one promoted steps, one at a time under `--only`
#   663s  the promoted tier minus the suite, measured whole rather than summed
#         (`--fast --skip "fast behavioral tests" --jobs 2 --inner-jobs 1`, 334s of wall
#         over two workers), which is the 653s the two rows above predict
#  1034s  the suite itself -- not a new reading, but the one already recorded beside
#         `FAST_SUITE_BUDGET_SECONDS` below, and about 1100s of CI's twenty-minute job
#
# So the second worker goes from 115s to 663s of serial work, or about 860s scaled to
# CI, and stays under the suite that sets the wall time. The pull-request job takes what
# it took. The margin is about 240s of CI time and it is the number to re-measure before
# promoting a twenty-second step: past it the tier stops being priced by the suite and
# starts being priced by this queue.
#
# `_run_selected` submits the budgeted steps first for this reason and no other. The
# suite is declared fifteenth and eleven of the promoted steps are declared ahead of it,
# including the three sweeps that are half the promoted total; in submission order the
# suite would have started only once those had cleared, which would have spent on the
# scheduler exactly what the arithmetic above saves.
#
# Three are deferred, each on its own measurement rather than on a rule:
#
# - `exhaustive exact behavioral tests`, 1943s on CI: the suite it would have to fit
#   beside is not that large, so it would set the tier's wall time itself. It has its
#   own workflow job as of think-tr2z, which is what a step of that size needs -- its
#   own budget and its own verdict rather than a larger share of someone else's.
# - `negative controls`, 544s on CI: the same arithmetic, the other side of the line. It
#   would put the second worker at about 1400s against the suite's 1100s, so the pull
#   request would start waiting on the controls instead of on its own tests and take
#   about five minutes longer. It clones the tree per worker for 148 declared mutations,
#   which makes it the one surface here that really is a second test suite.
# - `n=40 rigidity bracket still reproduces`, 221s on CI: this one fits, and only just --
#   it is about the whole remaining margin, which would leave the tier priced by the
#   queue rather than by the suite and the next promotion with nothing to spend. It also
#   re-derives mathematics rather than checking a record, no pull request moves its
#   answer without editing `assess_n40_rigidity.py` or the assessor beneath it, and
#   `--since` already selects it for exactly those changes.
#
# `test_the_pull_request_surface_defers_only_what_was_measured` is where a fourth
# deferral has to be argued. `fast` defaults to False, so without that test this gap
# reopens quietly the next time a step is added.
STEPS: tuple[Step, ...] = (
    # 47.14s, and the reason every engine-dependent step below is `broad` as well as
    # `fast`: selecting one of them builds sqsearch before any step starts, and that
    # build is serial time the edit loop should never pay. The edit tier stays Python
    # with no toolchain behind it; the pull request compiles the engine once and gets
    # the perimeter, the selftest, the differential and the Rust lint floor for it,
    # none of which any pull request checked before.
    Step(
        "soundness perimeter",
        _soundness_perimeter,
        fast=True,
        broad=True,
        needs_engine=True,
        touches=(*_CORE, *_ENGINE_SRC, "packing/devtools/check_soundness_perimeter.py"),
    ),
    Step("lint floor (ruff)", _lint_floor, fast=True, records=True, touches=_ANY_PYTHON),
    Step("type floor (basedpyright)", _type_floor, fast=True, touches=_ANY_PYTHON),
    # 9.63s.
    Step(
        "basin atlas",
        _basin_atlas,
        fast=True,
        broad=True,
        geometry=True,
        touches=(*_CORE, "packing/atlas/*", "packing/devtools/check_atlas.py"),
    ),
    # 7.89s.
    Step(
        "basin event record and replay",
        _basin_events,
        fast=True,
        broad=True,
        geometry=True,
        touches=(*_CORE, *_CASES, *_RESULTS, "packing/frontier/*"),
    ),
    # 29.35s.
    Step(
        "historical regressions",
        _historical_regressions,
        fast=True,
        broad=True,
        geometry=True,
        touches=(
            *_CORE,
            *_ENGINE_SRC,
            *_CASES,
            *_RESULTS,
            "packing/devtools/check_regressions.py",
        ),
    ),
    # 19.80s.
    Step(
        "small-n exact models and local geometry",
        _small_n,
        fast=True,
        broad=True,
        geometry=True,
        touches=(*_CORE, *_CASES, *_RESULTS, "packing/atlas/*"),
    ),
    # 26.39s, and the step D-455 was caught by -- on main, three merges and nine hours
    # after the commit that broke it, because this tier ran nowhere else.
    Step(
        "deterministic SVG rendering",
        _svg_rendering,
        fast=True,
        broad=True,
        geometry=True,
        touches=(
            *_CORE,
            "packing/atlas/*",
            "packing/devtools/*",
            "packing/cases/*",
            # It asserts facts about every Markdown file in the repository:
            # `surface_expectations` pins examples in TUTORIAL.md and SYNOPSIS.md, and
            # three checks walk `REPO.rglob("*.md")` for inline SVG targets.
            "*.md",
        ),
    ),
    # The record sweeps below are the tier's expensive half -- 598.9s of about 1,100s of
    # CI step time -- and they are on the pull-request surface anyway. They are the class
    # D-369 measured: every CI failure on that branch was a registry, a generated view or
    # a declared contract going stale, and these are what re-derives the largest of those
    # from 100 retained witnesses. A pull request that retains a witness or edits a source
    # map is exactly the change that breaks them, and before 2026-09-05 exactly the change
    # that could not find out until after the merge.
    #
    # `sweep=True` is where they run rather than whether: the pull request pays them on a
    # second runner, concurrently with everything else. What that is worth, and why it is
    # a second runner and not a wider one, is argued on `Step.sweep`.
    Step(
        "known-best n=1..100 atlas",
        _known_best_atlas,
        fast=True,
        broad=True,
        sweep=True,
        touches=(
            *_CORE,
            *_CASES,
            "packing/devtools/*",
            "packing/atlas/*",
            "packing/witnesses/*",
            "packing/frontier/*",
            "packing/resources/*",
        ),
    ),
    # Split out of the step above on 2026-09-06, and it keeps that step's attribution
    # rather than a narrower one of its own. The two halves read overlapping corners of
    # the same corpus, an over-wide pattern costs a step that need not have run while a
    # narrow one costs a verdict nobody checked, and only the second is a soundness
    # failure -- so the conservative move on a split is to give both halves the parent's
    # set and narrow later with a measurement.
    Step(
        "known-best chunk census",
        _known_best_chunk_census,
        fast=True,
        broad=True,
        sweep=True,
        touches=(
            *_CORE,
            *_CASES,
            "packing/devtools/*",
            "packing/atlas/*",
            "packing/witnesses/*",
            "packing/frontier/*",
            "packing/resources/*",
        ),
    ),
    # 0.39s locally, against 88.37s for the seed it used to share a step with. It is not
    # a sweep and does not belong on the second runner: it reads one source map.
    Step(
        "prospective n=101..324 source map",
        _prospective_source_map,
        fast=True,
        touches=(
            *_CORE,
            "packing/atlas/prospective/*",
            "packing/resources/web/*",
            "packing/devtools/map_prospective_sources.py",
        ),
    ),
    Step(
        "prospective n=101..324 safe seed",
        _prospective_atlas,
        fast=True,
        broad=True,
        sweep=True,
        touches=(
            *_CORE,
            "packing/atlas/prospective/*",
            # The generated witnesses declare a schema one level up, so the whole tree.
            "packing/witnesses/*",
            "packing/resources/web/*",
            "packing/devtools/map_prospective_sources.py",
            "packing/devtools/build_prospective_atlas.py",
        ),
    ),
    Step(
        "single-square translation escape screen",
        _translation_escape_screen,
        fast=True,
        broad=True,
        sweep=True,
        touches=(
            *_CORE,
            "packing/atlas/known-best/*",
            "packing/witnesses/*",
            "packing/devtools/screen_translation_escape.py",
        ),
    ),
    # 2.09s, so `fast` without `broad`: cheaper than several steps the edit tier already
    # carries, and the rule for `broad` is a cost argument, not a tier's habit.
    Step(
        "abstract size-five contact-scaffold atlas",
        _contact_scaffold_atlas,
        fast=True,
        touches=(
            *_CORE,
            "packing/atlas/enumerated/*",
            "packing/devtools/build_contact_scaffold_atlas.py",
        ),
    ),
    # 1268s measured uncapped at 137 controls (D-366), and the suite only grows. The
    # budget is that measurement plus room for the growth, not a number chosen to make
    # today's run pass; a control suite that doubles again should be re-argued, not
    # re-padded.
    #
    # One of the three steps the pull-request tier deliberately does not carry: 543.67s
    # on CI, which is the point at which a promoted step stops fitting beside the
    # behavioural suite and starts being the thing the job waits for. See the note above
    # `STEPS`.
    Step("negative controls", _negative_controls, budget_seconds=1800),
    # 9.76s.
    Step(
        "fixed-angle cell is an LP, rebuilt independently",
        _independent_lp,
        fast=True,
        broad=True,
        geometry=True,
        touches=(*_CORE, "packing/cases/trump11/*"),
    ),
    # 1209s measured on 2026-09-03 at 1607 passing tests, in the full gate at 13:47Z,
    # against the 900s shared cap the step had been dying on. The 1187s reading this
    # comment first cited is a floor and not the measurement: it was taken at 1533 passing
    # tests on a red tree -- 38 failures, 33 of them the four n = 17 packages an edit broke
    # and the same commit reverted -- and a test that fails does not run the rest of its
    # body. It is left named rather than deleted, because a budget argued from a number
    # nobody can find again is not an argument. Two earlier readings disagree and the
    # disagreement is left visible rather than averaged away: 880s on 2026-09-03 at 07:35Z
    # when the step still passed, and 910s reported by the W9 lane the same morning. CI
    # supplies only a floor too, because it kills the step at the cap rather than timing
    # it. The suite grew by roughly a hundred tests during that window -- the n = 5
    # rigidity instrument and the runner trust boundary -- which accounts for the direction
    # but not the whole spread; the local readings were taken with other work in flight.
    #
    # The budget is the measurement plus room for that uncertainty and for growth, not a
    # number chosen to make today's run pass. A suite that reaches this ceiling should be
    # re-argued, not re-padded, and the step still fails if it exceeds what it asked for.
    #
    # Re-measured on 2026-09-05 at 1781 passing tests, after the integer sweep
    # (d8733ad0) took the four retained certificate decisions out of the suite's critical
    # path: 1034s on four cores, with light editing in flight; CI's `validate`
    # job on the same tree ran in 996s on its two-core runner (run 33931098324). The 1800s
    # budget stands at about 1.7 times the local reading. A 2700s budget was
    # proposed on a 1791s measurement of the Fraction sweep the same day; that
    # measurement no longer describes the suite. The second half of that argument --
    # that 2700s "sits above the 1800s CI allows the job" -- was wrong and is struck:
    # the `validate` job declares no `timeout-minutes` and never has, so it inherits
    # GitHub's 360-minute default and there is no such ceiling (D-456).
    # No `budget_seconds` here either, and for a separate reason. This step carried an
    # 1800s exception to the shared 900s cap for as long as it ran every non-exhaustive
    # test; since BC-214 split the slow ones off it does not need one, and a step that no
    # longer needs an exception should not keep it -- the shared cap is the guard against
    # one hung test, and this step is now ordinary enough to live under it. What the lane
    # is allowed to *cost*, as against how long one hung subprocess may hang, is
    # `devtools/gate-budgets.yaml`.
    # `suite=True` is where this step runs rather than whether: it is the pull request's
    # third job, alone, so that `_pytest_workers` hands xdist every cpu instead of the
    # two it gets beside 57 other steps. 142.43s of the 221.70s `checks` job on CI
    # (run 34010470187) at two workers, and the longest single unit anywhere on the
    # surface. The argument for a job rather than a wider `--jobs` is on `Step.suite`.
    Step(
        "fast behavioral tests",
        _fast_tests,
        fast=True,
        broad=True,
        suite=True,
    ),
    # The half of the behavioural suite that costs the wall. It is the same tests under
    # the same runner, selected by the `slow` marker instead of against it, and it runs
    # in the full gate -- so nothing the pull-request surface stopped running stopped
    # running. `SLOW_TESTS` and `QUICK_TESTS` are complements within the non-exhaustive
    # suite, which is what makes that claim checkable rather than asserted.
    # It takes the whole non-exhaustive suite's budget rather than a smaller one argued
    # from today's membership: the lane is defined by a ceiling, so its membership grows
    # whenever a test crosses that ceiling, and a budget pinned to today's members would
    # have to be re-argued every time the rule admits one. Its upper bound is the suite it
    # is a subset of.
    Step(
        "slow behavioral tests",
        _slow_tests,
        budget_seconds=FAST_SUITE_BUDGET_SECONDS,
    ),
    # 1943.05s on CI, and since 2026-09-05 the only step its workflow job runs: the
    # `exhaustive` job selects it with `--only` and every other job excludes it with
    # `--skip`, so it reports its own verdict against its own budget instead of deciding
    # whether sixty other steps are reported at all (think-tr2z). It is also the one
    # step whose cost rules it out of the pull-request tier outright.
    Step(
        "exhaustive exact behavioral tests",
        _exhaustive_exact_tests,
        budget_seconds=EXHAUSTIVE_SUITE_BUDGET_SECONDS,
    ),
    Step(
        "bead tree",
        _bead_tree,
        fast=True,
        records=True,
        # The bead data lives in a sync worktree, not the tracked tree, so a bead-only
        # change produces no changed path at all -- which selects the whole gate.
        touches=(*_CORE, ".tbd/*", "packing/devtools/check_bead_tree.py"),
    ),
    # 0.51s on the fast path, which is what runs without `--deep`.
    Step(
        "golden basin maps (proved cases, checked against mathematics)",
        _golden_basins,
        fast=True,
        touches=(
            *_CORE,
            *_ENGINE_SRC,
            "packing/golden/*",
            "packing/frontier/*",
            "packing/devtools/check_golden_basins.py",
        ),
    ),
    # 4.95s.
    Step(
        "basin identity",
        _canonical_identity,
        fast=True,
        touches=(
            *_CORE,
            "packing/cases/trump11/*",
            *_RESULTS,
            "packing/devtools/check_canonical.py",
        ),
    ),
    Step("soft-schema validation", _schemas, fast=True, records=True),
    Step(
        "derivation (needs sympy)",
        _derivation,
        fast=True,
        touches=(*_CORE, "packing/cases/trump11/*"),
    ),
    # 2.19s and 14.94s, both `broad` for the toolchain rather than for their own cost:
    # the first needs the built engine and the second runs clippy and rustfmt. Until
    # 2026-09-05 no pull request compiled this crate at all, so a Rust change was linted
    # and selftested for the first time after it had merged.
    Step(
        "search engine (sqsearch)",
        _search_engine,
        fast=True,
        broad=True,
        needs_engine=True,
        touches=_ENGINE_SRC,
    ),
    Step("lint floor (rust)", _rust_quality, fast=True, broad=True, touches=_ENGINE_SRC),
    # 13.82s.
    Step(
        "Trump exact branchwise linearized cones",
        _trump_cones,
        fast=True,
        broad=True,
        geometry=True,
        touches=(*_CORE, "packing/cases/trump11/*", *_RESULTS),
    ),
    # 0.49s and 0.34s: two replays of a retained certificate, cheap enough for the edit
    # tier on the same rule as the scaffold atlas above.
    Step(
        "H-041 Stromquist repaired-cover exact certificate",
        _stromquist_repair,
        fast=True,
        touches=(
            *_CORE,
            "packing/cases/stromquist/*",
            *_RESULTS,
            "packing/resources/papers/*",
        ),
    ),
    Step(
        "H-010 Stromquist printed-cover exact rejection",
        _stromquist_rejection,
        fast=True,
        touches=(
            *_CORE,
            "packing/cases/stromquist/*",
            *_RESULTS,
            "packing/resources/papers/*",
        ),
    ),
    Step(
        "exact verification",
        _exact_verification,
        fast=True,
        touches=(
            *_CORE,
            *_CASES,
            "packing/witnesses/*",
            "packing/frontier/*",
            "packing/devtools/check_basic_bounds.py",
            "packing/devtools/generate_known_best_n011_rational_control.py",
            "packing/devtools/check_rational_witness_independent.py",
        ),
    ),
    Step(
        "verifier perturbation limits",
        _verifier_limits,
        fast=True,
        touches=(*_CORE, "packing/cases/trump11/*"),
    ),
    # D-355's measured case: a two-file edit to the rigidity assessor was verified with a
    # 979.79s full gate, and these three are what such an edit can reach.
    #
    # 0.53s: a hundred frontmatter blocks and one replay of the n=29 source.
    Step(
        "frontier corpus",
        _frontier_corpus,
        fast=True,
        touches=(
            *_CORE,
            "packing/frontier/*",
            "packing/cases/kingbird29/*",
            "packing/resources/papers/*",
        ),
    ),
    Step(
        "frontier rigidity assessed here",
        _frontier_rigidity,
        fast=True,
        touches=(
            *_CORE,
            "packing/frontier/*",
            "packing/devtools/assess_frontier_rigidity.py",
            # `SCREEN` is atlas/known-best/translation-escape-screen.json, and the pinned
            # rigid/not-rigid/undetermined counts are exactly what changing it moves.
            "packing/atlas/known-best/*",
        ),
    ),
    Step(
        "generated tables in sync with frontier/",
        _generated_tables,
        fast=True,
        records=True,
        touches=(
            *_CORE,
            "packing/frontier/*",
            "packing/devtools/render_research_tables.py",
            "packing/devtools/render_certificate_reach.py",
            "packing/src/sqpack/fractional/certificate.py",
            # `MAIN` is the n=11 research report, read and compared cell by cell; the
            # step exists to catch a hand-edited table in exactly that file.
            "docs/*",
        ),
    ),
    Step(
        "strategy catalogues",
        _strategy_catalogues,
        fast=True,
        records=True,
        touches=(*_CORE, "packing/frontier/*"),
    ),
    Step(
        "defect log",
        _defect_log,
        fast=True,
        records=True,
        touches=(
            "packing/defects.yaml",
            "packing/defects.schema.yaml",
            "defects.md",
            *_CORE,
            "packing/devtools/render_defects.py",
            "packing/devtools/check_generated_markdown.py",
            ".flowmarkignore",
            "*.md",
        ),
    ),
    Step(
        "skills mirrored between .agents and .claude",
        _skills_mirrored,
        fast=True,
        records=True,
        # The mirrored list is a Make variable, so the Makefile is part of the contract.
        touches=("Makefile", ".agents/*", ".claude/*"),
    ),
    Step("synopsis agrees with the artifacts", _synopsis, fast=True, records=True),
    Step("README agrees with the directory", _readme, fast=True, records=True),
    Step(
        "AGENTS.md mirrors the operating rules",
        _operating_rules,
        fast=True,
        records=True,
        touches=(
            "AGENTS.md",
            "CLAUDE.md",
            "operating-rules.md",
            "packing/devtools/render_operating_rules.py",
        ),
    ),
    Step(
        "agenda map agrees with the agendas",
        _agenda_map,
        fast=True,
        records=True,
        touches=(
            "packing/campaign/agendas/*",
            "packing/campaign/agenda-map.md",
            "packing/campaign/schemas/agenda.schema.yaml",
            "packing/devtools/render_agenda_map.py",
            *_CORE,
        ),
    ),
    # 23.54s, so it stays out of `--edit`. That used to follow from `fast=False` alone --
    # `_select_steps` filters to the fast steps before `broad` is consulted, so the flag
    # was once set here and did nothing. Now that the step is in the pull-request tier the
    # flag is what keeps it out of the edit loop, which is the job it was written for.
    Step(
        "D-034's n=5 identity pair still reproduces",
        _n5_identity_pair,
        fast=True,
        broad=True,
        geometry=True,
        touches=(
            *_CORE,
            "packing/devtools/build_n5_identity_pair.py",
            "packing/devtools/check_golden_basins.py",
            "packing/devtools/check_soundness_perimeter.py",
            "packing/campaign/series/*/results/bc-083-n5-identity-pair.json",
        ),
    ),
    Step(
        "the decimal route still cannot price an exact pose",
        _exact_construction_price,
        fast=True,
        broad=True,
        geometry=True,
        touches=(
            *_CORE,
            "packing/witnesses/*",
            "packing/atlas/known-best/contact-structures.json",
            "packing/devtools/price_exact_construction.py",
            "packing/campaign/series/*/results/bc-049-exact-construction-price.json",
        ),
    ),
    Step(
        "work accounting agrees on one unit",
        _work_accounting,
        fast=True,
        records=True,
        touches=(
            *_CORE,
            "packing/atlas/known-best/contact-full-cell-control.json",
            "packing/devtools/audit_work_accounting.py",
            "packing/campaign/series/*/results/bc-017-work-accounting.json",
        ),
    ),
    Step(
        "assembly coverage agrees with the contract",
        _assembly_coverage,
        fast=True,
        records=True,
        touches=(
            *_CORE,
            "packing/atlas/known-best/chunk-components.json",
            "packing/atlas/known-best/contact-assembly-grammar.yaml",
            "packing/atlas/known-best/manifest.json",
            "packing/witnesses/*",
            "packing/devtools/certify_assembly_coverage.py",
            "packing/devtools/census_chunk_taxonomy.py",
            "packing/campaign/series/*/results/bc-019-assembly-coverage.json",
        ),
    ),
    Step(
        "chunk taxonomy agrees with the corpus",
        _chunk_taxonomy,
        fast=True,
        records=True,
        touches=(
            *_CORE,
            "packing/atlas/known-best/chunk-components.json",
            "packing/atlas/known-best/manifest.json",
            "packing/witnesses/*",
            "packing/devtools/census_chunk_taxonomy.py",
            "packing/campaign/series/*/results/bc-024-chunk-taxonomy.json",
        ),
    ),
    Step(
        "session clocks are readable",
        _session_clocks,
        fast=True,
        records=True,
        touches=(
            *_CORE,
            "packing/campaign/agent-sessions/*",
            "packing/campaign/schemas/agent-session.schema.yaml",
            "packing/devtools/check_session_clocks.py",
        ),
    ),
    Step(
        "n=5 rigidity certificates still verify",
        _n5_rigidity_certificates,
        fast=True,
        records=True,
        touches=(
            *_CORE,
            "packing/devtools/assess_n5_rigidity.py",
            *_CASES,
            "packing/campaign/series/*/results/bc-049-n5-rigidity-certificates.json",
        ),
    ),
    Step(
        "every session's cost is attributed",
        _session_close,
        fast=True,
        records=True,
        touches=(
            *_CORE,
            "packing/devtools/close_session.py",
            "packing/devtools/codex_task_tree_delta.py",
            "packing/campaign/agent-sessions/*.md",
            "packing/campaign/resource-usage/*.yaml",
            "packing/campaign/schemas/codex-task-tree-delta.schema.yaml",
            "packing/campaign/schemas/session-close-report.schema.yaml",
            # The step now also checks the reader-facing view spliced into the synopsis,
            # so editing that section has to be able to fail it.
            "SYNOPSIS.md",
        ),
    ),
    Step(
        "the branch cost rollup renders",
        _pr_rollup,
        fast=True,
        records=True,
        touches=(
            *_CORE,
            "packing/devtools/render_pr_rollup.py",
            "packing/devtools/codex_task_tree_delta.py",
            "packing/campaign/agent-sessions/*.md",
            "packing/campaign/resource-usage/*.yaml",
            "packing/campaign/schemas/codex-task-tree-delta.schema.yaml",
        ),
    ),
    Step(
        "control anchors still resolve",
        _control_anchors,
        fast=True,
        records=True,
        touches=(*_CORE, "packing/devtools/controls.yaml", "packing/devtools/*.py"),
    ),
    Step(
        "tier ceilings are declared and not slack",
        _gate_budgets,
        fast=True,
        records=True,
        touches=(
            *_CORE,
            "packing/devtools/check_gate_budgets.py",
            "packing/devtools/gate-budgets.yaml",
            # The step also checks that the guide still names every tier, so editing the
            # guide has to be able to fail it.
            "development.md",
        ),
    ),
    Step(
        "the borrowed lower bounds re-derive",
        _nagamochi_bounds,
        fast=True,
        records=True,
        touches=(
            *_CORE,
            "packing/devtools/check_nagamochi_bounds.py",
            "packing/frontier/n-*.md",
            "packing/frontier/evidence.yaml",
        ),
    ),
    Step(
        "the inventory agrees with the register",
        _evidence_inventory,
        fast=True,
        records=True,
        touches=(
            *_CORE,
            "packing/devtools/render_evidence_inventory.py",
            "packing/frontier/evidence.yaml",
            "packing/frontier/INVENTORY.md",
        ),
    ),
    Step(
        "results rungs are earned and the view agrees",
        _results_register,
        fast=True,
        records=True,
        # The register names arbitrary artifact, control, and review paths. An empty
        # attribution selects this subsecond step for every change, so a rename or
        # deletion cannot evade its existence checks.
        touches=(),
    ),
    Step(
        "the synopsis headline carries every result",
        _results_headline,
        fast=True,
        records=True,
        touches=(
            *_CORE,
            "SYNOPSIS.md",
            "epistemics.md",
            "packing/frontier/results.yaml",
            "packing/devtools/render_results_headline.py",
            "packing/devtools/render_research_tables.py",
            "packing/devtools/significance.py",
        ),
    ),
    Step(
        "exact certificates are named by their records",
        _certificate_citations,
        fast=True,
        records=True,
        touches=(
            *_CORE,
            "packing/devtools/check_certificate_citations.py",
            "packing/cases/*/verify_exact.py",
            "packing/frontier/n-*.md",
            "packing/frontier/evidence.yaml",
        ),
    ),
    Step(
        "rung figures agree with their certificates",
        _rung_figures,
        fast=True,
        records=True,
        touches=(
            *_CORE,
            *_CASES,
            "packing/devtools/check_rung_figures.py",
            "packing/frontier/results.yaml",
            "packing/frontier/evidence.yaml",
            "packing/defects.yaml",
        ),
    ),
    Step(
        "case prose agrees with its own front matter",
        _case_prose,
        fast=True,
        records=True,
        touches=(
            *_CORE,
            "packing/devtools/check_case_prose.py",
            "packing/devtools/check_rung_figures.py",
            "packing/frontier/n-*.md",
        ),
    ),
    Step(
        "terminal sessions name what they cost",
        _session_rollups,
        fast=True,
        records=True,
        touches=(
            *_CORE,
            "packing/devtools/check_session_rollups.py",
            "packing/campaign/agent-sessions/*.md",
            "packing/campaign/resource-usage/*.yaml",
            "packing/campaign/schemas/agent-session.schema.yaml",
            "packing/campaign/schemas/codex-task-tree-delta.schema.yaml",
        ),
    ),
    Step(
        "terminal sessions name the gate that certified them",
        _session_gate,
        fast=True,
        records=True,
        touches=(
            *_CORE,
            "packing/devtools/check_session_gate.py",
            "packing/campaign/agent-sessions/*.md",
            "packing/campaign/schemas/agent-session.schema.yaml",
        ),
    ),
    Step(
        "Goebel's family reaches the sizes it reaches",
        _gobel_family,
        fast=True,
        records=True,
        touches=(
            *_CORE,
            "packing/devtools/price_gobel_family.py",
            "packing/cases/gobel40/packing.py",
            "packing/frontier/n-*.md",
            "packing/campaign/series/*/results/bc-049-gobel-family-coverage.json",
        ),
    ),
    Step(
        "n=40 rigidity bracket still reproduces",
        _n40_rigidity_bracket,
        touches=(
            *_CORE,
            "packing/devtools/assess_n40_rigidity.py",
            "packing/devtools/assess_n5_rigidity.py",
            *_CASES,
            "packing/campaign/series/*/results/bc-049-n40-rigidity-bracket.json",
        ),
    ),
    # 0.34s, and `broad` only because it needs the engine built.
    Step(
        "differential: search energy vs validity oracle",
        _differential,
        fast=True,
        broad=True,
        needs_engine=True,
        touches=(*_CORE, *_ENGINE_SRC, "packing/devtools/check_search_differential.py"),
    ),
    Step(
        "provenance: recorded commits are reachable",
        _provenance,
        fast=True,
        # Also depends on git history and where HEAD points, which no path expresses. An
        # empty changed-path set already selects the whole gate, so that is bounded.
        touches=(*_CORE, *_RESULTS),
    ),
    Step(
        "campaign record",
        _campaign_record,
        fast=True,
        records=True,
        touches=(
            *_CORE,
            "packing/campaign/*",
            "packing/frontier/*",
            "packing/defects.yaml",
            "packing/devtools/check_declared_commands.py",
        ),
    ),
)


def _positive_integer(name: str, value: str) -> int:
    try:
        parsed = int(value)
    except ValueError as error:
        raise UsageError(f"{name} must be a positive integer, got {value!r}") from error
    if parsed <= 0:
        raise UsageError(f"{name} must be a positive integer, got {value!r}")
    return parsed


def _positive_seconds(name: str, value: str) -> float:
    try:
        parsed = float(value)
    except ValueError as error:
        raise UsageError(
            f"{name} must be a positive number of seconds, got {value!r}"
        ) from error
    if not math.isfinite(parsed) or parsed <= 0:
        raise UsageError(f"{name} must be a positive number of seconds, got {value!r}")
    return parsed


def _environment_flag(name: str) -> bool:
    value = os.environ.get(name, "0")
    if value not in {"0", "1"}:
        raise UsageError(f"{name} must be 0 or 1, got {value!r}")
    return value == "1"


@dataclass(frozen=True)
class Selection:
    """Which steps a set of changed paths reaches, and why."""

    steps: tuple[Step, ...]
    unattributed_paths: tuple[str, ...]
    """Changed paths no step claims. Non-empty means the whole selection was returned."""

    universe_size: int
    """How many steps were offered. Not `len(STEPS)`: `--since` narrows whatever tier
    preceded it, so "everything" means everything in that tier."""

    @property
    def is_whole_gate(self) -> bool:
        return len(self.steps) == self.universe_size


def select_for_paths(paths: Sequence[str], steps: Sequence[Step] | None = None) -> Selection:
    """The steps a change to `paths` can affect, erring toward running too much.

    Two refusals rather than one, because under-selection is the failure that costs
    coverage and it can arrive from either direction:

    - a path no step claims means the attribution is incomplete for this change, so the
      whole gate runs. Returning the steps that happened to match would be an answer
      derived from an admittedly incomplete map.
    - a step that claims nothing is claimed by everything.

    An empty `paths` is not "nothing changed"; it is "nothing was determined", and it
    also selects the whole gate.
    """
    universe = STEPS if steps is None else tuple(steps)
    if not paths:
        return Selection(steps=universe, unattributed_paths=(), universe_size=len(universe))

    attributed = {
        path
        for path in paths
        if any(step.touches and step.reachable_from(path) for step in universe)
    }
    unclaimed = tuple(sorted(set(paths) - attributed))
    if unclaimed:
        return Selection(
            steps=universe, unattributed_paths=unclaimed, universe_size=len(universe)
        )

    reached = tuple(
        step for step in universe if any(step.reachable_from(path) for path in paths)
    )
    return Selection(steps=reached, unattributed_paths=(), universe_size=len(universe))


def _git(*args: str) -> str:
    result = subprocess.run(
        ("git", *args), cwd=REPOSITORY_ROOT, capture_output=True, text=True, check=False
    )
    if result.returncode != 0:
        raise UsageError(f"git {' '.join(args)} failed: {result.stderr.strip()}")
    return result.stdout


def changed_paths(since: str) -> list[str]:
    """Repo-relative paths changed against a git ref, including uncommitted work.

    Uncommitted changes are included deliberately: the question is "what do I need to run
    before pushing this", and a working tree the diff ignored would be exactly the change
    nobody checked.

    Four details, each of which silently under-reported before it was fixed, and an
    under-reported path is a step that does not run:

    - **`--no-renames`.** Rename detection reports only the destination, so moving a file
      out of an attributed subtree drops the path that named the steps it used to reach.
      Renaming `devtools/assess_frontier_rigidity.py` left the step that imports it by
      name unselected, and that step would then die with `ModuleNotFoundError`.
    - **The merge base, not the ref tip.** A two-dot diff compares against the tip, so a
      file this branch changed disappears from the answer once the base converges on the
      same content. The question is what this branch did, which is the three-dot one.
    - **`rev-parse --verify` and `--`.** Without them a `--since` value naming an existing
      path is taken as a pathspec: `--since packing` exits 0 and returns a pathspec-limited
      unstaged diff, dropping every committed change. Silent exactly when the argument
      looks plausible.
    - **`-z`.** With `core.quotePath` at its default a non-ASCII path arrives C-quoted,
      quotes included, and matches no pattern. That fails safe -- an unmatched path selects
      the whole gate -- but it defeats the feature for anyone with such a filename, and
      splitting on NUL fixes the leading/trailing-whitespace corruption at the same time.
    """
    resolved = _git("rev-parse", "--verify", "--quiet", f"{since}^{{commit}}").strip()
    if not resolved:
        raise UsageError(f"--since {since!r} does not name a commit")
    base = _git("merge-base", resolved, "HEAD").strip() or resolved

    out: set[str] = set()
    for args in (
        ("diff", "--name-only", "--no-renames", "-z", base, "--"),
        ("diff", "--name-only", "--no-renames", "-z"),
        ("diff", "--name-only", "--no-renames", "-z", "--cached"),
        ("ls-files", "--others", "--exclude-standard", "-z"),
    ):
        out |= {entry for entry in _git(*args).split("\0") if entry}
    return sorted(out)


def _push_test_step(base: str) -> Step:
    """The behavioral tests reachable from the change against `base` (BC-086).

    Selection happens in `devtools.reachable_tests`, which errs toward inclusion the
    same way `Step.touches` does; this wrapper only needs to know whether the answer is
    the whole suite, because that is what decides whether the run contends like a gate
    and must take the marker -- and whether it carries the whole suite's budget. The
    probe is a subprocess because the selector lives in `devtools`, which `sqpack` does
    not import.
    """
    probe = subprocess.run(
        (sys.executable, "-m", "devtools.reachable_tests", "--summary", "--since", base),
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    if probe.returncode != 0:
        detail = probe.stderr.strip() or probe.stdout.strip() or "selector failed"
        raise UsageError(f"--push could not resolve the change against {base!r}: {detail}")
    everything = probe.stdout.strip().splitlines()[-1] == "everything"

    def action(context: Context) -> str:
        return _run(
            context,
            (sys.executable, "-m", "devtools.reachable_tests", "--run", "--since", base),
        )

    return Step(
        name="reachable behavioral tests",
        action=action,
        fast=True,
        broad=everything,
        # When the selector expands to everything this is `fast behavioral tests` under
        # another entry point, and it takes that step's budget. D-432 is the run that did
        # not: the whole-suite fallback died at the shared 900s cap at 84%, and the
        # failing test it had reached could not be named from what it printed. A true
        # subset keeps the shared cap, which is the guard against one hung test.
        budget_seconds=FAST_SUITE_BUDGET_SECONDS if everything else None,
    )


def _select_steps(
    *,
    only: list[str],
    fast: bool,
    records: bool = False,
    edit: bool = False,
    checks: bool = False,
    sweeps: bool = False,
    suite: bool = False,
    geometry: bool = False,
    skip: Sequence[str] = (),
) -> list[Step]:
    """The steps a tier and its name filters select.

    `--checks`, `--suite`, `--sweeps` and `--geometry` are the four parts of `--fast`,
    and they exist because the pull request runs them as four concurrent GitHub jobs.
    They are a partition by construction here -- one takes the fast steps marked `sweep`,
    one the fast steps marked `suite`, one the fast steps marked `geometry`, and
    `--checks` takes the fast steps marked none of the three -- so no step can be in two
    and none in none, which is the same property that makes the quick and slow
    behavioural lanes safe.

    Four jobs could have divided the tier with `--only` and `--skip` instead, and that
    was rejected on the register rather than on taste. A subset of a tier has no
    declared cost: `--only` reports no tier at all, and `--skip` reports the tier it
    narrowed, so a part-tier run would have been judged against the whole tier's
    recorded 502.3s and failed the stale rule for finishing early. Naming the parts
    makes each a tier with its own ceiling and its own record, which is what
    `D-466` says a surface CI runs on every push has to have.

    `--skip` is `--only` read the other way round, and it exists so a surface can be run
    as everything-but-one. Two CI jobs cannot divide the gate between them with `--only`
    alone: naming the sixty steps one job keeps is a list that goes stale the moment a
    step is added, and the step that gets forgotten is one nobody runs.

    An unmatched `--skip` pattern is refused, and this is the half worth arguing. An
    unmatched `--only` empties the selection, so it announces itself; an unmatched
    `--skip` leaves the selection whole and the run merely does more than it meant to --
    safe for the verdict, silent about the fact that the name it was written against has
    moved. The workflow's exhaustive-tier split is exactly that dependency, so a renamed
    step has to fail the job that names it rather than quietly cost it half an hour.

    The pattern is matched against every declared step rather than against this tier, so
    `--fast --skip "negative controls"` is a no-op and not an error: whether a real step
    is in the chosen tier is the tier's business, and only a name that matches nothing at
    all is a mistake. `--push` builds its test step outside `STEPS`, so naming that step
    is refused rather than silently ignored, which is the honest answer to a request this
    selector cannot carry out.
    """
    if sweeps:
        selected = [step for step in STEPS if step.sweep]
    elif suite:
        selected = [step for step in STEPS if step.suite]
    elif geometry:
        selected = [step for step in STEPS if step.geometry]
    elif checks:
        selected = [
            step
            for step in STEPS
            if step.fast and not (step.sweep or step.suite or step.geometry)
        ]
    else:
        selected = [step for step in STEPS if not (fast or edit) or step.fast]
    if edit:
        selected = [step for step in selected if not step.broad]
    if records:
        selected = [step for step in selected if step.records]
    if only:
        selected = [step for step in selected if any(pattern in step.name for pattern in only)]
        if not selected:
            patterns = ", ".join(repr(pattern) for pattern in only)
            raise UsageError(
                f"--only {patterns} matched no validation step; "
                "`packing-validate --list` shows names"
            )
    if skip:
        unmatched = [
            pattern for pattern in skip if not any(pattern in step.name for step in STEPS)
        ]
        if unmatched:
            patterns = ", ".join(repr(pattern) for pattern in unmatched)
            raise UsageError(
                f"--skip {patterns} matched no validation step; "
                "`packing-validate --list` shows names"
            )
        selected = [
            step for step in selected if not any(pattern in step.name for pattern in skip)
        ]
    if not selected:
        patterns = ", ".join(repr(pattern) for pattern in skip)
        raise UsageError(
            f"--skip {patterns} left no validation step to run; "
            "`packing-validate --list` shows names"
        )
    return selected


def _execute_step(step: Step, context: Context) -> StepResult:
    started = time.perf_counter()
    if (
        step.budget_seconds is not None
        and not context.timeout_is_explicit
        and step.budget_seconds > context.timeout_seconds
    ):
        context = replace(context, timeout_seconds=step.budget_seconds)
    try:
        output = step.action(context)
    except StepSkippedError as error:
        return StepResult(
            name=step.name,
            status="skipped",
            seconds=time.perf_counter() - started,
            output=error.output,
            reason=str(error),
        )
    except StepFailureError as error:
        return StepResult(
            name=step.name,
            status="failed",
            seconds=time.perf_counter() - started,
            reason=str(error),
        )
    except Exception:  # noqa: BLE001 - whatever a step raises is that step's failure, with its traceback
        return StepResult(
            name=step.name,
            status="failed",
            seconds=time.perf_counter() - started,
            reason=traceback.format_exc().rstrip(),
        )
    return StepResult(
        name=step.name,
        status="passed",
        seconds=time.perf_counter() - started,
        output=output,
    )


def _build_engine(context: Context, selected: Sequence[Step]) -> str:
    if not any(step.needs_engine for step in selected):
        return ""
    cargo = shutil.which("cargo", path=context.environment.get("PATH"))
    if cargo is None:
        return "  SKIP: cargo is unavailable; sqsearch-dependent checks cannot run"
    output = _run(
        context,
        (cargo, "build", "--locked", "--release", "--quiet"),
        cwd=PROJECT_ROOT / "sqsearch",
    )
    suffix = "  built sqsearch/target/release/sqsearch"
    return f"{output}\n{suffix}".strip()


@contextmanager
def _validation_activity(marker: Path) -> Iterator[None]:
    try:
        marker.mkdir()
    except FileExistsError as error:
        raise StepFailureError(
            f"validation marker already exists at {marker}; another gate may be running. "
            f"Wait for it, or delete {marker.name} if a crash left it behind."
        ) from error
    try:
        yield
    finally:
        # `missing_ok`, because releasing a lock that is already released is not a
        # failure and the alternative is worse than the problem. On 2026-08-30 an
        # operator cleared what they took for a stale marker while this run held it;
        # the bare `rmdir` then raised out of the `finally`, and a 25-minute `--fast`
        # whose steps had all completed reported nothing at all -- no results, no
        # timings, just a `FileNotFoundError` traceback (D-383). The marker exists to
        # stop two gates running at once, and by this point this gate is over.
        with suppress(FileNotFoundError):
            marker.rmdir()


def _selection_needs_marker(selected: Sequence[Step]) -> bool:
    """Does this selection contend for the machine the way a gate does?

    The marker is a load lock, not a correctness lock: no step mutates the working tree
    (the controls corrupt private snapshots), so what two concurrent runs threaten is
    each other's step budgets, and only the heavy runs carry budgets calibrated to an
    uncontended machine. A selection of edit-tier steps is seconds of read-only work,
    and refusing it while one's own full gate holds the marker is how the third red
    push of 2026-08-30 went out unvalidated (BC-086): the floor must never be the thing
    the lock talks an operator out of.
    """
    return any(not step.fast or step.broad for step in selected)


def _submission_order(selected: Sequence[Step]) -> list[Step]:
    """The order steps are handed to the pool: longest first, declared order after.

    The pool has `--jobs` workers and takes steps in submission order, so a long step
    submitted late starts late and the run ends when it finishes. In declared order the
    behavioural suite is fifteenth, and the fourteen ahead of it were seconds of record
    checks until 2026-09-05, when eight promoted steps joined them (think-k4fb). Those
    eight would have delayed the suite's start by about half their total, and a tier
    whose wall time is one long step would have started paying for the short ones.

    `budget_seconds` is the ordering key because it is already the file's declaration
    that a step runs long, argued next to each of the three that carry one; nothing here
    guesses a duration. Descending, so the longest budget goes first, and stable, so
    everything unbudgeted keeps declared order.

    This changes when steps start, never what is reported: `_run_selected` collects
    results by name and replays them in declared order, which is the property that keeps
    two runs comparable.
    """
    return sorted(selected, key=lambda step: -(step.budget_seconds or 0.0))


def _run_selected(
    selected: Sequence[Step],
    context: Context,
    patterns: list[str],
    skipped: Sequence[str] = (),
) -> RunSummary:
    started = time.perf_counter()
    if _selection_needs_marker(selected):
        activity = _validation_activity(ACTIVITY_MARKER)
    else:
        print("== no gate marker: every selected step is read-only and edit-tier ==")
        activity = nullcontext()
    with activity:
        setup_output = _build_engine(context, selected)
        by_name: dict[str, StepResult] = {}
        with ThreadPoolExecutor(max_workers=context.jobs) as pool:
            futures = {
                pool.submit(_execute_step, step, context): step.name
                for step in _submission_order(selected)
            }
            try:
                for future in as_completed(futures):
                    result = future.result()
                    by_name[result.name] = result
            except BaseException:
                for future in futures:
                    future.cancel()
                context.processes.stop()
                raise
    ordered = [by_name[step.name] for step in selected]
    return RunSummary(
        results=ordered,
        wall_seconds=time.perf_counter() - started,
        setup_output=setup_output,
        selected_count=len(selected),
        total_count=len(STEPS),
        partial_pattern=patterns,
        skipped_pattern=list(skipped),
    )


def _tier_id(namespace: argparse.Namespace) -> str | None:
    """Which declared tier this invocation is, or `None` when it is a slice of one.

    A slice has no declared cost, and giving it one would waive the ceiling by accident:
    `--only "lint floor"` finishing in a second says nothing about whether `--fast` has
    tripled. `--push` is a tier despite selecting its tests from the diff, because its
    ceiling is declared for the widest thing that selector can expand to.
    """
    if namespace.only or (namespace.since and not namespace.push):
        return None
    return next((flag for flag in TIER_FLAGS if getattr(namespace, flag)), "full")


def _judge_budget(
    summary: RunSummary,
    *,
    tier_id: str | None,
    jobs: int,
    inner_jobs: int,
    force: bool,
) -> gate_budgets.Verdict:
    """Compare this run's own wall against the ceiling declared for its tier."""
    steps = tuple((result.name, result.seconds) for result in summary.results)
    try:
        register = gate_budgets.load()
    except gate_budgets.BudgetError as error:
        return gate_budgets.Verdict(
            tier=tier_id,
            wall_seconds=summary.wall_seconds,
            status="unknown",
            notes=(f"the tier register could not be read: {error}",),
        )
    return gate_budgets.judge(
        register,
        tier_id,
        wall_seconds=summary.wall_seconds,
        steps=steps,
        jobs=jobs,
        inner_jobs=inner_jobs,
        cpus=os.process_cpu_count() or DEFAULT_CPU_COUNT,
        force=force,
    )


def _render_budgets(register: gate_budgets.Register) -> None:
    """Print the standing cost of every tier, which is what a W5 block reads first."""
    policy = register.policy
    print(f"== declared tier ceilings ({register.path}) ==")
    print(
        f"  band: a ceiling within {policy.max_headroom:g}x of the recorded cost; a run "
        f"over {policy.drift_ratio:g}x of it fails; a run under {policy.stale_ratio:g}x "
        "of it means the record is stale"
    )
    for tier in register.tiers:
        recorded = (
            f"{tier.measured_seconds:g}s recorded {tier.measured_on}"
            if tier.measured_seconds is not None
            else "never recorded at the reference shape"
        )
        print(f"\n  {tier.command}")
        print(f"    ceiling {tier.ceiling_seconds:g}s, {recorded}")
        print(f"    reference: {tier.reference.describe()}")
        if tier.measured_where:
            print(f"    measured: {tier.measured_where}")


def _render_early_exit(namespace: argparse.Namespace, selected: Sequence[Step]) -> int:
    """`--budgets` and `--list` both answer a question about the gate without running it."""
    if namespace.budgets:
        _render_budgets(gate_budgets.load())
        return 0
    listing = [{"name": step.name, "tags": step.tags} for step in selected]
    if namespace.format == "json":
        print(json.dumps(listing, indent=2))
    else:
        for step in selected:
            print(f"{step.name} [{step.tags}]")
    return 0


def _summary_status(summary: RunSummary, *, strict: bool) -> int:
    failed = any(result.status == "failed" for result in summary.results)
    skipped = any(result.status == "skipped" for result in summary.results)
    over_budget = summary.budget is not None and summary.budget.failed
    return 1 if failed or over_budget or (strict and skipped) else 0


def _render_text(summary: RunSummary, *, strict: bool) -> int:
    if summary.setup_output:
        print("\n== building sqsearch ==")
        print(summary.setup_output)
    for result in summary.results:
        print(f"\n== {result.name} ==")
        if result.output:
            print(result.output)
        if result.status == "skipped":
            print(f"  SKIP: {result.reason}")
        elif result.status == "failed":
            print(result.reason, file=sys.stderr)

    print("\n== where the time went ==")
    for result in sorted(summary.results, key=lambda item: item.seconds, reverse=True)[
        :TOP_TIMING_COUNT
    ]:
        print(f"  {result.seconds:7.2f}s  {result.name}")
    print(f"  {summary.wall_seconds:7.2f}s  TOTAL (wall)")

    budget = summary.budget
    if budget is not None:
        print("\n== the tier against its ceiling ==")
        for line in gate_budgets.render(budget):
            print(line)

    failed = [result for result in summary.results if result.status == "failed"]
    skipped = [result for result in summary.results if result.status == "skipped"]
    print()
    if budget is not None and budget.failed and not failed:
        print("THE TIER IS OUTSIDE ITS DECLARED COST BAND:")
        for reason in budget.failures:
            print(f"  - {reason}")
        return _summary_status(summary, strict=strict)
    if failed:
        noun = "STEP" if len(failed) == 1 else "STEPS"
        print(f"{len(failed)} {noun} FAILED:")
        for result in failed:
            print(f"  - {result.name}")
        return _summary_status(summary, strict=strict)
    if skipped:
        print(f"VALIDATION COMPLETED, BUT {len(skipped)} CHECKS WERE SKIPPED:")
        for result in skipped:
            print(f"  - {result.name}: {result.reason}")
        if strict:
            print("strict mode: a skipped check is not a passed check", file=sys.stderr)
            return _summary_status(summary, strict=strict)
    if summary.selected_count != summary.total_count:
        narrowings = [
            f"{flag} {patterns!r}"
            for flag, patterns in (
                ("--only", summary.partial_pattern),
                ("--skip", summary.skipped_pattern),
            )
            if patterns
        ]
        qualifier = "; ".join(narrowings) if narrowings else "a named tier"
        print(
            f"{summary.selected_count} of {summary.total_count} STEPS PASSED "
            f"({qualifier}; this is not the full gate)"
        )
    else:
        print("ALL CHECKS PASSED")
    return _summary_status(summary, strict=strict)


def _parser() -> ArgumentParser:
    parser = ArgumentParser(
        prog="packing-validate",
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    add_version_argument(parser)
    parser.add_argument(
        "--edit",
        action="store_true",
        help="run the edit-loop checks: everything in --fast except the broad test suite",
    )
    parser.add_argument("--fast", action="store_true", help="run the fast edit-loop checks")
    parser.add_argument(
        "--checks",
        action="store_true",
        help=(
            "run the part of --fast that is none of the other three: the floors, the "
            "record checks, and everything that needs the Rust engine"
        ),
    )
    parser.add_argument(
        "--geometry",
        action="store_true",
        help=(
            "run the part of --fast that re-derives geometry without the engine; the "
            "pull request runs it beside --checks on a runner of its own"
        ),
    )
    parser.add_argument(
        "--suite",
        action="store_true",
        help=(
            "run the part of --fast that is the quick behavioral lane; the pull request "
            "gives it its own runner so xdist can have every cpu"
        ),
    )
    parser.add_argument(
        "--sweeps",
        action="store_true",
        help=(
            "run the part of --fast that re-derives the retained atlases from their "
            "witnesses; the pull request runs it on a runner of its own"
        ),
    )
    parser.add_argument(
        "--push",
        action="store_true",
        help=(
            "run the pre-push floor: the edit tier plus the behavioral tests reachable "
            "from the change against --since REF (default origin/main)"
        ),
    )
    parser.add_argument(
        "--records",
        action="store_true",
        help="run only the record checks: registries, generated views, declared contracts",
    )
    parser.add_argument(
        "--since",
        metavar="REF",
        help=(
            "run only the steps a change against REF can affect, including uncommitted "
            "work; a path no step claims selects the whole gate"
        ),
    )
    parser.add_argument(
        "--only",
        action="append",
        default=[],
        metavar="TEXT",
        help="run step names containing TEXT; repeat for more than one pattern",
    )
    parser.add_argument(
        "--skip",
        action="append",
        default=[],
        metavar="TEXT",
        help=(
            "run everything the tier selects except step names containing TEXT; "
            "repeat for more than one pattern, and a TEXT naming no step is refused"
        ),
    )
    parser.add_argument(
        "--strict", action="store_true", help="run deep checks and fail on skips"
    )
    parser.add_argument(
        "--deep", action="store_true", help="rebuild expensive golden producers"
    )
    parser.add_argument("--jobs", metavar="N", help="maximum concurrent validation steps")
    parser.add_argument("--inner-jobs", metavar="N", help="worker cap exported to each step")
    parser.add_argument(
        "--timeout-seconds",
        metavar="SECONDS",
        help=(
            "maximum time for each validation subprocess (default: 900; also "
            "PACKING_VALIDATE_TIMEOUT_SECONDS)"
        ),
    )
    parser.add_argument(
        "--list", action="store_true", help="list check names and tiers, then exit"
    )
    parser.add_argument(
        "--budgets",
        action="store_true",
        help="print the declared cost ceiling of every tier, then exit",
    )
    parser.add_argument(
        "--enforce-budget",
        action="store_true",
        help=(
            "fail on the tier's declared cost band even when this machine is not the "
            "shape the ceiling was measured for (also PACKING_VALIDATE_ENFORCE_BUDGET)"
        ),
    )
    parser.add_argument(
        "--format",
        choices=("text", "json"),
        default="text",
        help="render a human transcript or one machine-readable summary",
    )
    return parser


def _validate_invocation(
    *,
    strict: bool,
    only: list[str],
    fast: bool,
    records: bool = False,
    edit: bool = False,
    checks: bool = False,
    sweeps: bool = False,
    suite: bool = False,
    geometry: bool = False,
    since: str | None = None,
    push: bool = False,
    skip: Sequence[str] = (),
) -> None:
    parts = checks or sweeps or suite or geometry
    narrowed = only or skip or fast or records or edit or parts or since or push
    if strict and narrowed:
        raise UsageError(
            "--strict cannot be combined with --only, --skip, --fast, --checks, "
            "--suite, --sweeps, --geometry, --records, --edit, --push, or --since"
        )
    if edit and fast:
        raise UsageError(
            "--edit and --fast select different tiers; --fast is the wider of the two"
        )
    if [checks, sweeps, suite, geometry].count(True) > 1:
        raise UsageError(
            "--checks, --geometry, --suite and --sweeps are the four parts of --fast; "
            "ask for --fast to run them all, or for one of them to run that part"
        )
    if parts and (fast or records or edit or push):
        raise UsageError(
            "--checks, --geometry, --suite and --sweeps are parts of --fast and are not "
            "combined with another tier; --fast is all four of them"
        )
    if push and (fast or records or edit):
        raise UsageError(
            "--push is its own tier: the edit tier plus reachable tests; "
            "combine it only with --since to change the base ref"
        )


def _validate_runtime() -> None:
    if sys.version_info[:2] != SUPPORTED_PYTHON:
        raise UsageError(f"Python 3.14 is required, running {sys.version.split()[0]}")


def main(argv: Sequence[str] | None = None) -> int:
    """Run validation and return a process-compatible status code."""
    parser = _parser()
    try:
        namespace = parser.parse_args(argv)
        strict = namespace.strict or _environment_flag("PACKING_VALIDATE_STRICT")
        deep = namespace.deep or _environment_flag("PACKING_VALIDATE_DEEP") or strict
        _validate_invocation(
            strict=strict,
            only=namespace.only,
            fast=namespace.fast,
            records=namespace.records,
            edit=namespace.edit,
            checks=namespace.checks,
            sweeps=namespace.sweeps,
            suite=namespace.suite,
            geometry=namespace.geometry,
            since=namespace.since,
            push=namespace.push,
            skip=namespace.skip,
        )
        jobs_value = namespace.jobs or os.environ.get("PACKING_VALIDATE_JOBS")
        jobs = (
            _positive_integer("--jobs", jobs_value)
            if jobs_value is not None
            else (os.process_cpu_count() or DEFAULT_CPU_COUNT)
        )
        inner_value = namespace.inner_jobs or os.environ.get("PACKING_VALIDATE_INNER_JOBS")
        inner_jobs = (
            _positive_integer("--inner-jobs", inner_value)
            if inner_value is not None
            else max(1, jobs // INNER_JOB_DIVISOR)
        )
        if namespace.timeout_seconds is not None:
            timeout_name = "--timeout-seconds"
            timeout_value = namespace.timeout_seconds
        else:
            timeout_name = "PACKING_VALIDATE_TIMEOUT_SECONDS"
            timeout_value = os.environ.get(timeout_name)
        timeout_is_explicit = timeout_value is not None
        timeout_seconds = (
            _positive_seconds(timeout_name, timeout_value)
            if timeout_value is not None
            else DEFAULT_TIMEOUT_SECONDS
        )
        _validate_runtime()
        require_project_root(PROJECT_ROOT)
        selected = _select_steps(
            only=namespace.only,
            fast=namespace.fast,
            records=namespace.records,
            edit=namespace.edit or namespace.push,
            checks=namespace.checks,
            sweeps=namespace.sweeps,
            suite=namespace.suite,
            geometry=namespace.geometry,
            skip=namespace.skip,
        )
        if namespace.push:
            base = namespace.since or "origin/main"
            step = _push_test_step(base)
            selected = [*selected, step]
            scope = "the whole suite" if step.broad else "a reachable subset"
            print(f"== pre-push floor against {base}: tests select {scope} ==\n")
        elif namespace.since:
            paths = changed_paths(namespace.since)
            selection = select_for_paths(paths, selected)
            selected = list(selection.steps)
            print(f"== change-scoped against {namespace.since}: {len(paths)} paths ==")
            if selection.unattributed_paths:
                shown = ", ".join(selection.unattributed_paths[:5])
                more = (
                    f" (+{len(selection.unattributed_paths) - 5} more)"
                    if len(selection.unattributed_paths) > 5
                    else ""
                )
                print(f"  no step claims {shown}{more}; running the whole selection")
            else:
                print(f"  {len(selected)} steps reachable from those paths")
            print()
        if namespace.budgets or namespace.list:
            return _render_early_exit(namespace, selected)
        environment = os.environ.copy()
        environment["PACK_JOBS"] = str(inner_jobs)
        context = Context(
            deep=deep,
            strict=strict,
            jobs=jobs,
            inner_jobs=inner_jobs,
            environment=environment,
            timeout_seconds=timeout_seconds,
            timeout_is_explicit=timeout_is_explicit,
        )
        summary = _run_selected(selected, context, namespace.only, namespace.skip)
        summary.budget = _judge_budget(
            summary,
            tier_id=_tier_id(namespace),
            jobs=jobs,
            inner_jobs=inner_jobs,
            force=namespace.enforce_budget
            or _environment_flag("PACKING_VALIDATE_ENFORCE_BUDGET"),
        )
    except ParserExitError as error:
        if error.message:
            stream = sys.stdout if error.status == 0 else sys.stderr
            print(error.message, end="", file=stream)
        return error.status
    except gate_budgets.BudgetError as error:
        print(f"packing-validate: error: {error}", file=sys.stderr)
        return 2
    except (UsageError, StepFailureError, ProjectLayoutError) as error:
        print(f"packing-validate: error: {error}", file=sys.stderr)
        return 2 if isinstance(error, (UsageError, ProjectLayoutError)) else 1

    if namespace.format == "json":
        print(json.dumps(asdict(summary), indent=2))
        return _summary_status(summary, strict=strict)
    return _render_text(summary, strict=strict)


if __name__ == "__main__":
    raise SystemExit(main())
