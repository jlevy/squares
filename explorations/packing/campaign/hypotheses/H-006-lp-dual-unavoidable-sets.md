---
title: H-006 — primal-dual column generation exposes unavoidable-set candidates
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-006
  kind: hypothesis
  claim: >-
    Fractional-transversal column generation at the n = 12 side-4 boundary and within
    the n = 11 gap yields primal piercing-point support with at least half its normalized
    mass in the top decile of preregistered spatial bins, with coarse-grained primal
    support distributions within Jensen-Shannon distance 0.1 across two successive
    refinements.
  lane: proof
  derived_from: [X-001]
  strategy_refs: ['proof:17', 'proof:21', 'proof:22']
  criterion:
    shape: determination
    metric: top-decile primal-mass share and coarse-grained Jensen-Shannon distance
    direction: mass share at least 0.5 and distance at most 0.1 on two refinements
  instrument: >-
    Not yet built. A primal-dual column-generation loop in which dual hard-to-hit square
    poses drive a point-column oracle, while primal piercing-point support supplies
    candidate loci. Export both supports, weights, resolutions, residuals, and every
    continuous escape counterexample.
  instrument_ready: false
  regime: candidate generation only; a discretized LP is never a packing lower-bound proof
  instance: {axis: n, point: 12}
  sweep: {axis: n, points: [11, 12]}
  priority: 3
  cost_estimate: tier M exploratory LP sweep
  prereqs: []
  replication: true
  registered: retroactive
  notes: >-
    Kill if either numerical threshold is missed. Dual variables live on square poses,
    not spatial point loci; the primal support is what proposes points. A positive result
    still goes to a separate continuous falsifier and interval-proof loop and is not
    itself a certificate. Bin construction is frozen before either refinement.
---
# H-006 — use relaxations to propose proof objects

The proof lane needs generators of unavoidable-set candidates, not numerical lower
bounds presented as proofs.
Dual pose weights identify hard instances for point-column generation; primal support
proposes the actual geometric objects.
Refinement stability provides a falsifiable screen against grid artifacts.

Any promoted candidate still has to survive a continuous falsifier and then an
independent proof procedure.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
