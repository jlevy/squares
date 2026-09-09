---
title: H-127 — pricing the four corner blockers gives a covering surplus at 96/25
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-127
  kind: hypothesis
  claim: >-
    At side 96/25 the corner-class covering program — every admissible core inside a
    placement that meets one of the four open corner boxes of side 0.88 priced at a
    threshold w_c, every core at w_f = 1, objective mass − 4 w_c − 7 w_f — has a strictly
    negative optimum on some site set, so eleven unit squares are excluded at 96/25 by a
    certificate that uses the four distinct corner blockers.
  lane: proof
  derived_from: [X-021]
  strategy_refs: ['proof:9', 'proof:15']
  criterion:
    shape: determination
    metric: exact optimum of the corner-class program decided by the sweep restricted to a safe superset of the corner-region cells
    direction: strictly negative
    threshold: 0
  instrument: >-
    classcert's two-threshold LP with a region predicate in place of the angle class,
    folded over D4; the sweep restricted to a superset of the corner-region event cells
    (safe: imposing the higher threshold on more cores only weakens the certificate).
    A small extension of the row generator; no new engine.
  instrument_ready: false
  regime: >-
    n = 11, side 96/25, retained shrink 9977/10000 and 181-direction net; the corner boxes
    of side 0.88 are the ones insertion saturation with overhang forces every packing to
    meet, so the four blockers are distinct squares by X-021's Lemma 1
  instance: {axis: n, point: 11}
  priority: 1
  cost_estimate: one session of three to four hours on one core; class programs cost one to eight minutes each at grid 79
  prereqs: [region predicate for cores, site set from the 3.82 runs or the dilated 3.81 atoms]
  replication: true
  registered: '2026-09-08'
  notes: >-
    Lane A's Theorem A is sound and unrun. The falsifier is an optimum at or above zero on
    a converged site set together with a census showing tight cells inside the corner
    region, which forces w_c = 1 and no gain. A non-refutation on a product grid is not
    evidence; the lane records its site set with the result.
---
# H-127 — Do the Four Blockers Buy Anything?

[X-021](../explorations/X-021-what-can-be-proved-about-eleven-squares.md) proves that
every packing at side up to `3.96` has four distinct squares meeting the four open
corner boxes of side `κ = L − 2.96`, and that no argument valid up to `U` forces those
blockers any deeper or any straighter.
This hypothesis asks the only question that can be asked of that fact without a further
theorem: whether a certificate that prices the four blockers’ cores above the rest has a
surplus at `96/25`.

The mechanism is X-014’s class certificate with a region in place of an angle class.
If the retained measure at `3.82` already over-covers the corner region, the answer is a
new rung for the price of one LP; if the tight cells lie in the corners, the answer is
that corner information must go through banking (lane A’s Theorem B) instead.
[Agenda 030](../agendas/agenda-030-parallel-structural-lanes-at-n11.md) owns the lane as
BC-292.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
