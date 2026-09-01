---
title: H-051 — a blinded n = 68 public-parent surgery pilot matches the released child
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-051
  kind: hypothesis
  claim: >-
    Starting only from the hash-verified public n = 68 parent, a proposer isolated from
    all child-bearing data and limited to the frozen delete/reinsert, connected-block
    shear, contiguous-strip move, and local-reoptimization grammar emits an independently
    valid packing whose certified side upper bound is no greater than the released
    child's reported side, within a tier-S budget of at most 1e9 dynamic pair tests.
  lane: search
  derived_from: [X-011]
  strategy_refs: ['search:5', 'search:7', 'search:8', 'search:20']
  criterion:
    shape: determination
    metric: >-
      independently valid proposer output with certified side upper bound compared with
      the released n = 68 child's reported side after the proposal is frozen
    direction: >-
      accepted only if at least one output matches or beats the released child's reported
      side; rejected if the full counted budget completes with no such output; unresolved
      if provenance, blinding, precision, validity, or work-accounting guards fail
    threshold: released n = 68 child side
  instrument: >-
    Agenda-012 BC-113 builds the versioned proposer and validator, freezes the exact move
    grammar and counted schedule in the experiment record, runs from an isolated
    allowlisted parent snapshot with network access disabled, and lifts the child blind
    only after proposer output is immutable.
  instrument_ready: false
  regime: >-
    n = 68 only; each BC-109 serialization model retained separately; maximum induced
    corner displacement, container-side interval width, and worst wall/pair-separation
    interval width each at most one quarter of the released 7.68618004216131e-5 gain
  instance: {axis: n, point: 68}
  priority: 1
  cost_estimate: >-
    tier S, capped at 1e9 dynamic pair tests and one 180-minute agent block; the counted
    proposal schedule is frozen before any child-bearing data is available
  prereqs:
  - BC-109 surgery-grade parent and child candidates under at least one serialization model
  - isolated allowlisted proposer snapshot with network access disabled
  replication: false
  registered: '2026-09-01'
  notes: >-
    This is one calibration cell, not a verdict on H-030's two-of-six claim and not an
    independent-discovery claim. A valid miss rejects H-051 under this grammar and budget;
    it does not reject public-parent surgery under a different preregistered grammar.
---
# H-051 — Blinded `n = 68` Surgery Calibration

The released improvement is large enough to separate a real response from the rounded
source floor once BC-109 supplies a surgery-grade parent and child model.
The information barrier is part of the instrument: operator separation without an
isolated input allowlist is not blinding.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
