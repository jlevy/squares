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
full gate on both hosts.
The Rust search engine uses the stable Cargo toolchain.

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

**The canonical reference for what runs where.** Two things are often confused and are
separate axes. A **tier** is a set of *steps* — which of the gate’s 64 declared steps a
command runs. A **lane** is a division of the *behavioural suite* — which pytest tests a
behavioural step runs.
A tier selects steps; a lane divides one step.

### The tiers

| Tier | Who runs it, and when | Steps | Ceiling | Cost when last measured |
| --- | --- | ---: | ---: | --- |
| `--records` | contributor, before touching a registry; also every pull request | 31 of 64 | 300 s | 11.0 s |
| `--edit` | contributor, in the edit loop | — | 240 s | 59.4 s |
| `--push` | contributor, before a push — the edit tier plus tests reachable from the diff (`--since`) | varies with the diff | 1800 s | about a minute for a code change |
| `--fast` | contributor, at a block boundary; the union of the four tiers below | 62 of 66 | 700 s | 502.3 s on CI, 2026-09-06, commit `5cad7540`, when CI still ran it whole |
| `--checks` | **CI, on every pull request**, in the `validate` job | 48 of 66 | 240 s | not yet clocked on CI |
| `--geometry` | **CI, on every pull request**, in the `geometry` job, concurrently | 9 of 66 | 200 s | not yet clocked on CI; 93.3 s locally at the reference shape |
| `--suite` | **CI, on every pull request**, in the `suite` job, concurrently | 1 of 66 | 240 s | not yet clocked on CI |
| `--sweeps` | **CI, on every pull request**, in the `sweeps` job, concurrently | 4 of 66 | 240 s | not yet clocked on CI |
| *(no flag)* | **CI, on `main`, on dispatch, and daily**; and what a block ends with | 66 of 66 | 3600 s | split across two jobs; not clocked whole |

**The pull-request surface is `--checks`, `--geometry`, `--suite` and `--sweeps`
together, run as four concurrent CI jobs**, so a pull request waits for the longest of
the four rather than for their sum.
All four feed the single required `packing-required` context, and
`test_the_pull_request_jobs_partition_the_surface` reads the workflow and checks that
they are pairwise disjoint and that they cover every step of `--fast` — so the split
cannot lose a check the way a set of independent filters could.

The split is arithmetic, not preference.
`--fast` was 501.97 s of wall over about 1,100 s of step time at `--jobs 3 --inner-jobs
1`, and 1,100 s of step time on a four-cpu runner cannot finish under 275 s however it
is scheduled — so one runner could not reach the two-to-three-minute target and a second
one had to be bought.
`--sweeps` takes the four steps that re-derive a retained atlas from its witnesses, and
nothing else in the tier is above 90 s; the measurement for each is in
`test_the_pull_request_runs_its_sweeps_and_its_suite_apart`.

`--suite` is the third job and it is one step, and the reason it is alone is a floor
rather than a budget.
`fast behavioral tests` cost 142.43 s on CI inside the `validate` job, where
`_pytest_workers` sizes xdist to `cpus - jobs + 1` — two workers beside two other outer
lanes. No outer parallelism shortens a wall that is one step, which is what `BC-218`
found one level up, so the only lever on it is the worker count, and the only way to
raise that without oversubscribing the runner is to stop sharing the job.
Alone at `--jobs 1` the step has all four cpus to spend on xdist.
That also retires `BC-218`’s objection to four workers: nineteen ordinary tests went
over the per-test ceiling on contention when the lane asked for every cpu *beside* other
work, and a lane that is the only work on its runner cannot create that contention.
The second cost the split pays off is not on the clock: five ordinary tests were
reporting over the quick lane’s 5 s per-test ceiling because 468 s of atlas rendering
was running beside them on the same four cpus, and moving that work to its own runner is
what removes the contention rather than relabelling the tests as slow.

`--geometry` is the fourth job, and it is the only one of the four that exists for cpus
rather than for a kind or a floor.
What was left in `--checks` once the behavioural lane moved out was 57 steps of pure
outer-parallel work with no unit large enough to floor the job, so the job was given the
freed cpu: `--jobs 4`, four units on four cpus.
CI run 34016999060 priced that and refused it.
The tier came in at 198.22 s — 23.5 s less than the three-worker job that still had the
142.43 s behavioural lane inside it — because saturating the runner inflated every step
by thirty to eighty per cent against the same steps at `--jobs 3` on the run before:

| Step | `--jobs 3` | `--jobs 4` |
| --- | ---: | ---: |
| soundness perimeter | 60.62 s | 84.41 s |
| exact verification | 61.75 s | 79.98 s |
| type floor (basedpyright) | 40.37 s | 72.31 s |
| deterministic SVG rendering | 41.30 s | 65.36 s |
| historical regressions | 36.04 s | 50.00 s |
| the decimal route | 40.40 s | 49.34 s |
| D-034’s n=5 identity pair | 34.18 s | 41.85 s |

Four workers over 790 inflated worker-seconds is the same work at a worse price than
three over 470, which is the lesson `_pytest_workers` already encodes as
`cpus - jobs + 1`. A queue of that shape is shortened by cpus and by nothing else, so
the queue was halved and both halves run at `--jobs 3`: eight cpus with a core of
headroom on each, for work that had four cpus and none.
The halves are 269.60 s and 275.48 s of a local 545.08 s step-time reading, within two
per cent of each other, and the boundary is bounded by two rules rather than chosen
freely — only a `broad` step may cross, so `--edit` stays wholly inside `--checks`, and
no engine or cargo step may, so only `--checks` pays the serial `cargo build --release`
that `_build_engine` puts in front of every step.
Measured locally at the reference shape, `--geometry` is 93.3 s of wall over 243.8 s of
step time.

**What the `sweeps` job is floored by is one step**, and since 2026-09-06 that step is
`known-best chunk census` at 90.38 s rather than `single-square translation escape
screen`. The job has four units and four cpus, so its outer pool is already saturated
and its wall is its longest unit’s wall; a fifth GitHub job cannot shorten it, for the
same reason `BC-218` found that a second job could not shorten a tier that was one step.
The escape screen was that unit at 110.66 s, and the lever on it was never the schedule:
`devtools/screen_translation_escape.py` screens 98 independent records and was given a
process pool, but the pool sizes itself from `PACK_JOBS`, which `--inner-jobs` sets, so
at 1 the parallelism was dormant and the step still ran serially on every pull request.
Best of five rounds on a four-cpu box: 103.94 s at one worker, 52.11 s at two, 35.40 s
at three, 27.50 s at four.
The job now passes `--inner-jobs 2` — two rather than four, because four outer slots
already fill four cpus and a step fanning out to four inner workers is exactly the
oversubscription the table above prices.
Measured whole at that shape on a four-cpu box the job is 79.5 s: the census 79.5 s, the
screen 65.3 s, the known-best atlas 50.5 s, the prospective seed 25.1 s. The screen
costs more than its isolated 52.1 s because two inner workers beside three other outer
steps is not two workers alone, and it is under the census either way, which is the only
thing the flag had to achieve.
Of the eleven modules this job runs, only `screen_translation_escape` reaches
`sqpack.workers` — checked per process, since a transitive import would be invisible to
a grep of the four entry points — so the blast radius is one step.
The census’s 90.38 s is now the floor on the *whole* pull-request surface, since no
job’s wall goes below its own longest step.
The lever from here is inside the steps that are still serial —
`devtools/census_known_best_chunks.py` and `devtools/build_prospective_atlas.py` rebuild
100 and 101 witnesses, each record independent of the others and each rebuilt in a
single process while `sqpack.workers.worker_count` sits unused.

Four steps are outside the pull-request surface entirely, each deferred on its own
measurement and pinned by `test_the_pull_request_surface_defers_only_what_was_measured`,
which computes the deferred set from what the workflow’s pull-request jobs actually
select rather than from a flag: `exhaustive exact behavioral tests` (1943 s, its own CI
job), `negative controls` (544 s), `n=40 rigidity bracket still reproduces` (221 s), and
`slow behavioral tests` (the lane below).
Adding a fifth means arguing it in that test, not editing a list.
What runs those four *before* a merge rather than after it is
[the deep gate](#the-deep-gate-the-deferred-surface-before-the-merge).

### The behavioural lanes

`QUICK_TESTS`, `SLOW_TESTS` and `EXHAUSTIVE_TESTS` in `sqpack/cli/validate.py` are
marker expressions over `slow` and `exhaustive_exact`. They are **complements**: every
test satisfies exactly one, so no test can be in two lanes and none can be in zero.

| Lane | Marker | Tests | Runs in | Bound |
| --- | --- | ---: | --- | --- |
| quick | neither | 2,106 | `--fast`, so every pull request | fails a test whose `call` phase reaches 5 s |
| slow | `slow` | 92 | the full gate | fails a test whose `call` phase is under 1 s |
| exhaustive | `exhaustive_exact` | 53 | its own CI job | its own 3600 s budget |

**Both bounds are enforced, in opposite directions.** A quick test that grows past the
ceiling fails the pull request in the week it grows; a deferred test that drops below
the floor fails the deep surface until its marker comes off.
That is what makes the split a rule rather than a hand-maintained list — the failure
mode `D-466` records.

### The deep gate: the deferred surface, before the merge

The four steps outside the pull-request surface are tabulated under
[Validation Loops](#validation-tiers); this is about *when* they run.
Until 2026-09-06 the answer was “after a merge, or on the 08:17 UTC backstop”, and both
report a break that is already on `main`. Twice on 2026-09-05 that is what happened, and
one of the two is on the record.
`test_the_retained_n20_certificate_is_accepted_on_the_full_doubled_net` asserted a
certificate rung a later commit displaced; it is marked `exhaustive_exact`, so no pull
request ran it and every pull request was green; run 34009814108 failed on the merge
commit `6bd136b0`, and `main` stayed red across three merges for about five hours.

[`deep-gate.yml`](.github/workflows/deep-gate.yml) runs that surface against a pull
request instead. Its selection is the **exact complement** of the pull-request surface,
not a sample of it:
`test_the_deep_gate_runs_exactly_what_the_pull_request_surface_defers` resolves the
workflow’s own commands through `packing-validate --list` and compares the union against
every step no pull-request job runs.
So the pull-request surface and the deep gate together are the whole gate, and a fifth
deferral argued into `test_the_pull_request_surface_defers_only_what_was_measured` fails
until it is added here too.

It costs about **32 minutes**, which is why it is not on every build.
That is `exhaustive-tier`’s measured 1943 s; `deferred-steps` runs beside it and should
land near the slow lane’s own 890 s, with the negative controls and the n=40 bracket
finishing underneath that.
Neither figure has been clocked at this shape yet.

**To run it on a pull request, add the `deep-gate` label.**

- The label starts it, and every subsequent push re-runs it, because a label that
  attested to an older commit would be the same stale evidence as the daily backstop.
  **Label last**, when the branch is otherwise ready.
- Without the label every job skips in seconds, so the workflow adds nothing to an
  ordinary pull request.
  It reports one context, `deep-gate-required`, for the reason `packing-required` is one
  context: `D-380` records what a fan-out of separately required checks cost here.
- To run it without touching the author’s labels, dispatch **Deep gate** with
  `pull_request: <number>`; it checks out that pull request’s merge ref.

**When a reviewer should require it.** The three largest deferrals declare no `touches`
at all, so there is no path rule to lean on and `--since` selects them for every change
— the judgement is a reviewer’s. Ask for the label when the branch:

- moves a certificate, a retained witness, a rung, or anything under `packing/cases/` —
  the exhaustive tier is what decides those, and it is what `6bd136b0` broke;
- edits `devtools/controls.yaml` or a mutation the negative controls declare (`D-403`:
  stale controls accumulate unseen because they do not run on a pull request);
- touches `devtools/assess_n40_rigidity.py` or `devtools/assess_n5_rigidity.py`, the
  n=40 bracket’s declared inputs;
- adds, removes or could slow a test marked `slow`;
- or changes mathematics rather than prose, which is the blunt version of all four.

**The mandatory form of this is the merge queue**, and it is wired and dormant.
Branch protection cannot make a check mandatory without making it universal: a required
context that does not run on some pull request sits pending on it forever, which is the
same trap the workflow header refuses a path filter for.
A merge-queue run happens once per merge *attempt*, on the commit that is about to
become `main`, so `deep-gate-required` can be required there without being required on
every pull request — and the queue re-tests against the updated base, which is the one
hole a pre-merge deep run cannot close on its own.
Turning it on is two repository settings and no file change: enable the merge queue for
`main`, and add `deep-gate-required` to the queue’s required checks.
`deep-gate.yml` already carries the `merge_group` trigger, so nothing else has to move.

There is a second arrangement, and the two must not both be taken.
`packing-validation.yml` selects its post-merge jobs by `github.event_name !=
'pull_request'`, so adding `merge_group` *there* would run the complete gate on every
merge attempt — the exhaustive tier included, which is the deep gate’s larger half.
Requiring `packing-required` on the queue and dropping the deep gate’s `merge_group`
trigger is the same guarantee by the other route; doing both pays 1943 s twice for one
commit. It would also need `packing-required`’s own condition widened, since it is
`pull_request`-only today and the `sweeps` job it waits on does not run post-merge.

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
# (against origin/main, or --since REF). About a minute for a code change; never blind.
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

# Merge or unattended-session handoff: deep checks and no skipped surface.
uv run --frozen --all-extras --group dev packing-validate --strict

# Structured result for agents and automation.
uv run --frozen --all-extras --group dev packing-validate --format json
```

The default command runs the complete ordinary surface: fast pytest contracts, Python
and Rust quality, exact and differential mathematics, replay, schemas, generated-view
drift, provenance, campaign invariants, and mutation controls.
Pytest is one layer of that gate, not a replacement for proof scripts and independent
implementations.

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

On pull requests, [`packing-validation.yml`](.github/workflows/packing-validation.yml)
runs the surface as four concurrent Linux jobs — `packing-validate --checks` in
`validate`, `packing-validate --geometry` in `geometry`, `packing-validate --suite` in
`suite` and `packing-validate --sweeps` in `sweeps` — and reports the stable
`packing-required` aggregate, which waits on all four.
One required context, four prerequisites: `BC-218` made that the condition for any
fan-out, because [D-380](defects.md) records what a fan-out of separately required
checks cost this repository once.
Since 2026-09-05 the surface is sixty-two of the sixty-six steps rather than
thirty-seven: twenty-one steps that had run only after a merge were promoted into it
([D-455, D-456](defects.md), think-k4fb). Four steps stay out, each on a measurement
recorded beside `STEPS` in `packing/src/sqpack/cli/validate.py`: the negative controls,
the `n=40` rigidity bracket, the exhaustive exact tier, and the slow behavioral lane.

**The behavioral suite runs in three lanes, and they partition it.** `QUICK_TESTS`,
`SLOW_TESTS` and `EXHAUSTIVE_TESTS` in `sqpack/cli/validate.py` are marker expressions
over `slow` and `exhaustive_exact`, and every test satisfies exactly one, so a test
cannot be in two lanes and cannot be in none.
`--fast` runs the quick lane; the full gate adds `slow behavioral tests` and
`exhaustive exact behavioral tests`, so nothing the pull-request surface stops running
stops running. Measured 2026-09-06: the tree collects 2,251 tests — 53 exhaustive exact,
92 slow, and 2,106 in the quick lane.

**The boundary is a ceiling the gate enforces, not a list it trusts.**
`fast behavioral tests` passes `QUICK_TEST_CEILING_SECONDS` to pytest as
`--durations-min` and fails, naming the test, when a test it ran reports a `call` phase
at or above it. A test that grows past the ceiling therefore fails the pull-request
surface in the week it grows; the fix is to make it faster, or to mark it `slow` with
its measurement in `test_the_slow_marker_is_declared_only_by_measured_nodes`, which
moves it to the deep surface rather than stopping it running.
The `call` phase and not setup, because a module-scoped fixture bills its whole cost to
whichever test triggers it first, and marking that test would move the cost rather than
remove it. The marker registries are checked the same way for both markers: the declared
set is pinned by a test, so a marker cannot be added without stating what it measured.
The quick lane runs under xdist at `cpus - jobs + 1` workers, sized to what the box has
left rather than to what it has, because asking for every cpu beside the other lanes put
nineteen ordinary tests over the per-test ceiling on contention alone.

Pushes to `main`, manual dispatches, and the daily schedule run the complete locked
command on Linux and macOS, split across two jobs since 2026-09-05: `validate` runs
everything but the exhaustive exact tier (`--skip`), and `exhaustive` runs that tier and
nothing else (`--only`), so a tier that was 1943s of a 2755s surface carries its own
budget and its own verdict instead of deciding whether the other sixty steps are
reported at all (think-tr2z). `--skip TEXT` is `--only` read the other way round,
repeatable and matching displayed step names the same way; a pattern naming no step is
refused rather than ignored, since a `--skip` that silently matches nothing runs more
than it meant to and says nothing.
The daily cadence is `BC-214`: it is the schedule that catches a deferred test breaking
on a branch that never reaches `main`, and a weekly one would leave up to seven days
between the break and the run that names it.
The macOS integration job also runs the focused deep-golden step directly.
Negative controls use at most two workers while honoring the `--inner-jobs` cap;
integration CI opts into two inner workers explicitly.
D-203’s temporary expected-failure classifier was removed after the repaired producer
passed on both architectures; the workflow test rejects its return.
Never accept a rebuilt golden to make the probe green, and do not add a second CI-only
implementation of either check.

### What each tier costs, and where its ceiling lives

A contributor runs `--edit` in the loop and `--push` before a push.
CI runs the tier named in
[`packing-validation.yml`](.github/workflows/packing-validation.yml) on a pull request,
and the complete locked command on `main`, on dispatch, and on the daily schedule.

**What each tier is allowed to cost is data the gate reads, not prose in this file.** It
is declared in
[`packing/devtools/gate-budgets.yaml`](packing/devtools/gate-budgets.yaml), one entry
per tier, and every whole-tier run compares its own wall against it:

```shell
uv run --frozen --all-extras --group dev packing-validate --budgets
```

The tiers and their ceilings are tabulated once, under
[Validation Loops](#validation-tiers).
This section is about why the register exists rather than what is in it.

The ceiling column is enforced and the cost column is not: the register is the
authority, and `packing-validate --budgets` prints it as of now.
Read that command rather than this table.

**A run outside its tier’s band fails and names the step that spent the time**, because
“the tier is slow” is not actionable and “`fast behavioral tests` is 1324 s of a 1370 s
tier” is. The band has more edges than a cap, and they exist because a cap alone did not
catch the 2026-08-30 to 2026-09-05 drift — 499 s to 1369.60 s, entirely inside an 1800 s
cap:

- a run over the ceiling fails;
- a run more than `drift_ratio` above the cost the register records for that tier fails,
  which is the edge a 2.65× regression crosses long before it reaches a generous cap;
- a run far enough *below* the recorded cost also fails, printing the figure to write —
  because a record bounded only from above rots downward, and a stale record makes the
  first two edges meaningless;
- and `python -m devtools.check_gate_budgets`, in the records tier, refuses a ceiling
  more than `max_headroom` above the cost its own tier records, without running anything
  at all. That is the rule that fires on 1800 s declared beside 499 s.

**Wall time is not comparable across machines, so the ratio rules enforce only on the
runner the ceiling was measured for.** Each tier declares a reference — CPU count,
`--jobs` and `--inner-jobs` — and a run whose shape differs is measured, reported, and
never failed; `--enforce-budget` overrides that for an operator who means it.
This is a deliberate trade: it makes the check quiet on a developer’s laptop and on a
contended agent box, and it means a regression is caught by CI rather than before the
push.

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
the merge queue closes it by building the merge commit itself.

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

### The gate’s standing cost, which a W5 block reads rather than re-measures

A `W5` `efficiency-loop` block on the gate has a baseline before it starts, and the
baseline is not in anybody’s prose:

```shell
uv run --frozen --all-extras --group dev packing-validate --budgets
```

[`packing/devtools/gate-budgets.yaml`](packing/devtools/gate-budgets.yaml) is the
standing measurement.
It carries, per tier, the ceiling the gate enforces, the cost last measured at that
tier’s reference runner, the date and the CI run that measured it, and the argument for
the number. `W5`’s entry contract asks for a baseline, a profile, a target and a guard;
this file is where the first two live for the gate, and the gate keeps them current
itself — a run outside the band fails and prints the figure to write.

**Do not re-measure the gate by hand and record the result in a comment.** That is the
failure `agenda-023` `BC-216` was opened to close: `validate.py` recorded `--fast` at
499 s on 2026-08-30 in a docstring beside an 1800 s cap, the tier reached 1369.60 s six
days later on CI run `33982455466`, and nothing objected, because 1370 is inside 1800
and because 499 was prose.
A number a machine does not read is a number that drifts.

The profile that block worked from, for the next one to start against rather than
rediscover: the tier was one step — `fast behavioral tests` was 1324 s of the 1369.60 s,
96.7 per cent of wall, and every other step in the tier together was about 45 s.
`--edit`, which is every floor and every record check but not the broad suite, was 59.35
s on a contended four-core box the same day.
The target was the operator’s own: a pull-request-blocking surface of at most four
minutes.

### What a deep run repeats, and what that licenses

The deep surface runs on every push to `main`, on the daily schedule and on dispatch,
and nothing about it is scoped to the change.
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
- **8 of the 64 steps declare no `touches` at all**, deliberately, and they are the
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
