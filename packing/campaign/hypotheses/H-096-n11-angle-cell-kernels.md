---
title: H-096 — rational angle-cell kernels beyond square cores
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-096
  kind: open_question
  claim: >-
    Can finite rational inner kernels, contained throughout their assigned angle
    cells, improve verified atomic coverage enough to extend the n = 11 bound
    beyond the adaptive-square-core route?
  lane: proof
  derived_from: [X-016]
  strategy_refs: ['proof:21', 'proof:22']
  instrument_ready: false
  regime: >-
    Rational polygonal inner witnesses, nonnegative atomic mass, complete closed
    angle cells and D4 accounting; exact containment and translation coverage.
  instance: {axis: n, point: 11}
  prereqs: [BC-235 representation and containment proof before BC-236 implementation]
  registered: '2026-09-06'
---
# H-096 — Rational Angle-Cell Kernels

The
[contributed strategy, B2](../../../docs/project/reviews/review-2026-09-05-strategy-gpt-56-pro-gemini-grok.md)
proposes a rational polygon inside the common intersection of unit squares across an
angle cell. That intersection need not itself have a polygonal boundary.
[BC-235 and BC-236](../agendas/agenda-025-adaptive-fractional-frontier.md) own the
theory and verifier work.

The first proposed discriminator fixes one limiting pose and angle cell from an adaptive
result, constructs a rational inner polygon, and proves containment for every angle in
the cell. Check whether the added region captures positive mass that the square core
misses. Extra area without useful captured mass does not justify a build.

That local calculation cannot establish universal translation coverage.
A global candidate needs a complete center-cell decision procedure, independent
verification and strict interior containment before disjoint mass can be counted.

Keep the declared adaptive-disposition prerequisite before implementation.
Price a verifier only after a useful containment and coverage comparison; retain
BC-236’s existing four-times square-core decision-cost guard.
A failed polygon or local test disposes that proposal, without ruling out every kernel.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
