---
title: H-117 — force a useful bound on minimizing angle complexity
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-117
  kind: open_question
  claim: >-
    Can a complete structural argument force at most k < 11 exact orientation
    classes in an n=11 minimizing representative below the Trump side? Separately,
    can a near-cluster/dispersed-cluster decomposition bound both branches strongly
    enough without reducing the number of independent actual angles?
  lane: proof
  derived_from: [X-017]
  instrument: >-
    Proposed typed contact implications with complete alternatives and independent
    feasible controls; a finite descriptor catalogue alone does not supply them.
  instrument_ready: false
  regime: >-
    Original side-minimizing representatives, with compactness and representative
    reduction stated; actual angles modulo pi/2, all contact degeneracies and
    the dispersed remainder retained
  instance: {axis: n, point: 11}
  priority: 3
  cost_estimate: a bounded proof-obligation audit before any whole-structure enumeration
  prereqs: [proved contact-equality hypotheses, complete representative or configuration cover]
  replication: false
  registered: '2026-09-07'
  notes: >-
    A bound of two exact orientation classes, combined with H-113, would connect
    the restricted theorem to exact value. A near-cluster split alone cannot do so.
    No such exact class bound is established. Positive-length edge contact can
    force an equality; corner contact, stress support size, or repeated numerical
    appearances does not force the required global structure.
---
# H-117 — The Missing Angle-Complexity Bridge

[X-017](../explorations/X-017-compatibility-and-complete-case-covers.md) retains this
question so a two-angle success cannot silently discard the three-or-more-angle
remainder. It refines a structural issue within H-103 without changing that claim.

Independent actual orientation classes are not folded-angle bins.
Connected components of a proved edge-equality graph bound the number of angle
variables; distinct components may still share the same angle.
The k=11 descriptor includes the unrestricted difficulty.

Search may attack a concrete proposed reduction after its quantifier is fixed, using
angle splitting and coordinated contact release.
A verified high-angle packing can refute a universal restriction on all feasible
packings. It does not alone refute the existence of a different low-angle minimizing
representative, which is the first question here.
A sub-U value together with a proved restricted-family lower bound could provide the
stronger contradiction.
Unsuccessful search proves neither claim.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
