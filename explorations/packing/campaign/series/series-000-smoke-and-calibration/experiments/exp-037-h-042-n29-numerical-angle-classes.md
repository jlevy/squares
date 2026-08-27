---
title: exp-037 — the retained n = 29 serialization has six numerical angle classes
softschema:
  contract: packing.squares:Experiment/v2
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-037
  series: series-000
  title: Numerically test the n = 29 serialization's three-class claim
  date: '2026-08-25'
  hypotheses: [H-042]
  tier: confirmatory
  subject:
    label: retained Kingbird n = 29 SVG serialization
    engine: kingbird SVG reconstruction checker 0.1.0
    engine_commit: ae034ba
    assurance: numerically-checked
    method: numerical-multiprecision
    precision: {decimal_digits: 160, rounding: nearest}
    tolerance: 1e-80
    host_system: macOS arm64
    selftest_passed: true
  instance: {axis: n, point: 29, role: target}
  method:
    candidate: retained primary Kingbird square-29.svg serialization
    runs_per_condition: 1
    interleaved: false
    operator: openai-codex
    commit: ae034ba
    dirty: true
    entry_point: cases.kingbird29.verify_svg
    command: >-
      uv run --frozen python -m cases.kingbird29.verify_svg
      resources/papers/kingbird-square-29-provenance.svg
      --record campaign/series/series-000-smoke-and-calibration/results/exp-037-h-042-n29-numerical-angle-classes.json
    budget: one deterministic source replay; stop on a failed numerical guard or a class count
      above three
    record: campaign/series/series-000-smoke-and-calibration/results/exp-037-h-042-n29-numerical-angle-classes.json
  effort:
    timebox: 15m
    wall_seconds: 0.315011
    agent_minutes: 15
    stopped_by: criterion
  results:
    - shape: determination
      question: Does the retained serialization have at most three numerical orientation classes?
      role: outcome
      outcome: criterion_missed
      checked_by: >-
        cases.kingbird29.verify_svg at 160 decimal digits and tolerance 1e-80; all 406
        pairs checked numerically, six disjoint angle intervals, source equations replayed
  verdict:
    decision: rejected
    primary_criterion: numerical orientation-class count no greater than three
    reason: >-
      The retained serialization has six numerical orientation classes, with minimum
      class gap 0.296067 degrees against a 1e-90 degree interval radius.
    commit: ae034ba
---
# exp-037 — six numerical classes reject H-042

The deterministic replay found the same six classes as exp-012: one aligned class and
five nonzero classes with multiplicities `15, 1, 9, 1, 2, 1`. The minimum gap between
classes is `0.296067318913687…°`, far above the declared `1e-90°` interval radius.

[`exp-037-h-042-n29-numerical-angle-classes.json`](../results/exp-037-h-042-n29-numerical-angle-classes.json)
records all 29 reconstructed squares, 406 pair checks, the arithmetic settings, source
equation residuals, mutation controls, and class intervals.

This rejects H-042 exactly as scoped: a claim about one numerical serialization under
one declared arithmetic regime.
It does not verify exact feasibility, prove the reported upper bound, or decide
optimality. H-024’s corpus claim was already refuted by exp-012’s reconstruction; H-042
scopes the three-class question to this serialization under the declared numerical
regime.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
