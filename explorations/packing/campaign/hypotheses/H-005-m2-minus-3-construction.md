---
title: H-005 — a Cleemann-style m-squared-minus-3 construction exists at m = 10
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-005
  kind: hypothesis
  claim: >-
    A Cleemann-style construction using a 3-4-5 tilt packs 97 unit squares in a square
    of side strictly less than 10.
  lane: search
  derived_from: [X-001]
  strategy_refs: ['search:6', 'search:8']
  criterion:
    shape: record
    metric: independently and exactly verified container side for 97 unit squares
    direction: below 10
    threshold: 10
  instrument: >-
    Not yet built. First derive the boundary synchronization equations analytically;
    only if they remain feasible, encode the resulting construction family and pass its
    candidate through the exact witness verifier.
  instrument_ready: false
  regime: exact construction first; targeted numerical search only after analytic triage
  instance: {axis: n, point: 97}
  sweep: {axis: n, points: [78, 97]}
  priority: 3
  cost_estimate: tier S analytic triage; tier M (1e11 pair-tests) only if it survives
  prereqs: []
  replication: false
  registered: retroactive
  notes: >-
    Honest prior is low. Kill the proposed family if its exact geometry cannot
    re-synchronize with the boundary; do not spend the numerical tier to rescue a failed
    derivation. The n = 78 cell is a diagnostic analogue, not a substitute verdict.
---
# H-005 — a cheap, high-payoff construction test

The conjectured pattern has little slack, and neighboring offset-one and offset-two
families are known to be tight.
That is a reason to screen it analytically, not to omit it: the screen is cheap and a
valid construction would be a new upper bound.

This hypothesis is blocked on a mathematical derivation, not on general search
infrastructure. It should therefore remain outside an unattended numerical queue until
the equations define an actual family to evaluate.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
