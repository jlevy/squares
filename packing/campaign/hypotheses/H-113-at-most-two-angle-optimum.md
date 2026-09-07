---
title: H-113 — at most two actual orientations require the Trump side
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-113
  kind: hypothesis
  claim: >-
    Every packing of eleven unit squares with at most two distinct actual
    orientations modulo pi/2 requires container side at least the exact Trump side U.
  lane: proof
  derived_from: [X-020]
  criterion:
    shape: determination
    metric: complete at-most-two-angle lower bound or a verified sub-U packing
    direction: >-
      Accept only with an independently checked proof covering both absolute
      angles, every multiplicity, the one-angle family, and all center/contact
      alternatives and seams. Reject with a verified sub-U packing in this domain.
      Descriptor enumeration or success on the six-plus-five subfamily is insufficient.
    threshold: U
  instrument: >-
    Proposed two-parameter geometry-bound LP/interval case cover, exact certificates,
    and independent feasible-witness checking; no complete solver exists.
  instrument_ready: false
  regime: >-
    n=11; at most two actual orientations modulo pi/2, with both absolute class
    angles free relative to the square container and all positive multiplicities
  instance: {axis: n, point: 11}
  priority: 3
  cost_estimate: reprice after the shared interface and first restricted pilot; no full-family estimate
  prereqs: [complete two-angle domain and symmetry proof, reviewed uniform certificate interface]
  replication: false
  registered: '2026-09-07'
  notes: >-
    H-112 is a strict subfamily, not an assumption. A proof here implies that every
    better packing has at least three actual orientations; it does not settle
    unrestricted optimality. Keep H-117's structural bridge separate.
---
# H-113 — The Complete Two-Angle Family

The
[enumeration addendum](../../resources/papers/n11-complete-research-bundle-2026-09-07/updates/enumeration_addendum.md)
supplies descriptors, not solved geometric cases.
[X-020](../explorations/X-020-compatibility-and-complete-case-covers.md) and
[Agenda 027](../agendas/agenda-027-compatibility-and-restricted-families.md) retain this
as a conditional successor.

Independent reflection of square orientations is not a container symmetry.
Folded-angle coincidence does not imply actual shared orientation.
Arbitrary whole-packing rotation cannot normalize the first class to zero while
preserving the axis-aligned container.
Cover equal-angle collisions, quarter-turn seams, and all multiplicities explicitly.

Positive-margin subfamily bounds may transfer to neighborhoods after the exact angular
loss is checked. The three-or-more-angle remainder stays open regardless of how often
numerical search returns to a two-angle construction.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
