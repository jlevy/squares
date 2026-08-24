---
title: H-006 — discretized LP duals expose structured unavoidable-set candidates
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-006
  kind: hypothesis
  claim: >-
    Fractional-transversal LP duals for pose discretizations at the n = 12 side-4
    boundary and within the n = 11 gap place at least half their normalized dual mass in
    the top decile of spatial bins, with coarse-grained support distributions within
    Jensen-Shannon distance 0.1 across two successive grid refinements.
  lane: proof
  derived_from: [X-001]
  strategy_refs: ['proof:17', 'proof:21', 'proof:22']
  criterion:
    shape: determination
    metric: top-decile dual-mass share and coarse-grained Jensen-Shannon distance
    direction: mass share at least 0.5 and distance at most 0.1 on two refinements
  instrument: >-
    Not yet built. A pose discretizer and fractional-transversal primal/dual LP that
    exports support, weights, resolution, residuals, and candidate geometric loci.
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
    Kill if either numerical threshold is missed. A positive result supplies conjectured
    points, segments, or families to a separate falsifier and interval-proof loop; it is
    not itself a certificate. Bin construction is frozen before either refinement.
---
# H-006 — use relaxations to propose proof objects

The proof lane needs generators of unavoidable-set candidates, not numerical lower
bounds presented as proofs.
Dual support offers a disciplined way to ask where such objects might live, while
refinement stability provides a falsifiable screen against grid artifacts.

Any promoted candidate still has to survive a continuous falsifier and then an
independent proof procedure.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
