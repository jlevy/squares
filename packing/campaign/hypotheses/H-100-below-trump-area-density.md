---
title: H-100 — can full-size area density improve the lower bound below Trump?
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-100
  kind: open_question
  claim: >-
    Is there a side L strictly between the retained verified lower bound and the exact
    Trump side, and a nonnegative integrable area density on its container, whose total
    mass is below 11 while every contained full unit-square placement has integral at
    least one?
  lane: proof
  derived_from: [X-016]
  strategy_refs: ['proof:12', 'proof:15', 'proof:17', 'proof:22']
  instrument: >-
    No runnable instrument yet. A concrete successor must freeze its target L, density
    family, exact mass representation, and continuum coverage verifier before
    measurements; BC-257 owns target selection and the decision to commission a
    separately tracked below-Trump primal certificate build.
  instrument_ready: false
  regime: >-
    n = 11; full-size unit squares at all admissible centers and angles, including wall
    strata; nonnegative absolutely continuous measure, not atoms or segment mass
  instance: {axis: n, point: 11}
  priority: 1
  cost_estimate: price one specified side and density family before a continuum build
  prereqs: [reviewed BC-242 semantics, prospectively specified target and density family]
  replication: true
  registered: '2026-09-06'
  notes: >-
    A finite-pose fit or sampled minimum supplies a candidate, not a certified upper
    bound on covering mass. A strict mass-below-11 certificate excludes eleven squares
    at its stated L only. H-099 finding a feasible dual above 11 at Trump's side does
    not refute this below-Trump question; a non-kill there does not justify a build here.
---
# H-100 — A Below-Trump Primal Route with Its Own Gate

The
[BC-242 contract](../series/series-000-smoke-and-calibration/results/agenda-026/bc-242-full-size-density-proof-contract.md)
proves why an area density with mass below eleven excludes a packing of eleven
interior-disjoint squares.
Its boundary convention works because shared square edges have area measure zero.
The remaining mathematical obligation is coverage of the entire continuous placement
space, with exact mass and rigorous lower coverage bounds for every pose box and wall
stratum.

Inverse design in a finite density basis is one possible candidate method.
Its basis, side, and verifier must become a concrete prospective hypothesis before a
measurement; this open question is not an executable queue item.
Failed fits or a failed density family do not exclude all absolutely continuous
densities.

This below-side arm is distinct from [H-101](H-101-trump-equality-density.md), which
asks about mass eleven at Trump’s exact side.
[Agenda 026’s BC-257](../agendas/agenda-026-density-stationarity-and-trump-capture.md)
prices this route separately from BC-244’s equality design.
The below-side mathematical question has no dependency on a non-killing H-099 result.
The common origin is
[X-016’s density route](../explorations/X-016-after-381-two-managers-one-proof-boundary.md#closure-route).

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
