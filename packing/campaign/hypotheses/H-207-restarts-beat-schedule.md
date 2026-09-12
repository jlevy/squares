---
title: H-207 — restarts beat schedule tuning at equal cost
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-207
  kind: hypothesis
  claim: >-
    At equal total cost, running k independent blind trials and taking the best reaches a
    better `closed` than any single longer or better-scheduled run of the same physics. The
    landscape is multi-modal and the budget is better spent on restarts than on annealing
    more carefully within one.
  lane: search
  derived_from: [X-028]
  criterion:
    shape: record
    metric: closed at the best trial within a fixed cost budget
    direction: higher
    threshold: best-of-k at the shipped schedule beats the best single-run schedule found by the sweep
  instrument: packing/devtools/bench_annealing.py --sweep
  instrument_ready: true
  regime: >-
    the workbench's simulation; cost measured as total simulated steps, so a longer run and
    more restarts are compared on the same budget rather than on wall clock
  instance: {axis: n, point: 5}
  sweep: {axis: n, points: [5, 11, 17, 29]}
  priority: 1
  cost_estimate: minutes per grid cell at a thousand seeds
  registered: '2026-09-12'
---
# H-207 — restarts beat schedule tuning at equal cost

The evidence that suggested it: at n = 5 and shake level 6, two trials in a thousand
land at 0.139% and 0.230% excess while the next best is 4.854%. That is a rare basin,
not a gradient, and a rare basin is reached by trying again rather than by descending
more carefully.

**What would refute it.** A schedule — a shake profile, a contraction rate, a step count
— whose single run reaches a `closed` that best-of-k at the same total step count does
not.

**The trap to avoid.** Cost has to be counted in steps, not in wall clock, or the
comparison measures the harness’s overhead rather than the method.
