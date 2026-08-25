---
title: exp-034 — exact n = 5 angle-and-slide sheet
softschema:
  contract: packing.squares:Experiment/v1
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-034
  series: series-000
  title: Test whether the exp-033 face lies in an exact angle-and-slide optimal sheet
  date: '2026-08-24'
  hypotheses: [H-023]
  tier: exploratory
  subject:
    label: exact two-parameter orientation-indexed LP optimal sheet through exp-033
    engine: n = 5 angle-sheet checker 0.1.0
    engine_commit: 329b848
    precision: exact
    host_system: macOS arm64, Apple M1 Pro
    selftest_passed: true
  instance: {axis: n, point: 5, role: target}
  method:
    control: four exact boundary fixtures and four mutations of the sheet certificate
    candidate: one exact half-angle-and-slide family at the exp-033 optimal side
    runs_per_condition: 1
    interleaved: false
    operator: openai-codex
    commit: 329b848
    dirty: false
    entry_point: explorations/packing/tools/check_n5_angle_sheet.py
    command: >-
      timeout 30 uv run --frozen --quiet python tools/check_n5_angle_sheet.py
      --record campaign/series/series-000-smoke-and-calibration/results/exp-034-h-023-n5-angle-sheet.json
      && timeout 30 uv run --frozen --quiet python tools/check_n5_angle_sheet.py
      --replay campaign/series/series-000-smoke-and-calibration/results/exp-034-h-023-n5-angle-sheet.json
    budget: >-
      one 30-minute exact-geometry slice; separate 30-second generation and replay caps;
      stop on an empty parameter strip, nonpositive residual margin, invalid boundary
      fixture, failed exact dual, surviving mutation, or retained-record drift
    record: campaign/series/series-000-smoke-and-calibration/results/exp-034-h-023-n5-angle-sheet.json
  effort:
    timebox: 30m exact-geometry slice; 30s generation and 30s replay caps
    wall_seconds: 0.27
    agent_minutes: 10
    stopped_by: criterion
  results:
  - shape: determination
    question: >-
      Does the exp-033 exact segment lie inside a two-parameter feasible family at the
      same exactly certified side when square 0 may rotate through a small interval?
    role: outcome
    outcome: criterion_met
    checked_by: >-
      universal exact inequalities over Q(sqrt(2)), four independent exact boundary
      fixtures, the unchanged LP dual, retained-record regeneration, and four controls
  verdict:
    decision: accepted
    primary_criterion: >-
      exact universal half-angle inequalities, four valid boundary fixtures, the
      unchanged exact LP dual, independent replay, and all four declared mutations
    reason: >-
      The full declared parameter strip is feasible at the exp-033 side, the exact dual
      proves every orientation-indexed LP cell optimal, and generation and replay agree.
    commit: 7c6fe96
---
# exp-034 — an exact n = 5 angle-and-slide sheet

Write `r = sqrt(2)`, `S = 1 + 5r/4`, and `t = tan(theta_0/2)` for the angle of the
moving square in exp-033. This round accepts only if exact arithmetic proves that every
parameter pair

`|t| <= 1/100`,

`e(t) <= u <= 3r/2 - 2 - e(t)`,

with `e(t) = |t|(1 - |t|)/(1 + t^2)`, gives a valid packing at side `S` when square 0
has centre `(1/2 + u, 5/2 - r/4 + u)` and angle `2 atan(t)`, while the other four
squares remain fixed.

The checker must verify the universal containment and separating-axis inequalities, not
infer them from samples.
Four exact boundary fixtures, covering both angle signs and both slide endpoints at
`|t| = 1/100`, must also pass the independent exact packing verifier.
The exp-033 LP dual may certify optimality only if its support excludes the moving
square and replays unchanged.
Excessive angle, an unshrunk endpoint, a signed rather than absolute support correction,
and dual drift must all be rejected.

The criterion is met.
The universal exact inequalities and all four boundary fixtures pass, and the exp-033
dual has support only on squares 2, 3, and 4, so it remains valid for every
orientation-indexed LP cell in the sheet.
Generation and independent replay took 0.27 wall-seconds together; all four declared
mutations fail.

This proves a two-dimensional sheet of optima within the declared orientation-indexed
separating cells.
It does not prove that this sheet is a whole stationary component, that
every point attracts the quench, or that the `n = 5` census is complete.

[`exp-034-h-023-n5-angle-sheet.json`](../results/exp-034-h-023-n5-angle-sheet.json)
retains the universal certificate, four exact fixtures, dual, determination scope, and
controls.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
