---
title: exp-029 — four-seed n=8 BasinEvent/v3 tool validation
softschema:
  contract: packing.squares:Experiment/v1
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-029
  series: series-000
  title: Test complete BasinEvent/v3 retention and replay at n=8
  date: '2026-08-24'
  hypotheses: [H-021]
  tier: exploratory
  known_defects: [D-126]
  subject:
    label: uniform independent starts followed by the audited Python bracket quench
    engine: basin_census.py BasinEvent/v3 and sqpack quench
    engine_commit: 69c6008
    precision: f64_screen
    host_system: macOS arm64, Apple M1 Pro
    selftest_passed: true
  instance: {axis: n, point: 8, role: positive_control}
  method:
    candidate: four fixed independently addressable starts under the unchanged v3 regime
    runs_per_condition: 4
    interleaved: false
    operator: openai-codex
    commit: 69c6008
    dirty: false
    entry_point: explorations/packing/tools/basin_census.py
    command: >-
      timeout 120 uv run --frozen --quiet python tools/basin_census.py run --n 8
      --seeds 0-3 --time-budget 10 --output
      campaign/series/series-000-smoke-and-calibration/results/exp-029-h-021-n8-basin-event-v3.jsonl
    budget: four seeds; 10 seconds per quench; 120-second process cap; retain every stop
    record: campaign/series/series-000-smoke-and-calibration/results/exp-029-h-021-n8-basin-event-v3.jsonl
  lease: {expires: '2026-08-24T18:55:00Z', host: local-m1-pro}
  results:
  - shape: determination
    question: >-
      At the upper edge of H-021's intended small-n range, do all four starts retain
      independently replayable events or typed stops without censoring evidence?
    role: outcome
    outcome: invalid
    checked_by: pending BasinEvent/v3 semantic replay
  verdict:
    decision: in-progress
    primary_criterion: complete independently replayable event outcome for every fixed seed
    reason: >-
      Preregistered before measurement. This validates event retention and cost only;
      D-126 prevents deterministic-work or frequency claims, and keys are not components.
---
# exp-029 — preregistered `n = 8` event validation

BC-006 tests the upper edge of H-021’s declared small-n classifier range without
changing the instrument, seeds, per-seed budget, validity screen, blockers, or replay
contract. Every attempted seed must become one replayable event, admissible or blocked.

After the event block, a bounded timing audit will separately measure retained quench
wall time, one full semantic replay, and five repeated batches each of independent pose
screening and canonical-key computation.
These timings diagnose the loop; they do not change the event verdict.
D-126 continues to prohibit basin-frequency inference from wall-clock-censored starts.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
