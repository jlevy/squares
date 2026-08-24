---
title: exp-026 — four-seed n=6 BasinEvent/v3 tool validation
softschema:
  contract: packing.squares:Experiment/v1
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-026
  series: series-000
  title: Test complete BasinEvent/v3 receipts at the first proved side-3 case
  date: '2026-08-24'
  hypotheses: [H-021]
  tier: exploratory
  subject:
    label: uniform independent starts followed by the audited Python bracket quench
    engine: basin_census.py BasinEvent/v3 and sqpack quench
    engine_commit: da6bac3
    precision: f64_screen
    host_system: macOS arm64, Apple M1 Pro
    selftest_passed: true
  instance: {axis: n, point: 6, role: positive_control}
  method:
    candidate: four fixed independently addressable starts under the unchanged v3 regime
    runs_per_condition: 4
    interleaved: false
    operator: openai-codex
    commit: da6bac3
    dirty: false
    entry_point: explorations/packing/tools/basin_census.py
    command: >-
      timeout 90 uv run --frozen --quiet python tools/basin_census.py run --n 6
      --seeds 0-3 --time-budget 10 --output
      campaign/series/series-000-smoke-and-calibration/results/exp-026-h-021-n6-basin-event-v3.jsonl
    budget: four seeds; 10 seconds per quench; 90-second process cap; retain every stop
    record: campaign/series/series-000-smoke-and-calibration/results/exp-026-h-021-n6-basin-event-v3.jsonl
  lease: {expires: '2026-08-24T18:25:00Z', host: local-m1-pro}
  results:
  - shape: determination
    question: >-
      Under the unchanged v3 regime, do all four n=6 starts retain independently valid,
      balanced events or a typed stop without censoring any fixed-point evaluation?
    role: outcome
    outcome: invalid
    checked_by: pending BasinEvent/v3 semantic replay
  verdict:
    decision: in-progress
    primary_criterion: complete independently replayable event outcome for every fixed seed
    reason: >-
      Preregistered before measurement. This is tool validation: reaching proved side 3
      is not required, and no endpoint key may be promoted to a component.
---
# exp-026 — preregistered `n = 6` event validation

BC-004 changes only the problem size after the complete n=5 event cell.
The instrument, four seeds, per-seed budget, independent geometry screen, and
balanced-receipt criterion remain unchanged.

The criterion is event-level only.
A valid nonoptimal endpoint is a successful tool observation, while any unsettled
fixed-point evaluation is a retained blocker and stops the size ladder.
Repeated sides, keys, or contact descriptors are not evidence of repeated or distinct
terminal components.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
