---
title: H-041 — a one-coordinate repair restores Stromquist's Theorem 2 mechanism
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-041
  kind: hypothesis
  claim: >-
    At s = 2 + 4/sqrt(5), replacing the printed Figure 14 point
    G = (4/5, 37/20) by G' = (79/100, 37/20) yields an unavoidable twelve-point
    set and restores all five implications needed for Stromquist's lower bound on
    eleven freely oriented unit squares.
  lane: proof
  derived_from: [X-001]
  strategy_refs: ['proof:2', 'proof:3', 'proof:15']
  criterion:
    shape: conditions
    metric: complete independently replayed finite cover and five-node implication chain
    direction: every cover cell, strict inequality, conditional triple, and capacity implication certifies
  instrument: >-
    The H-010 exact checker with a source-distinct repaired Figure 14 tuple, a complete
    face-to-lemma cover, exact or outward-rounded inequality certificates, explicit
    uncovered-cell witnesses, a finite resource-count checker, and independent replay.
  instrument_ready: false
  regime: >-
    Stromquist's exact Figure 13 geometry and strict open-box semantics at
    s = 2 + 4/sqrt(5), with only G moved from x = 4/5 to x = 79/100 in Figure 14
  instance: {axis: n, point: 11}
  sweep: {axis: n, points: [11]}
  priority: 1
  cost_estimate: tier S once the finite face cover is encoded
  prereqs: [exact terminal rejection of H-010 on the printed Figure 14 set]
  replication: true
  registered: '2026-08-24'
  notes: >-
    This is a post-falsification successor, not a correction silently attributed to
    Stromquist. Defeating the known H-010 escape witness is necessary but insufficient:
    acceptance requires the complete repaired unavoidability cover and the other four
    proof nodes. Any uncovered pose rejects the claim.
---
# H-041 — test the smallest visible repair

The printed point `G = (0.8, 1.85)` leaves a narrow escape through the adjacent Lemma 4
quadrilateral.
Moving only its x-coordinate left by `0.01` is the smallest simple decimal
repair currently proposed.

This claim was registered after finding the printed-set witness and before checking the
repaired cover. It therefore tests a new construction; it does not rescue H-010’s
source-faithful claim after the fact.

The checker must search for a fresh escape and certify every face in the reconstructed
Figure 14 partition.
Passing the one witness that killed H-010 is not evidence that the new set is
unavoidable.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
