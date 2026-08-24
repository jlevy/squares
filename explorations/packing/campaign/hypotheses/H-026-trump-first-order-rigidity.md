---
title: H-026 — Trump’s branchwise fixed-side linearized cones are zero
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-026
  kind: hypothesis
  claim: >-
    In open real orientation charts, Trump’s exact n = 11 pose has no nonzero direction
    in the union of branchwise one-sided linearized cones of the fixed-side containment
    and non-overlap system.
  lane: proof
  derived_from: [X-002]
  strategy_refs: ['proof:15', 'proof:17']
  criterion:
    shape: determination
    metric: feasibility of the normalized branchwise linearized system at fixed side
    direction: infeasible for every nonzero normalized direction
    threshold: null
  instrument: >-
    Enumerate unique square-wall incidences and every locally available separating
    feature. Form the one-sided linearized constraints for each complete disjunctive
    branch pattern in open real angle charts, then solve each cone for a normalized
    nonzero direction with replayable exact coefficients.
  instrument_ready: true
  regime: exact Trump witness in Q(u), fixed side, all active nonsmooth branches
  instance: {axis: n, point: 11}
  priority: 1
  cost_estimate: measured 47.121 s generation plus 10.187 s exact replay after derivation
  prereqs: []
  replication: true
  registered: '2026-08-24'
  notes: >-
    The verifier's 20 boundary count is corner coordinates, not constraints. The exact
    pose has 11 square-wall incidences and 14 contacting pairs; neither feature count
    decides rigidity because axis alignment and SAT separation are nonsmooth. The
    linearized cones overapproximate the true Bouligand tangent: a zero result proves
    the true tangent is zero, while a nonzero linearized vector needs nonlinear
    continuation before it may be called a feasible motion. Finite symmetries and
    relabellings are discrete and remove no infinitesimal variable. Exp-013 certifies all
    128 derivative-distinct cones, covering 512 raw feature selections.
---
# H-026 — confirmed by exp-013

All 128 exact branch matrices have rank 33 and strictly positive exact left-kernel
stresses, so every cone is `{0}`. A separate finite-branch subsequence argument now
upgrades that result to local isolation and strict local side optimality of Trump’s pose
in the anchored pose–side chart.
It does not address global optimality or provide a quantitative neighborhood radius.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
