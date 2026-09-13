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
  derived_from: [X-028]
  criterion:
    shape: determination
    metric: whether any cell of the parameter sweep produces a trial inside the close tolerance
    direction: no cell does
    threshold: 0.1
  instrument: packing/devtools/bench_annealing.py --sweep
  instrument_ready: true
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

Stated so it can be wrong, and worth stating because the negative is the useful outcome:
it would say the animation’s physics is a picture of a search rather than a search, and
that improving it means changing the method rather than its dials.

80,000 trials at the shipped force law found nothing inside 0.1% at any n. The best
result anywhere was 0.139% at n = 5 — close enough that the claim is not safe, which is
why it is worth a full grid rather than an assumption.

**What would refute it.** One trial, at any cell, inside the tolerance.
A single counterexample settles it, which makes this the cheapest claim in the registry
to disprove and the most expensive to confirm.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
