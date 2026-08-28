---
title: exp-033 — exact n = 5 equal-side fixed-angle face
softschema:
  contract: packing.squares:Experiment/v2
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-033
  series: series-000
  title: Test whether the equal-side n = 5 golden rows share one exact LP face
  date: '2026-08-24'
  hypotheses:
  - H-023
  tier: exploratory
  subject:
    label: exact fixed-angle common-cell connection between golden seeds 2 and 5
    engine: n = 5 equal-side face checker 0.1.0
    engine_commit: 26360f1
    assurance: verified
    method: exact-algebraic
    host_system: macOS arm64, Apple M1 Pro
    selftest_passed: true
  instance:
    axis: n
    point: 5
    role: target
  method:
    control: independently valid exact endpoints and mutations that break the path
    candidate: one exact side-constant segment in a common fixed-angle separating cell
    runs_per_condition: 1
    interleaved: false
    operator: openai-codex
    commit: 26360f1
    dirty: false
    entry_point: explorations/packing/tools/check_n5_equal_side_face.py
    command: timeout 30 uv run --frozen --quiet python tools/check_n5_equal_side_face.py --record
      campaign/series/series-000-smoke-and-calibration/results/exp-033-h-023-n5-equal-side-face.json
      && timeout 30 uv run --frozen --quiet python tools/check_n5_equal_side_face.py --replay campaign/series/series-000-smoke-and-calibration/results/exp-033-h-023-n5-equal-side-face.json
    budget: one 30-minute local-geometry slice; separate 30-second generation and replay caps; stop
      on source mismatch, invalid endpoint, failed exact dual, wrong rank/nullity, mutation survivor,
      or retained-record drift
    record: campaign/series/series-000-smoke-and-calibration/results/exp-033-h-023-n5-equal-side-face.json
  effort:
    timebox: 30m local-geometry slice; 30s generation and 30s replay caps
    wall_seconds: 0.24
    agent_minutes: 15
    stopped_by: criterion
  results:
  - shape: determination
    question: After a declared D4 action and relabelling, do the two equal-side n = 5 golden rows
      lie on one exact feasible segment whose common fixed-angle cell has the same exact optimal side?
    role: outcome
    outcome: criterion_met
    checked_by: exact Q(sqrt(2)) regeneration, independent retained-record replay, sqpack exact endpoint
      validity, exact Gaussian rank, an exact LP dual, and five controls
  verdict:
    decision: accepted
    primary_criterion: exact source alignment, endpoint validity, full-segment feasibility, LP dual,
      endpoint/interior rank-nullity, independent replay, and all declared mutations
    reason: The source poses match two exact valid endpoints, their whole declared segment is feasible
      and optimal in one fixed-angle cell, and the exact nullities are 0/1/0.
    commit: 07a7f96
---
# exp-033 — the equal-side n = 5 pair shares an exact optimal face

This is the first genuine basin-structure slice admitted by the confidence ladder.
It asks a deliberately local question about the two golden rows at side
`1 + 5 sqrt(2) / 4`.

The round accepted because one declared container quarter-turn and square relabelling
bind both floating-point source poses to exact endpoints, both endpoints verify as
packings, the full exact segment stays in one fixed-angle separating cell, and an exact
dual proves that cell cannot use a smaller side.
Generation and independent regeneration agree, and all five declared controls pass.

Write `r = sqrt(2)` and `S = 1 + 5r/4`. After the D4 action and relabelling, four
squares coincide exactly.
The fifth moves as

`p0(u) = (1/2 + u, 5/2 - r/4 + u)`,

for `0 <= u <= 3r/2 - 2`, while its angle and the other four poses remain fixed.
Both endpoints satisfy the exact packing verifier.
The common separating cell has 30 rows; endpoint feasibility therefore proves the whole
segment feasible by convexity.

An exact dual has weights `-1/2` on the lower walls of square 2 and upper walls of
square 3, and `-r/2` on pair rows `(2,4)` and `(3,4)`. It satisfies `A^T y = e_side`,
`y <= 0`, and `b^T y = S`, proving that `S` is the minimum side in this fixed-angle
cell. With side fixed, the active matrix has rank 11 at each endpoint and rank 10 in the
interior, so the local linear-face nullities are `0, 1, 0`. The interior kernel is
exactly the declared slide `dx0 = dy0`.

Generation took 0.13 wall-seconds and separate regeneration and replay took 0.11
seconds, both far below their 30-second caps.

This result establishes only a connected fixed-angle LP optimal face.
It does not prove that every interior point is selected by the deterministic quench,
that the endpoints share one full angle-varying stationary component, or that the six
observed n = 5 rows form a complete census.

[`exp-033-h-023-n5-equal-side-face.json`](../results/exp-033-h-023-n5-equal-side-face.json)
retains the exact endpoints, source alignment, common-cell certificate, rank data,
determination scope, and controls.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
