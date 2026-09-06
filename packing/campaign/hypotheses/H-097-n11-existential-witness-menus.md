---
title: H-097 — existential witness menus for n = 11
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-097
  kind: open_question
  claim: >-
    Can a finite witness menu certify that every admissible unit-square pose
    contains at least one strictly interior witness of sufficient mass where
    universal coverage by a single core family fails?
  lane: proof
  derived_from: [X-016]
  strategy_refs: ['proof:7', 'proof:21', 'proof:22']
  instrument_ready: false
  regime: >-
    One nonnegative measure and a finite menu of witnesses; a complete
    for-every-pose, there-exists-a-witness containment and mass statement.
  instance: {axis: n, point: 11}
  prereqs: [identified universal-witness restriction and a specified pose domain]
  registered: '2026-09-06'
---
# H-097 — Choose a Witness Within Each Square

The
[contributed strategy, B5](../../../docs/project/reviews/review-2026-09-05-strategy-gpt-56-pro-gemini-grok.md)
allows witness options to differ in offset, orientation or shape.
The counting proof requires at least one heavy witness strictly inside each packed
square; it need not require every menu member to be heavy.

The first proposed discriminator fixes a closed pose box containing a difficult pose, a
measure and a finite menu.
Prove that every pose in the box admits a contained menu member with mass at least one.
The selected member may vary across the box, so the proof must cover the selection
boundaries as well as the interiors.

A result on that box proves only the stated local selection property.
A global certificate requires a complete pose-domain cover and total measure below
eleven. Sampling poses does not establish the quantified statement.

Nested concentric sizes add no choice when the largest member is admissible throughout
the box. Translation also cannot enlarge the maximum inscribed square at a fixed
orientation; any benefit must come from capturing mass.
Stop an unproved containment or selection proposal before building a global verifier.
Register a measurable successor only after its box, menu and measure are fixed.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
