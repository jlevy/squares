---
title: H-237 — an angular capture radius around Trump's packing larger than the BC-240 radius
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-237
  kind: hypothesis
  claim: >-
    There is an explicit rational r > rho = 808514697/200000000000 such that every
    feasible labelled pose z in Trump's anchored 33-coordinate chart with
    ||z - z*||_inf <= r has container side at least U, with equality only at z*.
  lane: proof
  derived_from: [X-046]
  criterion:
    shape: determination
    metric: >-
      The certified radius from an exact lower bound on the first-order growth
      g(d) = min over the 128 derivative-distinct branches of the max over each
      branch's normalized stress cone of the first-order side change along d,
      minimized over the whole sup-norm sphere of directions, combined with an exact
      second-order remainder and inactive-row slack bound on the ball
    direction: >-
      Confirm only with explicit rational constants, every inequality exactly computed
      or proved in checkable steps, and a retained replayable tool producing the
      constants. Reject as a bounded negative when the best certified radius from this
      route is at most rho, naming the binding constant. A face-only or sampled minimum
      of g is a discriminator, not a confirmation; a float estimate decides neither.
    threshold: rho
  instrument: >-
    packing/cases/trump11/capture_radius.py on the exp-013 tangent-cone record and
    sqpack.research.exact_jets
  instrument_ready: false
  regime: >-
    n=11; Trump's labelled anchored pose chart of BC-240; sup norm over centres and
    angles in radians; exact rational arithmetic
  instance: {axis: n, point: 11}
  priority: 1
  cost_estimate: About four hours of derivation and exact LPs
  prereqs: [think-nbij]
  replication: false
  registered: '2026-09-23'
  notes: >-
    X-046 candidate H-d. A tenfold larger terminal leaf shortens every rung of the
    H-112 ladder. The record's uniform constants already give a floor of about 0.0057
    in side per radian inside half the uniform ball.
---
# H-237: An Angular Capture Radius Around Trump’s Packing

Every verified cover of the n11 problem needs a terminal leaf around Trump’s packing,
and the only one on record is the BC-240 radius of about $0.004$. The registered tangent
cones are all zero, which says Trump is isolated at first order; this claim asks for the
quantitative version with explicit constants, on a ball larger than the one on record.

A confirm makes every rung of the settlement ladder cheaper.
A bounded negative names which constant caps the ball, and that is itself the price of
the terminal leaf.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
