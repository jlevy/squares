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
  derived_from: [X-034]
  criterion:
    shape: record
    metric: closed at the best trial within a fixed cost budget
    direction: higher
    threshold: best-of-k at the shipped schedule beats the best single-run schedule found by the sweep
  instrument: packages/workbench/tools/workbench_tools/benchmark.py --sweep
  instrument_ready: false
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

**Identity.** Derived from X-034, which was X-028 until 2026-09-13 and X-029 until
2026-09-14.

**Why it is worth testing.** Once runs are repaired to packings, a single run scores
below the trivial grid at every `n` measured, while the best of a thousand sometimes
comes within a fraction of a per cent of the record
([X-034](../explorations/X-034-the-workbench-physics-as-a-search.md)). If that holds
under a fair comparison, budget spent on restarts is worth more than budget spent on one
careful run. Those observations are prefix values without spread, so they motivate the
test and do not decide it.

**What would refute it.** A schedule — a shake profile, a contraction rate, a step count
— whose single run reaches a `closed` that best-of-k at the same total step count does
not.

**The trap to avoid.** Cost has to be counted in steps, not in wall clock, or the
comparison measures the harness’s overhead rather than the method.

**No instrument can run the test yet.** The harness sweeps only the shake level and the
container inflation, drops any other sweep key without saying so, and budgets in wall
clock. The test needs an instrument that varies the schedule this claim names (the shake
profile, the contraction rate and the step count) and budgets both arms in simulated
steps. The package benchmark on #160 refuses the keys it cannot set instead of dropping
them, but it still sweeps only those two parameters and budgets in seconds.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
