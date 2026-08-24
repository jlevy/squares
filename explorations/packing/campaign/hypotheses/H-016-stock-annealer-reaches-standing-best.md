---
title: H-016 — the stock annealer reaches the standing best on every cell
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-016
  kind: hypothesis
  claim: >-
    The stock sqsearch annealer, at 100M moves per chain over 8 chains and 5 seeds,
    reaches within 1e-4 of the standing best on every cell of the sweep n = 10, 11, 12.
  lane: search
  derived_from: []
  strategy_refs: ['search:10']
  criterion:
    shape: record
    metric: best_side
    direction: lower
    threshold: 1e-4
  instrument: cases.campaign_smoke.baseline_sweep, gated by sqsearch --selftest
  instrument_ready: true
  regime: sqsearch 0.1.0, f64 screening, M1 Pro 8P+2E, deterministic seeds 1-5
  instance: {axis: n, point: 11}
  sweep: {axis: n, points: [10, 11, 12]}
  priority: 3
  cost_estimate: 12e9 moves, ~5 minutes wall
  prereqs: []
  replication: false
  registered: retroactive
  notes: >-
    The null hypothesis, resolved by exp-001. Renumbered from H-001 when this campaign
    merged with the standing review's register, which owns H-001..H-015; no artifact had
    been published under the old id.
---
# H-016 — the null hypothesis

The claim anyone would make before looking: a general-purpose annealer, given a serious
budget, finds the best known packing.

It was worth registering precisely because it was expected to be partly wrong, and the
shape of the failure was the campaign’s starting information.
[exp-001](../series/series-000-smoke-and-calibration/experiments/exp-001-baseline-sweep.md)
refuted it — within `1e-4` only at `n = 12`, missing by `4.19e-04` at `n = 10` and
`3.73e-02` at `n = 11` — and the two failures turned out to be different in kind, which
one criterion could not distinguish.

That distinction is the reason [H-002](H-002-lp-in-cell-polish.md) is now the registry’s
top priority: `n = 10` was a polish failure inside the right basin.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
