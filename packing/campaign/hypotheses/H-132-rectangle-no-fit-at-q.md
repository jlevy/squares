---
title: H-132 — eleven unit squares do not fit in the rectangle 3.84 × 3.81
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-132
  kind: hypothesis
  claim: >-
    Eleven unit squares with pairwise disjoint interiors do not fit in the rectangle
    [0, 96/25] × [0, 381/100]. Consequently, in every packing of eleven at side 96/25 both
    extents are at least 3.81 and every wall is within 0.03 of some square.
  lane: proof
  derived_from: [X-021]
  strategy_refs: ['proof:9', 'proof:15']
  criterion:
    shape: determination
    metric: a frozen weighted certificate for the rectangle decided by the exact sweep and the interval route, as for T-018
    direction: mass below eleven with every admissible core covered
    threshold: 11
  instrument: >-
    The T-018 pipeline with a rectangular centre domain: sweep.centre_domain as a rotated
    rectangle, the float mirror's separate x and y bounds, the four half-planes of the
    interval route, and Condition 1's symmetry group reduced to the two reflections so the
    net spans a quarter turn. The domain stays convex; no new engine.
  instrument_ready: false
  regime: >-
    n = 11; container 96/25 by H for H in {3.80, 3.81, 3.815, 3.82}; shrink 9977/10000
    and the doubled net
  instance: {axis: n, point: 11}
  priority: 2
  cost_estimate: one session of three to four hours, including the bounded instrument change
  prereqs: [rectangle centre domain in sweep, generate and interval]
  replication: true
  registered: '2026-09-08'
  notes: >-
    Lane D's Session S1 and lane A's Session S5 in X-021. A rectangle bound is the
    strongest symmetry-breaking premise available: with the spanning lemma it gives an
    anchor chain plus near-contacts on the other two walls, and it decides whether a
    both-directions spanning representative can be forced at 96/25. The falsifier is a
    verified packing in the rectangle; none is known below the square side.
---
# H-132 — The First Rectangle Bound for Eleven

A side-minimal packing spans the container in at least one direction, and nothing forces
the other; the two-square minimiser is the counterexample.
[X-021](../explorations/X-021-what-can-be-proved-about-eleven-squares.md) turns the
missing direction into a measurement: the largest `H₀` such that eleven squares provably
do not fit in `3.84 × H₀`.

The instrument change is bounded and convex, and the result is a theorem type the record
does not yet carry at `n = 11`.
[Agenda 030](../agendas/agenda-030-parallel-structural-lanes-at-n11.md) owns it in
BC-298.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
