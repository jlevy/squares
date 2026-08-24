---
title: H-029 — adaptive splitting beats independent restarts on rare target events
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-029
  kind: hypothesis
  claim: >-
    After passing exact synthetic rare-event controls, adaptive multilevel splitting
    estimates one preregistered n = 10 target-event probability within its declared
    reference interval and achieves at least four times the pair-test-normalized inverse
    variance of independent restarts under the same proposer and quench.
  lane: search
  derived_from: [X-002]
  strategy_refs: ['search:12', 'search:16']
  criterion:
    shape: paired
    metric: pair-test-normalized inverse estimator variance, conditional on synthetic coverage and n = 10 reference agreement
    direction: splitting at least four times restarts
    threshold: 4
  instrument: >-
    Pass synthetic mixtures with exact probabilities and coverage first. Freeze nested
    side-and-structure levels, then estimate the n = 10 event by restarts and splitting
    with genealogical weights and compare against an independent high-precision restart
    reference. Estimate variance across outer replicates; clones are never counted as
    independent hits. The n = 11 leg requires a new registered cell after identity.
  instrument_ready: false
  regime: fixed P/Q/event definition and pair-test budget; proved n = 10 control first
  instance: {axis: n, point: 10}
  priority: 2
  cost_estimate: tier S estimator control; tier M n = 11 only after H-021 and H-023
  prereqs: [exact synthetic rare-event controls, independent n = 10 reference estimate]
  replication: true
  registered: '2026-08-24'
  notes: >-
    Zero direct arrivals cannot measure a rare probability. Splitting is promoted to a
    separately registered n = 11 cell only if exact synthetic controls and the n = 10
    reference pass, and its efficiency includes clone correlation.
---
# H-029 — rare-event machinery earns the target leg on a control

The score levels must describe progress toward the event without using the hidden answer
after preregistration.
Genealogical dependence is part of the uncertainty, not a reason to count clones as
independent hits.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
