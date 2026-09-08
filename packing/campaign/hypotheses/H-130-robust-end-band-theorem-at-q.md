---
title: H-130 — a robust {0°, 45°} band is excluded at 96/25
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-130
  kind: hypothesis
  claim: >-
    Every packing of eleven unit squares at side at most 96/25 has a square whose folded
    angle is farther than 1.5° from both 0° and 45°. Equivalently, the class covering
    value restricted to the end cells [0°, α] ∪ [45° − β, 45°] with α + β ≥ 3° is
    below eleven at 96/25, decided exactly.
  lane: proof
  derived_from: [X-021]
  strategy_refs: ['proof:9', 'proof:10', 'proof:15']
  criterion:
    shape: determination
    metric: exact-decided class covering value on the widest end-cell class the site set allows
    direction: below eleven with α + β of at least 3°
    threshold: 3
  instrument: >-
    classcert's composition-(11, 0) program on a union of end cells, decided by
    decide_class_program on rationalised atoms; symmetric widening cell by cell, then
    asymmetric; the falsifier is a fractional packing on the end cells of value at least
    eleven at 96/25 or eleven disjoint cores in the class.
  instrument_ready: true
  regime: >-
    n = 11, side 96/25, shrink 9977/10000, 181-direction net; the exact {0°, 45°} class is
    not integrally obstructed at 96/25 because Hämäläinen's packing needs side B·L₀ =
    3.8767
  instance: {axis: n, point: 11}
  priority: 1
  cost_estimate: one session of two to three hours on one core
  prereqs: [lane B's end-cell rows at grid 79 as controls]
  replication: true
  registered: '2026-09-08'
  notes: >-
    Transporting Stromquist's Theorem 3 to 96/25 proves 0.6848° (X-021, lane B
    Proposition 1.6), and the planning lane exact-verified [0°, 1.45°] ∪ [43.76°, 45°]
    at grid 79 (mass 10.702) with no Stromquist input; the next widenings were not
    refuted on that grid. Anything at or beyond 3° is a theorem of a new kind below U
    and the first rung of the band ladder. H-036 asks 0.25° at 3.878 and stays open;
    the method here transfers to it.
---
# H-130 — The First Rung of the Band Ladder

A band-restricted theorem says that every packing all of whose folded angles lie in a
set `S` has side above `L`. Stromquist’s Theorem 3 is `S = {0°, 45°}` at `3.8856`;
[X-021](../explorations/X-021-what-can-be-proved-about-eleven-squares.md) transports it
to `0.6848°` bands at `96/25` and shows that the class program proves such theorems
exactly whenever the restricted covering value is below eleven.

This claim is the widest end band the instrument can decide at `96/25`. The planning
lane already decided `1.45°` at the axis end and `1.24°` at the diagonal end on one site
set; the claim asks for twice that.
It is not integrally obstructed there, it needs no new code, and it is the base case
every later case analysis may assume.
[Agenda 030](../agendas/agenda-030-parallel-structural-lanes-at-n11.md) owns it in
BC-295.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
