---
title: exp-032 — exact terminal-component known-answer controls
softschema:
  contract: packing.squares:Experiment/v1
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-032
  series: series-000
  title: Test the exact n = 3 and n = 4 terminal-component policy
  date: '2026-08-24'
  hypotheses: [H-021]
  tier: confirmatory
  subject:
    label: exact n = 3 connected interval with n = 4 isolated-point guard
    engine: terminal-component known-answer checker 0.1.0
    engine_commit: d3d4ace
    precision: exact
    host_system: macOS arm64, Apple M1 Pro
    selftest_passed: true
  instance: {axis: n, point: 3, role: positive_control}
  method:
    control: complete exact exp-014 and exp-015 quotient models
    candidate: evidence-gated component assignment with ambiguity-preserving fallback
    runs_per_condition: 1
    interleaved: false
    operator: openai-codex
    commit: d3d4ace
    dirty: false
    entry_point: explorations/packing/tools/check_terminal_components.py
    command: >-
      timeout 30 uv run --frozen --quiet python tools/check_terminal_components.py
      --record campaign/series/series-000-smoke-and-calibration/results/exp-032-h-021-terminal-component-controls.json
      && timeout 30 uv run --frozen --quiet python tools/check_terminal_components.py
      --replay campaign/series/series-000-smoke-and-calibration/results/exp-032-h-021-terminal-component-controls.json
    budget: >-
      one 30-minute implementation slice; 30-second generation cap; 30-second separate
      replay cap; stop on any exact-model drift, false assignment, or failed mutation
    record: campaign/series/series-000-smoke-and-calibration/results/exp-032-h-021-terminal-component-controls.json
  effort:
    timebox: 30m implementation; 30s generation and 30s replay caps
    wall_seconds: 0.92
    agent_minutes: 10
    stopped_by: criterion
  results:
  - shape: determination
    question: >-
      Does the frozen policy recover the exact n = 3 quotient interval and n = 4
      quotient point without treating keys, contact strata, or samples as components?
    role: outcome
    outcome: criterion_met
    checked_by: >-
      deterministic regeneration from exp-014 and exp-015, separate retained-record
      replay, exact quotient membership, and seven false-policy mutation controls
  verdict:
    decision: baseline
    primary_criterion: exact known answers plus all declared false-policy mutations
    reason: >-
      The exact connected and isolated controls pass, every declared conflation fails,
      and all unsupported floating-point observations remain unresolved.
    commit: 93baf5c
---
# exp-032 — exact component controls pass

This is a measurement-system round, not a basin census.
It tests the evidence boundary needed before any sampled endpoint can be called a
terminal component.

The assignment policy is intentionally asymmetric.
A complete exact quotient model, or a separately replayable membership certificate, may
assign a member to a component.
Geometric keys, contact signatures, finitely many samples, and floating-point
compatibility may not.
Without sufficient evidence, the only valid output is `unresolved`.

The retained generation took 0.50 wall-seconds and the independent rebuild and replay
took 0.42 seconds. Both report one `n = 3` quotient component across two contact
signatures, one `n = 4` quotient component, 16 unresolved floating-point observations,
and seven of seven rejected false-policy mutations.

## Preregistered acceptance rule

The round passes only if one deterministic generation and one separate rebuild satisfy
all of these conditions:

- the four exact `n = 3` quotient samples lie in one connected component even though
  they have four geometric keys and cross two contact signatures and three strata;
- all 24 exact labelled `n = 4` grid states map to one point after the declared
  `D4 x S4` quotient;
- every retained floating-point observation remains unresolved because this checker has
  no exact membership witness for it;
- the known nonoptimal `n = 3` observation and the out-of-domain `n = 5` observations
  remain unresolved; and
- mutations that equate a geometric key, contact signature, sample, labelled state, or
  floating-point match with a component are all rejected.

Any exact-record drift, quotient-scope drift, forced numerical assignment, missing
known-answer stratum, or mutation survivor rejects the instrument.
This round admits the first bounded `n = 5` connectivity work; it does not validate a
scalable classifier, estimate basin mass, or close the general identity bead.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
