---
title: H-129 — the shrink-free fractional packing value stays below eleven up to 3.87
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-129
  kind: hypothesis
  claim: >-
    With closed unit placements (shrink B = 1) and a direction net dense near 0° and
    40.18°, no depth-one fractional packing of value at least eleven exists in the
    container of side 3.87. Equivalently, the shrink-free covering value at 3.87 is
    below eleven, so a one-body certificate can in principle reach past the retained
    instrument's caps at 3.868983 and 3.876681.
  lane: proof
  derived_from: [X-021]
  strategy_refs: ['proof:9', 'proof:15']
  criterion:
    shape: determination
    metric: exact depth-scaled value of the best depth-one family found by the cutting-plane loop at B = 1, verified by verify_ceiling at every arrangement vertex
    direction: below eleven at 3.87; a family at or above eleven with at least one unit of weight outside Trump's neighbourhood refutes the claim and kills every capture certificate at that side
    threshold: 11
  instrument: >-
    sqpack.fractional.ceiling in its unit regime with the cutting-plane loop, seeded from
    BC-200's family after rescaling positions only (sizes fixed at one, so the seed is a
    warm start and not a valid family until re-verified); readings at 3.84, 3.86 and 3.87.
  instrument_ready: true
  regime: >-
    n = 11; closed unit squares at finitely many net directions, which is admissible for a
    packing lower bound because Condition 4 is not needed on the dual side; sides 3.84,
    3.86 and 3.87
  instance: {axis: n, point: 11}
  priority: 1
  cost_estimate: one session of three to four hours on one core
  prereqs: [BC-200 family and state as warm start]
  replication: true
  registered: '2026-09-08'
  notes: >-
    X-021's duality lemma (lane D) says this number decides routes (b) and (c) and every
    capture design at once. A refutation is the earliest possible hopelessness signal
    for the dot-based endgame; a confirmation opens the first rung above the shrink cap.
    Direction matters: the fractional packing value with unit squares is at most the
    value with B-cores, so the retained 3.82 bracket says nothing about it.
---
# H-129 — The Number That Decides the Endgame

Every conditional, capture or class certificate exists exactly when a restricted
fractional packing value sits below its threshold; that is
[X-021](../explorations/X-021-what-can-be-proved-about-eleven-squares.md)’s duality
lemma. With the retained shrink the `{0°, 45°}` packing already kills every
Trump-neighbourhood capture certificate above `3.876681`, and with `B = 1` that
particular kill disappears — so the shrink-free value near `U` is the one quantity on
which the ambitious route turns.

[Agenda 030](../agendas/agenda-030-parallel-structural-lanes-at-n11.md) measures it in
BC-294, and BC-301 waits on its first reading.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
