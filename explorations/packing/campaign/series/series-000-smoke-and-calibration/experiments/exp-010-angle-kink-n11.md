---
title: exp-010 — the angle objective is a corner, not a basin floor
softschema:
  contract: packing.squares:Experiment/v1
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-010
  series: series-000
  title: One-sided derivatives of the LP-in-cell optimum at Trump's tilt
  date: '2026-08-23'
  hypotheses: [H-019]
  tier: exploratory
  subject:
    label: sqpack.quench single-cell fixed point, probed either side of the optimal tilt
    engine: 'sqpack.quench 0.2.0'
    engine_commit: '8b450a1'
    precision: polished
    host_system: Linux container, 8 cores (remote session)
    selftest_passed: true
  instance: {axis: n, point: 11, role: target}
  method:
    control: 'delta = 0: the exact tilt, where the cell solve must reproduce the published side'
    candidate: 'the shared tilt of all five tilted squares displaced by delta, centres re-optimised by LP'
    runs_per_condition: 1
    interleaved: false
    operator: claude-opus-5
    commit: '8b450a1'
    entry_point: explorations/packing/sqpack/quench.py
    command: 'solve_to_fixed_point over delta in +/-{1e-6 .. 1e-2}, tilted squares moved together'
    budget: '11 probes'
    record: campaign/series/series-000-smoke-and-calibration/results/exp-010-angle-kink.jsonl
  effort:
    timebox: 15m
    wall_seconds: 1.0
    agent_minutes: 10
    stopped_by: criterion
  results:
  - shape: conditions
    metric: one_sided_slope_of_s_at_optimal_tilt
    role: outcome
    control_median: 0.1747
    candidate_median: 0.3841
    control_range: [0.1747, 0.1748]
    candidate_range: [0.3840, 0.3846]
    overlapping: false
  - shape: determination
    question: 'do the two one-sided derivatives of s at the optimal tilt differ'
    role: outcome
    outcome: reached_basin
    checked_by: 'left slope 0.1747, right slope 0.3841, ratio 2.198, over five decades of delta on each side'
  - shape: record
    metric: excess_at_exact_tilt
    role: guard
    direction: lower
    score: 1.742e-10
    standing_best: 0.0
    standing_best_source: 'frontier/n-011.md (Trump 1979)'
    beat_record: false
    runs: 1
  complexity:
    lines_changed: 0
    new_dependencies: []
    new_failure_modes: []
    notes: 'Pure measurement; no instrument change. First observed during exp-006 and re-run here as its own round, since it tests a different claim.'
  verdict:
    decision: accepted
    primary_criterion: one_sided_slope_of_s_at_optimal_tilt
    reason: >-
      Confirms H-019: the one-sided slopes are 0.1747 and 0.3841, a ratio of 2.198 that
      is stable over five decades on each side, so the optimum of s(theta) is a corner
      rather than a smooth minimum - which is why no smooth local model converges to it.
    commit: '8b450a1'
---
# exp-010 — the corner

Move the shared tilt of Trump’s five tilted squares off its optimal value, re-optimise
the centres by LP at each step, and record the excess over the published side.

| `δ` | `s(θ* + δ) − s*` | slope |
| ---: | ---: | ---: |
| `−1e-2` | `1.748e-03` | `0.1748` |
| `−1e-4` | `1.747e-05` | `0.1747` |
| `−1e-6` | `1.746e-07` | `0.1746` |
| `0` | `1.742e-10` | — |
| `+1e-6` | `3.841e-07` | `0.3841` |
| `+1e-4` | `3.840e-05` | `0.3840` |
| `+1e-2` | `3.846e-03` | `0.3846` |

Linear on both sides, and the slopes do not match: `0.1747` against `0.3841`, a ratio of
`2.198` holding over five decades either way.
A smooth minimum has one derivative and it is zero.
This has two, and neither is.

## Why the optimum has to be a corner

The tilt is held in place by contacts.
Rotating one way loads one set of them; rotating the other way loads a different set.
The two one-sided slopes are the marginal cost of the two different active contact
structures, and they have no reason to agree — so the optimum sits exactly at the angle
where the active set changes.
That establishes a kink on this one-dimensional angle slice, not rigidity of the full
packing. It is the same local response that [exp-005](exp-005-basin-entry-n11.md) met
from the other side: a corner produces a *linear* response to perturbation, which is why
that round’s return distance scaled like `eps` rather than `eps²` and never revealed a
basin radius.

## What it decides

Method choice for the quench spine’s angle half, and not as a preference:

- **Measured to fail:** finite-difference descent stalls five orders short
  ([exp-006](exp-006-lp-quench-n5-n10-n11.md)); Powell and Nelder-Mead do *worse* than
  descent, because a smooth local model is exactly the wrong model at a corner.
- **Measured to work:** golden-section bracketing over merged angle classes reaches the
  analytic optimum to machine precision on both proved cells
  ([exp-007](exp-007-quench-bracket-n5.md), [exp-008](exp-008-quench-bracket-n10.md)).

A bracketing search needs no derivative and so does not care that none exists.

## Limits

- One direction in angle space, at one instance.
  The claim’s sweep declares `n = 5` and `n = 10` as well, and both cells are open: the
  ledger shows the coverage.
- The `δ = 0` cell carries an excess of `1.742e-10` rather than zero because the tilt is
  read from a `f64` export of the degree-8 field, not from the field itself.
  It is a floor on this probe’s resolution, and it is far below every slope measured.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
