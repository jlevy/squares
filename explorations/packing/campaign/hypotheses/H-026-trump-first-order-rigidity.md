---
title: H-026 — Trump has no generalized first-order fixed-side motion
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-026
  kind: hypothesis
  claim: >-
    After quotienting finite container symmetries and relabelling, Trump's exact n = 11
    pose has no nonzero direction in the union of branchwise one-sided tangent cones of
    the exact fixed-side containment and non-overlap system.
  lane: proof
  derived_from: [X-002]
  strategy_refs: ['proof:15', 'proof:17']
  criterion:
    shape: determination
    metric: feasibility of the normalized generalized tangent system at fixed side
    direction: infeasible for every nonzero normalized direction
    threshold: null
  instrument: >-
    Enumerate unique square-wall incidences and every locally available separating
    feature. Form the Bouligand-style one-sided linearized constraints for each complete
    disjunctive branch pattern, then solve each cone for a normalized nonzero direction
    with replayable exact or interval coefficients.
  instrument_ready: false
  regime: exact Trump witness in Q(u), fixed side, all active nonsmooth branches
  instance: {axis: n, point: 11}
  priority: 1
  cost_estimate: sub-second LPs after an agent-tier exact derivation and branch audit
  prereqs: []
  replication: true
  registered: '2026-08-24'
  notes: >-
    The verifier's 20 boundary count is corner coordinates, not constraints. The exact
    pose has 11 square-wall incidences and 14 contacting pairs; neither feature count
    decides rigidity because axis alignment and SAT separation are nonsmooth. Passing
    this test proves first-order rigidity only, not nonlinear local optimality.
---
# H-026 — the corrected cheap leg of H-022

An explicit feasible direction would be an immediate structural result.
Infeasibility would justify the more expensive second-order and interval-neighborhood
legs of H-022. No expected rank is preregistered.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
