---
title: H-003 — basin frequency anti-correlates with contact count
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-003
  kind: hypothesis
  claim: >-
    Under one versioned proposer, quench, and terminal-component relation, component
    attraction frequency decreases as independently measured contact count increases on
    the proved small-n ladder and at n = 11.
  lane: search
  derived_from: [X-001]
  strategy_refs: ['search:12', 'search:18']
  criterion:
    shape: determination
    metric: held-out rank association between component attraction frequency and contact count
    direction: negative at every preregistered ladder cell and at n = 11
  instrument: >-
    Not yet built. H-011's event archive and terminal-component relation, augmented with
    an independently calibrated contact extractor and a preregistered cross-n analysis.
  instrument_ready: false
  regime: one declared P/Q/E; contact tolerance calibrated independently of component identity
  instance: {axis: n, point: 11}
  sweep: {axis: n, points: [5, 6, 7, 8, 9, 10, 11]}
  priority: 3
  cost_estimate: tier M (1e11 pair-tests), mostly shared with H-011 and H-012
  prereqs: [H-011]
  replication: true
  registered: retroactive
  notes: >-
    Kill if the preregistered association is not negative on the ladder and at n = 11.
    Contact count is a predictor to test, not a definition of rigidity or component
    identity; algebraic degree is a separate model rather than an interchangeable proxy.
---
# H-003 — does contact structure predict attraction frequency?

Ellsworth’s four hits in 3,004 starts for the highly constrained `s(51)` construction
motivates the claim, but it does not measure the proposed relation across components.
The test must use held-out components or cells: fitting and evaluating on the same small
atlas would turn a descriptive correlation into a flattering steering rule.

A negative result is useful.
It would retire contact count as a generic search prior while leaving component
discovery and frequency estimates intact.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
