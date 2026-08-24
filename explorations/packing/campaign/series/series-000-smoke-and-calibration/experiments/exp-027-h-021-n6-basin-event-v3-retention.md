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
  known_defects: [D-126, D-183]
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
  effort:
    timebox: 30m result slice; 90s measurement cap
    wall_seconds: 34.42512999998871
    agent_minutes: 5
    stopped_by: criterion
  results:
  - shape: determination
    question: >-
      Does the repaired run retain all four n=6 outcomes, including an independently
      invalid endpoint as a replayable non-admissible event with an exact blocker?
    role: outcome
    outcome: criterion_met
    checked_by: >-
      BasinEvent/v3 replay: 4/4 outcomes retained and independently valid; 3/4
      producer-converged and admissible; seed 3 is a typed time-budget stop; all 18,462
      fixed-point evaluations settled
  verdict:
    decision: baseline
    primary_criterion: four replayable outcomes with validity and admissibility derived from evidence
    reason: >-
      The complete block is retained and replays. Seed 3 does not reproduce the prior
      invalid endpoint; it remains visibly non-admissible for producer non-convergence.
      The deterministic invalid-event regression closes D-183, while D-126 explains why
      a wall-clock-limited seed need not reproduce one endpoint.
    commit: a3be8e4
---
# exp-027 — the `n = 6` retention replication is complete

Exp-026 censored seed 3 after its endpoint failed independent validation.
This round repeats all four fixed starts under the committed D-183 repair.
It changes only the event retention contract: no solver tolerance, retry budget,
validity screen, seed, or quench budget changes.

All four outcomes are retained and replay.
Seeds 0 through 2 converge at side 3 and are admissible.
Seed 3 reaches valid side `3.040392660291`, hits the time budget, and remains
non-admissible with `producer_not_converged`. The archive contains 18,462 fixed-point
evaluations, all settled and none unsettled, in 34.43 seconds of quench wall time.

The earlier invalid endpoint does not reproduce because D-126 makes the amount of work
inside a wall-clock budget host- and load-dependent.
That does not erase exp-026’s failure.
The deterministic regression now sends an independently invalid endpoint through the
same retention helper used by `run()`, proves that it replays only with
`independent_validity_failure`, and rejects forged admissibility or an omitted blocker.

This closes D-183’s censoring bug.
It does not close D-126, count components, or interpret the three side-3 returns as a
complete basin map.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
