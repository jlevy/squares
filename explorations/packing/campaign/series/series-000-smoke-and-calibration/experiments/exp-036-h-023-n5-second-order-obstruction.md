---
title: exp-036 — exact n = 5 second-order obstruction
softschema:
  contract: packing.squares:Experiment/v1
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-036
  series: series-000
  title: Test whether exp-035's displayed direction survives second order
  date: '2026-08-24'
  hypotheses: [H-023]
  tier: exploratory
  subject:
    label: exact second-order feasibility of the exp-035 common-angle direction
    engine: n = 5 second-order obstruction checker 0.1.0
    engine_commit: f2d2e53
    precision: exact
    host_system: macOS arm64, Apple M1 Pro
    selftest_passed: true
  instance: {axis: n, point: 5, role: target}
  method:
    control: >-
      exact semantic predecessor binding plus six source, direction, branch, row,
      coefficient, margin, and scope mutations
    candidate: >-
      one asymptotic inequality certificate for each of the only two nearby pair (3,4)
      owner-axis branches at all three exp-035 strata
    runs_per_condition: 1
    interleaved: false
    operator: openai-codex
    commit: f2d2e53
    dirty: false
    entry_point: explorations/packing/tools/check_n5_second_order_obstruction.py
    command: >-
      timeout 30 uv run --frozen --quiet python
      tools/check_n5_second_order_obstruction.py --record
      campaign/series/series-000-smoke-and-calibration/results/exp-036-h-023-n5-second-order-obstruction.json
      && timeout 30 uv run --frozen --quiet python
      tools/check_n5_second_order_obstruction.py --replay
      campaign/series/series-000-smoke-and-calibration/results/exp-036-h-023-n5-second-order-obstruction.json
    budget: >-
      one 30-minute exact-geometry slice; separate 30-second generation and replay caps;
      stop on source drift, a missing active row or owner branch, a nonpositive exact
      obstruction margin, a surviving mutation, or retained-record drift
    record: campaign/series/series-000-smoke-and-calibration/results/exp-036-h-023-n5-second-order-obstruction.json
  effort:
    timebox: 30m exact-geometry slice; 30s generation and 30s replay caps
    wall_seconds: 0.21
    agent_minutes: 20
    stopped_by: criterion
  results:
  - shape: determination
    question: >-
      Is the normalized common-angle direction retained by exp-035 excluded from the
      true fixed-side Bouligand tangent cone at endpoint A, the interior, and endpoint B?
    role: outcome
    outcome: criterion_met
    checked_by: >-
      exact Q(sqrt(2)) coefficient derivation, source-bound branch exhaustion,
      deterministic record regeneration, and six declared controls
  verdict:
    decision: accepted
    primary_criterion: >-
      bind every required exp-035 wall and SAT branch; derive exact positive owner-4
      excess, negative owner-3 gap, and positive relative-angle cusp margin; exhaust the
      two nearby owner axes; replay independently; and reject all six controls
    reason: >-
      Both possible nearby owner-axis branches have a strict exact second-order
      obstruction, all six controls reject, and retained replay is identical.
    commit: a54c838
---
# exp-036 — exact n = 5 second-order obstruction

Exp-035 found one exact direction with `dtheta_3 = dtheta_4 = 1` in every retained
branchwise linearization.
This round asks whether that specific direction is a true fixed-side Bouligand tangent.
It does not ask whether all directions outside exp-034’s sheet are obstructed.

Write `r = sqrt(2)`, `S = 1 + 5r/4`, `w_i = cos(theta_i) + sin(theta_i)`, and
`delta = theta_3 - theta_4`. A sequence normalized to the displayed direction has

`w_i = r - (r/2)t^2 + o(t^2)` and `delta = o(t)`.

The checker must bind the source direction, square 2’s two lower walls, square 3’s two
upper walls, pair `(2,4)`’s unique zero owner axis, and both zero owner axes for pair
`(3,4)` at A, the interior, and B. Continuity then leaves only two branches.

For the owner-4 branch, acceptance requires the necessary inequality

`S >= 1 + w_3/2 + 3/(2w_4)`

to exceed the fixed side by the exact positive coefficient `(r/8)t^2 + o(t^2)`. For the
owner-3 branch, the exact common-angle upper-minus-lower coefficient must be `-1/4`; its
relative-angle cusp must have positive margin `1/2 - |r/2 - 3/4| = r/2 - 1/4`, so
`delta = o(t)` cannot repair the deficit.

The controls reject a changed common-angle direction, a missing pair `(2,4)` row, a
missing pair `(3,4)` owner branch, nonpositive owner-4 or relative-angle margins, and a
component-isolation overclaim.
Generation and replay had independent 30-second caps.

The criterion is met.
The owner-4 branch requires the fixed side to exceed itself by
`(sqrt(2)/8)t^2 + o(t^2)`. The owner-3 upper-minus-lower gap is `-(1/4)t^2 + o(t^2)`
before the nonhelpful relative-angle cusp, whose exact positive margin is
`sqrt(2)/2 - 1/4`. Continuity exhausts the two owner-axis choices at every declared
stratum. All six controls reject, and independent regeneration matches the retained
record. Generation and replay took 0.21 external wall-seconds together.

This excludes only exp-035’s displayed vector from the true tangent cone at the three
declared strata. It establishes a strict gap between the branchwise linearized and
Bouligand cones in that direction.
It does not establish local isolation, classify other non-sheet directions, identify a
whole stationary component, measure basin mass, complete the census, or bear on
unequal-side clearance.

[`exp-036-h-023-n5-second-order-obstruction.json`](../results/exp-036-h-023-n5-second-order-obstruction.json)
retains the two exact branch arguments, their coefficients, source binding,
determination scope, and six controls.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
