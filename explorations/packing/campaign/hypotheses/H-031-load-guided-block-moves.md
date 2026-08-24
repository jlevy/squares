---
title: H-031 — LP-load-guided block moves beat coordinate-only moves
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-031
  kind: hypothesis
  claim: >-
    Under a common temperature schedule and LP-in-cell quench, a move kernel that uses
    normalized fixed-cell dual loads to translate or rotate stressed blocks reaches the
    preregistered n = 10 and n = 17 target scores at least twice as often per pair-test
    as coordinate-only moves, without increasing independent-verifier rejection.
  lane: search
  derived_from: [X-002]
  strategy_refs: ['search:10', 'search:11', 'search:12']
  criterion:
    shape: paired
    metric: independently valid target events per pair-test under matched schedules
    direction: load-guided at least two times coordinate-only with no higher rejection rate
    threshold: 2
  instrument: >-
    Retain primal-dual LP receipts, define block proposals before the comparison, and
    run paired seeds at n = 10 and 17. Report target events, score trajectories, move
    acceptance, validity transitions, and load sparsity.
  instrument_ready: false
  regime: common proposer schedule, quench, pair-test budget, and independent verifier
  instance: {axis: n, point: 10}
  sweep: {axis: n, points: [10, 17]}
  priority: 2
  cost_estimate: one-minute smoke, then tier S paired comparison
  prereqs: [retained LP dual receipts, verified n = 17 pose]
  replication: true
  registered: '2026-08-24'
  notes: >-
    The LP dual is treated as an empirical load signal, not as a self-stress or proof of
    rigidity. A null result parks load guidance while preserving block moves as a
    separately ablatable mechanism.
---
# H-031 — turn a free solver output into a falsifiable move signal

This comparison changes one move family at a time.
It does not combine load guidance, block moves, and a new schedule into an
uninterpretable proposer bundle.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
