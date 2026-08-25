---
title: exp-031 — source-bound n=10 known-answer return
softschema:
  contract: packing.squares:Experiment/v1
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-031
  series: series-000
  title: Test four source-bound returns to the proved n=10 side
  date: '2026-08-24'
  hypotheses: [H-002]
  tier: exploratory
  known_defects: [D-126]
  subject:
    label: deterministic perturbations of the published Göbel n=10 packing
    engine: basin_census.py BasinEvent/v3 and sqpack quench
    engine_commit: dab797c
    precision: f64_screen
    host_system: macOS arm64, Apple M1 Pro
    selftest_passed: true
  instance: {axis: n, point: 10, role: positive_control}
  method:
    candidate: four fixed perturbations of source fixture gobel10-svg-v1 at scale 1e-4
    runs_per_condition: 4
    interleaved: false
    operator: openai-codex
    commit: dab797c
    dirty: false
    entry_point: explorations/packing/tools/basin_census.py
    command: >-
      timeout 90 uv run --frozen --quiet python tools/basin_census.py run --n 10
      --seeds 0-3 --time-budget 15 --start-source gobel10-svg-v1
      --perturbation-scale 1e-4 --output
      campaign/series/series-000-smoke-and-calibration/results/exp-031-h-002-n10-source-return.jsonl
    budget: four seeds; 15 seconds per quench; 90-second process cap; retain every stop
    record: campaign/series/series-000-smoke-and-calibration/results/exp-031-h-002-n10-source-return.jsonl
  effort:
    timebox: 30m result slice; 90s measurement cap
    wall_seconds: 10.336620375979692
    agent_minutes: 5
    stopped_by: criterion
  results:
  - shape: determination
    question: >-
      Do all four declared source perturbations converge to independently valid n=10
      endpoints within 1e-12 of the proved side, with complete balanced receipts?
    role: outcome
    outcome: criterion_met
    checked_by: >-
      BasinEvent/v3 replay: 4/4 producer-converged, independently valid, admissible,
      and balanced; maximum analytic-side error 2.220446049250313e-15;
      6,631/6,631 fixed-point evaluations settled
  verdict:
    decision: baseline
    primary_criterion: >-
      Four of four retained events are producer-converged, scientifically admissible,
      independently valid, fully accounted, and within 1e-12 of 3 + sqrt(2)/2.
    reason: >-
      All four source perturbations satisfy every declared condition and return to the
      proved side within floating-point precision. This confirms the narrow known-answer
      control without reopening H-002's refuted universal claim.
    commit: 29d99b1
---
# exp-031 — the `n = 10` source-return control passes

BC-008 is a known-answer tool control, not a landscape sample.
Each start was a deterministic `1e-4` perturbation of the full Göbel pose reconstructed
from Kingbird’s primary SVG and identified by its retained fixture path and source URL.
The proposer, quench, independent screen, event contract, and `1e-12` side criterion are
frozen before these four outcomes were observed.

All four events meet that criterion.
They converge and independently validate with empty promotion-blocker lists; all 6,631
fixed-point evaluations are settled.
Their maximum absolute error from `3 + sqrt(2)/2` is `2.220446049250313e-15`. Retained
quench wall is 10.337 seconds, the complete command takes 11.35 seconds, and a separate
frozen semantic replay takes 0.48 seconds.

All four endpoints share one geometric key and one contact key.
That is a diagnostic of this local source-return control, not evidence that `n=10` has
one terminal component or that random starts reach it.

This round does not reopen H-002’s refuted universal claim.
It tests the narrower local known-answer behavior that the quench must reproduce before
the campaign trusts more distant starts.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
