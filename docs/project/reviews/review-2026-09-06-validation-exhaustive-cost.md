# Exhaustive Checkpoint Exploration

## Provenance and Disposition

Independent read-only candidate audit prepared on 2026-09-06 against main
`6b21d14b64c19003d597ed3c993c051b64336b0c`, retained from the working report
`pr93-efficiency-exhaustive.md`. The observations below describe that baseline, not
subsequent implementation.
The timing source is the
[hosted full checkpoint](https://github.com/jlevy/squares/actions/runs/34025346801); its
downloaded working log was `squares-current-main-validation.log`.

Candidates are proposals, not accepted performance improvements.
Their implementation, measurements, independent guards, and final dispositions belong to
the
[validation efficiency and checkpoints plan](../specs/active/plan-2026-09-06-validation-efficiency-and-checkpoints.md).
Any illustrative improvement target below is subordinate to that plan’s preregistered
acceptance criteria.
Source line references are baseline locations and may move.

Read-only exploration at main `6b21d14b`; no timing experiments run.

## Completed Local Profile and Next Work

The completed pre-merge working-tree checkpoint is retained as a
[compressed artifact archive](../../../packing/benchmarks/validation-efficiency/checkpoints/2026-09-06-pre-main-integration.tar.gz)
and
[SHA-256 manifest](../../../packing/benchmarks/validation-efficiency/checkpoints/2026-09-06-pre-main-integration.manifest.json).
It started at 2026-09-06 17:12:03 UTC on base `6b21d14b`, with dirty diff digest
`37677394d0450f64d422978b56265c606675372eb0302cf6c37d8f0ad8ce6f6d`. It used Python
3.14.7, ten available host CPUs, two outer jobs, and two inner workers.
This is not verification of subsequently integrated main `edccf294`, nor a clean-tree or
paired hosted-run comparison.
No complete measurement-time source patch accompanies this checkpoint archive; its run
receipt records the dirty digest and untracked hashes.

The coordinator reported 1687.79 seconds overall: 65 steps passed and one failed on
generated `close_session` YAML and SYNOPSIS drift.
All 55 exhaustive tests passed; the exhaustive step took 1414.32 seconds.
Raw logs retain setup/call/teardown durations, while JUnit retains test identity,
outcome, and total test time.
The largest calls were:

| Exhaustive test | Call seconds |
| --- | ---: |
| All-certificate witness admissibility | 207.83 |
| n=40 record round trip | 182.71 |
| Full doubled-net interval decision, live n=12 | 105.11 |
| Full doubled-net interval decision, retained n=20 | 92.94 |
| Independent retained verifier bytes, full net | 68.76 |
| Benign lightening retains every condition | 58.33 |
| Full doubled-net interval decision, retained n=17 | 54.82 |

These observations update the priorities below.
First compare bounded exhaustive pytest scheduling with identical complete selections
and explicit inner caps; the worker cap and duration reporting are now implemented.
Next expose the four certificate witness walks as separately attributable scheduling
units, preserving every direction and witness assertion.
The case inventory changes explicitly under parametrization and must be checked against
the original four-certificate contract.

The n=40 duplicate remains: pytest spent 182.71 seconds recomputing `assess()`, and the
named full replay spent 262.89 seconds doing the same assessment under different
overlap. Their sum is not a measurement of CPU saved or potential checkpoint wall
reduction. Removing one replay remains a policy follow-up because it changes standalone
exhaustive pytest coverage.
Before removal, retain one complete replay in each relevant full or deferred topology,
add cheap nested-record drift/missing-record/CLI outcome contracts, and preserve motion,
cone, stress, and refusal tests.
Neither replay was removed here.

Interval decisions warrant profiling after the scheduling experiment; they still use
independent algorithms and complete doubled nets.
Standalone verifier bytes and perturbation decisions must remain independent.
Shared n5 row setup is a lower priority on this profile.
PR94 already fixes the 235.78-second typed-ceiling negative control; reuse it rather
than adding a duplicate optimization.
A new full checkpoint must measure the integrated result before any whole-checkpoint
improvement claim.

## Historical Baseline and Missing Evidence

Current-main GitHub log `squares-current-main-validation.log`: exhaustive pytest ran 55
tests, deselected 2292, and took 1625.08 seconds; gate step took 1626.32 seconds.
The workflow wall was 27m33s. The integration job beside it took 24m19s, so shortening
exhaustive alone eventually reaches that second bottleneck.

`packing/src/sqpack/cli/validate.py::_exhaustive_exact_tests` invokes ordinary serial
pytest and emits no durations.
The log therefore cannot rank individual exhaustive nodes.
Historical comments in `packing/tests/test_module_boundaries.py:428` are leads, not
current measurements: all-certificate witness walk 282s under contention; standalone
verifier perturbations roughly six minutes; n40 full assessment roughly three minutes;
retained integer decisions 14–39s apiece; interval decisions remain minutes each.

Existing tools should own measurements: pytest `--durations=0 --durations-min=0` for
per-phase wall, `packing-validate --format json` for step wall, and
`devtools.measure_gate_repetition` for repeated gate costs.
The latter consumes summaries with `--timings`, supports `--ref`, `--days`, and JSON
output. The optional `devtools.cpu_durations` plugin reports incomplete CPU lower bounds
only; it must not establish complete CPU savings or replace wall acceptance criteria.

## Historical Candidate Ranking

1. **Instrument the exhaustive lane, then test bounded xdist.** Smallest route to a
   material wall reduction without removing a test.
   Add pytest duration reporting in the existing CLI, measure serial versus bounded
   parallel on the same complete node set, and compare verdicts/counts.
   However, `fractional/certificate.py::_worker_count` defaults to
   `os.process_cpu_count()` and does not read `PACK_JOBS`; naive four-worker xdist can
   multiply into sixteen direction processes.
   Resolve that cap first, or partition pure serial tests from already pooled
   certificate tests. Preserve memory caps, forkserver behavior, and module fixture
   ownership. Expected gain is unmeasured.

2. **Remove the duplicated n40 full replay from the checkpoint.**
   `tests/test_n40_rigidity.py::test_the_record_round_trips` compares retained JSON to
   `assess()`. `devtools/assess_n40_rigidity.py::main --check` independently calls the
   same `assess()` and compares the same JSON; the full gate’s `n=40 rigidity bracket
   still reproduces` runs this command.
   There is no independent oracle in that duplicate.
   Replace the pytest replay with a cheap contract test of check-mode failure/success,
   retaining all mathematical motion/stress tests and the full replay gate step.
   Historical cost is about three minutes per replay.
   The gate already partitions postmerge jobs; extend coverage tests to require the
   surviving replay exactly once.
   Potential work and wall savings require measurement; integration retains its own
   copy.

3. **Parametrize the all-certificate witness walk before parallel scheduling.**
   `test_fractional_sweep_integer.py:198` serially loops n11/n12/n17/n20 and all
   directions in one node.
   Four parametrized certificate nodes preserve every direction, witness-admissibility
   assertion, and declared minimum while exposing scheduling opportunities and
   identifying the actual expensive case.
   Do not sample directions.
   Splitting directions further needs measurement because fixture and grid overhead may
   erase the gain. This is a small test-only change and pairs with candidate 1.

4. **Reuse the existing n5 execution-scoped row inventory in fixture-heavy tests.**
   `cases/n5/minus_w_row_jets.py::RowJetInventory` already builds all strata once, uses
   field identity checks, and returns fresh row mappings.
   Tests currently rebuild rows across six owner/stratum parametrizations plus three
   active-stratum cases and a curvature case.
   Reuse field-bound immutable inventory where assertions are consumers; retain direct
   builder-versus-authoritative-row tests and mutation-isolation tests.
   Avoid a new global cache or caching an oracle and implementation into the same value.
   Cost needs per-node measurement; moderate implementation scope.

5. **Parallelize independent interval directions only if profiling ranks them first.**
   `fractional/interval.py::verify_by_intervals` loops the full doubled net serially.
   Directions carry independent searches and results; ordered bounded process mapping
   could shorten six full-net tests.
   This changes production verifier execution and requires preserving ordered outcomes,
   early-refutation behavior, numerical errstate, box budgets, enclosure, and all
   361-direction decisions.
   It is a larger, riskier optimization than test scheduling.
   Keep the independent integer and interval routes; sharing their verdicts would weaken
   the contract.

## Rejected Shortcuts

Do not shrink nets, replace full retained-certificate decisions with declaration checks,
remove independently implemented standalone verifier runs, or move more tests off PRs
merely to improve timings.
`verify_claim` already short-circuits falsifications that fail Conditions 1–4; its
ten-case table is not ten unconditional full sweeps.
Full-net benign perturbations carry meaningful declaration and condition contracts, so
reducing them to one direction requires a separate coverage argument and is not
recommended here.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
