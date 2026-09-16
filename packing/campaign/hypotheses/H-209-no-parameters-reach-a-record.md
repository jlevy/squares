---
title: H-209 — no parameter set in the workbench's own space reaches a record
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-209
  kind: hypothesis
  claim: >-
    No combination of the workbench's exposed parameters -- the shake dial, the container
    inflation, the force law's four terms, the step count -- produces a blind run that lands
    within 0.1 per cent of a known-best side at any n between 5 and 29.
  lane: search
  derived_from: [X-034]
  criterion:
    shape: determination
    metric: whether any cell of the parameter sweep produces a trial inside the close tolerance
    direction: no cell does
    threshold: 0.1
  instrument: packages/workbench/tools/workbench_tools/benchmark.py --sweep
  instrument_ready: false
  regime: >-
    the workbench's simulation as shipped; a negative here is about this instrument and not
    about annealing in general
  instance: {axis: n, point: 5}
  sweep: {axis: n, points: [5, 10, 11, 17, 26, 29]}
  priority: 1
  cost_estimate: one full grid, tens of minutes
  registered: '2026-09-12'
---
# H-209 — no parameter set in the workbench’s own space reaches a record

**Identity.** Derived from X-034, which was X-028 until 2026-09-13 and X-029 until
2026-09-14.

Stated so it can be wrong, and worth stating because the negative is useful: it would
say the animation’s physics is a picture of a search rather than a search, and that
improving it means changing the method rather than its dials.

**Where it stands.** No repaired run in the retained summaries is within 0.1% of a
record. The closest is 0.15% above `s(5)`, the best of 39,871 runs at shake level 6
([exp-207](../series/series-000-smoke-and-calibration/experiments/exp-207-h207-what-restarts-buy.md)).
Only the shake dial has been swept on repaired runs; inflation, the force law and the
step count have not.

**What would refute it.** One trial, at any cell, inside the tolerance.
A single counterexample settles it, which makes this the cheapest claim in the registry
to disprove and the most expensive to confirm.

**No instrument can run the test yet.** The harness passes only the shake level and the
inflation to the page and drops any other sweep key without saying so.
A sweep of the force law or the step count would run identical cells under different
labels, a false negative in this claim’s favour.
The test needs an instrument that sets the force law’s four terms and the step count,
refuses what it cannot set, and records the configuration the page ran.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
