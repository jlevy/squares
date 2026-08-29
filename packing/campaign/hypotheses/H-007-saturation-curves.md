---
title: H-007 — component-discovery curves support stable coverage estimates
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-007
  kind: hypothesis
  claim: >-
    For a fixed proposer, quench, and terminal-component relation, independently
    replicated component-discovery curves admit a prespecified coverage model whose
    parameters and held-out predictions are stable on the proved ladder and at n = 11.
  lane: search
  derived_from: [X-001]
  strategy_refs: ['search:12']
  criterion:
    shape: determination
    metric: held-out predictive calibration and parameter variation across independent seed blocks
    direction: within preregistered calibration and stability bounds at every tested cell
  instrument: >-
    Not yet built. H-011's event archive plus at least two independently seeded discovery
    sequences and a coverage model selected before looking at the held-out block.
  instrument_ready: false
  regime: one versioned P/Q/E; censored runs retained; visual plateau is not a criterion
  instance: {axis: n, point: 11}
  sweep: {axis: n, points: [5, 6, 7, 8, 9, 10, 11]}
  priority: 2
  cost_estimate: tier M (1e11 pair-tests), shared with the atlas campaign
  prereqs: [H-011]
  replication: true
  registered: retroactive
  notes: >-
    Kill if fitted parameters or held-out coverage predictions are unstable across seed
    blocks. This is the fallback when a near-complete census is not credible: estimate
    conditional coverage instead of relabeling a plateau as completeness.
---
# H-007 — make negative search results quantitative

A discovery curve that keeps rising is informative only if the campaign can estimate how
much support remains unseen.
A curve that looks flat is not enough: the model and its evaluation split must be
declared before the held-out observations are read.

The estimand is conditional on `P/Q/E`. Changing any of those creates a new curve rather
than improving the old one retroactively.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
