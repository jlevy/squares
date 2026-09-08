---
title: H-131 — exact angle-cell counts at 96/25 and U
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
    squares have folded tilt in cells 0–24, at most ten in cells 0–39, at most nine
    in cells 171–180, at most ten in cells 149–169, and at most ten in cells
    117–180. At side U the counts are at most nine in cells 0–24, ten in cells
    0–29, and ten in cells 175–180. Cells are the closed half-gap cells of the
    retained net t_k = k·207107/90000000, k = 0..180, with exact tangent boundaries
    supplied by DirectionClasses.cell_bounds; the degree labels are approximate.
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
    Replayed under session-102 (lane B, 2026-09-08) and registered as exp-131: every
    cell count reproduces the planning lane's mass to the fraction. Review correction
    on 2026-09-08 replaces outward-rounded degree claims with the exact cells that
    were tested; this changes no run and claims no new replay. In particular, the
    result forces an angle below the lower boundary of cell 117, approximately
    30.0148588 degrees, and does not establish an angle below 30 degrees.
---
# H-131 — Exact Counts by Angle at `96/25`

The class program gives the eight exact cell counts in the claim above, registered under
[exp-131](../series/series-000-smoke-and-calibration/experiments/exp-131-h131-near-axis-counts-replay-at-q.md).
The site set supplies the certificate’s atoms; Condition 4 and the exact sweep make each
accepted count a statement about every packing of unit squares in its stated angle
class.

**Statement correction, 2026-09-08.** The registered runs used exact half-gap cells.
Some earlier degree summaries rounded their domains outward: cells 0–39 end at
approximately `10.3874656704°`, and cells 149–169 cover approximately
`[37.7332782363°, 42.6166465824°]`, which does not contain the whole interval
`40.19° ± 2.44°`. The lower tangent of cell 117 is `120639827500000/208829222337727`,
whose angle is approximately `30.0148587980°`. It is strictly above `30°`: three times
its numerator squared minus its denominator squared is `52259835509451319152473471 > 0`.
The proved conclusion is that one square has tilt below this exact cell boundary.
No result here forces tilt below `30°`. This correction restates the recorded
certificates and adds no run.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
