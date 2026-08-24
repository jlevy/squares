---
title: exp-013 — H-026 exact Trump tangent screen (in progress)
softschema:
  contract: packing.squares:Experiment/v1
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-013
  series: series-000
  title: H-026 exact Trump tangent screen (in progress)
  date: '2026-08-24'
  hypotheses: [H-026]
  tier: exploratory
  subject:
    label: exact branchwise fixed-side linearized cones of the Trump n=11 witness
    engine: trump linearized-cone checker 0.1.0
    engine_commit: c22573f
    precision: exact
    host_system: macOS arm64
    selftest_passed: false
  instance: {axis: n, point: 11, role: target}
  method:
    candidate: every locally active one-sided SAT/support branch at the exact witness
    runs_per_condition: 1
    interleaved: false
    operator: openai-codex
    commit: c22573f
    dirty: false
    entry_point: explorations/packing/tools/check_trump_tangent.py
    command: >-
      uv run --frozen python tools/check_trump_tangent.py
      --record campaign/series/series-000-smoke-and-calibration/results/exp-013-h-026-trump-tangent.json
      && uv run --frozen python tools/check_trump_tangent.py
      --replay campaign/series/series-000-smoke-and-calibration/results/exp-013-h-026-trump-tangent.json
    budget: >-
      180 agent-minutes; enumerate the exact active table and every unique feature
      branch; stop on one exact nonzero linearized direction, complete zero-cone
      certificates, or any branch-completeness or coefficient-replay failure
    record: campaign/series/series-000-smoke-and-calibration/results/exp-013-h-026-trump-tangent.json
  lease:
    expires: '2026-08-24T11:13:00Z'
  results:
  - shape: determination
    question: in progress
    outcome: invalid
  verdict:
    decision: in-progress
    primary_criterion: exact feasibility of a normalized nonzero direction in any complete branchwise linearized cone
    reason: Claimed; the active-feature enumeration and exact certificate checker are being built.
---
# exp-013 — preregistered first-order screen

This round asks whether any complete one-sided linearization at Trump’s exact fixed-side
pose has a nonzero direction.
It does not ask whether the packing is nonlinearly isolated, locally optimal, or
globally optimal.

The exact witness supplies the active-table control: 11 square-wall incidences and 14
touching pairs. The verifier’s 20 boundary coordinates are not 20 independent wall
constraints. Every pairwise branch must come from a zero-gap separating feature; a zero
projection on one axis does not count if the pair is already strictly separated on
another.

At an aligned wall or same-angle pair, absolute-value support derivatives are part of
the cone and must be represented by both linear halfspaces.
At a contacting pair with several locally available separating features, feasibility is
a union, so the checker must enumerate the complete finite feature selection rather than
intersecting those alternatives.

Orientations live in open real charts around `0` and Trump’s angle; folding them into a
canonical interval would erase legitimate signed one-sided directions.
The linearized cones overapproximate the true Bouligand tangent.

The round confirms H-026 only if every unique branch has an independently replayable
exact zero-cone certificate.
It rejects H-026 if one explicit normalized nonzero direction satisfies an exact
linearized branch, but such a vector is only a continuation candidate until a nonlinear
feasible path realizes it.
It stops unresolved if the active-feature inventory, branch coverage, coefficient
derivation, or certificate replay cannot be closed inside the budget.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
