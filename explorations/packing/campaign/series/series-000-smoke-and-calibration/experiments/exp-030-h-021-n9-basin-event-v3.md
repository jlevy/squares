---
title: exp-030 — one-seed n=9 BasinEvent/v3 performance validation
softschema:
  contract: packing.squares:Experiment/v1
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-030
  series: series-000
  title: Time one complete BasinEvent/v3 path at n=9
  date: '2026-08-24'
  hypotheses: [H-021]
  tier: exploratory
  known_defects: [D-126]
  subject:
    label: one uniform independent start followed by the audited Python bracket quench
    engine: basin_census.py BasinEvent/v3 and sqpack quench
    engine_commit: 56bf66c
    precision: f64_screen
    host_system: macOS arm64, Apple M1 Pro
    selftest_passed: true
  instance: {axis: n, point: 9, role: positive_control}
  method:
    candidate: one fixed independently addressable start under the unchanged v3 regime
    runs_per_condition: 1
    interleaved: false
    operator: openai-codex
    commit: 56bf66c
    dirty: false
    entry_point: explorations/packing/tools/basin_census.py
    command: >-
      timeout 60 uv run --frozen --quiet python tools/basin_census.py run --n 9
      --seeds 0 --time-budget 20 --output
      campaign/series/series-000-smoke-and-calibration/results/exp-030-h-021-n9-basin-event-v3.jsonl
    budget: one seed; 20-second quench; 60-second process cap; retain every stop
    record: campaign/series/series-000-smoke-and-calibration/results/exp-030-h-021-n9-basin-event-v3.jsonl
  lease: {expires: '2026-08-24T19:15:00Z', host: local-m1-pro}
  results:
  - shape: determination
    question: >-
      Does one n=9 start traverse generation, quench, independent validation, keying,
      retention, and replay inside the declared performance stop?
    role: outcome
    outcome: invalid
    checked_by: pending BasinEvent/v3 semantic replay and bounded stage timing
  verdict:
    decision: in-progress
    primary_criterion: one complete independently replayable event with attributed stage cost
    reason: >-
      Preregistered before measurement. Stop for a profile rather than expanding the
      sample if the complete cell exceeds 30 seconds or exposes a launch-path defect.
---
# exp-030 — preregistered `n = 9` performance cell

BC-007 asks whether the complete event path remains cheap enough to inspect before any
broader sampling at n=9. It changes only the size, the per-seed cap, and the number of
starts from exp-029. The single event must be retained and semantically replayed whether
it is admissible or blocked.

After the event, the same bounded audit used by exp-029 measures independent screening,
canonical-key computation, and semantic replay.
If the complete cell exceeds 30 seconds, this round stops at one seed and hands the
measured bottleneck to `think-xzew`; it does not expand the sample or infer a basin
frequency.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
