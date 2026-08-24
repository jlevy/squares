---
title: exp-028 — four-seed n=7 BasinEvent/v3 tool validation
softschema:
  contract: packing.squares:Experiment/v1
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-028
  series: series-000
  title: Test complete BasinEvent/v3 retention and replay at n=7
  date: '2026-08-24'
  hypotheses: [H-021]
  tier: exploratory
  known_defects: [D-126]
  subject:
    label: uniform independent starts followed by the audited Python bracket quench
    engine: basin_census.py BasinEvent/v3 and sqpack quench
    engine_commit: ce84ef6
    precision: f64_screen
    host_system: macOS arm64, Apple M1 Pro
    selftest_passed: true
  instance: {axis: n, point: 7, role: positive_control}
  method:
    candidate: four fixed independently addressable starts under the unchanged v3 regime
    runs_per_condition: 4
    interleaved: false
    operator: openai-codex
    commit: ce84ef6
    dirty: false
    entry_point: explorations/packing/tools/basin_census.py
    command: >-
      timeout 90 uv run --frozen --quiet python tools/basin_census.py run --n 7
      --seeds 0-3 --time-budget 10 --output
      campaign/series/series-000-smoke-and-calibration/results/exp-028-h-021-n7-basin-event-v3.jsonl
    budget: four seeds; 10 seconds per quench; 90-second process cap; retain every stop
    record: campaign/series/series-000-smoke-and-calibration/results/exp-028-h-021-n7-basin-event-v3.jsonl
  lease: {expires: '2026-08-24T18:45:00Z', host: local-m1-pro}
  results:
  - shape: determination
    question: >-
      Under the unchanged v3 regime, do all four n=7 starts retain independently
      replayable events or typed stops without censoring validity or termination evidence?
    role: outcome
    outcome: invalid
    checked_by: pending BasinEvent/v3 semantic replay
  verdict:
    decision: in-progress
    primary_criterion: complete independently replayable event outcome for every fixed seed
    reason: >-
      Preregistered before measurement. This validates event generation and replay only;
      D-126 prevents deterministic-work or frequency claims, and keys are not components.
---
# exp-028 — preregistered `n = 7` event validation

BC-005 advances one size after the complete n=6 retention replication.
The instrument, seeds, per-seed budget, validity screen, typed blockers, and replay
contract remain unchanged.

Every attempted seed must become one replayable event, admissible or blocked.
The round does not require convergence or a proved optimum, and it cannot estimate basin
frequency under D-126’s wall-clock work budget.
Endpoint descriptors remain observations rather than component identities.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
