# Packing Development Guide

This is the engineering entry point for `packing/`. Read [`TUTORIAL.md`](TUTORIAL.md)
for the mathematics, [`SYNOPSIS.md`](SYNOPSIS.md) for research status, and
[`campaign/README.md`](packing/campaign/README.md) before operating the research loop.
This guide owns runtime support, code placement, validation, and refactoring practice.

The governing rule is assurance proportional to reuse and consequence.
Shared code and research-state boundaries are designed, typed, tested, and kept easy to
orient around. A retained checker for one value of `n` may stay direct and specialized.
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

From this directory:

```shell
uv sync --frozen --all-extras --group dev
uv run --frozen --all-extras --group dev python --version
uv run --frozen --all-extras --group dev packing-validate --fast
```

The version command must report Python 3.14.7. Do not run a bare `pip install`, commit a
second requirements file, or rely on packages from a global interpreter.
Use uv 0.12 or newer to bootstrap the pinned interpreter; uv 0.8.17 cannot install
CPython 3.14.7 on Linux and reports `No download found for cpython-3.14.7`. Change
dependencies in `pyproject.toml`, regenerate `uv.lock`, and commit both files together.
Use `uv sync --frozen --all-extras --group dev` in CI and when reproducing the locked
development environment; the explicit development group prevents an ambient uv
configuration from omitting the test and quality tools.

The atlas rasters and the composite PDF are drawn by `cairosvg`, which needs the
system’s `libcairo`. CI installs it; on macOS with Homebrew it is installed but not on
the loader’s path, so export `DYLD_FALLBACK_LIBRARY_PATH=/opt/homebrew/lib` before
rebuilding the atlas or running the push tier, whose reachable tests otherwise abort at
collection on the three modules that import it.

## Code Maturity and Placement

The maturity class says how a module is maintained, not how important its mathematics
is.

| Class | Location | Contract |
| --- | --- | --- |
| **E0 scratch** | Untracked scratch space or the repository `attic/` | Optimize for learning. Do not import it or cite it as evidence. Delete it or promote it when the investigation ends. |
| **E1 retained case code** | `cases/<case>/` | Scope the code to a named `n`, source, theorem, hypothesis, or experiment. State its evidence limits and retain enough input and output for replay. General APIs are optional. |
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
The ordinary full checkpoint has 66 steps.
The
[validation efficiency plan](docs/project/specs/active/plan-2026-09-06-validation-efficiency-and-checkpoints.md)
owns the current W5 work on cost, naming, and checkpoint placement.

Use **PR fast surface** for `--fast`, **full checkpoint** for the default command, and
**deferred checkpoint** for the four steps outside PR fast coverage.
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
| `--records` | contributor, before touching a registry; also every pull request | 31 of 66 | 300 s | 11.0 s |
| `--edit` | contributor, in the edit loop | — | 240 s | 59.4 s |
| `--push` | contributor, before a push — the edit tier plus tests reachable from the diff (`--since`) | varies with the diff | 1800 s | about a minute for a code change |
| `--fast` | contributor, at a block boundary; the union of the four tiers below | 62 of 66 | 700 s | 502.3 s on CI, 2026-09-06, commit `5cad7540`, when CI still ran it whole |
| `--checks` | **CI, on every pull request**, in the `validate` job | 48 of 66 | 195 s | 99.4 s on CI, the mean of four readings |
| `--geometry` | **CI, on every pull request**, in the `geometry` job, concurrently | 9 of 66 | 180 s | 91.6 s on CI, the mean of four readings |
| `--suite` | **CI, on every pull request**, in the `suite` job, concurrently | 1 of 66 | 205 s | 102.8 s on CI, the mean of four readings |
| `--sweeps` | **CI, on every pull request**, in the `sweeps` job, concurrently | 4 of 66 | 210 s | 107.1 s on CI, the mean of four readings |
| *(no flag)* | Full checkpoint before final review and at block close; main, dispatch, and daily CI | 66 of 66 | 3600 s | split across two jobs; not clocked whole |

The four PR partition costs are geometric means of four readings at the reference shape,
not maxima. Hosted variation remains material: unchanged atlas code ranged from 60.97 s
to 84.48 s, and the suite’s spread reached 1.52x. The geometric-mean baselines leave at
least 1.25x margin to the declared drift and stale limits in those four samples.
Refresh them as measurements accumulate; a recorded band would represent that variation
better than a point.
[D-472](defects.md) retains the calibration history, and `think-be1s` tracks the band
representation.

**The pull-request surface is `--checks`, `--geometry`, `--suite` and `--sweeps`
together, run as four concurrent CI jobs**, so a pull request waits for the longest of
the four rather than for their sum.
All four feed the single required `packing-required` context, and
`test_the_pull_request_jobs_partition_the_surface` reads the workflow and checks that
they are pairwise disjoint and that they cover every step of `--fast` — so the split
cannot lose a check the way a set of independent filters could.

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
The four PR partitions now have recorded baselines from four reference-shape readings in
[gate-budgets.yaml](packing/devtools/gate-budgets.yaml); their drift and stale checks
are armed. These later calibrated values are distinct from the dated workflow
observations above. See
[budget enforcement](#what-each-tier-costs-and-where-its-ceiling-lives).

### The behavioural lanes

`QUICK_TESTS`, `SLOW_TESTS` and `EXHAUSTIVE_TESTS` in `sqpack/cli/validate.py` are
marker expressions over `slow` and `exhaustive_exact`. They are **complements**: every
test satisfies exactly one, so no test can be in two lanes and none can be in zero.

| Lane | Marker | Tests | Runs in | Bound |
| --- | --- | ---: | --- | --- |
| quick | neither | 2,197 | PR fast surface | fails a test whose `call` phase reaches 12 s |
| slow | `slow` | 95 | full checkpoint | fails a test whose `call` phase is under 1 s |
| exhaustive | `exhaustive_exact` | 55 | its own CI job | its own 3600 s budget |

Counts are from
[main run 34025346801](https://github.com/jlevy/squares/actions/runs/34025346801), not
fixed test membership.
The marker expressions determine current membership.

**Both bounds are enforced, in opposite directions.** A quick test that grows past the
ceiling fails the pull request in the week it grows; a deferred test that drops below
the floor fails the deep surface until its marker comes off.
That is what makes the split a rule rather than a hand-maintained list — the failure
mode `D-466` records.

### The deep gate: the deferred surface, before the merge

The deferred checkpoint runs slow behavioural tests, exhaustive exact tests, negative
controls, and the n=40 rigidity replay.
These are the four steps outside the [PR fast surface](#validation-tiers).
[D-470](defects.md) records why checking them only after a merge is insufficient: a
stale certificate test left main red across three merges despite green PR checks.

[`deep-gate.yml`](.github/workflows/deep-gate.yml) runs that surface against a pull
request instead. Its selection is the **exact complement** of the pull-request surface,
not a sample of it:
`test_the_deep_gate_runs_exactly_what_the_pull_request_surface_defers` resolves the
workflow’s own commands through `packing-validate --list` and compares the union against
every step no pull-request job runs.
So the pull-request surface and the deep gate together are the whole gate, and a fifth
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
# per-test ceiling. CI runs it as the four parts below, one per runner; run it whole
# here, where there is only one machine and nothing to overlap with.
uv run --frozen --all-extras --group dev packing-validate --fast

# The four parts CI runs concurrently on a pull request. They partition --fast, so
# running all four is running the surface and running one is running a part of it.
uv run --frozen --all-extras --group dev packing-validate --checks
uv run --frozen --all-extras --group dev packing-validate --geometry
uv run --frozen --all-extras --group dev packing-validate --suite
uv run --frozen --all-extras --group dev packing-validate --sweeps

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

The `.gate-running` marker is a load lock protecting calibrated step budgets, not a
correctness lock — no step mutates the working tree.
The floor tiers say so: `--records`, `--edit`, and a `--push` whose test selection is
narrow take no marker and run even while a full gate holds it, because a floor the lock
can refuse is a floor that gets skipped.
Selections containing a broad or full-tier step still take the marker and still refuse a
second gate.

Every validation subprocess has a finite 900-second default deadline.
Override it with `--timeout-seconds SECONDS` or `PACKING_VALIDATE_TIMEOUT_SECONDS`;
values must be positive and finite, and an explicit smaller per-call timeout still wins.
Mutation-control commands retain their 120-second default deadline and may declare a
smaller `timeout_seconds` in `devtools/controls.yaml`. A timeout terminates and reaps
the whole process group, including a child that ignores the first termination signal.
Each command also gets an empty bytecode-cache root, so rapid same-size source mutations
cannot execute a stale control from the preceding snapshot use.

The validation deadline bounds subprocess commands on supported POSIX hosts.
It does not bound pure-Python worker code, the total duration of a step that runs
multiple commands, or detached daemons; Windows process-tree cleanup is not yet
implemented. These limits are why a subprocess timeout is not, by itself, evidence that
D-239 is resolved.

Pushes to `main`, manual dispatches, and the daily schedule run the ordinary full
checkpoint on Linux in two jobs: `validate` runs everything except exhaustive exact
tests, and `exhaustive` runs those tests.
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
Quick tests use xdist workers sized by `cpus - jobs + 1`; `--inner-jobs` controls other
internal pools, including the negative-control pool.
Avoid assuming that either flag alone caps total host concurrency.

The isolated exhaustive jobs use `--jobs 1 --inner-jobs 4`: their recorded hosted
runners expose four CPUs, and no second outer step competes for that budget.
The concurrent integration and deferred jobs retain `--jobs 2 --inner-jobs 2`.
Certificate pools also enforce actual CPU availability, the four-worker maximum, and the
grid-memory budget. This allocation preserves the parallelism previously available when
certificate pools ignored `PACK_JOBS`; it is not a measured speedup claim.

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
The records check independently rejects a ceiling above `max_headroom` times the
baseline. A `null` baseline leaves those ratio checks unarmed; a measurement printed by
CI does not update the file automatically.

A different CPU/worker shape reports the budget result without failing, unless
explicitly enforced.
Matching CPU counts alone does not establish comparable load or hardware.
`--only` invocations have no tier ceiling; per-command subprocess timeouts still apply.
The default subprocess timeout is 900 seconds, increased for steps with declared larger
budgets, including 1800 seconds for slow tests and negative controls and 3600 seconds
for exhaustive tests.
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

The explainer at <https://jlevy.github.io/squares/> is not checked in.
GitHub Pages builds it from `main` in `.github/workflows/pages.yml`, on every push that
touches one of the renderer’s declared inputs (`RENDER_INPUTS` in
`devtools/render_explainer.py`, which a test keeps equal to the workflow’s path filter).
The build renders the page (`site/index.html`), the Markdown edition
(`site/t-018-explainer.md`), the PDF (`site/t-018-explainer.pdf`, drawn by Playwright’s
Chromium) and the composite assets beside them, renders each twice and requires the two
to agree, checks the print layout, and only then deploys.
A pull request runs the same build without deploying, so a render that breaks fails
review rather than the next deploy.

**Merging is the whole publish.** Every repository link on the page is a permalink to
the commit the page was built from, read from the checkout at render time
(`link_revision()`), so no merge leaves the deployed page linking to files older than
the ones it describes, and nothing has to be bumped for the links to be right.
After a merge, wait for the “Certificate page” workflow on `main` and confirm the deploy
from the checkout:

```shell
uv run --frozen --all-extras --group dev python -m devtools.check_published_site --commit <merge commit>
```

It fetches the live page, the Markdown edition, the PDF and the assets, and checks that
the edition stamp is the one `sqpack.release` names, that every repository link names
that commit and resolves on GitHub, and that the PDF is a PDF.

**The stamp in the credits has two parts, and they move on different clocks.** The
version (`v0.2.0`) is editorial and pinned in `src/sqpack/release.py`; the hash after it
is the commit the page is built from, read at render time (`page_edition()`), so it
changes on every push, and a reader of the deployed page sees exactly which commit they
are looking at. The atlas footer and the generated claim documents are checked in and
drift-checked byte for byte, so they carry the pinned `PUBLICATION_REVISION` instead
(`PUBLICATION_EDITION` and `edition_file()`); the two spellings agree on the status and
the version and differ only in which commit they name.

**Cutting an edition** is the one manual step, and it is editorial: it changes the
version, and with it the revision the committed artifacts are stamped with.
To cut one:

1. Set `PUBLICATION_VERSION`, `PUBLICATION_REVISION` (the short hash of the commit whose
   content the edition describes, which is by construction older than the commit that
   carries the bump) and `PUBLICATION_DATE` in `src/sqpack/release.py`.
2. Rebuild the atlas family:
   `uv run --frozen --all-extras --group dev python -m devtools.build_known_best_atlas --update`
   (see the cairo note under Supported Environment), and regenerate the claim documents:
   `uv run --frozen --all-extras --group dev python -m devtools.render_verifiable_claim`.
3. Run `packing-validate --only "known-best"` and
   `pytest tests/test_explainer.py tests/test_verify_claim.py tests/test_release.py`,
   and commit the release module, the five atlas files and the three generated documents
   together.

## Focused Quality Commands

Use direct tools when their output is the point of the edit:

```shell
uv run --frozen --all-extras --group dev pytest -q
uv run --frozen --all-extras --group dev ruff check .
uv run --frozen --all-extras --group dev ruff format --check .
uv run --frozen --all-extras --group dev basedpyright

cargo test --locked --manifest-path sqsearch/Cargo.toml
cargo clippy --locked --release --all-targets --manifest-path sqsearch/Cargo.toml -- -D warnings
cargo fmt --manifest-path sqsearch/Cargo.toml --check
```

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
library module reports through `logging`. The one Python outside `packing/` is the
hand-written skill assets under `.agents/skills`, which the same two floors reach.
Comments explain non-obvious intent, invariants, units, evidence limits, and rejected
alternatives—not a line-by-line translation of the code.

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
`t`** — `O(t²)` is an ordinary second-order obstruction, `O(t)` means an equation is not
describing its constraint.
That distinction is the whole of `D-361`. Which direction it walked is printed, because
there are two: the steepest side-changing one where the null space contains such a
direction, and the free direction itself where it does not, as at Göbel’s `n = 5`.

[`probe_minimal_polynomial`](packing/devtools/probe_minimal_polynomial.py) runs the
integer-relation search under the promotion spec’s frozen margin rule and reports which
clause decided each degree.
It sweeps to the degree the digits reach rather than to a fixed ceiling.
Clause 3 read backwards at the search’s own coefficient bound puts that at **degree 35**
for the `n = 29` refinement at a thousand digits, where the flag used to stop at twenty
for no reason but the default; `--max-degree` still stops it earlier, which is usually
what you want, because the cost is almost all `pslq` and it climbs steeply with the
degree.

[`probe_system_degree`](packing/devtools/probe_system_degree.py) rationalises the
`n = 29` system by the half-angle substitution and reports what bounds the algebraic
degree of the Kingbird solution, which is what says whether an integer-relation refusal
at a given degree surveyed the space or a corner of it.
`--eliminate-side` also solves the smallest equation for `s` and reports the
five-unknown system that leaves.
The `n = 29` sweep takes about twelve minutes, which is why it is a tool with a recorded
result rather than a test.

Both pin their working precision per case and print it beside the number it bounds.
That is not decoration: a rank verdict is a judgement about a gap between singular
values, and at mpmath’s ambient default the gap a probe can *see* is many decades
narrower than the truth, with nothing in the output to say so.

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
uv run --frozen python -m devtools.render_results_headline
```

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
- **8 of the 66 steps declare no `touches` at all**, deliberately, and they are the
  expensive ones — so `touches` cannot prune the deep surface by cost.
  The escape hatch that protects a mis-declared pattern is reachable by 17 of 1,933
  tracked files, 0.9 per cent, which is far less protection than its own docstring
  assumes.

**The exact content address here is the git tree id, not a pattern.** Equal tree ids
mean equal bytes for every tracked file, including the code that does the verifying —
which is strictly stronger than hashing the artifacts a step reads.
**But it addresses only the tree**, and three steps in this gate answer to something
else. `campaign record` judges four refusals — an expired lease and a passed session,
workflow-phase or delegation deadline — against a reference instant, which until `D-468`
was the wall clock and is now HEAD’s committer date; two runs of one commit therefore
agree, and two commits carrying the same tree still need not.
`bead tree` reads the bead store in `.git/tbd/data-sync-worktree`, which is not in any
tree, and `provenance: recorded commits are reachable` reads the git graph and the clone
depth — `D-226` is the run where CI discarded the history its own provenance gate
needed. A rule that skips on tree identity has to keep running those three; what `D-468`
licenses is narrower and exact, that a scheduled rerun of the *same commit* now agrees
with the run before it, which is what the unmoved-tree count above is made of.
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
