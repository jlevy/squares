---
title: H-098 — segment-supported measures for n = 11
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-098
  kind: open_question
  claim: >-
    Can nonnegative segment-supported measures give stronger or cheaper n = 11
    lower-bound certificates than atomic measures while admitting exact
    intersection-length and continuum-coverage verification?
  lane: proof
  derived_from: [X-016]
  strategy_refs: ['proof:8', 'proof:12', 'proof:22']
  instrument_ready: false
  regime: >-
    Nonnegative measures on finitely many line segments, counted through witnesses
    strictly inside the original unit squares; exact intersection mass.
  instance: {axis: n, point: 11}
  prereqs: [kernel-route disposition and a costed BC-237 verifier design]
  registered: '2026-09-06'
---
# H-098 — Segment-Supported Measures

The
[contributed strategy, B3](../../../docs/project/reviews/review-2026-09-05-strategy-gpt-56-pro-gemini-grok.md)
proposes replacing dense rows of atoms with measure on line segments.
[BC-237](../agendas/agenda-025-adaptive-fractional-frontier.md) owns the deferred theory
and cost assessment.
Strictly interior witnesses keep the selected sets disjoint, including any segment mass
that an original square boundary could otherwise share.

The first proposed discriminator chooses one segment and a declared witness family,
derives its intersection-length formula and all changes of regime, and checks that
formula on exact contained, disjoint and boundary cases.
Identify which persistent atom support it would replace before pricing a complete
summed-mass minimizer.

A binary segment-hit predicate cannot measure captured mass.
The complete decision needs every intersection regime and the minimum of the summed
piecewise formulas over admissible poses.
A representation of one segment supplies neither that verifier nor a new bound.

Keep implementation deferred until the kernel route is disposed and the complete
verifier has a measured future allocation.
A later comparison must freeze the measure family and its exact decision rule.
A costly or unhelpful segment design is a reason to park that design; it does not
exclude every singular measure.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
