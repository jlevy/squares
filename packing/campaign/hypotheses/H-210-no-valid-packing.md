---
title: H-210 — the blind physics never settles to a valid packing
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-210
  kind: hypothesis
  claim: >-
    No blind run of the workbench's physics ends on a valid packing. At every n and every
    parameter setting the squares come to rest overlapping, so every side it reports is a
    bounding box around an invalid arrangement rather than a container a packing needs.
  lane: search
  derived_from: [X-034]
  criterion:
    shape: determination
    metric: the deepest pairwise overlap in the final arrangement, by separating axis
    direction: above tolerance in every trial
    threshold: 0.00001
  instrument: packages/workbench/tools/workbench_tools/benchmark.py
  instrument_ready: true
  regime: >-
    the workbench's simulation in blind mode; the tolerance is chosen, and the snapped mode,
    valid by construction, was observed once beside it and not kept (think-2ngs)
  instance: {axis: n, point: 11}
  sweep: {axis: n, points: [5, 10, 11, 17, 26, 29]}
  priority: 1
  cost_estimate: seconds
  registered: '2026-09-12'
---
# H-210 — the blind physics never settles to a valid packing

**Identity.** Derived from X-034, which was X-028 until 2026-09-13 and X-029 until
2026-09-14.

**Registered so the claim can be tested rather than assumed.** It was registered after
its data: the runs
[exp-210](../series/series-000-smoke-and-calibration/experiments/exp-210-h210-blind-runs-are-not-packings.md)
reports came first, so that round is the exploratory data behind the claim, filed under
the open question [H-212](H-212-the-workbench-physics-as-a-search.md), and not its test.
The test is a preregistered round on seed blocks those runs did not use.

Every blind run observed ended with squares overlapping: in 123,190 runs of the repaired
rounds, whose rows are not retained, the deepest overlap before repair ranged from 0.002
to 0.118 of a unit side.
A separating-axis test measured it over the final poses, against a chosen tolerance of
1e-5
([exp-210](../series/series-000-smoke-and-calibration/experiments/exp-210-h210-blind-runs-are-not-packings.md)).
The trials were not kept, so this is an observation to re-measure rather than a result.

**Why it happens.** The page’s blind contraction advances whenever the deepest overlap
is at most 0.08 of a unit side, and closes the walls onto the known-best side
(`BLIND.overlapTol` in `workbench.js`). The runs are squeezed into the record’s own
container with that much overlap allowed, and nothing afterwards drives it out.

**What would refute it.** One blind run, at any n and any parameters, whose deepest
final overlap is under 1e-5. That is the same falsifier as H-209’s and a cheaper one to
check, which is why it is worth having both.

**What follows if it stands.** Every side the instrument reads directly is a bounding
box rather than a container, so scoring needs a repair first.
The harness has one: it separates overlapping squares and scores the container the
repaired arrangement needs.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
