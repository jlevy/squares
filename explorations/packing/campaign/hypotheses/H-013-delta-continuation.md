---
title: H-013 — delta-continuation improves record-component arrival
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-013
  kind: hypothesis
  claim: >-
    Tracking configurations from an inflated container toward the target side with a
    quench after each decrement reaches the proved n = 10 record component, then Trump's
    n = 11 component, more often than direct multistart at equal pair-test budget.
  lane: search
  derived_from: [X-001]
  strategy_refs: ['search:11', 'search:12']
  criterion:
    shape: paired
    metric: record-component arrivals per pair-test, with bifurcation-tree agreement as a secondary metric
    direction: higher for delta-continuation than paired direct multistart
  instrument: >-
    Not yet built. A continuation proposer with fixed delta schedule, event-level branch
    identities, common quench and verifier, compared with the named raw-coordinate null.
  instrument_ready: false
  regime: n = 10 gate before n = 11; equal pair-test budgets and seed blocks
  instance: {axis: n, point: 10}
  sweep: {axis: n, points: [10, 11]}
  priority: 2
  cost_estimate: tier S at n = 10, then tier M at n = 11
  prereqs: [H-011]
  replication: true
  registered: retroactive
  notes: >-
    Kill the proposer as a discovery tool if it does not beat direct multistart on the
    n = 10 gate. Its paths may still be retained as landscape probes, including the
    merge-delta at which terminal components connect.
---
# H-013 — turn rare-event search into path following

Inflating the container may replace a direct hit on a rare terminal component with a
path that can be followed and checked.
The small proved case comes first so the method cannot consume an `n = 11` budget before
showing it can recover a known answer.

The bifurcation tree is a secondary deliverable, not an excuse to change the primary
record-arrival criterion after the run.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
