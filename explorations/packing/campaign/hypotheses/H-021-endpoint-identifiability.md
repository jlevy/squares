---
title: H-021 — the terminal-component classifier is decisive on the small-n ladder
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-021
  kind: hypothesis
  claim: >-
    After a fixed stationarity, isolation, continuation, and ambiguity policy is applied,
    at most 5 percent of converged endpoints at every n from 3 through 8 remain
    unclassified between declared terminal components.
  lane: search
  derived_from: [X-001]
  strategy_refs: ['search:12', 'search:18']
  criterion:
    shape: determination
    metric: per-n unresolved endpoint fraction with a 95% upper confidence bound
    direction: upper bound at most 0.05 at every cell
    threshold: 0.05
  instrument: >-
    Not yet built. Retained endpoint poses, active-constraint diagnostics, feasible
    tangent tests, local continuation, and ambiguity-preserving component assignment.
  instrument_ready: false
  regime: >-
    Proved small-n cases; exact n = 3 sliding family as the positive non-isolation
    control; classification definitions frozen before the endpoint sample is read.
  instance: {axis: n, point: 8}
  sweep: {axis: n, points: [3, 4, 5, 6, 7, 8]}
  priority: 1
  cost_estimate: tier S characterization over retained and newly generated endpoints
  prereqs: []
  replication: true
  registered: '2026-08-24'
  notes: >-
    This is the measurement-system gate for H-011. Kill the proposed discrete census if
    unresolved mass exceeds the threshold; preserve lower and upper count bounds rather
    than forcing ambiguous endpoints into singleton components.
---
# H-021 — test whether the counted object is operationally recoverable

The atlas cannot count components until its classifier is shown to decide most of the
support produced by a declared regime.
The exact `n = 3` sliding family is the control that prevents coordinate hashes from
masquerading as component identities.

Failure is a strategic result: the campaign should switch from a discrete census to an
ambiguity-preserving geometric or descriptor measure instead of spending more samples on
a denominator it cannot identify.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
