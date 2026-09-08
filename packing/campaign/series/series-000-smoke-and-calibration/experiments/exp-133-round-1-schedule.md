---
title: exp-133 — anneal length against the move set, the first factorial on this problem
softschema:
  contract: packing.squares:Experiment/v2
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-133
  series: series-000
  title: Anneal length against the move set, the first factorial on this problem
  date: '2026-09-08'
  hypotheses:
  - H-128
  tier: exploratory
  subject:
    label: sqsearch --steps 4000000, single-square moves only, against the stock schedule
    engine: sqsearch 0.1.0 with the arm flags
    engine_commit: 9ae7700
    assurance: numerically-checked
    method: numerical-f64
    precision:
      binary_bits: 53
      rounding: nearest-even
    tolerance: 1e-9 for the independent pose re-check; 1e-12 for the engine's own feasibility screen
    host_system: Apple M1 Pro class, 10 cores, 32 GB, shared with other agents at load 17 to 52
    selftest_passed: true
  instance:
    axis: n
    point: 11
    role: target
  method:
    control: sqsearch at its defaults, 400,000 steps per anneal
    candidate: the same engine at 4,000,000 steps per anneal, move set unchanged
    runs_per_condition: 5
    interleaved: false
    operator: claude-opus-5
    commit: 9ae7700
    dirty: true
    entry_point: devtools/run_arm_sweep.py
    command: python3 devtools/run_arm_sweep.py plan-part-2.yaml --out part-2
    budget: 1.25e9 pair tests per chain, 8 chains, 5 seeds, 11 cells
    record: campaign/series/series-000-smoke-and-calibration/results/exp-130-round-1/
  effort:
    timebox: 3h
    wall_seconds: 4281.0
    agent_minutes: 45
    pair_tests: 1573000000000
    stopped_by: criterion
  results:
  - shape: conditions
    metric: best_side_n11
    role: outcome
    control_median: 3.935790212325
    candidate_median: 3.895757722
    control_range:
    - 3.922760527419
    - 3.946821043844
    candidate_range:
    - 3.890426654
    - 3.914213579
    change_pct: -1.02
    overlapping: false
  - shape: conditions
    metric: best_side_n17
    role: outcome
    control_median: 5.0
    candidate_median: 4.707137980
    control_range:
    - 4.997152231858
    - 5.0
    candidate_range:
    - 4.700170154
    - 4.707559007
    change_pct: -5.86
    overlapping: false
  - shape: conditions
    metric: best_side_n26
    role: outcome
    control_median: 6.0
    candidate_median: 5.887456031
    control_range:
    - 6.0
    - 6.0
    candidate_range:
    - 5.795654518
    - 5.895860162
    change_pct: -1.88
    overlapping: false
  - shape: determination
    question: does a tenfold longer anneal lower the median best side by 0.01 with disjoint
      seed ranges on at least six of the eleven cells
    role: outcome
    outcome: criterion_missed
    checked_by: 'three cells (n = 11, 17, 26) meet both clauses; six were required'
  - shape: determination
    question: does anneal length reach the standing best basin where the stock schedule does not
    role: outcome
    outcome: reached_basin
    checked_by: 'n = 10: 5 of 5 seeds within 1e-4 and 3 of 5 within 1e-6 of the proved
      3 + 1/sqrt(2), against 0 of 5 for the control'
  - shape: determination
    question: do the collective move and the long schedule combine
    role: mechanism
    outcome: criterion_met
    checked_by: 'cells improved by at least 0.01 across the 2x2: control 0, long schedule
      alone 3, collective move alone 4, both 5, with the both-cell reaching n = 27 and
      n = 37 that neither factor reaches alone'
  - shape: determination
    question: is every archived pose a valid packing at the side its line claims
    role: guard
    outcome: criterion_met
    checked_by: 'packing-campaign verify-archive over 990 poses in a separate process,
      sqpack.verify at tolerance 1e-9, zero failures, zero candidates below any record'
  complexity:
    lines_changed: 0
    new_dependencies: []
    new_failure_modes: []
    notes: 'No code change: --steps already existed. The round is a parameter, not a feature.'
  verdict:
    decision: rejected
    primary_criterion: median best_side, candidate against control, at equal pair-test budget
    reason: 'The criterion was measured and missed -- three cells of eleven against the six
      declared -- but a parameter that costs nothing to carry recovers three quarters of
      what the new move family recovers, which contradicts the design input hard enough
      that the schedule axis has to be swept properly before any further move is built.'
    commit: 9ae7700
---
# exp-133 — the schedule was supposed to be the part that does not matter

## The question, and why it was not on the original plan

The design input for this campaign argues, in a section titled “the move set, not the
cooling schedule”, that the acceptance rule and the schedule are the least important
parts of a stochastic packing search.
Its evidence is good: Johnson, Aragon, McGeoch and Schevon found no non-adaptive cooling
law worth substituting for geometric (Observation 5) and no simple adaptive schedule
worth its running time (Observation 4), while changing only the *neighbourhood* bought
two whole colours at equal time on graph colouring.

This round exists because an ablation designed to confirm that produced the opposite.
[exp-129](exp-129-arm-calibration.md) pass 3 raised the annealing temperature from
`0.25` to `0.5`, `1.0`, `2.0` and `4.0` and turned reseeding off, to rule out the
possibility that the collective move was just a hotter search.
Every one of those twelve runs returned exactly the trivial grid, so the guard passed.
The seventh arm in that pass changed the anneal *length* instead — `--steps 4000000`,
tenfold, with the single-square move set untouched — and left the grid on three seeds of
six. [H-128](../../../hypotheses/H-128-cooling-schedule-length.md) was registered before
this round on that basis.

## Result

Same eleven non-grid cells, same five seeds, same `1.25e9` pair tests per chain, same
accept rule as [exp-130](exp-130-round-1-perturbation.md).

| cell | record | control median / best | long-schedule median / best | improvement | disjoint |
| ---: | --- | --- | --- | ---: | :---: |
| 5 | `2.707107` | `2.707107` / `2.707107` | `2.707107` / `2.707107` | `0.000` | – |
| 10 | `3.707107` | `3.707815` / `3.707526` | `3.707107` / `3.707107` | `0.0007` | yes |
| 11 | `3.877084` | `3.935790` / `3.922761` | `3.895758` / `3.890427` | **`0.040`** | **yes** |
| 17 | `4.675530` | `5.000000` / `4.997152` | `4.707138` / `4.700170` | **`0.293`** | **yes** |
| 19 | `4.885618` | `5.000000` / `5.000000` | `5.000000` / `4.979668` | `0.000` | no |
| 26 | `5.621320` | `6.000000` / `6.000000` | `5.887456` / `5.795655` | **`0.113`** | **yes** |
| 27, 29, 37, 50, 52 | — | grid on every seed | grid on every seed | `0.000` | – |

**H-128 is refuted on its declared criterion** — three cells of eleven, against six —
and the refutation is the least interesting thing in the table.

## The factorial, which is the round’s real output

The design input records, among the things it could not establish, that **no study was
found that crosses cooling schedules with move sets factorially and reports the
interaction, on any problem.** Round 1 ran that crossing, because the two candidate
factors were cheap to combine: anneal length at `4e5` or `4e6` steps, and proposals
single-square or collective.

Cells of eleven where the arm improves the control’s median by at least `0.01`:

|  | single-square moves | collective moves |
| --- | ---: | ---: |
| **`4e5` steps** | 0 (the control) | 4 |
| **`4e6` steps** | 3 | **5** |

And the cells reached, which the counts hide:

| arm | cells left the grid on the median | best result anywhere |
| --- | --- | --- |
| control | `5, 10, 11` | `n = 17` at `4.997152` |
| long schedule only | `5, 10, 11, 17, 26` | `n = 26` at `5.795655` |
| collective move only | `5, 10, 11, 17, 19, 26` | `n = 17` at `4.682227` |
| both | `5, 10, 11, 17, 26, 27, 37` | `n = 17` at **`4.677676`**, `+2.15e-03` from Bidwell |

Three readings, in order of how much they should change what gets built next.

**The two factors are not substitutes and they combine.** The both-cell reaches `n = 27`
and `n = 37`, which neither factor reaches alone, and it is the only arm whose `n = 50`
ever leaves the grid (one seed at `7.929171`). Its `n = 26` median is `5.710314`,
against `5.887456` for length alone and `5.823450` for the move alone.
At `n = 17` its best seed is `4.677676`, `+2.15e-03` from a 1998 hand construction,
found cold.

**The schedule axis recovers three quarters of what the new move family recovers, and it
costs nothing.** `--steps` already existed; this round changed no code at all.
A campaign that had swept anneal length before building a new move family would have had
most of this result for free.

**Length is not temperature and the two were being conflated.** Sixteen-fold changes in
`t_hot` did nothing; a tenfold change in anneal length moved three cells.
At a fixed pair-test budget, length trades restarts against cooling rate — ten times
fewer descents, each ten times slower — which is a resource-allocation question rather
than a cooling-law question, and it is not what Johnson and colleagues’ Observations 4
and 5 measured. The design input’s section 4 is right about cooling *laws* and its title
overreaches.

## What the prediction got wrong

The registered kill condition guessed the likely shape of a refutation as “the effect is
real at `n = 18` and absent everywhere else, which would make it a fact about one case
rather than about schedules”.
That is not what happened: the effect appears at `n = 11`, `17` and `26`, three cells
with three different provenances and margins from `0.12` to `0.38`, and it is absent at
exactly the cells where the collective move is also absent.
So the two factors fail together, at the same place, which is itself evidence that they
are limited by the same thing — the collective escape probability the sparsity
measurement puts at `0.0000` for `n >= 26`.

## Limits, and one that bites

- **The long-schedule arms overshot the budget, and by how much is recorded.** The
  pair-test cap is tested at restart granularity, so an arm with ten-times-longer
  anneals overshoots by up to one anneal.
  Delivered budget as a multiple of declared, per cell: control `1.001` to `1.015`; long
  schedule `1.024` to `1.31`, and specifically `1.024` at `n = 11`, `1.024` at `n = 17`
  and `1.12` at `n = 26` — the three cells that decide this round.
  Those are close enough that the verdict stands.
  The both-factors arm is not so clean: `1.31` at `n = 17`, `2.13` at `n = 37` and
  `3.92` at `n = 50`, so its `n = 37` and `n = 50` results are **not** at equal budget
  and are reported as observations rather than as comparisons.
  The fix is to test the budget inside the anneal loop rather than between restarts, and
  it belongs in round 2 before any of this is re-run.
- One alternative length.
  Nothing here brackets an optimum, and a tenfold step is coarse.
- At fixed budget, longer anneals mean fewer restarts, so this round cannot separate
  “slower cooling helps” from “fewer, deeper descents help”.
  Varying the two independently is the obvious round-2 sweep and it needs no new code.
- Two factors at two levels each, five seeds, eleven cells, one host, one budget tier.
  This is the first factorial crossing on this problem that could be found, which makes
  it a starting point rather than a finding to lean on.
- `f64` screening; 990 poses independently re-checked at tolerance `1e-9`, zero
  failures, zero candidates below any standing best.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
