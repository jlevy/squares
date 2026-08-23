---
title: exp-006 — the LP-in-cell quench, on annealer output at n = 5, 10, 11
softschema:
  contract: packing.squares:Experiment/v1
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-006
  series: series-000
  title: The LP-in-cell quench applied to annealer output, and why its angle half stalls
  date: '2026-08-23'
  hypotheses: [H-002]
  tier: exploratory
  subject:
    label: sqpack.quench (scipy HiGHS) over sqsearch output
    engine: 'sqpack.quench 0.1.0 over sqsearch 0.1.0'
    engine_commit: '8b450a1'
    precision: polished
    host_system: Linux container, 8 cores (remote session)
    selftest_passed: true
  instance: {axis: n, point: 11, role: target}
  method:
    control: 'the annealer''s own best configuration, unpolished'
    candidate: 'that configuration after the LP-in-cell quench (LP solve, cell re-read to a fixed point, finite-difference angle descent)'
    runs_per_condition: 5
    interleaved: true
    operator: claude-opus-5
    commit: '8b450a1'
    entry_point: explorations/packing/run_quench.py
    command: 'python3 run_quench.py'
    budget: '19 rounds, 20,135 LP solves, 72.8 s'
    record: campaign/series/series-000-smoke-and-calibration/results/exp-006-lp-quench.jsonl
  effort:
    timebox: 2h
    wall_seconds: 72.8
    agent_minutes: 115
    stopped_by: criterion
  results:
  - shape: record
    metric: quenched_gap_n11
    role: outcome
    direction: lower
    score: 0.06999
    standing_best: 0.0
    standing_best_source: 'frontier/n-011.md (Trump 1979), as the analytic target'
    beat_record: false
    runs: 5
  - shape: conditions
    metric: gap_to_analytic_n11
    role: outcome
    control_median: 0.08846
    candidate_median: 0.06999
    control_range: [0.06440, 0.10020]
    candidate_range: [0.04608, 0.08846]
    overlapping: true
  - shape: conditions
    metric: gap_to_analytic_n10
    role: outcome
    control_median: 0.005318
    candidate_median: 0.004507
    control_range: [0.002166, 0.015130]
    candidate_range: [0.000841, 0.013380]
    overlapping: true
  - shape: determination
    question: 'does the quench refine annealer output to the analytic value within 1e-12'
    role: outcome
    outcome: no_progress
    checked_by: 'gap to the analytic optimum at n = 5, 10, 11; best quenched gap 2.3e-08 at n = 5, 8.4e-04 at n = 10, 4.6e-02 at n = 11'
  - shape: record
    metric: single_cell_solve_at_exact_angles
    role: mechanism
    direction: lower
    score: 4.441e-16
    standing_best: 0.0
    standing_best_source: 'frontier/n-011.md; the LP at Trump''s own angles'
    beat_record: false
    runs: 1
  - shape: determination
    question: 'does a class-constrained one-dimensional angle search reach the analytic value'
    role: mechanism
    outcome: reached_basin
    checked_by: 'golden section on the shared tilt: theta error 3.3e-10 to 4.1e-10, gap 7.4e-12 to 2.2e-11, in 70 LP solves'
  - shape: determination
    question: 'is s(theta) smooth at the optimal angles'
    role: mechanism
    outcome: no_progress
    checked_by: 'one-sided slopes 0.175 and 0.384 at the optimal tilt; a kink, not a smooth minimum'
  complexity:
    lines_changed: 322
    new_dependencies: [scipy]
    new_failure_modes: ['LP solver tolerance can exceed the quantity being measured; every solution is post-checked against its own constraints']
    notes: 'Adds sqpack/quench.py and run_quench.py. No Rust; the spine is scipy and standard library, as the stack decision requires.'
  verdict:
    decision: rejected
    primary_criterion: gap_to_analytic
    reason: >-
      Refutes H-002 as stated: the quench does not refine annealer output to the
      analytic value, improving the gap by only 1.1-1.3x because it is a LOCAL cell
      optimiser and the annealer hands it the wrong basin. The single-cell half stands
      (4.4e-16 at exact angles) and a class-constrained 1-D angle search reaches 2e-11,
      so what fails is the free-angle descent - and H-019 says why.
    commit: '8b450a1'
---
# exp-006 — the quench works, and does not do what the hypothesis said it would

## What was measured

Three things, on one instrument:

1. **The claim.** `sqsearch`’s own best configuration at `n = 5, 10, 11`, five seeds
   each, quenched — LP solve, cell re-read to a fixed point, then finite-difference
   descent on the eleven angles — and scored against the analytic optimum.
2. **The single-cell half**, already established by the standing review and re-derived
   here independently.
3. **A class-constrained variant** at `n = 11`: all five tilted squares share one angle,
   found by golden section rather than descent.

## Result

| `n` | annealer gap (median) | quenched gap (median) | improvement | LP solves | converged |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 5 | `3.427e-08` | `3.187e-08` | 1.1× | 71 | 5/5 |
| 10 | `5.318e-03` | `4.507e-03` | 1.2× | 319 | 4/5 |
| 11 | `8.846e-02` | `6.999e-02` | 1.3× | 1,024 | 3/5 |

Control and candidate ranges overlap at every instance, which under the accept rule
means **no detectable effect**, not a small win.

**H-002 is refuted as stated.** Its claim was that alternating LP solves with local
angle moves refines *any* annealer output to a cell optimum matching the analytic value
to `1e-12`. The best quenched gap anywhere is `2.3e-08` (at `n = 5`, where the annealer
was already there), `8.4e-04` at `n = 10`, and `4.6e-02` at `n = 11`.

Two mechanism results explain the refutation and are worth more than it.

**The single-cell half is exact, and independently reproduced.** Solving the cell at
Trump’s own angles gives `s = 3.877083590022814` — `+4.4e-16` from the published value.
The review’s result was verified here from scratch, and the LP formulation is not what
fails.

**A class-constrained angle search reaches the analytic value.** Constrain the eleven
angles to two classes — six axis-aligned, five sharing one tilt — and golden-section the
shared tilt, and the answer arrives at `θ` error `3.3e-10` to `4.1e-10` and side gap
between `−7.4e-12` and `−2.2e-11`, in **70 LP solves** against the free descent’s 1,024.
The negative sign is the solver’s noise floor, not a record: at a primal feasibility
tolerance of `1e-10` a side is not resolvable below roughly `1e-11`, which is exactly
where these land.
Nothing here may claim anything about the record, and the tier says so.

## What the prediction got wrong

Two things, one about the quench and one about the landscape.

**The quench is a polisher, not a rescue.** The hypothesis said “refines *any* annealer
output” — but an LP-in-cell solve is a *local* operation: it finds the best packing in
the cell it is handed, and if the annealer is in the wrong basin the quench returns the
best point of the wrong basin.
At `n = 11` that is a 1.3× improvement on a gap of `8.8e-02`. The spine does not lift
the burden of finding the right basin off the proposer; it makes the landing point exact
and nameable, which is a different and still valuable thing.

**The angle objective has a kink at the optimum, and that is why descent stalls.**
Walking the shared tilt off its optimal value:

| `δ` | `s(θ* + δ) − s*` |
| ---: | ---: |
| `−1e-3` | `1.748e-04` |
| `−1e-5` | `1.747e-06` |
| `0` | `1.742e-10` |
| `+1e-5` | `3.840e-06` |
| `+1e-3` | `3.846e-04` |

Linear on both sides, slopes `0.175` and `0.384`. The optimum is a **corner**, where the
active contact set changes — which is what rigidity looks like from the angle side, and
it is fatal to any method that assumes a smooth local model.
Measured in the same round: finite-difference descent stalls five orders short; **Powell
and Nelder-Mead both did worse than descent** (`+1.06e-02` and `+3.34e-06` against
descent’s `+2.78e-07` at `eps = 1e-5`). Registered as
[H-019](../../../hypotheses/H-019-angle-optimum-is-a-kink.md) before this round was
recorded, since it is a claim H-002 did not make.

This also re-reads [exp-005](exp-005-basin-entry-n11.md): its return distance was linear
in the perturbation with no threshold, and a corner minimum is exactly what produces a
linear rather than quadratic response.
The two rounds are measuring the same geometric fact from opposite sides.

## The defect this round found, which is the repository’s own thesis one layer up

The first working version reported `s = 3.877083568103152` at `n = 11` — **below Trump’s
`3.877083590022814`**. The runbook’s rule held: a run that beats the record has found a
bug. It had.
The configuration overlapped on pair `(4, 8)` by `9.876e-08`, and the LP had
returned a solution violating *its own imposed constraint* by that amount, because HiGHS
defaults to a primal feasibility tolerance of `1e-7` — larger than the quantity being
measured.

That is precisely the failure the exact verifier exists to close ("a tolerance loose
enough to accept true contact is loose enough to accept a small overlap"), appearing
inside the refiner rather than the checker.
Two fixes, both in `sqpack/quench.py`: the tolerance is pinned at HiGHS’s floor of
`1e-10`, and every returned solution is post-checked against the constraints that were
imposed on it, with a violation rejecting the solve rather than being reported.
After the fix the same configuration scores `+4.8e-08`, and no gap anywhere in the
recorded sweep is negative beyond the `2.2e-11` solver floor.

## Annotation, 2026-08-23: this round is a sweep recorded as one cell

`exp-006` declares `instance: {point: 11}` but measures `n = 5`, `10` and `11`, which is
the defect the standing review raised as F-6 against `exp-001` — recorded here rather
than erased, because the same runner made the same mistake one round later.
Its numbers stand; what is wrong is that the ledger reads its sweep coverage from one
cell, so `H-002` showed two of three cells open when all three had been measured.

The successor sweep is split correctly, one round per cell:
[exp-007](exp-007-quench-bracket-n5.md), [exp-008](exp-008-quench-bracket-n10.md),
[exp-009](exp-009-quench-bracket-n11.md).
Those rounds also supersede this one’s central finding: the quench’s failure to reach
the analytic value was a property of the *angle search method*, not of the quench, and
the bracketing variant reaches machine precision on both proved cells.

## Limits

- `polished` tier: exact within a cell to *solver* precision, which this round measured
  at roughly `1e-11`, not exact in the algebraic sense.
  No claim here may be promoted without `sqpack.verify` over the packing’s own field.
- Five seeds per instance is enough to see the spread, not to claim an interval; the
  round is `exploratory`.
- The class-constrained arm assumes the answer’s own structure (two angle classes), so
  it demonstrates that the *angle search method* decides the outcome — it is not
  evidence that an unguided search would find that structure.
  That is [H-001](../../../hypotheses/H-001-angle-class-reduction.md)’s claim, and it
  remains untested.
- The kink was probed at `n = 11` only, along one direction in angle space.

## What to run next

1. **A non-smooth angle method** — bisection on the sign of the one-sided derivative,
   which is what the kink actually admits, generalised past one dimension.
   This is the successor to H-002 and the spine’s real angle half.
2. **H-001**, now with a concrete prior: the class-constrained search reached the solver
   floor in 70 LP solves where free descent needed 1,024 and landed five orders worse.
3. **Re-run [exp-005](exp-005-basin-entry-n11.md)’s basin-entry sweep against the
   quench** rather than the annealer, which was that round’s own stated successor.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
