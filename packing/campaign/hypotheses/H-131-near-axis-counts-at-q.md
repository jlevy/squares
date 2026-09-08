---
title: H-131 — at most nine squares within 6.45° of the axes at 96/25, and at most ten within 10.39°
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-131
  kind: hypothesis
  claim: >-
    In every packing of unit squares in the container of side 96/25, at most nine
    squares have folded tilt at most 6.4537°, at most ten have folded tilt at most
    10.3875°, at most nine have folded tilt within 2.155° of 45°, at most ten have
    folded tilt within 2.44° of 40.19°, and at most ten have folded tilt in
    [30.01°, 45°], so some square is tilted below 30°. At side U the corresponding
    counts are nine within 6.4537°, ten within 7.7671° of the axes, and ten within
    1.24° of 45°.
  lane: proof
  derived_from: [X-021]
  strategy_refs: ['proof:9', 'proof:15']
  criterion:
    shape: determination
    metric: exact-decided mass of the composition-(11, 0) class measure on the stated cell unions
    direction: below the next integer above the stated count on every listed class
    threshold: 10
  instrument: >-
    classcert's composition-(11, 0) program at grid 79 with inset 1/10, decided by
    decide_class_program; the counting step is X-021's Theorem 1.5 (each square's core is
    at a direction in the class and the cores are disjoint).
  instrument_ready: true
  regime: >-
    n = 11, sides 96/25 and 3877084/10⁶, shrink 9977/10000, the retained 181-direction net;
    classes are unions of half-gap cells, so a square belongs to the class of the direction
    whose cell holds its angle
  instance: {axis: n, point: 11}
  priority: 2
  cost_estimate: under one hour of replay; the planning-lane decisions took one to eight minutes each
  prereqs: []
  replication: true
  registered: '2026-09-08'
  notes: >-
    Exact-verified in the planning lane on 2026-09-08 (lane B, Section 2.3) on a stated
    site set; registered so that the first lane session replays the decision under an
    experiment record before the counts are cited as results. The floors are sharp in
    kind: nine squares at any common tilt up to 30° fit in the container, so no covering
    method gets a near-axis count below nine, and the only room is the band's width.
---
# H-131 — Exact Counts by Angle at `96/25`

The nine-point argument gives at most nine squares tilted below `2.44°` at `96/25`.
[X-021](../explorations/X-021-what-can-be-proved-about-eleven-squares.md) widens that to
`4.61°` with nine pushed points and, with the class program, to `6.45°` — and adds a
count of ten out to `10.39°`, nine within `2.155°` of `45°`, ten within `2.44°` of
Trump’s angle, and ten in `[30.01°, 45°]`, which is the first count that forces a square
below `30°`.

These are theorems of the exact verifier on a stated site set, not hand proofs, and they
were decided in a planning lane rather than a registered round.
Replaying them under an experiment record is the first task of BC-295 in
[Agenda 030](../agendas/agenda-030-parallel-structural-lanes-at-n11.md); until then they
are cited as planning evidence only.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
