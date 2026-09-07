---
title: H-112 — six axis-aligned and five common-angle squares require the Trump side
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-112
  kind: hypothesis
  claim: >-
    Every packing of six axis-aligned unit squares and five unit squares sharing one
    arbitrary actual orientation modulo pi/2, with all centers and contacts free,
    requires container side at least the exact Trump side U.
  lane: proof
  derived_from: [X-017]
  criterion:
    shape: determination
    metric: complete restricted-family lower bound or a verified sub-U packing
    direction: >-
      Accept only after an independently checked complete family proof of L >= U,
      including every class angle, center placement, separating alternative and
      boundary. Reject with a rigorously feasible packing in the family at L < U.
      A closed interval, a sampled optimum, or a timeout is partial or inconclusive.
    threshold: U
  instrument: >-
    Proposed uniform parametric LP/Farkas exclusions with complete case coverage,
    selected exact basis elimination, and independent construction verification.
    The retained Trump contact cell is a control, not the complete family.
  instrument_ready: false
  regime: >-
    n=11; six squares have actual orientation zero modulo pi/2; the remaining five
    share one free actual orientation; legal touching and all contact graphs remain
  instance: {axis: n, point: 11}
  priority: 1
  cost_estimate: first price a nontrivial complete angle interval; full theorem cost is unknown
  prereqs: [reviewed restricted-family semantics, uniform geometry enclosures and complete case controls]
  replication: false
  registered: '2026-09-07'
  notes: >-
    The known exact Trump construction supplies the matching upper witness.
    This specializes H-102 and differs from H-036 and from the retained local
    theorem. No assumption fixes Trump's contacts or wall pattern.
---
# H-112 — A Contact-Independent Six-Plus-Five Theorem

[X-017](../explorations/X-017-compatibility-and-complete-case-covers.md#b-restricted-families-the-principal-structural-theorem-pilot)
explains the proposed proof and falsifier.
[Agenda 027](../agendas/agenda-027-compatibility-and-restricted-families.md) first asks
for one complete continuous interval, with the unsolved family retained explicitly.
Such a pilot does not accept the full hypothesis.

The common angle of the five squares may coincide with the axis class; cover that
boundary too.
All wall attachments, pair choices, ties, and determinant-zero loci remain.
Each fixed-angle branch has a center-and-side LP; a successful numerical basis does not
account for all other bases or branches.

Any transferred neighborhood bound must start from the optimum over the entire declared
family. A bound equal to U has no positive margin for uniform angular shrink loss at the
endpoint.

An independent search should vary wall patterns and contacts within this family.
Its candidate becomes a refutation only after rigorous feasibility verification below U.
An unsuccessful search is not a lower bound.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
