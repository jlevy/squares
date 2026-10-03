# Packing Development Guide

This is the engineering entry point for `packing/`. Read [`TUTORIAL.md`](TUTORIAL.md)
for the mathematics, [`SYNOPSIS.md`](SYNOPSIS.md) for research status, and
[`campaign/README.md`](packing/campaign/README.md) before operating the research loop.
This guide owns runtime support, code placement, validation, and refactoring practice.

The governing rule is assurance proportional to reuse and consequence.
Shared code and research-state boundaries are designed, typed, tested, and kept easy to
orient around. A retained checker for one value of $n$ may stay direct and specialized.
Do not turn a one-off investigation into a framework without a second real consumer.

## Supported Environment

Python **3.14 is the only supported minor version**. Local development and CI pin the
interpreter to **3.14.7** through `.python-version` and the workflow.
Package metadata, Ruff, and BasedPyright express the broader `3.14`-only compatibility
boundary; `uv.lock` pins dependencies, not the interpreter.
macOS and Linux are supported development hosts.
Pull requests run the bounded Linux fast surface; integration events run the ordinary
full checkpoint on Linux and four focused portability checks on macOS. The Rust search
engine uses the stable Cargo toolchain.

From the repository root, then from `packing/`:

```shell
npm ci --ignore-scripts
cd packing
uv sync --frozen --all-extras --group dev
uv run --frozen --all-extras --group dev python --version
uv run --frozen --all-extras --group dev packing-validate --fast
```

`npm ci` installs the pinned Node tools the browser-floor step runs; without them that
step fails. `make hooks-install` runs the same install and then the Git hooks.
The version command must report Python 3.14.7. Do not run a bare `pip install`, commit a
second requirements file, or rely on packages from a global interpreter.
Use uv 0.12 or newer to bootstrap the pinned interpreter; uv 0.8.17 cannot install
CPython 3.14.7 on Linux and reports `No download found for cpython-3.14.7`. Change
dependencies in `pyproject.toml`, regenerate `uv.lock`, and commit both files together.
Use `uv sync --frozen --all-extras --group dev` in CI and when reproducing the locked
development environment; the explicit development group prevents an ambient uv
configuration from omitting the test and quality tools.

The atlas rasters and the composite PDF are drawn by `cairosvg`, which needs the
system’s `libcairo`. CI installs it.
On macOS, `packing-validate` detects Cairo in the default Apple Silicon and Intel
Homebrew prefixes and supplies the corresponding loader path to its child processes,
unless the caller set `DYLD_FALLBACK_LIBRARY_PATH` explicitly.
Direct renderer commands do not pass through the validator; export
`DYLD_FALLBACK_LIBRARY_PATH=/opt/homebrew/lib` before running them when Homebrew’s
library is otherwise outside the loader’s path.

## Code Maturity and Placement

The maturity class says how a module is maintained, not how important its mathematics
is.

| Class | Location | Contract |
| --- | --- | --- |
| **E0 scratch** | Untracked scratch space or the repository `attic/` | Optimize for learning. Do not import it or cite it as evidence. Delete it or promote it when the investigation ends. |
| **E1 retained case code** | `cases/<case>/` | Scope the code to a named $n$, source, theorem, hypothesis, or experiment. State its evidence limits and retain enough input and output for replay. General APIs are optional. |
| **E2 reusable research code** | `src/sqpack/research/` and shared helpers such as `workers.py` | Serve multiple research loops through typed contracts, deterministic tests, explicit errors, and case-free policy. Optimize only from representative measurements. |
| **E3 trust and persistence code** | `src/sqpack/field.py`, `verify.py`, `witness.py`, `src/sqpack/campaign/`, and `src/sqpack/cli/` | Meet E2 expectations plus independent or mutation checks, tested failures, atomic durable writes, and fail-fast persisted-format handling. Campaign and CLI modules are repository applications, not general library APIs. |

Developer infrastructure has its own explicit locations:

- `devtools/` contains repository checks, renderers, schema validation, and negative
  controls. It is not an application API.
- `benchmarks/` contains performance probes whose purpose is measurement, not pass/fail
  correctness.
- `tests/` contains fast behavior, architecture, and CLI contracts.
- `sqsearch/` contains the Rust screening engine.
- `campaign/`, `frontier/`, `atlas/`, and `golden/` contain research state and retained
  evidence, not importable implementation code.

Dependencies flow toward more foundational code:

```text
cases/ and devtools/ ──> sqpack.research ──> sqpack foundations
      campaign app ────> foundations and retained campaign state
           CLI app ────> foundations and named cases/devtools subprocesses
```

`tests/test_module_boundaries.py` enforces the important edges and rejects Python left
in the old top-level, `tools/`, `campaign/`, or `sqpack/` implementation locations.
Reusable foundations, research modules, and campaign code may not import or name a
process dependency on `cases` or `devtools`. The outer validation CLI intentionally
starts named case and developer-tool modules in subprocesses; the architecture test
inventories those string edges as well as Python imports.
A case may consume a maintained API; the maintained API may not grow a Trump-, Göbel-,
checkpoint-, or single-`n` exception to accommodate it.

The four installed commands operate on repository-owned state, so they require a valid
`packing/` checkout.
Source and editable installs locate that checkout directly; a non-editable installation
can use the current checkout or set `PACKING_PROJECT_ROOT` explicitly.
A missing or malformed project root is a hard, actionable error.
Importing reusable `sqpack` modules does not require repository state.

Promote E1 code only after identifying a shared contract and a second real consumer.
Copying ten clear lines twice is often cheaper than inventing an abstraction whose
policy is still changing.
When a supposedly reusable path loses its consumers, demote or remove it instead of
preserving an empty layer.

## Command Surfaces

The installed commands are:

| Command | Purpose |
| --- | --- |
| `packing-validate` | Read-only project validation, focused selection, and machine-readable summaries |
| `packing-campaign` | State-machine operations for preregistered numerical rounds |
| `packing-ledger` | Check campaign invariants and freshness, or atomically render the generated ledger |
| `packing-witness` | Inspect, numerically check, or formally verify a portable packing witness without changing it |

Run `COMMAND --help` before using a command in automation.
A maintained CLI must parse arguments before doing work, keep data on stdout and
diagnostics on stderr, return a nonzero status for partial or complete failure, and
expose JSON or JSONL when its output is a data contract.
Names should say what the command does without directory context.

Use these verbs consistently:

- `check` reads and compares without changing durable state; for a packing witness it
  reports numerical assurance and the actual arithmetic, precision, and tolerance;
- `verify` is reserved for a formal decision from exact arithmetic, a rigorous
  certificate, or a complete proof;
- `replay` validates retained output without rerunning the producer;
- `render` regenerates a derived view atomically;
- `run` performs the declared experiment or workflow;
- `update` replaces a reviewed golden or source-of-truth artifact.

CLI modules adapt typed operations; they do not carry a second implementation of the
algorithm. Use argument-vector subprocess calls, never shell interpolation, for normal
process execution.

## Validation Loops

<a id="validation-tiers"></a>

A **tier** selects validation steps; a **lane** selects tests within a behavioural step.
The
[validation efficiency plan](docs/project/specs/active/plan-2026-09-06-validation-efficiency-and-checkpoints.md)
owns the current work on cost, naming, and checkpoint placement.

Use **PR fast surface** for `--fast`, **full checkpoint** for the default command, and
**deferred checkpoint** for the eleven steps outside PR fast coverage.
The advisory `Deferred checkpoint` workflow runs those steps.
**Golden rebuild** means `--deep`, which also regenerates expensive golden producers;
**strict checkpoint** means `--strict`, which includes that rebuild and refuses skipped
checks. The deferred workflow does not pass `--deep`; its filename and label remain
`deep-gate`.

Run focused/edit checks during ordinary work and the change-reachable push check before
pushing.
Obtain a full checkpoint when the PR is ready for final review and repeat checks
whose evidence later changes invalidate.
Record the checked source and base, selected steps, and failures or skips.
Expensive final evidence must not delay every editing cycle, but a green fast surface
alone is not full pre-merge evidence.

### The tiers

| Tier | Who runs it, and when | Steps | Ceiling | Cost when last measured |
| --- | --- | ---: | ---: | --- |
| `--records` | contributor, before touching a registry; also every pull request | 39 of 92 | 300 s | 11.0 s |
| `--edit` | contributor, in the edit loop | 54 of 92 | 240 s | 59.4 s |
| `--push` | contributor, once before a push — the edit tier plus tests reachable from the diff (`--since`) | varies with the diff | 1800 s | about a minute for a narrow code change; an implicitly configured broad diff selects the whole suite and assigns one outer job so pytest can use the host, see below |
| `--fast` | contributor, at a block boundary; the union of the ten tiers below | 80 of 92 | 600 s | record cleared 2026-09-07 when the corpus widened; 229.1 s locally, only the ceiling applies |
| `--checks` | **CI, on every pull request**, in the `validate` job | 57 of 92 | 140 s | 103.70 s, the geometric mean of thirty-three hosted readings on 2026-09-30 and 10-01, with the band 59.4–137.1 s (2.31x) the runner pool spanned on unchanged steps; the 114.34 s two-attempt record stays in the register as history |
| `--frontend` | **CI, on every pull request**, in the `frontend` job, concurrently | 4 of 92 | 150 s | 104.74 s, the geometric mean of 32 hosted readings from 27 to 30 September (70.97–134.86 s, 1.90x); 85.25 s from two readings stays in the register as history |
| `--typecheck` | **CI, on every pull request**, in the `typecheck` job, concurrently | 1 of 92 | 111 s | 76.5 s, the centre of eighteen hosted readings, with the band 56.67–92.27 s that its two runner regimes span |
| `--geometry` | **CI, on every pull request**, in the `geometry` job, concurrently | 9 of 92 | 180 s | 98.07 s, the geometric mean of fourteen hosted readings, with the band 58.75–116.19 s that its two runner regimes span |
| `--suite-a` | **CI, on every pull request**, in the `suite-a` job, concurrently | 1 of 92 | 131 s | 114.58 s, the geometric mean of twelve hosted readings on 2026-10-01 of the three-shard partition after the day’s growth, band 83.91–128.65 s (1.53x); two more walls that day, 131.58 and 132.67 s, were over the ceiling with every test green and are named, not averaged; the 85.03 s two-reading record stays in the register as history |
| `--suite-b` | **CI, on every pull request**, in the `suite-b` job, concurrently | 1 of 92 | 154 s | 114.38 s, the geometric mean of eleven hosted readings on 2026-10-01 of the same partition, band 79.30–139.35 s (1.76x); the 104.65 s single reading stays as history |
| `--suite-c` | **CI, on every pull request**, in the `suite-c` job, concurrently | 1 of 92 | 154 s | 132.05 s, the geometric mean of eleven hosted readings on 2026-10-01 after the day’s files landed in it, band 90.34–147.16 s (1.63x); the 102.94 s thirty-one-reading record and the 88.59 s first reading stay as history |
| `--suite-d` | **CI, on every pull request**, in the `suite-d` job, concurrently | 1 of 92 | 131 s | pending its first hosted cohort under `think-t7k5`; the record’s cohort predicts about 84 s for its 278.9 test-second share |
| `--sweeps` | **CI, on every pull request**, in the `sweeps` job, concurrently | 4 of 92 | 200 s | 101.51 s, the geometric mean of six 4-of-80 hosted readings (66.36–130.77 s, spread 1.97x); the 119.72 s seven-reading mean and PR 180’s 138.84 s predecessor remain in the register as history |
| `--measure-verifier` | **CI, on every pull request**, in the `measure-verifier` job, concurrently | 1 of 92 | 90 s | pending its first hosted cohort under `think-th8p`; its one step read 21.20 s and, on a runner where every step was about 1.9x slow, 45.30 s inside `--checks` |
| *(no flag)* | Full checkpoint before final review and at block close; main, dispatch, and daily CI | 92 of 92 | 3600 s | integration plus nine deferred workers; new whole-wall measurement pending |

Step counts describe the current 89-step registry.
Dated costs retain their measured source and resource shape; they are not fresh
measurements of the new scheduling.

`--geometry`’s recorded cost is the geometric mean of seven readings at the reference
shape. The earlier four-reading baseline remains in the register’s history.
The superseded `--suite` tier’s final record was a single reading: merging PR 137
brought sixteen test files and the threshold work four more, taking that quick selection
from 4,283 tests to 4,639.
[run 34326478984](https://github.com/jlevy/squares/actions/runs/34326478984) cost 183.44
s where the previous 118.72 s mean would have failed the drift rule at 1.55x. Nothing
regressed: no test’s `call` phase reaches the per-test backstop, and the growth is in
the count. The 275 s ceiling is 1.499x of that reading, just inside the drift rule, and
the earlier mean of two 2026-09-08 readings —
[158.64 s](https://github.com/jlevy/squares/actions/runs/34285770932/job/102260892830)
and
[88.84 s](https://github.com/jlevy/squares/actions/runs/34288782986/job/102270405743),
whose 1.79x spread was runner variation rather than a code speedup — stays in the
register as history of the previous selection.

The unsplit lane later grew to 6,096 passing tests and exceeded its 275-second ceiling
twice, at 280.83 seconds and 278.93 seconds on exact-head hosted runs.
The second run also reported six skips.
Changing only xdist’s scheduler did not recover the target: the local default measured
302.70 seconds, `loadscope` measured 318.54 seconds, and `worksteal` measured 323.69
seconds. The latter two were rejected as 5.2 and 6.9 percent slower than the default.

The current surface therefore runs pre-collection shards, four since 2026-10-01.
`devtools.suite_files` packs recorded per-file costs longest-first across them; a file
absent from the record uses a stable `crc32(path) mod 4` fallback.
Each file belongs to exactly one shard and each runner imports only its own files.
The shard jobs retain full Git history for history-reading tests, but none installs Node
or a browser.
Browser-floor liveness runs under `--frontend`, on the runner that owns the
pinned Node toolchain, and so does `site table layout in Chromium`, the two test files
that pin the tables’ pixels, on the runner that installs the pinned Chromium.
They launch it with `--font-render-hinting=none`: the headless shell hints text at
`HINTING_FULL` by default, which on Linux rounds every glyph’s advance to a whole pixel,
and the pins were read on macOS, where nothing is hinted ([D-513](defects.md)). Where no
Chromium launches they fail rather than skip, because a skip on that runner is a hole in
the surface. Each shard writes a per-file cost report beside its JUnit and timing
artifacts; the recorder accepts complete coherent cohorts and rejects failed, partial,
duplicated, coverage-mismatched, and mixed-provenance evidence, and a cohort recorded at
one shard count may be packed into another, which is how the lane is repartitioned.
The current declared ceilings are 131 seconds for shards A and D and 154 seconds for B
and C.

The frontend browser runner builds one page and runs eight isolated browser contracts.
The gate permits two contracts concurrently when the CPU count and outer job count leave
room; otherwise it uses one.
Both routes run the same checks and propagate failures.
For a same-host comparison, run `python -m workbench_tools.check_frontend --workers 1
--timings PATH` and then `--workers 2` with a different receipt path, using the project
interpreter. Receipts include per-check times and source identity.
The
[PR 246 integration review](docs/project/reviews/review-2026-09-29-native-rectangle-contract.md#end-to-end-integration-review)
records the initial comparison; it does not change the frontend gate’s thresholds.

The first PR 188 integration run at exact head `c5a33270` measured 84.00 and 143.98
seconds, respectively, over the complete 6,345-item quick selection: 2,362 passes in
suite A, and 3,977 passes with 6 skips in suite B. `c4f0660d` rebuilt the cost record
from same-speed cohort 35175474610 and rebalanced the shards.
At exact head `be28ad5a`, run 35182460400 then set the current records.
Suite A records 109.92 seconds, the geometric mean of 81.26, 133.91 and 122.06 seconds
over attempts 1–3, with 3,422 tests passing each time.
Suite B then read 125.16 and 124.40 seconds over attempts 2–3, with 3,008 passes and 6
skips; attempt 1 is excluded because a gate-budget test failed there.
On 2026-09-21 that record failed its own stale rule at 0.59x, and three runs of one
byte-identical shard that day settled why: 73.90, 74.98 and 133.81 seconds, on 240.2,
240.2 and 449.9 test-seconds of accumulated test time, with 3,140 passes and 6 skips
every time. The tier has no cost, it has a distribution 1.81 times wide, and a record
built from one cohort of it starves whichever rule it is not next to.
Suite B now records 102.91 seconds, the geometric mean of all five readings at the
reference shape, and its ceiling came down with it — from OR-14’s 180-second
pull-request wall to 154 seconds of its own, which is where the drift rule already sits.
The `c5a33270` readings, the `be28ad5a` record and the predecessor PR 175 geometric
means remain in the budget register as history.

Before the reconciliation runs, `--sweeps`, `--checks`, and `--frontend` had no current
recorded cost. The corpus widening of 2026-09-07 invalidated the first two baselines.
Two of the sweeps tier’s four steps were split that day, so the tier those readings
measured no longer exists.
The `checks` record was cleared the same day and by its own rule firing rather than by
hand: at n = 1..324 the tier ran 189.09 s against a recorded 99.39 s — 1.90x, where 1.5x
fails — and the gate’s verdict named `exact verification` as 133.4 s of it.
The grid replay inside that step was the corpus-scaling member and is now deferred; the
[readings are retained](packing/benchmarks/gate-cost-at-324/README.md).
Two PR 160 attempts then measured `--checks` at 197.56 s and 195.15 s against its 195 s
ceiling. The second run spent 132.21 s in exact verification, 106.34 s in BasedPyright,
62.74 s in the soundness perimeter, and 37.31 s in the browser floor.
The browser floor and the new full-page accessibility check now form `--frontend`,
leaving every verdict in `--fast` while removing that work from the saturated queue.
At that point, the first hosted run of each changed partition supplied its new baseline.
The table above now carries those readings; the final reconciliation head must refresh
any entry whose topology changed.
Splitting the partitions did not end the overruns.
After `main` merged into the stack, #160 read 200.68 s and 199.74 s at `72629c03`.
`think-lrs0` records three causes:
- runner speed, which moved every step of one branch by about 1.3x together;
- the branch cost rollup’s render step, at 45 to 61 s, which `main` fixed at `65a5c001`;
- type-floor time from the Python #160 adds.
  With `main`’s fix merged, #125 read 146.04 s of 195 s at `bca21da0` (run 34923097435).
  #160 has not been re-read since, and `think-lrs0` stays open until it is.
  [D-472](defects.md) retains the calibration history, and `think-be1s` tracks the band
  representation.

**The pull-request surface is `--checks`, `--frontend`, `--typecheck`, `--geometry`,
`--suite-a`, `--suite-b`, `--suite-c`, `--suite-d`, `--sweeps`, and `--measure-verifier`
together, run as ten concurrent CI jobs**, so a pull request waits for the longest part
rather than for their sum.
All ten feed the stable `packing-required` aggregate context.
Repository protection settings determine whether GitHub requires that context before a
merge. `test_the_pull_request_jobs_partition_the_surface` reads the workflow and checks
that they are pairwise disjoint and that they cover every step of `--fast` — so the
split cannot lose a check the way a set of independent filters could.

The four behavioral shards use a source-bound file-cost record and deterministic
partitioning weighted by the planning capacities 131/154/154/131, which were the live
ceilings when the record was taken; the frozen weights define the measured assignment,
and the ceilings are enforced separately.
Each test file belongs to exactly one shard.

The fourth shard was added on 2026-10-01, when about 450 tests landed in a day on a
record that no longer named the lane.
The record then packed 433 of 499 test files from a two-shard cohort of 2026-09-30
([run 36728602528](https://github.com/jlevy/squares/actions/runs/36728602528)); the 66
unrecorded files took the path hash, and `crc32(path) mod 3` sent 25 of them, with 106.8
of their 200.0 test-seconds and the lane’s largest new file (`test_overview.py`, 57.5
s), into shard C. The three-shard cohort of
[run 36924379492](https://github.com/jlevy/squares/actions/runs/36924379492) measured
the shards at 410.7, 339.7 and 463.1 test-seconds, 2,701, 2,721 and 3,967 tests, and
121.14, 101.75 and 145.18 s of wall, about 0.30 s of wall per test-second; over the day
shard A read 83.91 to 132.67 s against its 131 s ceiling and failed PR 277 twice with
every test green. Three balanced shards would carry 404.5 test-seconds each: about 121 s
of wall, and 150 to 157 s at the top of the runner band, which is B and C’s ceiling and,
with about 44 s of checkout and setup, about 200 s of job wall against OR-14’s 180 s
outer edge. The record was rebuilt from that cohort into four shards, 278.9 test-seconds
for A and D and 327.9 for B and C, predicting about 84 and 98 s.
`python -m devtools.suite_files check` reports each shard’s unrecorded share against the
tree, and the plugin warns in a shard’s own log when more than a tenth of its files have
no recorded cost; a file added after the record falls to the hash until the next rebuild
from a green cohort’s reports.
The third shard supplied capacity after
[run 36735084578](https://github.com/jlevy/squares/actions/runs/36735084578) measured
156.19 and 165.06 seconds for the two-shard partition: their combined 321.25 seconds
left less than one second against the combined ceilings.
The first three-shard cohort,
[run 36739024277](https://github.com/jlevy/squares/actions/runs/36739024277), passed
7,958 behavioral tests with seven skips at 65.67/104.65/88.59 seconds.
These are hosted observations, not a controlled speedup estimate.
Calibration tightens shard A while preserving the observed file assignment.
The unchanged shard A then passed the same 2,213 tests with seven skips in 110.09
seconds in [run 36740609969](https://github.com/jlevy/squares/actions/runs/36740609969).
Its declared timing band retains both observations, 65.67–110.09 seconds, with a
geometric mean of 85.03 seconds; its absolute limit remains 131 seconds.

The merged [PR95](https://github.com/jlevy/squares/pull/95) implementation pools the
known-best census and prospective-atlas rebuilds through the shared worker policy.
Integration CI also caches the Cargo registry, git cache, and engine target directory;
Cargo still checks and builds the selected source with its locked dependencies.
These reduce repeated work without changing the partition or treating a cache hit as
validation evidence.

These dated observations include hosted setup and are not controlled speedup
comparisons:

| Surface | Observed wall time | Run |
| --- | ---: | --- |
| PR fast surface | 2m22s; four Linux jobs 1m58s–2m15s | [34023121156](https://github.com/jlevy/squares/actions/runs/34023121156) |
| Full main checkpoint | 27m33s; integration 24m19s and exhaustive 27m28s concurrently | [34025346801](https://github.com/jlevy/squares/actions/runs/34025346801) |
| Deferred checkpoint | 27m01s; deferred checks 12m32s and exhaustive 26m53s concurrently | [34028227026](https://github.com/jlevy/squares/actions/runs/34028227026) |

All three runs are from 2026-09-06. The durations are observations, not necessary lower
bounds or enforced tier baselines.
The [tier table](#the-tiers) lists the current declarations and identifies the entries
that still cite the predecessor topology pending the exact reconciliation run.

### The pull-request wall

A tier clock and a pull-request wall are different measurements.
Tier clocks begin when `packing-validate` runs.
The `pull_request_walls` register measures from the workflow run’s start through the
start of the wall-check step inside its required aggregator, `packing-required` or
`pages-required`. That includes prerequisite queues, checkout, setup, work, artifact
transfer, and the aggregator’s queue, result assertion, blobless checkout, and pinned
Python setup; it excludes the wall check itself and subsequent teardown.
If GitHub withholds the running step’s timestamp, the live check can instead use its own
process invocation time as a labeled conservative upper bound.
This requires the matching run, attempt and aggregator, complete prerequisites, and
ordered timestamps; it can charge extra wall time but cannot reduce the measured wait.
Historical and sample measurements continue to use API timestamps.

`packing/devtools/check_pr_wall.py` runs inside both aggregators and judges the wall
against OR-14’s absolute 180-second budget.
Once a pull-request kind (`main` or `stacked`) has at least 15 recorded samples, it also
judges the wall against 1.2 times that kind’s median.
An unmeasurable current run fails closed.
A missing or undersampled median produces an explicit warning while the absolute budget
still applies. Partial reruns, missing jobs or required timestamps, an incomplete
jobs-API page, and non-finite register values cannot produce a passing measurement.

**Both walls are currently advisory under `think-g4n9`.** Each workflow’s entry in
`pull_request_walls` declares its `enforcement`. Absent means `enforcing`: a wall over
the budget or the regression ratio fails `packing-required` or `pages-required`. An
`advisory` entry must also name a `tracking_bead` and an `advisory_reason`, and a wall
over its budget or its regression ratio then warns rather than fails.
The checker prints the same diagnosis, marks the verdict advisory in the log and the
step summary, raises a warning annotation that names the bead, and exits successfully.
Nothing else is relaxed.
Unmeasurable runs, missing prerequisites and malformed register entries still fail, the
tier ceilings are unaffected, and the budget stays at 180 seconds.
`devtools.check_gate_budgets` refuses an advisory wall whose bead is closed or unknown,
and an enforcing wall that still names a tracker.
With no bead store to read, it fails under `CI` and prints a skip note on a local
checkout.

The owner made both walls advisory on 2026-09-17, after five hosted Packing walls on PR
188 read 194, 189, 178, 166, and 216 seconds.
Hosted runner speed varied about 1.6–1.8x on identical code, and the `frontend` job
alone ran 158–180 seconds end to end.
The decision covers the pull-request wall generally, so the Pages wall is advisory too;
it has also read over 180 seconds on PR 188, at 182 seconds in run 35182460356.
`think-g4n9` switches both walls back to enforcing once five consecutive exact-head
hosted runs hold both walls at or under 180 seconds.
Five is the planned default, and `think-g4n9` owns it.

On a push to `main`, the integration job looks for a successful pull-request run that
validated the exact same Git tree and explicitly passed `packing-required`. A match
licenses reuse only for fast steps named in the positive `TREE_REUSABLE_FAST_STEPS`
allowlist. Every deferred step and every unclassified fast step repeats after merge;
missing artifacts, expired artifacts, API errors, fork runs, and incomplete checks all
fall back to the complete surface.

### The behavioural lanes

`QUICK_TESTS`, `SLOW_TESTS` and `EXHAUSTIVE_TESTS` in `sqpack/cli/validate.py` are
marker expressions over `slow` and `exhaustive_exact`. They are **complements**: every
test satisfies exactly one, so no test can be in two lanes and none can be in zero.

| Lane | Marker | Tests at last count | Runs in | Bound |
| --- | --- | ---: | --- | --- |
| quick | neither | 9,389 file-shard tests (9,193 passed; 196 skipped) | PR fast surface: file shards in `suite-a`, `suite-b`, `suite-c` and `suite-d`, browser-floor liveness and the site table layout in `frontend` | fails a test whose `call` phase reaches 12 s |
| slow | `slow` | 97 | full checkpoint, under xdist in CI | fails a test whose `call` phase is under 1 s |
| exhaustive | `exhaustive_exact` | 55 | its own CI job | its own 3600 s budget |

The quick file-shard count is from the three shards’ per-file reports in run 36924379492
on 2026-10-01, before the fourth shard was added; the separate browser-floor controls
are not included in that count.
The slow and exhaustive counts are `--collect-only` readings from 2026-09-08 against the
n = 1..324 corpus. These are measurements rather than fixed membership; marker
expressions determine the three lanes, and counts move with the corpus.
A stale quick count in this table is how [D-488](defects.md)’s cause stayed invisible,
since the tests grew and the budget bounding them did not.
[Main run 34025346801](https://github.com/jlevy/squares/actions/runs/34025346801)
reported 2,197 quick and 95 slow on 2026-09-06, before the corpus expansion of
2026-09-07. The marker expressions determine current membership.

**The slow lane’s xdist is conditional on the shape it is run in.** Both lanes size
their workers as `cpus - jobs + 1`, so the two CI jobs that carry the slow lane run it
at three workers on four cpus, while `packing-validate` with no `--jobs` defaults jobs
to the cpu count, leaves one worker, and runs the lane in a single process exactly as it
did before [D-484](defects.md).
The change bites only where `--jobs` is below the cpu count, so the default local full
gate is unimproved. The 718.52 s against 1020.77 s that argued for it was measured at
four workers, a shape no gate runs; at three workers on a contended box the same tests
were 795.11 s, about 1.28x.

**Both bounds are enforced, in opposite directions.** A quick test that grows past the
ceiling fails the pull request in the week it grows; a deferred test that drops below
the floor fails the deep surface until its marker comes off.
That is what makes the split a rule rather than a hand-maintained list — the failure
mode `D-466` records.

### The deep gate: the deferred surface, before the merge

The deferred checkpoint runs slow behavioural tests, exhaustive exact tests, negative
controls, the n=40 rigidity replay, the whole known-best atlas rebuild, the whole
single-square translation escape screen, and the whole exact rational grid replay.
T-024 and T-026 add four exact dilation-limit replays at 720 and 1440 steps.
These are the eleven steps outside the [PR fast surface](#validation-tiers).
[D-470](defects.md) records why checking them only after a merge is insufficient: a
stale certificate test left main red across three merges despite green PR checks.

The deferred workflow resolves one immutable checkout and distributes the work over nine
jobs: a slow-test job, a screen job, three exhaustive-test shards, and four groups of
whole deferred checks.
Exhaustive shards partition test files using retained costs; new files receive a
deterministic assignment.
Every shard keeps the same exhaustive marker and complete test bodies.
`deep-gate-required` waits on every job and the source resolver; a missing, skipped or
unsuccessful prerequisite fails the aggregate.
Timing artifacts have distinct job names and record the checked-out commit.
For a dispatched PR, that resolved merge commit can differ from the workflow dispatch
ref; the checkout receipt identifies the source actually validated.
Main, daily and manually dispatched packing validation use the same deferred groups.
Their separate `post-merge-required` aggregate requires the integration job and all nine
deferred workers to succeed; the seven-job PR aggregate remains separate.

The last three joined on 2026-09-07 because the corpus tripled, not because the gate
changed its mind about them.
At n = 1..324 the escape screen measured 766.26 s and `build_known_best_atlas --check`
691.19 s of a 703.28 s step, against a 210 s ceiling on the job that carried both.
`exact rational grid replay` is `devtools.check_basic_bounds` run whole, at 34.81 s
inside `exact verification` — the one member of that step that grows with the corpus, in
a `checks` job that had just run 189.09 s against a 195 s ceiling.
[The readings are retained](packing/benchmarks/gate-cost-at-324/README.md).
None left without a stand-in: `known-best atlas records and sample`, `translation escape
screen records and sample`, and the sampled replay inside `exact verification` run on
every pull request, re-derive the whole record layer of each artifact, and rebuild a
fixed, recorded sample of the cases, so per-case geometry is the only evidence that
waits for this surface.

[`deep-gate.yml`](.github/workflows/deep-gate.yml) runs that surface against a pull
request instead. Its selection is the **exact complement** of the pull-request surface,
not a sample of it:
`test_the_deep_gate_runs_exactly_what_the_pull_request_surface_defers` resolves the
workflow’s own commands through `packing-validate --list` and compares the union against
every step no pull-request job runs.
So the pull-request surface and the deep gate together are the whole gate, and another
deferral argued into `test_the_pull_request_surface_defers_only_what_was_measured` fails
until it is added here too.

The [dated measurement above](#the-tiers) is about 27 minutes.
Both jobs need profiling: improving only the exhaustive job can leave the integration
work on the critical path.
A duration does not establish that the work is irreducible.

**To run it on a pull request, add the `deep-gate` label.**

- The label starts it, and every subsequent push re-runs it, because a label that
  attested to an older commit would be the same stale evidence as the daily backstop.
  **Label last**, when the branch is otherwise ready.
- Without the label every job skips in seconds, so the workflow adds nothing to an
  ordinary pull request.
  It reports one context, `deep-gate-required`, for the reason `packing-required` is one
  context: `D-380` records what a fan-out of separately required checks cost here.
- To run it without touching the author’s labels, dispatch **Deferred checkpoint** with
  `pull_request: <number>`; it checks out that pull request’s merge ref.
  Select the PR head branch as the dispatch ref when the PR changes the workflow: GitHub
  loads the workflow definition from that ref, independently of the checkout selected
  inside its jobs. Dispatching an older main workflow can therefore omit newly added
  checks even while testing the correct PR merge tree.
  Verify both the workflow definition and the selected step union in the final receipt.

**Run the full checkpoint for final review.** A passing PR fast surface and a deferred
checkpoint together cover the ordinary gate when their source and base identities agree.
Request the deferred run when the PR is otherwise ready; subsequent invalidating changes
require fresh evidence.
Pay particular attention when the branch:

- moves a certificate, a retained witness, a rung, or anything under `packing/cases/` —
  the exhaustive tier is what decides those, and it is what `6bd136b0` broke;
- edits `devtools/controls.yaml` or a mutation the negative controls declare (`D-403`:
  stale controls accumulate unseen because they do not run on a pull request);
- touches `devtools/assess_n40_rigidity.py` or `devtools/assess_n5_rigidity.py`, the
  n=40 bracket’s declared inputs;
- adds, removes or could slow a test marked `slow`;
- or changes mathematics rather than prose, which is the blunt version of all four.

**These runs provide advisory evidence.** A reviewer can request and inspect the deep
run before merging, but neither the label nor the dispatch enforces a merge
prerequisite. A dispatch checks out the requested PR’s merge ref; its check run belongs
to the dispatch ref, so reviewers must inspect that workflow run directly.
If `main` moves after a successful run, that evidence does not cover the new combined
tree.

This repository is publicly hosted under a personal account.
[GitHub merge queues](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/managing-a-merge-queue)
require an organization-owned repository (and an eligible plan for private
repositories), so queue enforcement is unavailable here.
The workflow has no `merge_group` trigger.

Future queue adoption would require an eligible repository and a workflow change before
changing protection settings.
GitHub shares required status checks between pull requests and merge groups: every
required context must report on both events.
In particular, `packing-required` currently runs only on pull requests.
A future design must run and aggregate the intended fast and deep checks on merge
groups, while reporting the chosen PR contexts on opening and subsequent updates.
It must also partition the deep work to avoid running the exhaustive tier in both
workflows: adding `merge_group` to `packing-validation.yml` alone selects its complete
post-merge gate, but leaves its PR-only aggregate skipped.
Verify the complete required-context set on both events before enabling the queue.

### What it is allowed to cost

Ceilings are **data the gate reads, not prose in this file**: one entry per tier in
[`packing/devtools/gate-budgets.yaml`](packing/devtools/gate-budgets.yaml), compared
against every whole-tier run’s own wall.

```shell
uv run --frozen --all-extras --group dev packing-validate --budgets
```

Choose the smallest loop that protects the change:

```shell
# Discover the available contracts.
uv run --frozen --all-extras --group dev packing-validate --list

# Records loop: registries, generated views and declared contracts, and no solver.
# The cheapest thing that catches what actually breaks; takes no gate marker.
uv run --frozen --all-extras --group dev packing-validate --records

# Edit loop: everything fast except the broad test suite. Seconds, runs during a gate.
uv run --frozen --all-extras --group dev packing-validate --edit

# Pre-push floor: the edit tier plus the behavioral tests reachable from the change
# (against origin/main, or --since REF). Broad changes may select the whole suite.
uv run --frozen --all-extras --group dev packing-validate --push

# The pull-request surface: the edit tier plus every behavioral test under the
# per-test ceiling. CI runs it as the nine parts below, one per runner; run it whole
# here, where there is only one machine and nothing to overlap with.
uv run --frozen --all-extras --group dev packing-validate --fast

# The ten parts CI runs concurrently on a pull request. They partition --fast, so
# running all ten is running the surface and running one is running a part of it.
uv run --frozen --all-extras --group dev packing-validate --checks
uv run --frozen --all-extras --group dev packing-validate --frontend
uv run --frozen --all-extras --group dev packing-validate --typecheck
uv run --frozen --all-extras --group dev packing-validate --geometry
uv run --frozen --all-extras --group dev packing-validate --suite-a
uv run --frozen --all-extras --group dev packing-validate --suite-b
uv run --frozen --all-extras --group dev packing-validate --suite-c
uv run --frozen --all-extras --group dev packing-validate --suite-d
uv run --frozen --all-extras --group dev packing-validate --sweeps
uv run --frozen --all-extras --group dev packing-validate --measure-verifier

# One named component. --only is repeatable and matches displayed step names.
uv run --frozen --all-extras --group dev packing-validate --only "basin identity"

# Everything but one. --skip takes the same repeatable, substring-matched names, and
# refuses a pattern that names no step rather than quietly removing nothing.
uv run --frozen --all-extras --group dev packing-validate --skip "negative controls"

# Full integration checkpoint used locally and in CI.
uv run --frozen --all-extras --group dev packing-validate

# Rebuild expensive mathematical golden producers while comparing read-only.
uv run --frozen --all-extras --group dev packing-validate --deep

# Strict checkpoint: full coverage, golden rebuild, and refusal of skips.
uv run --frozen --all-extras --group dev packing-validate --strict

# Structured result for agents and automation.
uv run --frozen --all-extras --group dev packing-validate --format json
```

The default command runs the complete ordinary surface: fast pytest contracts, Python
and Rust quality, exact and differential mathematics, replay, schemas, generated-view
drift, provenance, campaign invariants, and mutation controls.
Pytest is one layer of that gate, not a replacement for proof scripts and independent
implementations.

The fractional certificate sweeps have a separate geometric oracle in
[`devtools.check_fractional_sweep`](packing/devtools/check_fractional_sweep.py).
It constructs event cells independently, decides their intersection with the admissible
center domain by separating axes, sums atom weights directly, and checks that the
witness center each sweep returns admits a square and covers the reported minimum.
It shares no clipping, strip-range, or prefix-sum implementation with the two standalone
verifiers it checks.
Small deterministic controls and a seeded corpus run in the ordinary pytest lane, so
every pull request exercises them.
For a larger reproducible falsification pass, run from `packing/`:

```shell
uv run --frozen --all-extras --group dev python -m devtools.check_fractional_sweep --cases 20000 --seed 89213
```

The report includes the seed and comparison counts; a discrepancy fails the command and
identifies its reproducing case.
The
[adversarial review](docs/project/reviews/review-2026-09-06-published-core-claims-adversarial.md)
records the original 20,000-case comparison and its scope.
These comparisons can expose implementation regressions.
Agreement on a finite corpus does not prove either program correct or replace replaying
the actual certificate over its complete direction net and center domain.

A retained depth-scaled family, the witness behind a cutting floor, is replayed from its
bytes with
[`devtools.replay_ceiling_family`](packing/devtools/replay_ceiling_family.py), which
re-decides the exact maximum depth with the final verifier and, under `--check`, fails
unless the record’s own vertex count, depth or scaled total is reproduced.
The retained n=11 families take several minutes each.

The validation command builds `sqsearch` only when a selected step needs it.
Checks run concurrently, but their captured output is replayed in declared order.
`--jobs` controls outer check concurrency; `--inner-jobs` caps each check’s internal
workers.
Strict mode cannot be combined with a partial selection and fails on every skip.

`--push` is the pre-push floor (`BC-086`). It selects the edit tier plus a
`reachable behavioral tests` step: `devtools.reachable_tests` computes the test files
the change can reach — import closure over `src/sqpack`, `devtools`, `cases` and
`tests`, text mention of a changed module or file, repository walkers always included —
and errs toward running too many, up to the whole suite when nothing narrower is
defensible. Each of 2026-08-30’s three red pushes broke a test reachable this way from
the changed paths ([D-381, D-393](defects.md)), and the floor would have caught all
three.

**Large implicit push selections receive a separate pytest phase.** A changed workflow
file or suite configuration expands the selector to everything: the quick and slow lanes
together, against `FAST_SUITE_BUDGET_SECONDS`. A large proper subset can also dominate
the run. When resource settings are implicit, the edit checks run with their normal
concurrency, then the reachable tests use the available pytest workers after the edit
pool has drained. Nested tool pools are capped at one during the parallel pytest phase.
Tests marked `pool_heavy` run afterward in a separate serial pytest process with the
reserved CPUs assigned to their internal pool.
The whole-atlas composite test uses this allocation; its per-case builder and global
assertions are unchanged.
Both phases use the same selected files and complementary markers, so every selected
non-exhaustive test belongs to exactly one phase.
Other slow tests remain parallel.
This prevents the CPU-wide outer default from leaving pytest with one worker after the
other checks finish.
It also prevents two internally parallel checks from each claiming the same CPUs.
Explicit resource settings remain authoritative.

[D-488](defects.md) is that timeout, and what it fixed is narrower than the failure:
until it, `_xdist_distribution`’s flag never reached the selector’s pytest at all, so
`--jobs 1` was serial too and there was no shape that worked.
There is one now, and the implicit large-selection phase uses it.
The historical 1403-second reading used that one-outer-job shape and finished inside the
cap; the reconciliation branch still owes its final-source push and full-checkpoint
receipts before closeout.

The `.gate-running` marker is a load lock protecting calibrated step budgets, not a
correctness lock — no step mutates the working tree.
The floor tiers say so: `--records`, `--edit`, and a `--push` whose test selection is
narrow remain runnable while a full gate holds it, because a floor the lock can refuse
is a floor that gets skipped.
A large narrow push opportunistically reserves the load lock for its exclusive pytest
phase. If the lock is already held, it retains its conservative worker allocation
instead. Whole-suite fallback still requires the lock.
The CLI reports which allocation it selected, and command receipts record the effective
worker settings. Selections containing a broad or full-tier step still take the marker
and still refuse a second gate.

When command artifacts are enabled, the reachable-test wrapper records separate JUnit
and duration reports for each child phase.
Flushed per-worker JSONL progress identifies the source commit, run, test node and
effective worker allocation; an interrupted test leaves its start event available before
JUnit can finish. These are operational timing receipts, not mathematical acceptance
evidence. Artifacts stay outside the source tree.

Every validation subprocess has a finite 900-second default deadline.
Override it with `--timeout-seconds SECONDS` or `PACKING_VALIDATE_TIMEOUT_SECONDS`;
values must be positive and finite, and an explicit smaller per-call timeout still wins.
Mutation-control commands retain their 120-second default deadline and may declare a
smaller `timeout_seconds` in `devtools/controls.yaml`. A timeout terminates and reaps
the whole process group, including a child that ignores the first termination signal.
Each command also gets an empty bytecode-cache root, so rapid same-size source mutations
cannot execute a stale control from the preceding snapshot use.
Each snapshot is itself a git checkout of the tracked files it carries, so a check that
asks git what this repository holds — rather than walking the working directory — is
answered inside the worker, and its control rehearses the code the gate runs rather than
a refusal or a fallback.

The validation deadline bounds subprocess commands on supported POSIX hosts.
It does not bound pure-Python worker code, the total duration of a step that runs
multiple commands, or detached daemons; Windows process-tree cleanup is not yet
implemented. These limits are why a subprocess timeout is not, by itself, evidence that
D-239 is resolved.

Pushes to `main`, manual dispatches, and the daily schedule run the ordinary full
checkpoint on Linux in four jobs: `validate` excludes the slow lane, exhaustive exact
tests, and whole translation escape screen.
`slow-lane`, `exhaustive`, and `screen` run those three selections separately.
The two solo jobs are solo for different reasons.
`exhaustive` is a verdict split, carried as `think-tr2z`: the tier was 1943 s of the
complete surface’s 2755 s wall, just over seventy per cent of it, and killed at its
budget it reported nothing about the sixty steps beside it.
That kill is [D-456](defects.md), which re-measured the tier at 2036 s on four cores and
raised its budget rather than splitting it.
`screen` is a worker split ([D-484](defects.md)): the step is a process pool sized by
`PACK_JOBS`, and beside the rest of the gate at `--inner-jobs 2` it gets two of the
runner’s four. What the other two workers buy is not established.
The four hosted readings of the split job are 944 s, 861 s, 949 s and 947 s, none of
them below the 858.62 s the step cost at two workers on a different runner, so the
argument for the split is the pool it was not filling and the cap it kept failing
against, not a measured speedup.
macOS runs four portability checks.
Neither workflow invocation enables the golden rebuild or strict checkpoint.
The daily run checks the default branch at 08:17 UTC; unmerged branches need their own
labelled or dispatched deferred checkpoint.

The behavioural [lane definitions](#the-behavioural-lanes) preserve the partition.
Quick-test timing uses the `call` phase because shared fixture setup can be charged to
whichever test starts first.
Optimize a test that exceeds its ceiling, or retain its measurement when moving it to
`slow`; remove that marker when its measured cost falls below the floor.
The marker registry tests enforce both declarations.
Both behavioural lanes use xdist workers sized by `cpus - jobs + 1`; `--inner-jobs`
controls other internal pools, including the negative-control pool.
The slow lane ran in a single process until [D-484](defects.md): `BC-214` split the
lanes and gave xdist to the quick half only, leaving the half selected for costing the
most as the one place in the gate that ran a test suite serially.
Avoid assuming that either flag alone caps total host concurrency.

The screen and exhaustive shard jobs use `--jobs 1 --inner-jobs 4` on the hosted
four-CPU runners. The slow lane also has its own job, using `--jobs 1 --inner-jobs 2`:
xdist supplies four test workers, while tests that create their own pools retain two
inner workers. Each hosted deferred-check group runs one whole step at a time on its own
runner with `--jobs 1 --inner-jobs 2`, preserving PR #120’s response to the concurrent
corpus-pool timeout in
[run 34181619739](https://github.com/jlevy/squares/actions/runs/34181619739). The
workflow tests derive selections through the CLI and require complete, disjoint coverage
in both workflows. They also require full Git history wherever the slow retained-theorem
review runs.

The efficiency review records the
[allocation and measurement contract](docs/project/reviews/review-2026-09-29-validation-parallelism.md).
Fresh hosted results, rather than the predecessor jobs’ durations, establish the new
combined wall time. They do not establish a total process bound when tests spawn pools,
or a speedup. Certificate pools still enforce actual CPU availability, the four-worker
maximum, and the grid-memory budget.

CPU observations are diagnostic only.
Process counters can charge a child’s setup to the call that reaps it and omit
forkserver descendants; they cannot decide whether an individual test exceeds a CPU
ceiling or establish complete CPU savings.

### What each tier costs, and where its ceiling lives

[gate-budgets.yaml](packing/devtools/gate-budgets.yaml) declares each tier’s ceiling,
reference CPU and worker counts, and optional measured baseline.
Inspect it through `packing-validate --budgets`. The [tier table](#validation-tiers)
summarizes the ceilings; those values are not latency targets or GitHub job timeouts.

A run at the reference shape, or with `--enforce-budget`, fails above its ceiling.
With a recorded baseline it also fails above `drift_ratio` or below `stale_ratio`,
subject to the declared noise floor.
A tier whose hosted walls form a distribution records a `measured_band`, the lowest and
highest readings at its reference shape, and the ratios are then applied to the band’s
edges: the stale rule to the low edge and the drift rule to the high one.
The band must contain the record and be no wider than `drift_ratio / stale_ratio`; a
ceiling under its drift edge binds first (`think-be1s`, D-472). The price is sensitivity
in the fast regime: a run from the band’s low end can grow to the drift edge, or the
ceiling if lower, before a rule fires, and each banded tier’s record states that figure.
The records check independently rejects a ceiling above `max_headroom` times the
baseline. A `null` baseline leaves those ratio checks unarmed; a measurement printed by
CI does not update the file automatically.

**On a hosted pull-request run the drift and stale rules are advisory under
`think-be1s`, since 2026-10-01; the ceiling is not.** The register’s
`policy.pull_request_relative_rules` declares it, the way `pull_request_walls` declares
an advisory wall: `enforcing` when absent, and `advisory` only with a `tracking_bead`
and an `advisory_reason`, which `devtools.check_gate_budgets` refuses when the bead is
closed or unknown. The gate detects the run from the runner’s own `GITHUB_ACTIONS` and
`GITHUB_EVENT_NAME`, computes both rules as before, prints each finding as
`FAIL (advisory, not enforced)` with the bead, raises a warning annotation on the run,
and passes; a run over its ceiling still fails, and `--enforce-budget` overrides the
relaxation for an operator asking on purpose.
Off a pull request nothing changes.
The measurement behind it, 2026-09-30, is retained with every reading’s verdict in
`packing/tests/fixtures/tier-walls/hosted-readings-2026-09-30.yaml` and replayed by
`test_the_day_of_2026_09_30_is_judged_on_code_not_on_the_runner`: on unchanged steps the
`checks` tier read 59.4 to 137.1 s and shard C 62.96 to 143.87 s across one day’s hosted
runs, 2.3x apart with every test green, and the two rules failed four runs for the
runner they drew while a re-run of the identical commit passed.
The policy’s window around a point record is 2.5x, so no record can hold that pool, and
a single hosted reading cannot tell a slow draw from a slow change.
What can is a median over several hosted readings, which the wall register already
judges and `think-be1s` owns for the tiers, or a wall normalised by the runner’s
measured speed; until one of those judges a pull request, the ceiling is the rule a pull
request is held to.

A different CPU/worker shape reports the budget result without failing, unless
explicitly enforced.
Matching CPU counts alone does not establish comparable load or hardware.
`--only` invocations have no tier ceiling; per-command subprocess timeouts still apply.
The default subprocess timeout is 900 seconds, increased for steps with declared larger
budgets, including 1800 seconds for slow tests, negative controls and the full
translation escape screen, and 3600 seconds for exhaustive tests.
An explicit shorter timeout still wins.
The full checkpoint’s 3600-second tier declaration is not a universal wall limit on
split CI jobs. Preserve source, selection, runner, and cache information with timings
before promoting an observed value into a reference baseline.

### A pull request with no checks at all is a mergeability question

Zero check runs on a pull request does not mean CI has not started yet.
It also means GitHub could not build the pull request’s merge ref, which happens the
moment the branch conflicts with its base — and a `pull_request` workflow has nothing to
check out, so no run is created and no check appears.
The two look identical from the API, and the second one does not heal by waiting.

So when a push produces no check run within a couple of minutes, ask whether the branch
still merges before pushing again:

```bash
git fetch origin main && git merge-tree --write-tree HEAD origin/main >/dev/null \
  && echo "merges cleanly" || echo "CONFLICTS: no run will be created"
```

Measured on 2026-09-05 (`D-459`): five pushes over twenty-five minutes produced no run
and no check on `PR 83` while other branches in the same repository ran normally
throughout, because `main` had moved under it.
Resolving the conflict restored CI on the next push.
The failure mode is quiet in the dangerous direction — an absent check reads as pending
rather than as red — so the absence is what to investigate, not the wait.

**That command now runs on every push**, in
[`branch-mergeability.yml`](.github/workflows/branch-mergeability.yml), which is the one
placement that can fire at all: a `pull_request`-triggered check has the same blind spot
as the runs it would report on, because the defect *is* that no run is created.
A `push` event fires off the branch tip, which exists whatever the base is doing, and
its check run is keyed to the head commit — so it appears on the pull request, where the
missing runs would have been.

When it fails, it is telling you one thing: **no `pull_request` run will be created for
this branch until the conflict is resolved**, so the pull request’s checks will sit
pending rather than turn red.
The job summary lists the conflicting paths and the two commands that fix it.
A non-zero exit other than a conflict means git could not answer, and that is reported
as a failure too, because “the check could not tell” must not read the same as “the
branch is fine”.

What it does not catch is `main` moving under a branch nobody pushes to, which produces
no event on that branch.
In the measured incident the branch was pushed five times inside the window, so the
incident itself is covered; the residual is a labelled, approved branch left to sit, and
a future merge queue could close it by building the merge commit itself;
[queue enforcement is unavailable here](#the-deep-gate-the-deferred-surface-before-the-merge).

### Every pull request carries what it cost

Open or update a pull request and the description leads with the branch’s cost, then
reports the checked agenda closeout when the branch completed one:

```bash
uv run --frozen --all-extras --group dev python -m devtools.render_pr_rollup
```

It prints a markdown block — agent turns, model and thinking level, every tool called,
and the tokens behind them — for the checked-out branch, or for `--branch <name>`. Paste
it at the top of the description.
A reviewer can see what changed and otherwise cannot see what it took, and that number
has existed in `campaign/resource-usage/` the whole time.
For an agenda closeout, pass `--agenda agenda-NNN`; for a Codex session, also pass
`--session session-NNN`. The combined rendering preserves the cost block first, then
adds actual outcomes and stop reasons, dispositions, grouped file changes, validation,
documentation decisions, limits, ranked candidates, and the selected successor.
The final session command performs the generated-view and live-tbd reconciliation before
printing the same description:

```bash
uv run --frozen --all-extras --group dev python -m devtools.close_session \
  --render --session session-NNN --agenda agenda-NNN
```

A session that did not close an agenda still fills
[`.github/PULL_REQUEST_TEMPLATE.md`](.github/PULL_REQUEST_TEMPLATE.md) by hand.
The cost block is the opening, not the description.
Check the filled body before updating the pull request:

```bash
uv run --frozen --all-extras --group dev python -m devtools.check_pr_description --file BODY.md
```

The same command with no arguments checks that the template still carries the required
headings. Filled mode also refuses a Cost that enumerates every experiment wall.
`OR-9` treats that dump as unfinished, headings or not.

**The attribution is a bound and the block says so.** `turns.by_branch` is the only
branch-aware field in `ClaudeEfficiencyRollup`, so a log that ran on more than one
branch has an exact turn count here and no way to split its tokens or tool calls.
The block prints three columns — on-branch logs only, prorated by turn share, and every
log that touched the branch — of which the outer two are measurements and the middle is
the estimate to quote.
Do not replace them with a single number: the interval is wide because the measurement
is, and narrowing it needs a branch-aware token count that the harness does not emit.

The gate step `the branch cost rollup renders` runs the renderer over every branch in
the records, including one no rollup mentions, because a division by a turn count fails
on exactly that edge.

## Publishing the Explainer

For every newly retained result, first complete the
[new result publication sequence](packing/campaign/documentation-pass.md#new-result-publication):
update the frontier, README and atlas data, and re-pin the data revision.
The survey posters are not redrawn for a result; they are
[release assets](#release-assets-are-drawn-at-a-version-bump-or-on-demand).
That sequence also applies when no explainer edition changes.

**The site’s two papers are served under `papers/`, each by its slug**, and the slug is
the paper’s name in the source too (see
[conventions.md → Naming](conventions.md#2-naming)): `n11-lower-bounds-explainer`, “New
lower bounds for square packing for n = 11”, and `n11-optimality-review`, “A review of
the optimality proof of the Trump packing of 11 squares”.
Each is `papers/<slug>.html` with `papers/<slug>.md` and `papers/<slug>.pdf` beside it.
A renderer is given the site’s root (`--site`, by default `packing/site/`) and writes
its paper there, where it is served, so every check reads the page at its published path
and the publication renames nothing.

The explainer at
<https://jlevy.github.io/squares/papers/n11-lower-bounds-explainer.html> is not checked
in. GitHub Pages builds it from `main` in `.github/workflows/pages.yml`, on every push
that touches one of the renderer’s declared inputs (`RENDER_INPUTS` in
`devtools/render_n11_lower_bounds_explainer.py`, which a test ensures the workflow’s
path filter covers).
The build writes the page (`site/papers/n11-lower-bounds-explainer.html`), the Markdown
edition beside it (`.md`), the PDF (`.pdf`, drawn by Playwright’s Chromium), and the
atlas’s composite assets at the site’s root, where the overview links them too and a
link preview names the card.
It checks that the prepared HTML reproduces itself and compares the stored PDF with a
fresh render, including the receipt that binds it to the HTML source.
Font and page-count checks inspect that stored PDF. The workflow uploads the checked
bytes unchanged; deployment waits for the print-layout and browser checks.
A pull request runs the same build without deploying, so a render that breaks fails
review rather than the next deploy.
It builds only the pages its changes can affect: the workflow’s `scope` job runs
`devtools.pages_scope`, which reads each builder’s `RENDER_INPUTS` and the tools the
workflow runs for that page, and a page none of the changed files touches is skipped by
a job named for the reason.
`pages-required` is the aggregate a branch rule would require; it passes such a skip and
nothing else.

The separate **T-060 optimality paper** lives at `/papers/n11-optimality-review.html`.
Its source is
[`n11-optimality-review-article.md`](packing/devtools/templates/n11-optimality-review-article.md);
[`render_n11_optimality_review.py`](packing/devtools/render_n11_optimality_review.py)
uses the same KPress fonts and
[`paper-publication.css`](packing/devtools/templates/paper-publication.css) as the
historical explainer for screen and print typography, metadata, and format links.
Its separate stylesheet contains diagram layout only.
It takes the publication layer whole, the stylesheet with the head script its math rule
reads the platform from (`render_n11_lower_bounds_explainer.publication_layer`), and
typesets its mathematics with the pipeline every page of the site shares
(`render_n11_optimality_review.math_scripts`); the Math section of
[`paper-design.md`](packing/devtools/templates/paper-design.md) says why both matter.
It reuses the Trump witness rendering and draws the center cells and capture graph from
the retained proof packet.
From `packing/`, with the scratch environment required by `AGENTS.md`:

```bash
uv run --frozen --all-extras --group dev python -m devtools.render_n11_optimality_review --pdf
```

The outputs are `site/papers/n11-optimality-review.html`, `.md`, and `.pdf`. `--site`
selects another site root; `--check` compares the HTML and Markdown without writing.
Repository citations name the source commit selected by `--revision` (the publication
revision by default).
A dedicated Pages job builds this paper and its PDF independently of the historical
explainer. The paper is an explanation of accepted evidence, and rendering it does not
rerun the geometric proof.

Publication uses `python -m devtools.render_n11_lower_bounds_explainer --prepare-math`
after installing the locked Playwright Chromium.
This pass measures the final math bases under the page’s CSS and ships their geometry
with the initial HTML, so decoding a font does not change the space a formula occupies.
It prepares the supported custom/system and serif/sans settings, shares identical
fragments, and uses the head bootstrap’s root attributes to select one before paint.
The client hydrates that selected fragment.
Geometry checks require a reservation for every visible base, including when a saved
preference changes the selected font profile.
`--prepare-math --check` repeats the same preparation before comparing bytes.
The pure `render()` function remains available for source and certificate tests that do
not need a browser. The canonical
[font and math loading architecture](vendor/kpress/docs/project/architecture/arch-2026-09-08-font-and-math-loading.md)
lives in KPress, alongside the shared runtime’s public API documentation.

The prepare job renders the page twice at once, requires the two renders to agree, and
shares one page artifact with the Chromium PDF, print, typography, screen and geometry
jobs and the Firefox/WebKit loading and geometry jobs, which run in parallel.
Deployment waits for all of them.
The workbench job selects Node 24.18.0, installs the root lockfile with scripts
disabled, and builds the typed workbench package into the self-contained `/workbench/`
page, beside `prepare` rather than after it.
The publish job puts the two papers, the checked PDF, the site’s own pages and the
workbench back into one tree; only a push to `main` uploads that tree to Pages.

**An address the site has served keeps working.** The papers moved to `papers/<slug>` on
2026-10-01, from `explainer.html` and from `n11-optimality/t-060-explainer.html`.
`render_overview.MOVED_PAGES` lists each page that moved, and the overview’s build
writes a forwarder at each old address: a page of a few lines whose script
(`devtools/overview/forward.js`, the one the overview forwards its own old fragments
with) sends the reader on with the query string and the fragment they came with, with a
refresh and a link for a reader without scripts and the new address as its canonical
URL. `render_overview.MOVED_FILES` lists each file that moved and cannot forward, a
paper’s Markdown and PDF; the publish job copies each to its old address, and a test
holds that step to the list.
Nothing on the site links an old address.
`check_published_site` asks the deployed site for every one of them, and visits each
forwarder in the pinned browser with a query string and a fragment.
To move a page again, add it to the list; do not delete an entry.
Before drawing PDF bytes, the exporter checks that visible math is typeset; a completed
font-error fallback that exposes literal TeX fails this check.
Readable native MathML fallback is accepted by that check and remains subject to the
separate PDF font policy.
Pages exercises the production exporter with normal math and injected font errors and
timeouts once it has drawn the publication candidate: the normal-math control reads that
PDF rather than drawing it again, and each fault control drives a draw of its own.
These browser controls require the prepared page and pinned Chromium in Pages; the
Python-only validation jobs leave them to that dedicated invocation.
The PDF command `--check-artifact` requires an existing PDF and never rewrites it;
`--check` remains available for repeated fresh-render diagnosis.
On a reproduction disagreement, `--diagnostics-dir` retains the two raw PDFs and a
neutral difference report in a separate directory for that invocation.
Pages uploads those diagnostics on failure with seven-day retention.
Download them before rerunning the job: GitHub can make a previous attempt’s artifacts
unavailable on a rerun, even when their names differ
([upstream report](https://github.com/actions/upload-artifact/issues/585)). Normal
parameter startup and neighboring text movement are measured by
`devtools.check_math_startup`; its controlled fixtures run in CI, while timing
comparisons are retained in the
[math startup campaign](packing/benchmarks/math-startup/README.md).
The site’s other pages load math through the same pipeline, typeset in the client;
[paper-design.md → Math Loading](packing/devtools/templates/paper-design.md#math-loading)
describes it and records its load timings, which `devtools.measure_site_pages` measures.

**Merging is the whole publish.** Every repository link on the site names `main`, the
branch the site deploys from, through one helper
([`packing/devtools/repo_links.py`](packing/devtools/repo_links.py)), and nothing has to
be bumped for the links to be right.
A link to the commit a page was built from 404s once a squash merge leaves that commit
on no branch, so `check_published_site` refuses any repository link that names a commit
hash, and checks that every path linked on `main` is in the deployed commit’s tree.
The reader documents the site links by name (the status table, the results register,
`epistemics.md` and the rest) are constants in that module, so each has one stable path.
The committed claim documents are the one exception: they are not site pages, and they
pin the verifier at the edition’s revision
(`render_n11_lower_bounds_explainer.edition_file`). After a merge, wait for the
“Certificate page” workflow on `main` and confirm the deploy from the checkout:

```shell
uv run --frozen --all-extras --group dev python -m devtools.check_published_site --commit <merge commit>
```

It fetches the live pages, both papers with their Markdown editions and PDFs, the assets
and the workbench. It checks the explainer edition, verifies that repository links name
and resolve at the expected commit, and requires the PDF source receipt to match the
exact served HTML bytes and its page count to match the publication.
It also requires the workbench’s exact source revision, starts its public API in pinned
Chromium, and follows its project-relative link to the overview.
It asks for every address a paper used to have, as the paragraph above says.
Whether a link resolves is not whether it is there, so the check also asks the renderer
what record links it writes at that commit: every result row of the overview and the
results page carries its own, and the overviews of three sampled results carry every
repository link the renderer writes for them ([D-512](defects.md)). Run it from a
checkout at the deployed commit, since the register it reads is the checkout’s.

The check also reads every page’s head for the site’s identity and link-preview tags and
fetches the card they name:
[paper-design.md → Page Metadata and Social Cards](packing/devtools/templates/paper-design.md#page-metadata-and-social-cards)
has the rule. `--local DIR` asks only that, of a site built into a directory, and
`devtools.preview_site` runs it on every build.

The whole check also runs on a build before it is deployed.
`python -m devtools.preview_site --output DIR --serve` builds the whole site into one
directory and serves it at `http://127.0.0.1:8765/`, and
`python -m devtools.check_published_site --site http://127.0.0.1:8765/ --commit <the commit the build was made from>`
asks it the same questions; a local address is the one kind that is not https and is
still asked. A preview has the first paper’s PDF only if one is put there: that PDF is
drawn from `packing/site/` by `render_n11_lower_bounds_explainer_pdf`, which a preview
never writes.

**One version, shared by the site and its data** (the owner, 2026-09-22): every site
page’s footer and the workbench stage print `PUBLICATION_EDITION` from
`src/sqpack/release.py`, written like `v0.4.1-3b50e2`. The version comes from the first
entry in `PUBLICATION_HISTORY`, and the six characters after it name the data.
The atlas posters and the films carry the same spelling at the data commit each was
drawn from, as
[Release assets](#release-assets-are-drawn-at-a-version-bump-or-on-demand) describes.
The six characters after the version name the data, not the build: they are the pinned
`DATA_REVISION`, the last commit that changed `DATA_PATHS` (the frontier records and the
atlas data), so artifacts built from the same data carry the same version whatever code
commit built them. Nothing reads git for it at build time, which is why a shallow deploy
clone stamps correctly.
The claim documents still link to the pinned `PUBLICATION_REVISION` (`edition_file()`),
which moves only when an edition is cut.

**`PUBLICATION_HISTORY` is the site’s edition record.** It lists every edition ever
published, newest first, and an edition never comes off it — a new one goes on the
front. It used to keep “the two retained editions”, and adding v0.4.1 under that rule
dropped v0.3.0, the proof of s(11) ≥ 381/100 the publication began with.
Each date is when that edition was first *live on the public page*, read from the
repository’s GitHub Pages deployments, not when its version label first appeared in Git.
The two differ in both directions — v0.3.0 went live on September 5 and was named on
September 8; v0.4.0 was named on September 10 and went live on September 13 — and the
deployment behind each date is recorded beside the list.
No page of the site lists this record: the first paper did until 2026-10-02, when it was
the paper’s own history, and a site-only edition read as an edition of the paper.
A reader finds it in `release.py` and here.

**The papers are versioned on their own, and the site’s version goes on no paper** (the
owner, 2026-10-01: “the repository version should not go on the papers anymore.
Papers should be individually versioned”). Each paper’s version line prints its own
version from `release.py`: the explainer’s is `EXPLAINER_VERSION`, the newest entry of
`EXPLAINER_HISTORY`, and the review’s is `OPTIMALITY_REVIEW_EDITION`, its status and the
newest entry of `OPTIMALITY_REVIEW_HISTORY` (“Draft v0.1.3”). The top of the explainer
reads, on two lines, like “v0.4.2 (version history)” and “First published September 5,
2026 · Last revised October 1, 2026”: which version of the paper is being read, with a
link to the paper’s own editions at the foot of the page, then when the paper first
reached a reader and when the article last changed.
Both papers write their front, the formats row, the title and the credits, from one
component (`devtools.paper_front`), and `devtools.paper_structure` compares the two
rendered papers axis by axis
([paper-design.md → The Papers’ Front](packing/devtools/templates/paper-design.md#the-papers-front)).
The first date is `EXPLAINER_FIRST_PUBLISHED`, the paper’s oldest edition’s, so it does
not move.
The second is `EXPLAINER_REVISED`, the date of the last commit that changed the
article, which is changed in that commit; [Dates](#dates-on-generated-artifacts) has the
rule. The colophon on a paper is the site’s two lines without the version part
(`render_overview.colophon_lines(edition="")`): the project and its repository, then the
credit to Flowmark and KPress.
`PUBLICATION_EDITION`, `PUBLICATION_STAMP` and the data hash appear on no paper page, in
no Markdown edition and in no PDF; `tests/test_n11_lower_bounds_explainer.py` and the
review’s tests hold that, and `check_published_site` refuses a served paper that carries
the site’s edition or lacks its own.

**A paper’s history lists the editions in which the paper changed, and nothing else.** A
published number under which the paper changed stays exactly as published, number and
date, and is never renumbered; an edition under which the paper did not change is not a
version of the paper and is not in its history (the owner, 2026-10-01). The explainer
carried the site’s number while the two were one, so `EXPLAINER_HISTORY` keeps v0.4.2,
v0.4.0 and v0.3.0 at the site’s dates and drops v0.4.1 and v0.5.0, under which the
article did not change; the comment on it records what changed in the paper under each
and the commits read.
v0.4.3 is the paper’s first number of its own, a patch revision for the changes the
article took after the v0.4.2 deployment, dated by the deployment that first served it
in that substance.
`tests/test_release.py` holds the shared editions to the site’s record
and the site-only ones out.
Each entry’s sentence says what changed in the paper, and the explainer’s Version
History is written from the list.

**A release is cut only to host generated assets.** The site’s version is complete when
the merge deploys and `check_published_site` passes; no tag and no GitHub release follow
a version bump (the owner, 2026-10-01: releases “are only important for the assets that
are generated, like the PDFs or the videos”). A release exists to give an asset a
download address, which only the films need: they are linked through
`render_overview.FILM_RELEASE` (currently `v0.4.2`) and stay on the release that carries
them until they are cut again.
The posters are served from the site itself, and the papers’ PDFs are built by Pages
from the merge. A release tag carries the version alone, without the data revision:
`v0.4.2` is `PUBLICATION_VERSION`; the stamp in a frame’s corner is
`PUBLICATION_EDITION`, which appends the data revision.
A tag names a release; a stamp names the evidence one artifact was drawn from, and a
release may carry assets drawn from different revisions.

**Videos are published as release assets, never committed.** The whole route -- why not
Actions artifacts, Git LFS or a committed file; the tag; the upload’s content type; the
receipt that travels with each video; and the `<video>` embed with its codec string --
is
[Publication](docs/project/specs/active/plan-2026-09-21-video-delivery-profiles.md#publication)
in the delivery-profiles plan.
To re-cut and publish them, follow
[Regenerating and publishing the ascent videos](packages/workbench/README.md#regenerating-and-publishing-the-ascent-videos),
the ordered runbook from prerequisites to the post-merge check.

**After any commit that changes the data, re-pin, which is one line.** A commit cannot
contain its own hash, so a data change is followed by a second commit that sets
`DATA_REVISION` to the data commit:

```bash
uv run --frozen --all-extras --group dev python -m devtools.release_pin --update
```

`tests/test_release.py` fails until it does, and names the command.
Nothing is rebuilt for it and no binary changes.
Only a branch’s head has to agree; a merge keeps the branch’s data commit unless main’s
data moved too, and then the merge is the data commit and the branch re-pins after
merging `main`.

### Release assets are drawn at a version bump, or on demand

The atlas posters (`known-best-1-100` and `known-best-1-324`, each an SVG with its PNG
and PDF exports) and the films are expensive to draw and large to keep, so they are
drawn when the version is bumped and when someone asks, never because the data moved
(the owner, 2026-10-01). Each states what it was drawn from.
A poster records the data commit and that commit’s date in its SVG metadata, prints them
as its footer stamp and its dateline, and binds its PNGs and PDF to the SVG by digest
receipts. A film’s frames carry the stamp they were captured with.

A poster may therefore trail the data between bumps.
While its data revision is the pin, every label on it must agree with the figure record.
Once the pin has moved, the cards that differ are listed by every check and fail none.
A version bump fails every poster until it is redrawn.
`COMPOSITES_MAY_TRAIL` in `release.py` is the switch; `False` makes a trailing card a
failure. From `packing/`:

```bash
# Hold the retained posters to their own records. Rebuilds nothing; about five seconds.
uv run --frozen --all-extras --group dev python -m devtools.build_known_best_atlas --check-composites

# Redraw both posters and their six exports from the retained witnesses. About a minute.
uv run --frozen --all-extras --group dev python -m devtools.build_known_best_atlas --update-composites
```

`--update-composites` refuses a stale pin and uncommitted data, since the stamp it draws
has to name the data in the tree.
`--update` rewrites the data layer alone: witnesses, renderings, manifest and frontier
links. [The plan](docs/project/specs/active/plan-2026-10-01-release-assets-on-demand.md)
has the measurements behind this and the options that were weighed, and
`python -m devtools.measure_release_assets` repeats them.

### Dates on generated artifacts

Each date has one rule, and `python -m devtools.artifact_dates` prints every date with
its source and whether it is what the rule gives:

- A date derived from a commit is the commit’s author date, on the author’s own
  calendar.
- A paper’s “revised” date is the date of the last commit that changed its article.
  The explainer’s is `EXPLAINER_REVISED` and the optimality paper’s is
  `OPTIMALITY_REVIEW_REVISED`, both in `release.py`, where each paper’s front reads it
  (`devtools.paper_front`). Change it in the commit that changes the article;
  `tests/test_artifact_dates.py` fails when it stands still.
- A poster’s dateline is the date of the data commit it was drawn from.
- A PDF’s `CreationDate` and `ModDate` are the date on its face, at noon UTC, and never
  the build clock.
- A date a person asserts stays typed: an edition’s first publication, the day a source
  published its proof, the day the register was reviewed.

### Cutting an edition

Bumping the site’s version is editorial, and it is when the release assets are redrawn.
Use at most one publication patch bump per merge, and keep the chosen version fixed
throughout a pull request.
One command prepares the bump and prints what is left.
From `packing/`, on a clean tree whose pin is current:

```bash
uv run --frozen --all-extras --group dev python -m devtools.cut_release v0.5.0 \
    --scope "One sentence on what the edition adds."
```

It does these, and `--dry-run` lists them without doing any:

1. Adds the edition to the front of `PUBLICATION_HISTORY`, dated by `--date` (today in
   UTC by default; correct it if the deployment lands on another day), and sets
   `PUBLICATION_REVISION`, the commit the claim documents link to, to `HEAD`.
   `DATA_REVISION` follows the data, not the edition.
2. Redraws both posters and their exports (`build_known_best_atlas --update-composites`;
   see the cairo note under Supported Environment).
3. Regenerates the claim documents (`render_verifiable_claim`).
4. Runs `--check-composites` and
   `pytest tests/test_release.py tests/test_n11_lower_bounds_explainer.py tests/test_verify_claim.py tests/test_known_best_composites.py tests/test_artifact_dates.py`.

It commits nothing and publishes nothing, and it moves no paper: a site bump adds no
entry to any paper’s history and changes no paper’s version line.
What it prints for the owner to do: commit the release module, the eight atlas files and
the generated documents together and merge them, with README’s edition sentence updated;
wait for the “Certificate page” workflow and run `check_published_site`, which completes
the version; correct the date and record the deployment above the history.
No tag and no GitHub release: a release is cut only when there are generated assets that
need a download address, the films, and they stay on `render_overview.FILM_RELEASE`
until they are cut again
([Regenerating and publishing the ascent videos](packages/workbench/README.md#regenerating-and-publishing-the-ascent-videos)).
The papers’ PDFs are built by Pages from the merge.

### Bumping a paper’s version

A paper’s version moves when the paper changes in a way its author calls a new version,
and only then; a site bump, a re-pin, a redraw of the posters and a change to the page’s
chrome are not versions of the paper.
It is one edit, in the commit that makes the change, with no command:

1. Add a `PublicationHistoryEntry` to the front of the paper’s history in `release.py`
   (`EXPLAINER_HISTORY`; the review gets one as the explainer’s when it leaves
   `OPTIMALITY_REVIEW_VERSION` behind, linked from its front through
   `PaperFront.history`): the new number, the day it will first be published, written
   `October 2, 2026`, and one sentence on what changed in the paper.
   The number is the paper’s own and is not the site’s; a number already published is
   never changed.
2. Set `EXPLAINER_REVISED` (or `OPTIMALITY_REVIEW_REVISED`) to the commit’s date, as any
   change to the article requires; `python -m devtools.artifact_dates --check` and
   `tests/test_artifact_dates.py` hold it to git.
3. Where the entry points name the paper’s version, update them: TUTORIAL.md names the
   explainer’s (`test_reader_facing_version_references_follow_release_metadata`).
4. Run
   `pytest tests/test_release.py tests/test_n11_lower_bounds_explainer.py tests/test_paper_structure.py tests/test_artifact_dates.py`.
   The explainer’s Version History is written from the list, so a longer history can
   move its PDF’s page count; draw the PDF and update `EXPECTED_PAGE_COUNT` if it does.

The version line and the history on a paper reflect versions of the paper, not of the
website or anything else.

## Focused Quality Commands

Use direct tools when their output is the point of the edit:

```shell
uv run --frozen --all-extras --group dev pytest -q
uv run --frozen --all-extras --group dev ruff check --config pyproject.toml . ../packages/workbench
uv run --frozen --all-extras --group dev ruff format --check --config pyproject.toml . ../packages/workbench
uv run --frozen --all-extras --group dev basedpyright

cargo test --locked --manifest-path sqsearch/Cargo.toml
cargo clippy --locked --release --all-targets --manifest-path sqsearch/Cargo.toml -- -D warnings
cargo fmt --manifest-path sqsearch/Cargo.toml --check
RUSTDOCFLAGS="-D warnings" cargo doc --locked --manifest-path sqsearch/Cargo.toml --no-deps

cd ..
npm ci --ignore-scripts
npm run check --workspace @squares/workbench
```

The `lint floor (rust)` validation step runs formatting, all-target Clippy, the crate’s
unit and integration tests, and rustdoc under the pinned Rust toolchain.
The manifest denies warnings, missing documentation, pedantic lints and `unwrap_used`,
with the geometry-specific exceptions documented beside their settings.
The crate forbids unsafe code.
These checks cover `sqsearch`; archived third-party verifier sources require their own
source-bound builds and replay checks.

The separate `sqverify_exact` crate implements optional exact rational rectangle
geometry. From `packing/`, after setting the task scratch environment required by
`AGENTS.md`, run its complete focused gate:

```bash
uv run --frozen --all-extras --group dev packing-validate --only "exact rectangle Rust geometry"
```

That gate uses the crate’s pinned toolchain, runs rustfmt, Clippy, tests, rustdoc and a
locked release build, then compares exact results with the Python reference.
It leaves the binary at `$CARGO_TARGET_DIR/release/sqverify-exact` when the target
directory is absolute.
Pass that path to `devtools.verify_rectangle_density` with
`--backend rust --rust-binary PATH`; Python remains the default.
The [tooling overview](docs/project/verification-tooling.md) records the supported
inputs, refusal behavior, golden controls and measured performance limits.
This crate verifies rectangle geometry, a separate contract from the global n11 proof.

The native rectangle CLI has
[five golden scenarios](packing/tests/golden/rectangle-density-cli/) covering complete,
partial, capped, counterexample and admission-refusal results.
Run `uv run --frozen pytest tests/test_rectangle_density_cli_golden.py` from `packing/`.
To approve an intentional output change, set `UPDATE_RECTANGLE_DENSITY_CLI_GOLDEN=1` for
that command, then review the full fixture diff.
The tests separately check mass, angle census, exact counterexample values and
input/source binding; approving output does not replace those assertions.

Ruff must be clean. BasedPyright runs in standard mode and must report zero diagnostics
across maintained and retained Python.
Its documented exclusions cover dynamically shaped YAML, JSON, and third-party
scientific-library boundaries; this project does not claim strict-mode coverage.
A per-file exception must name the narrow reason beside the configuration; never exempt
a maintained module from a rule family for convenience.
Use modern Python 3.14 syntax, absolute imports, `Path`, precise public-boundary types,
and exception chaining.
The enabled rule families include the pytest-style, unused-argument, blind-except,
commented-out-code, refurb, f-string and complexity-ratchet families, each argued for
beside its entry in `pyproject.toml`; printing is waived only where the tools live, so a
library module reports through `logging`. Python under `packages/workbench/` and the
hand-written skill assets under `.agents/skills` are also under the same two floors.
Comments explain non-obvious intent, invariants, units, evidence limits, and rejected
alternatives—not a line-by-line translation of the code.

The workbench’s stylesheet is under a design contract as well as Biome.
Its design values live only in the token block at the top of
`packages/workbench/assets/workbench.css`, and inline style writes are counted.
`npm run check` enforces both, along with WCAG AA contrast.
`check_frontend` measures the page’s shared layout at three viewports.
See the package README’s [Design system](packages/workbench/README.md#design-system)
section before changing either.

Markdown is owned by Flowmark at repository root.
Durable documentation follows the common documentation guidelines and carries their
footer. Run the repository hook or `make format`; do not introduce a second Markdown
formatter.

### Probing the promotion pipeline

**Reach for these before writing a one-off script.** Both exist because a finding that
overturned something in the record was first made in a throwaway probe, which is the
wrong place for a measurement the next reader has to be able to replay.

```shell
uv run --frozen --all-extras --group dev python -m devtools.probe_contact_system
uv run --frozen --all-extras --group dev python -m devtools.probe_contact_system --case trump11 --walk
uv run --frozen --all-extras --group dev python -m devtools.probe_minimal_polynomial --case trump11
uv run --frozen --all-extras --group dev python -m devtools.probe_system_degree --eliminate-side
```

[`probe_contact_system`](packing/devtools/probe_contact_system.py) reports, per retained
case, what the assembled contact system determines: the typing, the equations against
the unknowns, the Jacobian’s rank and the gap that verdict rests on, the residual at the
pose, `side_leak`, and what `close` does — where `close` supplies conditions, the rank
and residual are re-measured on the closed system, so “it closed” is a measurement
rather than a count of conditions.
`--walk` steps a direction the equations leave free and reads the violation’s **order in
$t$** — $O(t^2)$ is an ordinary second-order obstruction, $O(t)$ means an equation is
not describing its constraint.
That distinction is the whole of `D-361`. Which direction it walked is printed, because
there are two: the steepest side-changing one where the null space contains such a
direction, and the free direction itself where it does not, as at Göbel’s $n = 5$.

[`probe_minimal_polynomial`](packing/devtools/probe_minimal_polynomial.py) runs the
integer-relation search under the promotion spec’s frozen margin rule and reports which
clause decided each degree.
It sweeps to the degree the digits reach rather than to a fixed ceiling.
Clause 3 read backwards at the search’s own coefficient bound puts that at **degree 35**
for the $n = 29$ refinement at a thousand digits, where the flag used to stop at twenty
for no reason but the default; `--max-degree` still stops it earlier, which is usually
what you want, because the cost is almost all `pslq` and it climbs steeply with the
degree.

[`probe_system_degree`](packing/devtools/probe_system_degree.py) rationalises the
$n = 29$ system by the half-angle substitution and reports what bounds the algebraic
degree of the Kingbird solution, which is what says whether an integer-relation refusal
at a given degree surveyed the space or a corner of it.
`--eliminate-side` also solves the smallest equation for $s$ and reports the
five-unknown system that leaves.
The $n = 29$ sweep takes about twelve minutes, which is why it is a tool with a recorded
result rather than a test.

Both pin their working precision per case and print it beside the number it bounds.
That is not decoration: a rank verdict is a judgement about a gap between singular
values, and at mpmath’s ambient default the gap a probe can *see* is many decades
narrower than the truth, with nothing in the output to say so.

## Browser Code Lives in Files

**No JavaScript in a Python string, with no exceptions.** Browser code lives in `.js`
and `.ts` files, where Biome formats and lints it and `tsc` type-checks it.
A Python string is invisible to all three, which is how a TeX escape doubled inside an
f-string once reached a rendered page.
The rule covers page probes, Playwright init scripts, Node scripts run by tests, and
`<script>` bodies built in Python; tests and spikes included.

A Python tool that drives a page uses a **probe**:

1. Write one JavaScript expression, normally an arrow function taking one argument
   object, in `probes/<tool>/<name>.js` beside the tool: `packing/devtools/probes/`,
   `packing/tests/probes/`, or a spike’s own `probes/`. Declare any page global it reads
   in a `.d.ts` in the same tree.
2. Load it with `probe(PROBES, "<tool>/<name>")` from `sqpack.probes`, where `PROBES` is
   that `probes` directory, and pass values as Playwright’s one argument:
   `page.evaluate(probe(PROBES, "check_layout/slots"), {"n": 26})`. Never format a value
   into the text. `add_init_script` takes no argument, so give it
   `applied(probe(...), argument)`, which serialises the argument as JSON.
3. Write the name out whole.
   `devtools.check_probes` reads names from string literals, and a probe no literal
   names fails as unused.

**One probe that needs another’s function takes a handle to it, never its text.**
Playwright calls a function-valued evaluation, so a probe other probes compose is a
*reference probe* whose file returns the function, or an object of functions, rather
than being one. A composer receives it in its argument as
`page.evaluate_handle(REFERENCE)`, and a direct caller evaluates `applied(REFERENCE)`,
which is the function itself.
`probes/math/library.js` is the explainer’s: `activeVariant`, `exposed`,
`requiredFonts`, `fontLoadObserver` and `mutatedMath`, written once for every checker.
An init script takes no argument and so no handle; it reads the global an earlier init
script installs, as `check_math_loading.MATH_LIBRARY_INIT` installs the library for
`FIRST_PAINT_SCRIPT`.

The probes are in Biome’s scope and under the ESLint promise overlay.
`packing/devtools/probe-typecheck.json` assigns each group to its own strict TypeScript
program, so ambient declarations in an unrelated group cannot satisfy a probe.
The manifest names each intentional shared declaration, and
`packing/devtools/node/typecheck-probe-groups.mjs` discovers every probe in those
groups.
A Node script a Python tool runs goes in `packing/devtools/node/`, and one a test
runs goes in `packing/tests/node/<test module>/`, both under
`tsconfig.devtools-node.json`. A test script that exercises a probe against stand-ins
loads the probe file itself through `packing/tests/node/probe.mjs`, so what runs under
Node is what runs in the page.
The workbench package’s `workbench_tools.probes` is the same loader bound to
`packages/workbench/probes/`.

Two checks hold the rule, and both run in `--edit` and on every pull request as the
`browser code lives in files` step:

- `devtools.check_no_embedded_js` parses every Python file and fails on a built script
  argument to Playwright’s evaluate family, a string that matches a JavaScript
  signature, or a `<script>` body written in Python.
  Its signatures and enforced empty allowlist are in
  `packing/devtools/embedded-javascript.yaml`. Any detected site fails the check;
  `--inventory` prints every site.
- `devtools.check_probes` fails on a probe that does not evaluate to a function, one no
  Python file beside its tree names, and a name no file answers.

`tests/test_no_embedded_js_contract.py` plants each forbidden form and requires the
guard to refuse it; three negative controls in `devtools/controls.yaml` do the same
against the real tree.

## Safe Refactoring

Use red-green-refactor for a behavior change and characterize intended behavior before a
structural move:

1. Identify the public behavior, persisted record, or scientific claim at risk.
2. Run its focused check and capture the clean baseline.
3. Add a failing test for corrected behavior, or a characterization test for correct
   behavior that is not yet protected.
4. Make one bounded change and keep structural movement separate from semantic change.
5. Run focused tests, Ruff, formatting, types, and the relevant exact, property, replay,
   or differential check.
6. Run full validation at the integration checkpoint.
7. Review a golden diff as a behavior change.
   Never regenerate a golden merely to make validation green.

Tests should be deterministic and behavior-focused.
Avoid network access, wall-clock assertions, uncontrolled randomness,
implementation-detail mocks, and tests that only prove a mock was called.
Include boundary values and failure paths.
A bug fix gets a test that fails for the old defect.
A new guard gets a negative control showing that the named corruption reaches it.

## Hashes and Repository-Owned Artifacts

Git is the integrity boundary for repository-owned sources, golden files, and retained
results. Compare their complete content or regenerate and compare their semantic model;
do not add SHA-256 fields or checksum controls for files committed beside the checker.

A cryptographic checksum is justified only when it is compared with an independently
supplied value across a real trust boundary.
The nearby code or documentation must name that boundary and the failure the comparison
detects. Compact content identities used for deduplication, append-only event ids, or
cache correctness are not integrity claims and must name that separate function.

Four shapes are ceremony here and are refused in review: a tool that hashes its own
source or its kernel’s and refuses a checkpoint or receipt whose digest differs; a
ledger or registry that lists verifiers, receipts or receipts-of-receipts by SHA-256; an
audit that compares a working file to its historical Git blob and fails on difference;
and a frozen copy of code kept so that bytes can be compared.
The shape that replaces all four is a provenance record: the blob id of the bytes the
process imported (`git hash-object`, or `hashlib.sha1(b"blob %d\0" + data)` as
`check_n17_local_minimum` does), the revision, and whether the tree was dirty; it is
recorded and never compared.
Determinism is a fixture test: produce a small instance and compare its bytes with the
committed fixture (`test_verify_n17_certificates`’s W7 at bins 8 is the model).
Content addressing may name files and deduplicate; a name is not a check, and a loader
does not refuse a file for not hashing to its name.
The
[integrity-ceremony audit](docs/project/reviews/review-2026-10-03-integrity-ceremony-audit.md)
inventories every instance with its verdict and the slices that remove them.
`devtools.check_integrity_ceremony` counts the two detectable forms, a module hashing
its own or a sibling’s source and an `==` or `!=` on a digest, in every tracked Python
file that is not a test and is outside the allowlist in
`devtools/integrity-ceremony.yaml`, where each listed file names its boundary by kind (a
download, an external checkout, a generated artifact, a legacy manifest).
Every other file may not rise above its per-file baseline.
A fall is never a finding, so removing ceremony costs no bookkeeping; `--update`
tightens the baseline when convenient.
Tests are not scanned: a test asserting that a receipt names the digest of what ran
refuses nothing at run time.
The step `integrity ceremony never grows` runs it in the edit tier.

Pytest collection is explicit in `pyproject.toml`; `tests/conftest.py` fails if the
configured test directory disappears.
Domain programs are named by what they check, not with `_test.py`, so pytest cannot
silently collect or omit them by accident.

## Durable State and Compatibility

Repository-owned callers are migrated together.
Do not retain an alias, wrapper, old module path, or compatibility branch without a
named external consumer.
There are no known external `sqpack` consumers, server APIs, plugin APIs, or databases
at this time.

Campaign, basin-event, atlas, and certificate formats are real persisted contracts.
Version them, reject unsupported versions clearly, and migrate only when retained older
data must remain readable.
Never reinterpret historical records in place.

Write generated views and complete artifacts through `strif.atomic_output_file` so a
crash cannot expose a partial replacement.
Validate before promotion.
Append-only campaign journals are the deliberate exception: each line is independently
validated, and a partial archive is retained as recovery evidence rather than presented
as a complete result.

Generated files name their producer.
Use:

```shell
uv run --frozen packing-ledger check
uv run --frozen packing-ledger render
uv run --frozen python -m devtools.render_defects --check
uv run --frozen python -m devtools.render_research_tables --check
uv run --frozen python -m devtools.render_document_map
uv run --frozen python -m devtools.render_results --update
uv run --frozen python -m devtools.render_results_headline
```

README carries no results tables; the site’s overview renders the results from the
register, the case records and the bibliography (`devtools.render_overview`). Edit the
records and re-render; a hand edit to a generated view fails its `--check`.

**Creating any durable Markdown file is a two-step change.** Register it in
[`docs/project/document-map.yaml`](docs/project/document-map.yaml) with its `role`,
`authority` and `lifecycle`, then run `devtools.render_document_map`, because SYNOPSIS
carries a generated copy of that map.
Skipping either step fails `check_documentation` — first with
`unmapped durable document`, then with `SYNOPSIS.md document map is stale`. This is
listed here because the requirement is not discoverable from the Markdown: the registry
is YAML, so grepping `*.md` for a sibling document finds the *rendered* map and not the
source, which is exactly how it gets missed.

## Shell Policy

There are currently no tracked Bash or shell entry points in the packing project, and
the architecture tests guard that state.
Python is the default when a command parses structured data, owns durable state,
branches meaningfully, coordinates subprocesses, handles timeouts, or needs focused
tests. A tiny transparent launcher may be justified, but adding one requires an explicit
architecture-test exception and an explanation of why direct configuration or Python is
less clear.

## Performance Work

Optimize E2 and E3 code only against a representative research loop.
Record the command, inputs, Python and engine revisions, worker settings, warm or cold
state, and the metric being improved.
Profile first; preserve the behavioral and scientific contract; compare before and after
under the same regime.
One-off E1 code need not be optimized unless it materially blocks the experiment that
owns it.

Gate wall time, solver throughput, pair tests, and time-to-retained-result are useful
metrics. Line count, abstraction count, and test count are not performance measures.

For long-running tests and runs, follow
[OR-14’s timing requirement](operating-rules.md#or-14-a-development-cycle-is-never-artificially-slow):
retain per-test, per-control, and per-phase measurements with setup/queue/execution
boundaries where applicable, source and worker configuration, and outcomes including
failure and cancellation.
Keep machine-readable records and a readable summary; total wall time alone cannot
justify an optimization.
The
[current plan](docs/project/specs/active/plan-2026-09-06-validation-efficiency-and-checkpoints.md)
tracks instruments that still need this detail.

CI retains a `validation-timings-<job>-<attempt>` artifact for each gate job for 30
days. It contains checkout provenance, subprocess start/end receipts and streamed logs,
completed step results, pytest JUnit, and incremental mutation-control timings.
JUnit records every selected case with its aggregate duration and outcome.
Slow and exhaustive logs also retain every setup, call, and teardown duration.
The quick lane preserves its 12-second console filter, so subthreshold phases are not
individually retained there.
Complete incremental per-phase records, including phases completed before termination,
remain a follow-up under `think-uhxt`; aggregate JUnit timing is not full phase
attribution. Upload runs after success or failure.
Pytest writes JUnit at exit, so a hard kill can leave only partial logs and an unmatched
start; loss of the runner can also prevent upload.
Neither case is a completed timing observation.

For a local checkpoint, select a fresh output directory outside the source tree:

```bash
PACKING_VALIDATION_ARTIFACT_DIR="$(mktemp -d /tmp/packing-validation.XXXXXX)" \
  uv run --frozen --all-extras --group dev packing-validate
```

Use `python -m devtools.checkpoint_manifest pack DIRECTORY ARCHIVE` to retain a flat
checkpoint directory as a deterministic tar.gz without macOS metadata (`._*`,
`.DS_Store`). The archive keeps the original receipt bytes; Git revision and path
identify repository-owned evidence under
[OR-16](operating-rules.md#or-16-use-git-for-repository-integrity-reserve-checksums-for-real-trust-boundaries).
New packs do not create checksum sidecars.
The `check` command remains available for the already retained legacy manifests; it
compares archive bytes with those records and does not certify the checkpoint’s outcome
or the truth of its provenance fields.

From `packing/`, check those retained manifests with:

```bash
uv run --frozen --all-extras --group dev python -m devtools.checkpoint_manifest \
  check benchmarks/validation-efficiency/checkpoints/*.manifest.json
```

The [engineering campaign](packing/benchmarks/validation-efficiency/README.md) records
controlled optimization comparisons separately from checkpoint evidence.
Its maintained instrument retains raw output and receipts; its generated report
validates the selected tests, outcomes, and comparison regime before calculating an
exploratory result.

### The gate’s standing cost, which a W5 block reads rather than re-measures

Start with `packing-validate --budgets` and the [dated hosted runs](#the-tiers).
The register owns enforceable cost declarations; the run receipts supply observations
and attribution. Establish a comparable baseline when the reference is unmeasured,
outdated, or a different execution shape.

The
[current W5 plan](docs/project/specs/active/plan-2026-09-06-validation-efficiency-and-checkpoints.md)
requires a baseline, profile, target, and equivalence guard before accepting an
optimization. Retain raw measurements and generate their report.
Do not replace those records with a timing comment or treat an incomplete CPU lower
bound as total test CPU. The prior
[efficiency infrastructure plan](docs/project/specs/active/plan-2026-08-25-research-loop-efficiency-infrastructure.md)
and
[gate validation plan](docs/project/specs/active/plan-2026-08-29-gate-validation-speed.md)
retain the earlier experiments and their outcomes.

### What a deep run repeats, and what that licenses

The ordinary full checkpoint runs on every push to `main`, on the daily schedule and on
dispatch, and nothing about it is scoped to the change.
How much of it repeats work whose inputs did not move is a measurement, and it has a
tool rather than an opinion:

```shell
uv run --frozen --all-extras --group dev packing-validate --format json > run.json
uv run --frozen --all-extras --group dev python -m devtools.measure_gate_repetition \
    --timings run.json --days 30 --attribution
```

It prices every deep run in a window against the run before it, taking reachability from
`Step.touches` and seconds from a real run summary.
A step the summary does not price, prices twice over, or records as skipped is a
refusal, because a step priced at zero repeats for free by arithmetic rather than by
evidence.

Three of its numbers, measured on 2026-09-05 over thirty days, set the shape of any skip
rule and none of them is about `touches`:

- **13 of 70 deep runs ran against a tree that had not moved** since the run before
  them. Every one of those repeated the whole gate.
- **53 of 55 merges to `main` carried a tree byte-identical to the pull-request head**
  merged, so the pull-request surface had already run against exactly those bytes.
- **8 of the 66 steps then declared no `touches` at all**, deliberately, and they are
  the expensive ones — so `touches` cannot prune the deep surface by cost.
  The escape hatch that protects a mis-declared pattern is reachable by 17 of 1,933
  tracked files, 0.9 per cent, which is far less protection than its own docstring
  assumes.

**The exact content address here is the git tree id, not a pattern.** Equal tree ids
mean equal bytes for every tracked file, including the code that does the verifying —
which is strictly stronger than hashing the artifacts a step reads.
**But it addresses only the tree**, and four steps in this gate answer to something
else. `campaign record` judges four refusals — an expired lease and a passed session,
workflow-phase or delegation deadline — against a reference instant, which until `D-468`
was the wall clock and is now HEAD’s committer date; two runs of one commit therefore
agree, and two commits carrying the same tree still need not.
`bead tree` reads the bead store in `.git/tbd/data-sync-worktree`, which is not in any
tree, and so does `tier ceilings are declared and not slack`, which refuses an advisory
pull-request wall whose tracking bead is closed or unknown.
`provenance: recorded commits are reachable` reads the git graph and the clone depth —
`D-226` is the run where CI discarded the history its own provenance gate needed.
A rule that skips on tree identity has to keep running those four; what `D-468` licenses
is narrower and exact, that a scheduled rerun of the *same commit* now agrees with the
run before it, which is what the unmoved-tree count above is made of.
`tests/test_gate_repetition.py` holds that agreement as an assertion rather than a
paragraph.

### Codex research-loop rollups

Use the recursive JSONL scanner when a clocked research session is slow, after a
material validation-surface change, and as an input to a recurring W5 efficiency sample:

```shell
uv run --frozen python -m devtools.codex_log_rollup \
  --sessions-root ~/.codex/sessions \
  --root-id <codex-task-id> \
  --format markdown
```

Repeat `--root-id` to compare task trees, use `--format json` for the stable
`CodexEfficiencyRollup/v2` contract, and add `--include-turns` only when the full turn
tree is needed. The scanner follows descendant task ids, removes inherited history from
current and legacy subagent logs, correlates command polling with its originating
command when the log permits it, and keeps parent active time, recursive agent-time,
active union, and parallel overlap separate.

Interpret the timing bounds literally.
The response envelope is active client time after explicit tools and compaction; it is
an upper bound that still includes API latency, dispatch, suspension, and uninstrumented
gaps. Explicit `Reasoning` and `AgentMessage` item timing is a lower-bound model stream
and is unavailable in older logs.
Do not call either measure provider-side inference latency.
An incomplete live turn ends at its last event, so its totals are lower bounds.

The scanner excludes prompt, message, and reasoning prose from its output, but the
result is not automatically safe to publish: JSON includes local log paths, task ids,
agent paths, token totals, and shortened normalized command excerpts.
Review and reduce a report before retaining it in the repository.
Store compact dated findings and comparison receipts, not raw Codex JSONL or complete
private command histories.

To retain a publishable AgentSession interval, do not archive the full v2 output.
Build the enforced privacy-reduced delta from two explicit cutoffs instead:

```shell
uv run --frozen python -m devtools.codex_task_tree_delta \
  --sessions-root ~/.codex/sessions --root-id <codex-task-id> \
  --start <AgentSession-started_at> --end <snapshot-at> \
  --out campaign/resource-usage/codex-task-tree-<session-id>.yaml
```

`CodexTaskTreeDelta/v1` keeps only additive aggregate counts, timing categories, model
settings and tokens.
It drops prose, paths, child and turn identifiers, and commands.
The AgentSession must declare both the receipt and its operator-attributed `branch`
because Codex records no Git branch; an in-flight snapshot remains a lower bound until a
later checkpoint replaces it.
Declare the receipt by its exact repository-relative path directly under
`packing/campaign/resource-usage/`; basename-only, absolute, traversal and nested paths
are rejected so the checker and renderers cannot resolve different files.

The session schema continues to represent an efficiency session through
`workflow_phases[].workflow: efficiency-loop` and `focus: efficiency`. Recursive timing
belongs in a linked review or versioned scanner artifact because its cardinality and
privacy boundary do not fit the concise session handoff.

## Governing Guidelines

This guide applies the repository guidelines rather than copying them.
Load the current text on demand with `tbd guidelines <name>`; generated `.tbd/docs`
copies are local working state and are not durable link targets.
The applicable names are:

- `general-eng-agent-principles` and `general-coding-rules`;
- `general-tdd-guidelines` and `general-testing-rules`;
- `python-rules`, `python-modern-guidelines`, and `python-cli-patterns`;
- `error-handling-rules` and `backward-compatibility-rules`;
- `golden-testing-guidelines`; and
- `common-doc-guidelines`.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
