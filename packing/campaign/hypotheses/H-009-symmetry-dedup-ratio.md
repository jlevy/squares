---
title: H-009 — symmetry canonicalization materially changes component counts
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-009
  kind: hypothesis
  claim: >-
    D4 and square-relabel canonicalization merges at least 10 percent of raw terminal
    endpoint keys on one or more declared small-n cells under a fixed identity policy.
  lane: search
  derived_from: [X-001]
  strategy_refs: ['search:12', 'search:18']
  criterion:
    shape: determination
    metric: per-n canonical-to-raw endpoint-count ratio with ambiguity bounds
    direction: ratio at or below 0.9 on at least one cell
    threshold: 0.9
  instrument: >-
    Existing canonical keys plus the not-yet-complete terminal-component and ambiguity
    policy, applied to the same retained endpoints before and after D4/relabel quotienting.
  instrument_ready: false
  regime: fixed key quantum and component relation; ambiguous identities reported as bounds
  instance: {axis: n, point: 10}
  sweep: {axis: n, points: [3, 5, 6, 7, 8, 9, 10, 11]}
  priority: 1
  cost_estimate: marginal analysis over H-011's retained endpoints
  prereqs: [H-011]
  replication: true
  registered: retroactive
  notes: >-
    The ratio is required metadata even if the 10 percent threshold is missed. It is not
    comparable with a published basin count unless both works use compatible endpoint,
    symmetry, and connected-component definitions.
---
# H-009 — quantify what the identity quotient removes

The `n = 3` angle-wrap defect already proves that a naive key can split one geometric
object. This experiment measures the effect on actual campaign output after the
terminal-component relation is fixed.

Raw and canonical counts remain side by side in the result.
The canonical count does not erase the diagnostic value of how the raw proposer and
serializer represented the same component.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
