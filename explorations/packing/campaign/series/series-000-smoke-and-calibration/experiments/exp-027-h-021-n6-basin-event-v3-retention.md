---
title: exp-027 — n=6 BasinEvent/v3 invalid-stop retention replication
softschema:
  contract: packing.squares:Experiment/v1
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-027
  series: series-000
  title: Replicate the n=6 block while retaining the independent-validity stop
  date: '2026-08-24'
  hypotheses: [H-021]
  tier: exploratory
  known_defects: [D-183]
  subject:
    label: uniform independent starts followed by the audited Python bracket quench
    engine: basin_census.py BasinEvent/v3 and sqpack quench
    engine_commit: a3be8e4
    precision: f64_screen
    host_system: macOS arm64, Apple M1 Pro
    selftest_passed: true
  instance: {axis: n, point: 6, role: positive_control}
  method:
    candidate: four fixed starts after the D-183 invalid-event retention repair
    runs_per_condition: 4
    interleaved: false
    operator: openai-codex
    commit: a3be8e4
    dirty: false
    entry_point: explorations/packing/tools/basin_census.py
    command: >-
      timeout 90 uv run --frozen --quiet python tools/basin_census.py run --n 6
      --seeds 0-3 --time-budget 10 --output
      campaign/series/series-000-smoke-and-calibration/results/exp-027-h-021-n6-basin-event-v3-retention.jsonl
    budget: four seeds; 10 seconds per quench; 90-second process cap; retain every stop
    record: campaign/series/series-000-smoke-and-calibration/results/exp-027-h-021-n6-basin-event-v3-retention.jsonl
  lease: {expires: '2026-08-24T18:35:00Z', host: local-m1-pro}
  results:
  - shape: determination
    question: >-
      Does the repaired run retain all four n=6 outcomes, including an independently
      invalid endpoint as a replayable non-admissible event with an exact blocker?
    role: outcome
    outcome: invalid
    checked_by: pending BasinEvent/v3 semantic replay
  verdict:
    decision: in-progress
    primary_criterion: four replayable outcomes with validity and admissibility derived from evidence
    reason: >-
      Preregistered before replication. D-183 closes only if the complete block is
      retained and the seed-3 validity failure remains visible and non-admissible.
---
# exp-027 — preregistered `n = 6` retention replication

Exp-026 censored seed 3 after its endpoint failed independent validation.
This round repeats all four fixed starts under the committed D-183 repair.
It changes only the event retention contract: no solver tolerance, retry budget,
validity screen, seed, or quench budget changes.

The expected repair behavior is asymmetric.
Valid events remain admissible.
An invalid endpoint must be written with `independent_validity_failure`, must replay as
non-admissible, and must not crash or disappear.
The result does not count components or interpret side-3 returns as a complete basin
map.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
