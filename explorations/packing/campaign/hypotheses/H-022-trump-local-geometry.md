---
title: H-022 — what is the certified local geometry of Trump's packing?
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-022
  kind: open_question
  claim: >-
    What explicit isolation radius and side-perturbation stability can be certified for
    Trump’s locally isolated n = 11 pose, and which parts of its exact stress structure
    can constrain distant contact classes?
  lane: proof
  derived_from: [X-001]
  strategy_refs: ['proof:20', 'proof:21']
  instrument: >-
    H-026's union of branchwise one-sided linearized cones, followed by the finite-branch
    subsequence lemma; quantitative isolation still needs an interval neighborhood.
  instrument_ready: false
  regime: exact algebraic reference packing with all containment and non-overlap inequalities
  instance: {axis: n, point: 11}
  priority: 1
  cost_estimate: local isolation complete in exp-013; quantitative radius remains separately budgeted
  prereqs: []
  replication: true
  registered: '2026-08-24'
  notes: >-
    Either answer matters. Isolation would justify a point-like local model; a feasible
    optimal family would change component identity and the interpretation of attraction
    measurements. Exp-013 answers the qualitative question: all 128 exact linearized
    cones are zero, and the finite-branch subsequence argument proves local isolation
    and strict local side optimality. A quantitative radius and global optimality remain
    open; the local statement uses the repository’s anchored pose–side chart.
---
# H-022 — certify the local object before using it as a landmark

Exp-013 settles the qualitative local question.
It retains the complete 512-to-128 branch map and exact zero-cone certificates, then
uses finiteness of the branch system to rule out any sequence of distinct feasible poses
approaching Trump’s pose.

What remains is quantitative and global: certify an explicit isolation radius, study
stability under perturbing the container side, and exclude distant contact classes.
The first structural successor is [H-043](H-043-trump-incidence-rigidity-cores.md),
which asks the narrower fixed-side question of whether every derivative branch has a
proper group-minimal wall/contact core.
Its answer does not settle any of those quantitative or global questions.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
