---
title: exp-013 — all Trump branchwise linearized cones are zero
softschema:
  contract: packing.squares:Experiment/v1
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-013
  series: series-000
  title: Exact certificates confirm H-026 and locally isolate Trump’s pose
  date: '2026-08-24'
  hypotheses: [H-026]
  tier: exploratory
  subject:
    label: exact branchwise fixed-side linearized cones of the Trump n=11 witness
    engine: trump linearized-cone checker 0.1.0
    engine_commit: faba023
    precision: exact
    host_system: macOS arm64
    selftest_passed: true
  instance: {axis: n, point: 11, role: target}
  method:
    candidate: every locally active one-sided SAT/support branch at the exact witness
    runs_per_condition: 1
    interleaved: false
    operator: openai-codex
    commit: faba023
    dirty: false
    entry_point: explorations/packing/tools/check_trump_tangent.py
    command: >-
      uv run --frozen python tools/check_trump_tangent.py
      --record campaign/series/series-000-smoke-and-calibration/results/exp-013-h-026-trump-tangent.json
      && uv run --frozen python tools/check_trump_tangent.py
      --replay campaign/series/series-000-smoke-and-calibration/results/exp-013-h-026-trump-tangent.json
      > campaign/series/series-000-smoke-and-calibration/results/exp-013-h-026-trump-tangent-replay.json
    budget: >-
      180 agent-minutes; enumerate the exact active table and every unique feature
      branch; stop on one exact nonzero linearized direction, complete zero-cone
      certificates, or any branch-completeness or coefficient-replay failure
    record: campaign/series/series-000-smoke-and-calibration/results/exp-013-h-026-trump-tangent.json
  effort:
    timebox: 180m
    wall_seconds: 57.307876
    agent_minutes: 100
    stopped_by: criterion
  results:
  - shape: determination
    question: >-
      Does any complete branchwise one-sided linearized cone at Trump’s exact fixed-side
      pose contain a nonzero direction?
    role: outcome
    outcome: criterion_met
    checked_by: >-
      tools/check_trump_tangent.py: 512 raw feature selections reduce to 128 exact
      42-row matrices; every matrix has exact rank 33 and a strictly positive Q(u)
      stress with exact zero residual; a separate replay validates all 128 records
  verdict:
    decision: accepted
    primary_criterion: exact feasibility of a normalized nonzero direction in any complete branchwise linearized cone
    reason: >-
      No nonzero linearized direction survives. All 128 derivative-distinct matrices
      have exact zero-cone certificates, covering all 512 raw nonlinear feature
      selections with zero unresolved branches.
    commit: faba023
---
# exp-013 — exact branch certificates locally isolate Trump’s pose

The preregistered screen accepted H-026. At Trump’s exact fixed side, every complete
one-sided branch linearization has only the zero direction.

## Complete active and branch inventory

The exact witness has 33 pose variables, 11 square-wall incidences, 20 tied-corner wall
rows, and 14 true pair contacts.
Two strict pairs, `(0,4)` and `(2,5)`, have an incidental zero projection but another
strictly separating feature, so they are locally interior and impose no row.

The contacts supply 24 raw zero-gap SAT features.
Their Cartesian product has 512 raw nonlinear selections.
Centered aligned contacts can have different owner axes with the same first derivative,
so exact row-set deduplication leaves 128 derivative-distinct matrices.
The retained record preserves the full 512-to-128 map because branches that agree to
first order may differ at second order.

Every matrix has 42 rows and exact rank 33.

## Exact certificate

For one branch, let `A` be its 42-by-33 exact matrix over `Q(u)` and suppose `Av ≥ 0`.
The checker retains a strictly positive vector `λ` with `Aᵀλ = 0`.

Then `λᵀAv = 0` is a strictly positive weighted sum of nonnegative row products.
Every row product must be zero; full column rank forces `v = 0`. The floating LP
proposes nine free stress weights only.
Deterministic exact elimination selects the other 33 rows, reconstructs every remaining
weight in `Q(u)`, and checks rank, positivity, and the zero residual exactly.

All 128 certificates pass.
The generation record reports `47.121073` internal seconds; the retained exact replay
reports `10.186803` seconds.
End-to-end process timings were `47.85` and `11.01` wall seconds, respectively.

The field guard independently checks that the degree-eight polynomial for `u` is
irreducible and squarefree over `Q` and has exactly one root in `(0.36,0.37)`. The
known-flexible control deletes square 0’s left-wall incidence and exactly verifies the
nonzero direction `dx₀ = −1`. A second control rejects duplicate branch records.

## Finite-branch local-isolation corollary

The computation decides linearized cones, not feasible motions.
The stronger local consequence requires a separate compactness argument.

Assume distinct fixed-side feasible poses `q_k` approach the exact pose `q`. Normalize
their displacements and pass to a convergent subsequence with unit limit `v`. There are
only finitely many SAT-feature selections, so pass again to a subsequence using one
fixed selection; tied wall supports remain simultaneous active corner inequalities.
First-order expansion of every inequality in that branch gives `A v ≥ 0`. Its
certificate forces `v = 0`, contradicting unit norm.

Thus the labeled fixed-side pose is locally isolated.
D4 actions and relabellings are finite, so a sufficiently small neighborhood excludes
every distinct orbit copy and the same statement holds modulo those symmetries.
Any nearby packing in a smaller container would also fit the fixed Trump container, so
the pose is a strict local minimum of side in the anchored pose–side chart.

This does **not** prove that Trump’s side is globally optimal, provide a quantitative
isolation radius, or exclude a better packing in another distant contact class.
No novelty claim is made without a separate literature comparison.

[`exp-013-h-026-trump-tangent.json`](../results/exp-013-h-026-trump-tangent.json)
retains the active inventory, every branch mapping and certificate, the determination
scope, and all known-answer controls
(`sha256:b70fe9806c9d54efb6cde45c99e4a8c7ff179e4bfb03c81eaf68040c181cb8d6`).
[`exp-013-h-026-trump-tangent-replay.json`](../results/exp-013-h-026-trump-tangent-replay.json)
retains the separate replay summary
(`sha256:d20b0fccab5487d66fda4b409829dcea837450b0704bb0da3a469ee18678ad68`).

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
