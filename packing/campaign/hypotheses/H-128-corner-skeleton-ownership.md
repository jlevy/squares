---
title: H-128 — a valid measure at 96/25 owns the four corner atoms
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-128
  kind: hypothesis
  claim: >-
    There is a valid D4-symmetric measure at side 96/25 on the retained shrink and net
    whose four atoms at the orbit of T-018's corner atom, scaled by 384/381, each carry
    weight at least 3/20 and whose total mass is below 11 + 3/20. Consequently every
    packing of eleven unit squares at side 96/25 has four distinct squares each containing
    one of those four corner atoms in its interior.
  lane: proof
  derived_from: [X-021]
  strategy_refs: ['proof:9', 'proof:15']
  criterion:
    shape: determination
    metric: converged and exactly verified total mass of the column-generation measure with the five atom lower bounds imposed
    direction: below 11.15
    threshold: 11.15
  instrument: >-
    Column generation with lower bounds on the four corner atoms and the centre atom (an
    LP bound change, no geometry change), seeded with T-018 scaled by 384/381, decided by
    the exact eighth-turn sweep; the ownership step is X-021's Corollary C.2, which needs
    only that the corner atoms are pairwise farther apart than B√2.
  instrument_ready: true
  regime: >-
    n = 11, side 96/25, shrink 9977/10000, 181-direction net; the measure need not be a
    certificate (its mass may exceed eleven), only valid with the stated skeleton weights
  instance: {axis: n, point: 11}
  priority: 1
  cost_estimate: one session of three to four hours on one core
  prereqs: [T-018 atom positions, column generation with atom lower bounds]
  replication: true
  registered: '2026-09-08'
  notes: >-
    Lane C's Corollary C.2 makes the theorem free once the measure exists: the four corner
    atoms sit at pairwise distance 1.8146 against a core diagonal of 1.411, so no core
    holds two, and with mass below 11 + w_c each atom of weight w_c is owned by exactly
    one core. The falsifier is a converged mass at or above 11.15 with the forced
    skeleton. At 3.81 the statement is vacuous because the mass is below eleven; the
    3.85 run stood at 11.23 unconverged.
---
# H-128 — Four Corners Owned, From the LP Alone

The ten-square proof forces containments by replacing one unavoidable point with another
and observing that ownership is preserved.
[X-021](../explorations/X-021-what-can-be-proved-about-eleven-squares.md) carries that
step over to weighted atoms: with mass `11 + ε`, every atom heavier than `ε` lies in
exactly one core, and atoms too far apart to share a core are owned by distinct squares.

Applied to T-018’s four heaviest atoms this gives a global structural theorem at any
side where a valid measure of mass below `11.147` exists — strictly sharper than
insertion saturation’s blockers, which need only meet an open corner box.
Whether such a measure exists at `96/25` is the measurement.
[Agenda 030](../agendas/agenda-030-parallel-structural-lanes-at-n11.md) owns it as
BC-293, and BC-299 consumes the pinned anchors it would supply.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
