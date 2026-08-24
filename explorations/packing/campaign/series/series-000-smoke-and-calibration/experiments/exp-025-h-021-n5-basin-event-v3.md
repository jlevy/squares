---
title: exp-025 — four-seed n=5 BasinEvent/v3 tool validation
softschema:
  contract: packing.squares:Experiment/v1
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-025
  series: series-000
  title: Test complete BasinEvent/v3 receipts at the first non-grid proved case
  date: '2026-08-24'
  hypotheses: [H-021]
  tier: exploratory
  subject:
    label: uniform independent starts followed by the audited Python bracket quench
    engine: basin_census.py BasinEvent/v3 and sqpack quench
    engine_commit: 5ab8dab
    precision: f64_screen
    host_system: macOS arm64, Apple M1 Pro
    selftest_passed: true
  instance: {axis: n, point: 5, role: positive_control}
  method:
    candidate: four fixed independently addressable starts under the unchanged v3 regime
    runs_per_condition: 4
    interleaved: false
    operator: openai-codex
    commit: 5ab8dab
    dirty: false
    entry_point: explorations/packing/tools/basin_census.py
    command: >-
      timeout 60 uv run --frozen --quiet python tools/basin_census.py run --n 5
      --seeds 0-3 --time-budget 10 --output
      campaign/series/series-000-smoke-and-calibration/results/exp-025-h-021-n5-basin-event-v3.jsonl
    budget: four seeds; 10 seconds per quench; 60-second process cap; retain every stop
    record: campaign/series/series-000-smoke-and-calibration/results/exp-025-h-021-n5-basin-event-v3.jsonl
  lease: {expires: '2026-08-24T18:20:00Z', host: local-m1-pro}
  results:
  - shape: determination
    question: >-
      Under the unchanged v3 regime, do all four n=5 starts retain independently valid,
      balanced events or a typed stop without censoring any fixed-point evaluation?
    role: outcome
    outcome: invalid
    checked_by: pending BasinEvent/v3 semantic replay
  verdict:
    decision: in-progress
    primary_criterion: complete independently replayable event outcome for every fixed seed
    reason: >-
      Preregistered before measurement. This is tool validation: reaching the proved
      optimum is not required, and no endpoint key may be promoted to a component.
---
# exp-025 — preregistered `n = 5` event validation

BC-003 moves one size beyond the exact `n=3,4` event controls without changing the
instrument, seeds, per-seed budget, or acceptance screen.
The question is whether the event stack retains a complete, independently valid and
replayable account for every start at the first non-grid proved case.

The criterion is event-level only.
A valid nonoptimal endpoint is a successful tool observation, while any unsettled
fixed-point evaluation is a retained blocker and opens a defect before the campaign
scales further.
Repeated sides, keys, or contact descriptors are not evidence of repeated
or distinct terminal components.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
