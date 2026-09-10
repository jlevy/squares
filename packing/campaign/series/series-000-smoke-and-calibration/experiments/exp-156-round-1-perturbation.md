---
title: exp-156 — the simultaneous perturbation move on eleven non-grid cells
softschema:
  contract: packing.squares:Experiment/v2
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-156
  series: series-000
  title: The simultaneous perturbation move on eleven non-grid cells
  date: '2026-09-08'
  hypotheses:
  - H-158
  tier: exploratory
  subject:
    label: sqsearch --p-perturb 1.0 --perturb-scale 2, against the stock annealer
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
    control: sqsearch at its defaults, single-square translate and rotate only
    candidate: the same engine with every proposal displacing all n squares at once
    runs_per_condition: 5
    interleaved: false
    operator: claude-opus-5
    commit: 9ae7700
    dirty: true
    entry_point: devtools/run_arm_sweep.py
    command: python3 devtools/run_arm_sweep.py plan-part-1.yaml --out part-1
    budget: 1.25e9 pair tests per chain, 8 chains, 5 seeds, 11 cells per arm
    record: campaign/series/series-000-smoke-and-calibration/results/exp-156-round-1/
  effort:
    timebox: 3h
    wall_seconds: 3663.0
    agent_minutes: 60
    pair_tests: 1116000000000
    stopped_by: criterion
  results:
  - shape: conditions
    metric: best_side_n11
    role: outcome
    control_median: 3.935790212325
    candidate_median: 3.893791421851
    control_range:
    - 3.922760527419
    - 3.946821043844
    candidate_range:
    - 3.886755282194
    - 3.896139518556
    change_pct: -1.07
    overlapping: false
  - shape: conditions
    metric: best_side_n17
    role: outcome
    control_median: 5.0
    candidate_median: 4.707375696052
    control_range:
    - 4.997152231858
    - 5.0
    candidate_range:
    - 4.682226780795
    - 4.708111421935
    change_pct: -5.85
    overlapping: false
  - shape: conditions
    metric: best_side_n26
    role: outcome
    control_median: 6.0
    candidate_median: 5.823449563505
    control_range:
    - 6.0
    - 6.0
    candidate_range:
    - 5.746573596103
    - 5.845242459340
    change_pct: -2.94
    overlapping: false
  - shape: conditions
    metric: best_side_n19
    role: outcome
    control_median: 5.0
    candidate_median: 4.984416587104
    control_range:
    - 5.0
    - 5.0
    candidate_range:
    - 4.958947727599
    - 5.0
    change_pct: -0.31
    overlapping: true
  - shape: determination
    question: does the candidate lower the median best side by 0.01 with disjoint seed ranges
      on at least six of the eleven cells
    role: outcome
    outcome: criterion_missed
    checked_by: 'three cells (n = 11, 17, 26) meet both clauses and a fourth (n = 19) meets
      the threshold with overlapping ranges; six were required'
  - shape: determination
    question: does the candidate reach the standing best basin on a cell where the control does not
    role: outcome
    outcome: reached_basin
    checked_by: 'n = 10: 5 of 5 seeds within 1e-4 and 3 of 5 within 1e-6 of the proved
      3 + 1/sqrt(2), against 0 of 5 for the control'
  - shape: record
    metric: best_side
    role: outcome
    direction: lower
    score: 3.886755282194
    standing_best: 3.877083590023
    standing_best_source: frontier/n-011.md (Walter Trump 1979)
    beat_record: false
    runs: 5
  - shape: determination
    question: how close does the candidate get on the oblique record-finding cell n = 17
    role: mechanism
    outcome: near_miss
    checked_by: 'best of five seeds 4.682226780795 against the 4.675530093605 recorded in
      frontier/n-017.md, a gap of +6.70e-03, with the control at the trivial 5.0'
  - shape: determination
    question: is every archived pose a valid packing at the side its line claims
    role: guard
    outcome: criterion_met
    checked_by: 'packing-campaign verify-archive over 990 poses in a separate process,
      sqpack.verify at tolerance 1e-9, zero failures, zero candidates below any record'
  - shape: determination
    question: does the n=10 positive control land within 1e-2 of its proved value
    role: guard
    outcome: criterion_met
    checked_by: 'control 3.707815, candidate 3.707107, proved 3.707107; no arm reported a
      side below any standing best'
  complexity:
    lines_changed: 236
    new_dependencies: []
    new_failure_modes:
    - 'The pair-test budget is enforced at restart granularity, so an arm overshoots by up
      to one anneal. Delivered budget per cell is recorded; the candidate overshot by 0.1
      to 4 percent on the cells that decide the verdict.'
    notes: One flag pair on the engine, off by default, with the control chain pinned in the selftest.
  verdict:
    decision: rejected
    primary_criterion: median best_side, candidate against control, at equal pair-test budget
    reason: 'The criterion was measured and missed: three cells of eleven meet both clauses
      and four meet the threshold, against the six declared -- but the four where it works
      it works by 0.017 to 0.29, and the six where it does nothing it does exactly nothing,
      so the move is not weak, it is inapplicable above n = 26 at this budget.'
    commit: 9ae7700
---
# exp-156 — a move that changes everything on four cells and nothing on six

## The benchmark, and why these eleven cells

Re-derived for this round from the 100 frontier case files: **36 of the 100 cases at
`n <= 100` have a best known packing that beats the `ceil(sqrt(n))` grid.** The other 64
are the grid, which `sqsearch` returns by construction, so they are not a search
problem. Of the 36: 15 hand construction, 10 simulated annealing, 6 diagonal strip, 3
extension from a neighbour, 2 unknown.

Eleven of the 36 were chosen, stratified by margin over the grid and by provenance.
Every one is non-grid, so no arm can score by returning the incumbent.

| cell | record | grid | margin | provenance | why it is in |
| ---: | --- | ---: | ---: | --- | --- |
| 5 | `2.707107` | 3 | `0.293` | Göbel 1979, proved | machinery control; a 45° mechanism blind search reaches |
| 10 | `3.707107` | 4 | `0.293` | Göbel 1979, proved | the campaign’s positive control, and exp-001’s *polish* failure |
| 11 | `3.877084` | 4 | `0.123` | Trump 1979 | the campaign target; oblique core, exp-001’s *exploration* failure |
| 17 | `4.675530` | 5 | `0.325` | Bidwell 1998 | the only cell that tests oblique record-*finding*; exp-011 refuted here |
| 19 | `4.885618` | 5 | `0.114` | Wainwright 1979 | the small-margin end |
| 26 | `5.621320` | 6 | `0.379` | Friedman 1997 | the large-margin end |
| 27 | `5.707107` | 6 | `0.293` | Göbel 1979 | a diagonal-strip family member, structured |
| 29 | `5.933833` | 6 | `0.066` | Schadt 2025 | the smallest margin in the set; Gensane’s record stood 21 years here |
| 37 | `6.598620` | 7 | `0.401` | Cantrell 2002 | largest margin in the thirties |
| 50 | `7.571429` | 8 | `0.429` | Schadt 2025 | largest margin above 40, annealing-found |
| 52 | `7.707107` | 8 | `0.293` | Göbel 1979 | the diagonal-strip family again, at larger `n` |

## The accept rule, declared before the round

An arm is **accepted** over the control when all of:

1. **Outcome.** Its median `best_side` over five seeds is at least `0.01` below the
   control’s median *and* the two seed ranges do not overlap, on at least **six of the
   eleven** cells — or it reaches `reached_basin` on a cell where the control does not.
2. **Evidence.** Five seeds per cell, median and min-max range both reported.
   Overlapping ranges mean no detectable effect, never a small win.
3. **Numerical guard.** Every reported configuration has `overlap == 0` under the engine
   screen and the engine selftest passed on the binary that ran.
4. **Guards.** The `n = 10` positive control lands within `1e-2`; every archived pose
   passes an independent `sqpack.verify` re-check in a separate process; any candidate
   below a standing best is flagged separately and never averaged into a median.
5. **Carrying cost.** One sentence of judgement.

Reported separately and *not* part of the rule: the hit rate, the fraction of runs
within `1e-6` of the record, and the basin rate at `1e-4`.

Every table below is regenerated from the archived summaries rather than retyped:

```
python3 devtools/run_arm_sweep.py \
  <results>/exp-156-round-1/part-1/summary-rebuilt.json \
  <results>/exp-156-round-1/part-2/summary.json \
  <results>/exp-156-round-1/part-3/summary.json --report
```

**Budget: `1.25e9` pair tests per chain, eight chains, so `1e10` per (arm, cell,
seed).** Pair tests, not moves and not seconds: a simultaneous perturbation scans every
pair where a single-square move scans one square’s, and the host carried other agents’
work throughout, with the one-minute load average between 17 and 52 on ten cores.
A wall-clock budget on this machine would have measured the other agents.

## Result

| cell | record | control median / best | candidate median / best | median improvement | ranges disjoint |
| ---: | --- | --- | --- | ---: | :---: |
| 5 | `2.707107` | `2.707107` / `2.707107` | `2.707107` / `2.707107` | `0.000` | – |
| 10 | `3.707107` | `3.707815` / `3.707526` | `3.707107` / `3.707107` | `0.0007` | yes |
| 11 | `3.877084` | `3.935790` / `3.922761` | `3.893791` / `3.886755` | **`0.042`** | **yes** |
| 17 | `4.675530` | `5.000000` / `4.997152` | `4.707376` / `4.682227` | **`0.293`** | **yes** |
| 19 | `4.885618` | `5.000000` / `5.000000` | `4.984417` / `4.958948` | `0.016` | no |
| 26 | `5.621320` | `6.000000` / `6.000000` | `5.823450` / `5.746574` | **`0.177`** | **yes** |
| 27 | `5.707107` | `6.000000` / `6.000000` | `6.000000` / `5.878417` | `0.000` | no |
| 29 | `5.933833` | `6.000000` / `6.000000` | `6.000000` / `6.000000` | `0.000` | – |
| 37 | `6.598620` | `7.000000` / `7.000000` | `7.000000` / `7.000000` | `0.000` | – |
| 50 | `7.571429` | `8.000000` / `8.000000` | `8.000000` / `8.000000` | `0.000` | – |
| 52 | `7.707107` | `8.000000` / `8.000000` | `8.000000` / `8.000000` | `0.000` | – |

| arm | verified poses | runs beating the grid | basin `1e-4` | hits `1e-6` | below any record |
| --- | ---: | ---: | ---: | ---: | ---: |
| control | 495 ok | 16/55 | 5 | 5 | 0 |
| candidate | 495 ok | 30/55 | 10 | 8 | 0 |

**H-158 is refuted on its declared criterion.** Three cells meet both clauses of the
rule, four meet the `0.01` threshold, and six were required.

That is the verdict, and it is a bad summary of what happened, so the rest of this
section says what did.

**On the cell this campaign exists for, the move roughly halves the gap.** At `n = 11`
the control’s median is `3.935790` and the candidate’s is `3.893791`; the gap to Trump
falls from `5.87e-02` to `1.67e-02`, and no candidate seed is worse than any control
seed. exp-001’s `n = 11` figure was `3.9144` best of five, and this arm’s worst seed
beats it.

**On the cell this campaign already refuted, the move is the difference between the
trivial grid and something close to the record.** exp-011 measured `5.000000` at
`n = 17` on five seeds of five, `+3.2447e-01`. The control here reproduces that
(`5.000000` median, one seed at `4.997152`). The candidate’s median is `4.707376` and
its best seed is `4.682227` — `+6.70e-03` from Bidwell’s 1998 hand construction, found
cold, at a gap forty-eight times smaller than the control’s.

**On `n = 10` the move fixes exp-001’s other failure, the one nobody had a fix for.**
exp-001 read `n = 10` as a *polish* failure: the search finds the right basin and stops
`4.19e-04` short. The control here reproduces that exactly (`+7.08e-04`). The candidate
reaches `+3.14e-07`, inside the `1e-4` basin proxy on 5 seeds of 5 and inside `1e-6` on
3 of 5. That satisfies the second branch of clause 1 — `reached_basin` on a cell where
the control does not — and it says the polish failure was never a polish failure.
It was the same plateau: the last `4e-4` at `n = 10` needs several squares to move
together, and no single-square move set can propose that.

**And on five cells of eleven it does exactly nothing.** At `n = 29, 37, 50, 52` every
seed of both arms returns the grid, bit for bit.
At `n = 27` the median is the grid for both, though the candidate’s best seed reaches
`5.878417`. The failure is not gradual: there is no cell where the arm gets partway.
It either leaves the grid or it does not, and above `n = 26` it does not.

## The mechanism, measured

`devtools/measure_objective_sparsity.py` draws proposals from the same two distributions
the engine draws from and counts what each does to `required_side`.

At the trivial grid, over 8,000 proposals per kind per cell at scales `0.01`, `0.05` and
`0.2` alike, **no single-square proposal lowers the objective at all** for any cell in
this subset except `n = 5`. A quarter to a third of them change it, and every one of
those raises it. The grid is a strict local minimum of `required_side` under the entire
single-square move set, because its binding span is attained by a whole row or column of
`m` squares at once and no one of them is the unique extremum whose retreat could shrink
it. Collective proposals do better but not much: `0.0034` to `0.0051` of them lower the
side at `n = 11`, `0.0006` to `0.0009` at `n = 17`, and `0.0000` at `n >= 26`.

Probing the arms’ own emitted configurations closes the loop.
Every control pose at `n = 18` is the grid and has a single-square improvement rate of
`0.0000`; every candidate pose is off the grid at side `4.83` to `4.87` and has a rate
of `0.017` to `0.040`. **The single-square move set is not weak in general.
It is exactly, and only, useless at the configuration every chain starts from and keeps
returning to.**

That also explains the shape of the failure at large `n`. The escape is a rare
collective event whose probability falls with `n` — the measured collective improvement
rate goes `0.0051`, `0.0009`, `0.0000` across `n = 11, 17, 26` — so a fixed budget buys
escapes at `n <= 26` and not beyond.

## What the prediction got wrong

**The dose, by a factor of twenty.** The design input proposed `p_perturb = 0.05`.
[exp-155](exp-155-arm-calibration.md) measured that value as indistinguishable from the
control, and the setting that works is `1.0` — every proposal collective, the stock move
set switched off entirely.
“Add a proposal at 5 %” and “replace the proposal distribution” are different changes
and only the second one moves the number.

**The reach.** The registered claim expected an effect on at least half the cells.
The effect is confined to `n <= 26`, and inside that range it is far larger than the
`0.01` the hypothesis asked for.
A threshold-and-count rule cannot express “transforms four cells, inert on six”, and
this round is the argument for scoring reach and depth separately in round 2.

**The cost, in the reassuring direction.** The perturbation arm was expected to be much
more expensive per pair test, because it recomputes `n` sine-cosine pairs per move
against the control’s one.
Over the whole sweep it cost `1999 s` against `1664 s`, about 20 % more, because the
transcendental overhead is `O(n)` while the pair work it is measured against is
`O(n^2)`. It is expensive only at small `n`, where it wins anyway.

## Limits

- One point in the `(p_perturb, perturb_scale)` plane, chosen on two held-out cells at
  `n = 18` and `n = 40`. A negative result on the six inert cells is a result about that
  point.
- **The pair-test budget is enforced at restart granularity, so an arm overshoots by up
  to one anneal.** Delivered budget as a multiple of declared, per cell: control `1.001`
  to `1.015`; candidate `1.001` to `1.040` on the four cells that decide the verdict,
  and up to `1.27` at `n = 52` where neither arm left the grid.
  The comparison is clean where it matters and the overshoot is recorded rather than
  assumed harmless.
- One budget tier, `1e10` pair tests per seed.
  The record engines run four to six orders of magnitude beyond this, so “inert above
  `n = 26`” is a statement about this budget.
- `f64` screening. 990 poses were rebuilt and re-decided by `sqpack.verify` in a separate
  process at tolerance `1e-9`, zero failures and zero candidates below any standing
  best. That refutes a forged pose and certifies nothing.
- Wall-clock figures are not comparable across arms or against other rounds: the host
  carried other agents’ work at load 17 to 52 on ten cores throughout.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
