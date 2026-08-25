---
title: exp-015 — exact n = 4 optimal moduli are one grid orbit
softschema:
  contract: packing.squares:Experiment/v1
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-015
  series: series-000
  title: Exact classification of the full n = 4 optimal configuration space
  date: '2026-08-24'
  hypotheses: [H-032]
  tier: confirmatory
  subject:
    label: full physical configuration space of four unit squares in side 2
    engine: exact small-n moduli checker 0.1.0
    engine_commit: 257cb0d
    precision: exact
    host_system: macOS arm64
    selftest_passed: true
  instance: {axis: n, point: 4, role: positive_control}
  method:
    control: n = 3 orientation-forcing lemma and the exact 2 x 2 grid
    candidate: exhaustive arbitrary-orientation classification and D4 x S4 orbit audit
    runs_per_condition: 1
    interleaved: false
    operator: openai-codex
    commit: 257cb0d
    dirty: false
    entry_point: explorations/packing/tools/check_small_n_moduli.py
    command: >-
      uv run --frozen python tools/check_small_n_moduli.py --n 4
      --record campaign/series/series-000-smoke-and-calibration/results/exp-015-h-032-n4-optimal-moduli.json
      && uv run --frozen python tools/check_small_n_moduli.py --n 4 --replay
      campaign/series/series-000-smoke-and-calibration/results/exp-015-h-032-n4-optimal-moduli.json
    budget: >-
      30 agent-minutes after exp-014; stop on one valid non-grid side-2 configuration,
      an orbit/stabilizer mismatch, or the replayed exact 24-state classification
    record: campaign/series/series-000-smoke-and-calibration/results/exp-015-h-032-n4-optimal-moduli.json
  effort:
    timebox: 30m
    wall_seconds: 0.65
    agent_minutes: 5
    stopped_by: criterion
  results:
  - shape: determination
    question: What is the full physical side-2 configuration space at n = 4 and its S4 and D4 x S4 quotients?
    role: outcome
    outcome: criterion_met
    checked_by: >-
      tools/check_small_n_moduli.py: the common exact orientation forcing, all 4096
      separation choices, 96 consistent zero-cells, 24 exact packing states, orbit and
      stabilizer checks, scoped literature comparison, six mutation controls, and a separate
      complete semantic replay
  verdict:
    decision: accepted
    primary_criterion: exhaustive exact classification of F_4(2) and its S4 and D4 x S4 quotients
    reason: >-
      Every physical packing is the axis-aligned 2 x 2 grid. F_4(2) consists of 24
      isolated labelled states, and both declared symmetry quotients are one point.
    commit: 257cb0d
---
# exp-015 — the complete optimal moduli space at n = 4

The preregistered corollary passed as its own sweep cell.
The orientation-forcing argument from exp-014 makes every square axis-aligned.
At side 2, all four lower-left coordinates must occupy the four corners of `[0,1]^2`.

The checker nevertheless exhausts the full separation disjunction rather than importing
the conclusion. Of 4,096 raw six-pair choices, 96 are consistent and every one is
zero-dimensional. They reduce four-to-one to exactly 24 labelled grid states, all
accepted by the exact packing oracle.
Thus the labelled space is 24 isolated points with Betti vector `[24,0]`. The `S4`
quotient is one point, and the `D4 x S4` quotient is the same point with combined
stabilizer order eight.

Alpert et al.'s reported Betti vector agrees.
Their table does not report an `n = 4` f-vector; the retained record preserves that null
instead of attributing the independently derived 24-state count to the source.

Generation took 0.33 wall seconds and complete replay took 0.32 seconds.
All six known-answer mutations passed.
The retained result is
[`exp-015-h-032-n4-optimal-moduli.json`](../results/exp-015-h-032-n4-optimal-moduli.json).

A valid rotated or continuously moving side-2 configuration rejects the classification.
An incomplete orientation argument, state enumeration, group action, or exact replay
leaves it unresolved.
Nothing in this round is evidence about `n = 5` or `n = 6`.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
