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
  known_defects: [D-183]
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
  effort:
    timebox: 30m result slice; 90s measurement cap
    wall_seconds: 19.01669858407695
    agent_minutes: 5
    stopped_by: error
  results:
  - shape: determination
    question: >-
      Under the unchanged v3 regime, do all four n=6 starts retain independently valid,
      balanced events or a typed stop without censoring any fixed-point evaluation?
    role: outcome
    outcome: invalid
    checked_by: >-
      BasinEvent/v3 replay validates the three retained prefix events; the runtime
      traceback shows seed 3 failed independent validation before it could be retained
  verdict:
    decision: blocked
    primary_criterion: complete independently replayable event outcome for every fixed seed
    reason: >-
      Seeds 0 through 2 replay as admissible, but seed 3 crashed at the retention
      boundary after failing independent validity. D-183 blocks the cell and all larger
      event slices until a separately preregistered replication retains that stop.
    commit: da6bac3
---
# exp-026 — the `n = 6` event validation exposes a retention failure

BC-004 changes only the problem size after the complete n=5 event cell.
The instrument, four seeds, per-seed budget, independent geometry screen, and
balanced-receipt criterion remain unchanged.

Seeds 0 through 2 reach side 3, independently validate, and account for 12,777 settled
fixed-point evaluations in 19.02 seconds of retained quench wall time.
Seed 3 then produces an endpoint that fails the independent validity screen.
Instead of retaining a blocked fourth event, `validate_event` raises and the batch exits
with only three JSONL rows.

That crash is D-183. The partial archive is retained as evidence, but it does not meet
the four-seed criterion and cannot be completed under changed code without corrupting
the round’s engine provenance.
A new round must reproduce the full block after the record contract can retain an
independently invalid endpoint as a typed stop.

The three side-3 endpoints are tool observations only.
Their descriptors are not terminal-component identities or evidence of census
saturation.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
