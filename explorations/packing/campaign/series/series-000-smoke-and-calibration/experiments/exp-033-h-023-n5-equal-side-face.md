---
title: exp-033 — exact n = 5 equal-side fixed-angle face
softschema:
  contract: packing.squares:Experiment/v1
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-033
  series: series-000
  title: Test whether the equal-side n = 5 golden rows share one exact LP face
  date: '2026-08-24'
  hypotheses: [H-023]
  tier: exploratory
  subject:
    label: exact fixed-angle common-cell connection between golden seeds 2 and 5
    engine: n = 5 equal-side face checker 0.1.0
    engine_commit: 26360f1
    precision: exact
    host_system: macOS arm64, Apple M1 Pro
    selftest_passed: false
  instance: {axis: n, point: 5, role: target}
  method:
    control: independently valid exact endpoints and mutations that break the path
    candidate: one exact side-constant segment in a common fixed-angle separating cell
    runs_per_condition: 1
    interleaved: false
    operator: openai-codex
    commit: 26360f1
    dirty: false
    entry_point: explorations/packing/tools/check_n5_equal_side_face.py
    command: >-
      timeout 30 uv run --frozen --quiet python tools/check_n5_equal_side_face.py
      --record campaign/series/series-000-smoke-and-calibration/results/exp-033-h-023-n5-equal-side-face.json
      && timeout 30 uv run --frozen --quiet python tools/check_n5_equal_side_face.py
      --replay campaign/series/series-000-smoke-and-calibration/results/exp-033-h-023-n5-equal-side-face.json
    budget: >-
      one 30-minute local-geometry slice; separate 30-second generation and replay caps;
      stop on source mismatch, invalid endpoint, failed exact dual, wrong rank/nullity,
      mutation survivor, or retained-record drift
    record: campaign/series/series-000-smoke-and-calibration/results/exp-033-h-023-n5-equal-side-face.json
  lease:
    expires: '2026-08-24T21:00:00'
    host: spud10.local
    pid: 63018
  results:
  - shape: determination
    question: >-
      After a declared D4 action and relabelling, do the two equal-side n = 5 golden
      rows lie on one exact feasible segment whose common fixed-angle cell has the same
      exact optimal side?
    role: outcome
    outcome: no_progress
    checked_by: preregistered but not yet run
  verdict:
    decision: in-progress
    primary_criterion: >-
      exact source alignment, endpoint validity, full-segment feasibility, LP dual,
      endpoint/interior rank-nullity, independent replay, and all declared mutations
    reason: The acceptance rule is frozen before generation or replay.
---
# exp-033 — preregistered n = 5 equal-side face test

This is the first genuine basin-structure slice admitted by the confidence ladder.
It asks a deliberately local question about the two golden rows at side
`1 + 5 sqrt(2) / 4`.

The round accepts only if one declared container quarter-turn and square relabelling
bind both floating-point source poses to exact endpoints, both endpoints verify as
packings, the full exact segment stays in one fixed-angle separating cell, and an exact
dual proves that cell cannot use a smaller side.
The active fixed-side matrix must have nullity zero at each endpoint and nullity one in
the interior, with the declared slide direction spanning the interior kernel.
Generation and independent regeneration must agree, and every declared mutation must
fail.

Even an accepted result would establish only a connected fixed-angle LP optimal face.
It would not prove that every interior point is selected by the deterministic quench,
that the endpoints share one full angle-varying stationary component, or that the six
observed n = 5 rows form a complete census.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
