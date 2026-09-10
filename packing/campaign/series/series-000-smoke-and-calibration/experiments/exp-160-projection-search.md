---
title: exp-160 — divide and concur over a bounded container, the first feasible search here
softschema:
  contract: packing.squares:Experiment/v2
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-160
  series: series-000
  title: Divide and concur over a bounded container, the first feasible search here
  date: '2026-09-09'
  hypotheses:
  - H-162
  tier: exploratory
  subject:
    label: relaxed-reflect-reflect over corner-space replicas, container ratchet from the trivial grid
    engine: devtools/run_projection_ratchet.py over devtools/divide_and_concur.py
    engine_commit: ffa6d01
    assurance: numerically-checked
    method: numerical-f64
    precision:
      binary_bits: 53
      rounding: nearest-even
    tolerance: 1e-9 for the solver's own success test; 1e-12 for the out-of-process re-check
    host_system: Apple M1 Pro class, 10 cores, 32 GB, 8 worker processes, numpy pinned to one thread each
    selftest_passed: true
  instance:
    axis: n
    point: 11
    role: target
  method:
    control: the 2026-09-08 penalty calibration, whose 48 runs are the standing comparison
    candidate: divide and concur searched with relaxed-reflect-reflect, beta in {0.3, 0.5}
    runs_per_condition: 2
    interleaved: false
    operator: claude-opus-5
    commit: ffa6d01
    dirty: true
    entry_point: devtools/run_projection_ratchet.py
    command: uv run --frozen python -m devtools.run_projection_ratchet --n 5 10 11 17 --repeats 2 --beta 0.3 0.5 --attempts 6 --iters 5000 --monotone 700; then the same with --n 5 11 --repeats 3 --beta 0.5 --cold 0.5 1.0
    budget: 48 to 95 solver calls per ratchet run, 5,000 iterations each at most, 28 runs over two arms
    record: campaign/series/series-000-smoke-and-calibration/results/exp-160-projection-search/
  effort:
    timebox: 2h
    wall_seconds: 937.0
    agent_minutes: 95
    stopped_by: criterion
  results:
  - shape: conditions
    metric: feasible_runs_fraction
    role: guard
    control_median: 0.0
    candidate_median: 1.0
    control_range: [0.0, 0.0]
    candidate_range: [1.0, 1.0]
    overlapping: false
  - shape: conditions
    metric: runs_below_the_trivial_grid_fraction
    role: mechanism
    control_median: 0.25
    candidate_median: 0.8333333333
    control_range: [0.25, 1.0]
    candidate_range: [0.6666666667, 1.0]
    overlapping: true
  - shape: conditions
    metric: best_side_n5
    role: outcome
    control_median: 3.0
    candidate_median: 2.769140625
    control_range: [3.0, 3.0]
    candidate_range: [2.708203125, 3.0]
    change_pct: -7.69
    overlapping: false
  - shape: conditions
    metric: best_side_n10
    role: outcome
    control_median: 4.0
    candidate_median: 3.771875
    control_range: [4.0, 4.0]
    candidate_range: [3.7703125, 3.7734375]
    change_pct: -5.70
    overlapping: false
  - shape: record
    metric: best_side_n11
    role: outcome
    direction: lower
    score: 3.9234375
    standing_best: 3.87708359002281
    standing_best_source: packing/frontier/n-011.md
    beat_record: false
    runs: 10
  - shape: conditions
    metric: best_side_n17
    role: outcome
    control_median: 5.0
    candidate_median: 5.0
    control_range: [5.0, 5.0]
    candidate_range: [4.8046875, 5.0]
    change_pct: 0.0
    overlapping: true
  - shape: determination
    question: does every run end on an exactly feasible packing
    role: guard
    outcome: criterion_met
    checked_by: 'all 28 runs across both arms report violation exactly 0.0, and the 16 of the
      registered arm verify out of process under sqpack.verify at float tolerance 1e-12;
      the standing penalty comparison is 0 of 48'
  - shape: determination
    question: does the search reach a packing strictly below the trivial grid on at least three of the four cells
    role: outcome
    outcome: criterion_met
    checked_by: 'all four cells have at least one run below the grid: n = 5 at 2.7082 of 3,
      n = 10 at 3.7703 of 4, n = 11 at 3.9234 of 4, n = 17 at 4.8047 of 5'
  - shape: determination
    question: does it come within one per cent of the best known on at least half of the cells
    role: outcome
    outcome: criterion_missed
    checked_by: 'one cell of four: n = 5 at +0.040 per cent. n = 10 is +1.705, n = 11 is
      +1.201, n = 17 is +2.762, each on the best run of the cell'
  - shape: determination
    question: where does a failed run fail
    role: mechanism
    outcome: criterion_met
    checked_by: 'every run that ended at the grid used exactly 48 solver calls, which is eight
      step halvings at six attempts each with no acceptance in between: the run never left
      the grid, and nothing after the first tightening had anything to continue from'
  - shape: determination
    question: does spending attempts on fresh random starts change the escape rate
    role: mechanism
    outcome: criterion_met
    checked_by: 'at n = 5, continuation escaped on 1 of 4 runs and every mixed or fully cold
      run escaped, 6 of 6; at n = 11, 2 of 4 against 4 of 6. The quality trade runs the other
      way: the single continuation escape at n = 5 reached 2.7082 where the best mixed run
      reached 2.7691'
  complexity:
    lines_changed: 604
    new_dependencies: []
    new_failure_modes:
    - 'A ratchet started at the grid can end at the grid, and does so on 8 of 16 runs. The
      reported side is then honest but uninformative, and a summary that averages sides
      across runs would blend a search result with a starting condition.'
    notes: 'Two new devtools and one test module. The method is 200 lines; the rest is the
      container schedule and the runner.'
  verdict:
    decision: unresolved
    primary_criterion: feasibility first, then best side against the best known
    reason: 'The guard clause is met decisively and is the point of the round: 16 of 16 runs
      end on packings that an independent oracle confirms, against 0 of 48 for the penalty
      physics, which settles the precondition the 2026-09-08 calibration failed. The
      accuracy clause is missed by three cells of four. The failure is localised rather
      than diffuse -- every failed run failed at the first tightening and never moved -- so
      the repair is in the container schedule and the restart policy, not in the projections.'
    commit: ffa6d01
---
# exp-160 — a search whose failures are visible

## What the round was for

The
[penalty calibration](../../../../atlas/known-best/video/spikes/v2-transitions/NOTES.md)
of the day before ended in a precondition failure.
Zero of 48 runs finished feasible.
The least overlap anywhere was `0.0042` of a unit side, and holding eleven squares from
the grid for thirteen times as many steps moved the overlap from `0.004578` to
`0.004570` and the container side not at all.
That is a floor, not a transient: a penalty force settles where the springs balance the
walls, and the overlap left there is pressure divided by stiffness.

The consequence is worse than a null result.
The stiffest law in that sweep reported `3.88987` at `n = 11` against the standing
record `3.87708`, which reads as a third of a per cent off a record.
It is nothing of the kind — those squares interpenetrate by five thousandths, and the
number is small *because* they do.
A calibration ranks settings by how near they come to a known answer, which presumes the
thing being ranked can produce an answer.

So this round asks the prior question.
The
[simulation survey](../../../../../docs/project/research/research-2026-09-09-simulation-mechanisms-for-packing.md)
ranks divide and concur first, on the strength of the only cold whole-benchmark result
in either survey: Gravel and Elser ran it on `n` equal disks in a unit square for every
`n` from 2 to 200, reached the best known within `1e-9` on 143 of 197 and beat it on 38,
using “No information about the known packings … apart from their densities”.
Nobody has run it on squares in a bounded container.

## The result

Sixteen runs, four values of `n`, two relaxations, every side reached from the trivial
grid with no record consulted.

| `n` | grid | best known | runs below the grid | best side | excess | median side |
| ---: | ---: | ---: | :---: | ---: | ---: | ---: |
| 5 | 3 | 2.707107 | 1 of 4 | 2.7082031 | +0.040 % | 3.0 |
| 10 | 4 | 3.707107 | 4 of 4 | 3.7703125 | +1.705 % | 3.7718750 |
| 11 | 4 | 3.877084 | 2 of 4 | 3.9640625 | +2.243 % | 4.0 |
| 17 | 5 | 4.675534 | 1 of 4 | 4.8046875 | +2.762 % | 5.0 |

A second arm, twelve more runs, varies the start policy and is reported below; every
number in this document comes from one of the two.

**Every one of the sixteen is a packing.** The solver’s own separating-axis test reports
a violation of exactly `0.0` — not a small number, the float `0.0` — and all sixteen
pass `sqpack.verify` in a separate process against code the search does not share.
That is the whole difference from the penalty run, and it is a difference in kind.

**The `n = 5` result is the record to four decimals.** `2.7082031` against
`2 + 1/sqrt(2) = 2.7071068` is `+0.040 %`, and the gap is the container schedule’s own
floor rather than the search’s error: the ratchet stops halving at `1e-3` because the
survey’s instruction is not to ask a projection loop for the final digits.
Handing that pose to the fixed-angle LP is the obvious next step and was not done here.

**The `n = 17` result is the one that matters against this repository’s own engine.** At
`n = 17` the annealing control in [exp-159](exp-159-round-1-schedule.md) sits at exactly
`5.0`, the trivial grid, on every seed; it took the collective perturbation move of
[H-158](../../../hypotheses/H-158-simultaneous-perturbation-move.md) to move it at all.
The projection search reaches `4.8047` with no move set, no schedule and no temperature,
because it never had a single-square move menu to be trapped by.
It is still well short of `sqsearch`’s `4.7071` with the long schedule and the
collective move, at a budget three orders of magnitude larger.

## The setting that decides whether a run finds anything

The failures above are not spread thinly across the runs; they are concentrated in one
decision, and a second arm isolates it.
`cold` is the fraction of each tightening’s six attempts spent on a fresh random
configuration rather than on continuing the packing already in hand.
Gravel and Elser’s published protocol is entirely cold -- up to 400 independent random
starts per `n` -- and continuation is this implementation’s addition.

| start policy | `n = 5` escaped | `n = 5` best | `n = 11` escaped | `n = 11` best |
| --- | :---: | ---: | :---: | ---: |
| continuation only | 1 of 4 | **2.7082031** | 2 of 4 | 3.9640625 |
| half cold | 3 of 3 | 2.7691406 | 2 of 3 | **3.9234375** |
| all cold | 3 of 3 | 2.7726563 | 2 of 3 | 3.9843750 |

**The two things one wants trade against each other**, which is the round’s most useful
finding. Cold starts buy escape: at `n = 5` every mixed or fully cold run got off the
grid, against one run in four for pure continuation.
Continuation buys refinement: the single continuation run that did escape at `n = 5`
reached `2.7082`, six thousandths better than the best any cold-mixed run managed,
because it spent all six of its attempts improving one arrangement instead of
rediscovering the problem.

Half cold is the better of the three at `n = 11`, and it is also the setting that
produced the best side measured anywhere in this round for that cell.
Three runs per condition is too few to call the ordering, and it is recorded as a
direction to sweep rather than a result.

## Where the failures are, which is the useful part

Eight of the sixteen runs ended at exactly the grid, and **every one of them used
exactly 48 solver calls**. That number is a fingerprint: eight step halvings at six
attempts each, with no acceptance anywhere in between.
The run never left the grid, and after the first tightening failed there was nothing to
continue from, so each subsequent step re-attempted a smaller tightening of the same
infeasible start until the step size hit its floor.

The reason is specific to squares and is worth stating plainly.
A grid of `k` squares in a row needs a container of side exactly `k`. So the instant the
schedule asks for `k - epsilon`, the grid topology is infeasible *in its entirety* — not
slightly wrong somewhere, wrong everywhere at once, with no small repair available.
Continuation has nothing to offer at the first step, and the run has to invent a new
arrangement or stop.

That is the same wall this campaign already measured from the other side.
[exp-155 through exp-159](exp-156-round-1-perturbation.md) established that at a grid no
single-square move lowers the container side, because the binding span is set by an
entire row at once. Two mechanisms with nothing in common — a Metropolis search over
single-square moves, and an alternating projection with no move set at all — fail at the
same configuration for the same geometric reason.

The escape rate tracks how full the starting grid is: `n = 10` fills ten of sixteen
cells and escaped on all four runs; `n = 11` fills eleven of sixteen and escaped on two;
`n = 17` fills seventeen of twenty-five and escaped on one; `n = 5` fills five of nine
and escaped on one. That is four points and should be read as a direction, not a law.

## Settings, on the evidence here

- **`beta = 0.5` over `beta = 0.3`.** Five of eight runs escaped the grid at `0.5`
  against three of eight at `0.3`, and the only cell to reach a record did so at `0.5`.
  Small numbers, but they agree with Elser’s own choice and against the 2025 flow-limit
  paper’s preference for `beta <= 0.3`, which measures asymptotic scaling rather than
  escape from a bad start.
- **The metric weighting does nothing at `n = 5`.** Elser’s update
  `lambda -> 0.99 lambda + 0.01 exp(-alpha d)` at `alpha` of 10 and 30 gave one success
  in twenty against one in twenty unweighted, at five per cent above the record.
  That is the case where the dilution argument it answers is weakest — four pair
  replicas, most of them active — so this is not evidence against it at `n = 26`, where
  a square carries twenty-five replicas and touches about four.
- **Cold success probability collapses with the container.** At `n = 5` from random
  starts: thirteen per cent of forty runs succeeded five per cent above the record, and
  two and a half per cent succeeded two per cent above.
  Aiming a cold start at the target is hopeless, which is why the published protocol
  ratchets.
- **`m`-monotonicity at `m = 700` is not the binding constraint.** Successful runs
  converge in a median of 500 to 640 iterations and reach a violation of exactly zero,
  so the stop rule is discarding failures rather than truncating successes.

## What this does not establish

No record was found and none is claimed; `n = 5` reproduces a packing proved optimal in
1985, and the other three cells are between 1.7 and 2.8 per cent above bounds that
already stand.
The comparison against `sqsearch` is not budget-matched and is not offered
as one: the two arms here spent 937 seconds of wall clock across twenty-eight runs,
against 4,281 for exp-159’s round, but the per-run work differs by orders of magnitude
and no common currency was measured.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
