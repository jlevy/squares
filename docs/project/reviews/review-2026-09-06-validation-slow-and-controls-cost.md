# Slow-lane and mutation-control inspection

## Provenance and Disposition

Independent read-only candidate audit prepared on 2026-09-06 against main
`6b21d14b64c19003d597ed3c993c051b64336b0c`, retained from the working report
`pr93-efficiency-slow.md`. The observations below describe that baseline, not subsequent
implementation. The timing source is the
[hosted full checkpoint](https://github.com/jlevy/squares/actions/runs/34025346801); its
downloaded working log was `squares-current-main-validation.log`.

Candidates are proposals, not accepted performance improvements.
Their implementation, measurements, independent guards, and final dispositions belong to
the
[validation efficiency and checkpoints plan](../specs/active/plan-2026-09-06-validation-efficiency-and-checkpoints.md).
Any illustrative improvement target below is subordinate to that plan’s preregistered
acceptance criteria.
Source line references are baseline locations and may move.

## Completed Local Profile

The
[pre-main-integration archive](../../../packing/benchmarks/validation-efficiency/checkpoints/2026-09-06-pre-main-integration.tar.gz)
and
[digest manifest](../../../packing/benchmarks/validation-efficiency/checkpoints/2026-09-06-pre-main-integration.manifest.json)
retain the completed 2026-09-06 checkpoint: base `6b21d14b` with dirty instrumentation
and candidate edits, Python 3.14.7, ten available CPUs, two outer jobs, and two inner
workers.
This predates integrated main `edccf294`; the dirty source digest is provenance,
not a retained complete source snapshot.
The coordinator reported 1687.79 seconds, 65 passing steps, and one generated
`close_session` report/SYNOPSIS drift failure.
This local overlapping run is not a paired comparison with the hosted baseline below.

All 95 slow tests passed in a 495.66-second gate step.
The largest JUnit totals were 63.72 seconds for phase-one promotion, 23.13 for exact
construction-price round trip, 20.18 for contact-assembly label invariance, 19.90 for
the composite atlas, and 19.89 for local-rigidity controls.
The float-oracle test was 15.64 seconds and bridge success 14.13 seconds.
These latter observations corroborate their execution in the full lane; the controlled
campaign, not this single profile, decides their performance acceptance.
Raw logs distinguish setup/call/teardown, so the JUnit totals need not equal call time.

All 163 negative controls detected their intended refusal.
Their gate step took 502.18 seconds; the runner journal records 501.11 seconds including
its own setup. The typed-ceiling relation-reach control dominated at 235.78 seconds.
Inspection found that its mutation demanded a real degree-twenty search before the
refusal assertion.
Merged PR94 already checks the requested degree at the solver boundary
and targets the specific pytest node; it retains the real degree-three success path.
Reuse that fix. No duplicated boundary test or second control rewrite is needed.

The next controls were the missing simplex pivot stop (25.67 seconds), reducible
polynomial discharge (21.94), negative exact-LP multiplier (19.71), and rank-deficient
active-set elimination (17.92). These are investigation priorities, not evidence that
narrowing their commands is safe.
Check the exact refusal path and retain independent end-to-end coverage before changing
selection.
The new journal now supports this work; the historical recommendation below to
add it is fulfilled.

Next measure the integrated checkpoint, then prioritize exhaustive scheduling and
four-certificate witness attribution using the
[exhaustive profile](review-2026-09-06-validation-exhaustive-cost.md).
Keep n=40 replay removal as a separately reviewed coverage-topology change.
Within the slow lane, phase-one promotion is the clearest remaining individual cost;
inspect its repeated exact arithmetic and setup before proposing parallelism or narrower
checks. No further costly trials were run for this update.

## Historical Baseline Inspection

Read-only inspection at current main 6b21d14b, using the retained hosted log
`squares-current-main-validation.log`. No new timings or validation runs.

The observed non-exhaustive full job used four CPUs, two outer jobs, two inner workers:
1,443.60s wall; slow behavioral tests 1,220.91s; negative controls 566.10s (163
controls, two private worker trees); n=40 rigidity bracket 219.00s. These are observed
wall times under overlapping work, not isolated CPU costs.
Slow pytest currently has no xdist flag.

## 1. Remove repeated per-cell midpoint/search work in the float-oracle regression

The largest individual test is
`test_fractional_generate.py::test_the_float_oracle_scores_every_cell_the_exact_sweep_scores`:
357.92s. `_oracle_against_sweep` (lines 118 onward) evaluates the exact minimum,
independently enumerates reference cells, then for every cell recomputes each axis’s
rational midpoint, converts it to float, and invokes scalar numpy.searchsorted twice.
Each u midpoint is repeated for all reachable v cells in its column, and vice versa.

Candidate: precompute the exact-to-float midpoint/search-index mapping once for each
axis interval, then index the existing reachability grid using those maps for every
reference cell. Keep the independent `reduce_to_cells`, exact minimum, all three
configurations, all directions, and all equality/reachability assertions.
Do not replace the reference reduction with production spans merely to share its work:
that would weaken the independence this test provides.

Acceptance proposal: exact equality of `(oracle minimum, exact minimum, lacking cells)`
for every existing configuration/direction, unchanged direction count, and a material
paired time reduction (e.g. at least 20%). This is a test-harness optimization, not a
mathematical algorithm change.
Existing pytest selection and --durations are sufficient for the full test timing; any
new per-phase measurements should become a reusable probe, not a throwaway script.
Existing `devtools/bench_colgen.py` measures separation/LP and could host a closely
related oracle comparison mode if phase instrumentation is needed.

## 2. Reuse the explicit row-jet inventory in the -W bridge

`tests/test_minus_w_bridge.py::test_the_bridge_agrees` costs 109.93s. Its sensitivity
test adds 19.21s and doctored-direction refusal 6.35s.
`devtools/check_minus_w_bridge.py:80` loops three strata.
Per stratum it calls owner4_record three times (-W, altered correction, +W) and
scale_records twice (-W,+W). All calls currently omit optional precomputed rows.

The API already supports this reuse: `minus_w_row_jets.RowJetInventory.build(field)` and
`.active_rows(field,stratum)`; `minus_w_scale.scale_records(...,row_inventory=...)`;
`minus_w_owner4.owner4_record(...,active_rows=...)`. The row jets describe source
geometry, while velocity/correction are separately supplied to evaluation.
Build a local inventory once in the bridge and pass it through these existing
parameters. Avoid a process-global cache that could hide a later source mutation or
cross-number-field data.

Acceptance proposal: byte-identical bridge summary and identical exact coefficient
records against the current uncached route; retain all +/-W, correction,
doubled-velocity, and bumped-velocity checks.
Measure the full existing test module and an explicit uncached-vs-inventory comparison.
No reason to rewrite the mathematical stress code before measuring this
already-supported caller-side reuse.

## 3. Schedule slow tests across a bounded xdist pool

`validate._slow_tests` invokes serial pytest, unlike the quick lane.
Its long tests are independent: float-oracle 357.92s, bridge 109.93s, exact phase1
91.90s, exact construction 55.06s, elimination35.19s, exactLP32.46s, labels32.36s, n17
sweep30.30s. There is enough work outside the largest test to overlap meaningfully, but
reducing candidate1 first also lowers the indivisible floor.

Candidate: bounded slow-lane workers derived from the declared host and other outer
work, ideally an isolated named job rather than making the existing job oversubscribe.
The current observed job already overlaps two mutation workers with slow pytest on four
CPUs. Do not simply set every layer to four workers.
xdist group/collection scheduling may matter where modules share cached builders;
inspect fixture rebuilds and shared writes before selecting --dist.
Keep all nodes and marker-floor checks.
Compare wall and summed step/test costs under identical CPU limits; require equal
collected/executed nodes and verdicts.
Promotion of newly sub-floor functions follows the existing measured registry policy,
never exemption from the floor.

## Negative-control constraints and next measurement

The observed controls already use two workers, so “turn on existing parallelism” is not
an explanation of the 566.10s. `run_negative_controls.py:629` makes one isolated
reusable snapshot per worker and uses a queue so concurrent mutations never share a
tree. Preserve that isolation and exact expected-refusal text.
Increasing jobs to four needs its own isolated CPU budget rather than competing with the
slow lane.

The harness currently prints only aggregate pass count, not per-control costs.
Its next useful change would be durable optional per-control timing output on the
existing runner, including snapshot preparation separately, before deciding which
controls to optimize.
Declared commands repeat substantial checker entry points: ledger check35,
promote-system pytest14, synopsis11, schemas10, promote-solve8, exactLP7, phase1
pytest5. These counts are static call counts, not evidence that every invocation
completes the expensive path: mutation expectations often fire early.
In particular, phase1’s five controls target small refusal contracts before the
expensive Trump known-answer solve in main(). Do not claim five complete 92s replays
without actual per-control observations.

Reusable tools inspected: run_negative_controls (-k and -j), pytest --durations,
benchmarks/exact_verification.py (field arithmetic/exact versus float geometry),
benchmarks/n17_weighted_certificate_parallel.py, and devtools/bench_colgen.py.
There is no need for a second general timing harness before extending or composing
these.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
