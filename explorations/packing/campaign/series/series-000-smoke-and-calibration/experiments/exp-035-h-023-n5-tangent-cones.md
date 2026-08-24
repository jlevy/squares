---
title: exp-035 — exact n = 5 full-angle tangent cones
softschema:
  contract: packing.squares:Experiment/v1
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-035
  series: series-000
  title: Test the complete active first-order cones along the exp-033 face
  date: '2026-08-24'
  hypotheses: [H-023]
  tier: exploratory
  subject:
    label: exact per-stratum full-angle active systems along the exp-033 face
    engine: n = 5 tangent-cone checker 0.2.0
    engine_commit: aa63cf4
    precision: exact
    host_system: macOS arm64, Apple M1 Pro
    selftest_passed: true
  instance: {axis: n, point: 5, role: target}
  method:
    control: >-
      exact pose-derived wall and SAT inventory plus seven source, branch, row,
      coefficient, scope, and witness mutations
    candidate: >-
      one normalized non-sheet direction checked against every active row at the two
      endpoints and one exact interior point
    runs_per_condition: 1
    interleaved: false
    operator: openai-codex
    commit: aa63cf4
    dirty: false
    entry_point: explorations/packing/tools/check_n5_tangent_cones.py
    command: >-
      timeout 30 uv run --frozen --quiet python tools/check_n5_tangent_cones.py
      --record campaign/series/series-000-smoke-and-calibration/results/exp-035-h-023-n5-tangent-cones.json
      && timeout 30 uv run --frozen --quiet python tools/check_n5_tangent_cones.py
      --replay campaign/series/series-000-smoke-and-calibration/results/exp-035-h-023-n5-tangent-cones.json
    budget: >-
      one 30-minute exact-geometry slice; separate 30-second generation and replay caps;
      stop on any active-inventory drift, missing owner axis, missing tied support row,
      stale stratum coefficient, invalid witness, surviving mutation, or replay drift
    record: campaign/series/series-000-smoke-and-calibration/results/exp-035-h-023-n5-tangent-cones.json
  effort:
    timebox: 30m exact-geometry slice; 30s generation and 30s replay caps
    wall_seconds: 0.28
    agent_minutes: 20
    stopped_by: criterion
  results:
  - shape: determination
    question: >-
      At the two endpoints and an exact interior point of the exp-033 face, does the
      complete active full-angle linearization admit a normalized direction outside
      exp-034's angle-and-slide sheet?
    role: outcome
    outcome: criterion_met
    checked_by: >-
      exact pose-derived inventories and matrices, exact row evaluation of three
      non-sheet directions, deterministic record regeneration, and seven controls
  verdict:
    decision: accepted
    primary_criterion: >-
      exact per-stratum wall and zero-axis inventories, both pair (3,4) owner-axis
      branches with both tied support rows in each, one exact non-sheet direction
      satisfying every retained active inequality, independent regeneration, and all
      seven declared controls
    reason: >-
      Both owner-axis systems and every tied support row replay at all three strata; the
      exact non-sheet direction satisfies every active row and all controls reject.
    commit: 26411ae
---
# exp-035 — exact n = 5 full-angle tangent cones

This round asks one first-order question about the exact face from exp-033 and exp-034.
At endpoint A, an exact interior point, and endpoint B, the checker must derive the
active wall and separating-axis inventory from the pose itself.
It must not reuse a contact differential across slide strata.

For pair `(3,4)`, the owner-axis choice is the only disjunction.
Within each of the two owner-axis branches, both tied support-feature derivatives are
simultaneous inequalities.
Acceptance requires the complete matrices for both owner branches and an exact
normalized direction outside exp-034’s sheet that satisfies every active row at all
three strata.

The controls must reject a missing owner branch, a missing tied support row, reuse of
endpoint A’s pair `(0,4)` coefficient in the interior, a false nonlinear-continuation
claim, source-digest drift, an invalid angle sign, and loss of diagonal angle motion.
Generation and replay had independent 30-second caps.

The criterion is met.
Endpoint A and endpoint B each have 17-row systems of exact rank 14 for both owner-axis
choices; the interior has 15-row systems of exact rank 12. Each owner branch contains
both tied support rows.
At every stratum, one exact direction with `dtheta_3 = dtheta_4 = 1` lies outside
exp-034’s sheet and makes every retained active derivative exactly zero.
All seven controls reject, and independent regeneration matches the retained record.
Generation and replay took 0.28 wall-seconds together.

An accepted result would establish only a non-sheet direction in the branchwise
linearized active systems at the three declared points.
It would not establish a true Bouligand motion, nonlinear continuation,
stationary-component connectivity, basin mass, census completeness, or a minimax path
between the unequal-side candidates.

[`exp-035-h-023-n5-tangent-cones.json`](../results/exp-035-h-023-n5-tangent-cones.json)
retains all six exact branch matrices, three directions, the determination scope, and
seven controls
(`sha256:6e803258e36b3f91518f2a8754dd82c977605815ffa365a8baf6f691e7afd477`).

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
