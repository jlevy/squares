---
title: H-032 — what are the exact small-n optimal configuration spaces?
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-032
  kind: open_question
  claim: >-
    What are the connected components, dimensions, active strata, and symmetry
    stabilizers of the optimal configuration spaces F_n(s(n)) modulo D4 and square
    relabelling for n = 3, 4, 5, and 6?
  lane: proof
  derived_from: [X-002]
  strategy_refs: ['proof:10', 'proof:11', 'proof:15', 'proof:27']
  instrument: >-
    Begin with an analytic parameterization and quotient of the exact n = 3 side-2
    family; then combine active-cell enumeration, certified continuation, interval
    exclusion, and semialgebraic decomposition for one n at a time.
  instrument_ready: false
  regime: proved optimal side for each n; quotient and boundary conventions declared
  instance: {axis: n, point: 3}
  sweep: {axis: n, points: [3, 4, 5, 6]}
  priority: 1
  cost_estimate: tier S analytic n = 3 control; agent-days for the first complete higher-n case
  prereqs: []
  replication: true
  registered: '2026-08-24'
  notes: >-
    A sampled endpoint census cannot determine this. The n = 3 solution is also the
    acceptance test for every family, stratum, quotient, and merge visualization.
---
# H-032 — topology begins on a case whose answer is known

The question deliberately asks for the optimal set, not every local optimum.
Once the representation is correct, a separate classification can enlarge the side
filtration.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
