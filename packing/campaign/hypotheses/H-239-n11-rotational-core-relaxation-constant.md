---
title: H-239 — the rotational-core relaxation loses little side per radian at generic n11 angle vectors
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-239
  kind: open_question
  claim: >-
    Whether rotational-core LPs at n=11 lose at most about 1.5 in side per radian of
    angle-box width at generic angle vectors, and whether the fixed-angle optimum
    exceeds U + 0.2 on most of angle space.
  lane: proof
  derived_from: [X-046]
  criterion:
    shape: record
    metric: >-
      The core-LP side at 20 random angle vectors and three box widths, and the quench
      optimum at frozen random angles, against the fixed-angle optimum
    direction: >-
      A loss above 3 per radian, or a median fixed-angle excess below 0.1, prices a
      full verified search out of reach; the opposite supports a one-week program. This
      is a pricing question and moves no bound either way.
    threshold: 1.5
  instrument: The H-236 cell-tree driver once admitted
  instrument_ready: false
  regime: n=11; float proposals at sampled angle vectors; exact only where a leaf is reported
  instance: {axis: n, point: 11}
  priority: 3
  cost_estimate: About one hour once the H-236 driver is admitted
  prereqs: [think-nbij]
  replication: false
  registered: '2026-09-23'
  notes: >-
    X-046 candidate H-f. Whether the far eleven-dimensional region can ever be closed
    by search turns on this constant and on the sublevel volume near U.
---
# H-239: The Rotational-Core Relaxation Constant

Kept as an open question because it prices a program rather than asserting a theorem.
It runs after H-236’s driver is admitted and is the cheapest way to learn whether a full
verified search at n11 is a bounded engineering task.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
