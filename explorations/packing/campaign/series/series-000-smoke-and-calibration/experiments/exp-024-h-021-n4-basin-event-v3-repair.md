---
title: exp-024 — four-seed n=4 BasinEvent/v3 repair replication
softschema:
  contract: packing.squares:Experiment/v1
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-024
  series: series-000
  title: The repaired n=4 block produces four admissible BasinEvent/v3 observations
  date: '2026-08-24'
  hypotheses: [H-021]
  tier: exploratory
  subject:
    label: uniform independent starts followed by the audited Python bracket quench
    engine: basin_census.py BasinEvent/v3 and sqpack quench
    engine_commit: f15d036
    precision: f64_screen
    host_system: macOS arm64, Apple M1 Pro
    selftest_passed: true
  instance: {axis: n, point: 4, role: positive_control}
  method:
    candidate: four independently addressable starts after the D-171 bounded repair
    runs_per_condition: 4
    interleaved: false
    operator: openai-codex
    commit: f15d036
    dirty: false
    entry_point: explorations/packing/tools/basin_census.py
    command: >-
      timeout 60 uv run --frozen --quiet python tools/basin_census.py run --n 4
      --seeds 0-3 --time-budget 10 --output
      campaign/series/series-000-smoke-and-calibration/results/exp-024-h-021-n4-basin-event-v3-repair.jsonl
    budget: four seeds; 10 seconds per quench; 60-second process cap; retain every stop
    record: campaign/series/series-000-smoke-and-calibration/results/exp-024-h-021-n4-basin-event-v3-repair.jsonl
  effort:
    timebox: 30m diagnosis-and-result slice; 60s measurement cap
    wall_seconds: 16.966654375079088
    agent_minutes: 15
    stopped_by: criterion
  results:
  - shape: determination
    question: >-
      After the preregistered D-171 repair, do all four n=4 positive-control starts
      produce independently valid, admissible BasinEvent/v3 terminal observations?
    role: outcome
    outcome: criterion_met
    checked_by: >-
      BasinEvent/v3 replay: 4/4 producer-converged, independently valid, admissible,
      and balanced; 14,301/14,301 fixed-point evaluations settled
  verdict:
    decision: baseline
    primary_criterion: admissible terminal-event fraction at the n=4 positive control
    reason: >-
      All four events reach proved side 2 and replay as admissible. This confirms the
      bounded numerical repair and completes the event-level control cell; it does not
      classify endpoint components or decide H-021.
    commit: f15d036
---
# exp-024 — the repaired `n = 4` event calibration is complete

The retained exp-023 failure was not evidence of a different basin.
Its first LP result already violated pair rows 16 and 21 by essentially the same amount.
Tightening only the single largest residual moved the second result’s maximum to the
other already-offending row.
D-171 therefore replaced the single-row choice with one bounded retry that tightens the
complete initial offending set; the unchanged `1e-10` acceptance screen still replays
the retry against every original row.

Under engine `f15d036`, seeds 0 through 3 all converge to proved side 2, pass the
independent geometry screen, and retain balanced receipts.
The four events account for 14,301 fixed-point evaluations, all settled and none
unsettled, in 16.97 seconds total.
Seed 3 now reaches side `2.0` with 4,657 settled evaluations.

This is a positive-control result for event admissibility, not a component census.
All four endpoints share the same current geometric and contact descriptors, but those
descriptors are not proofs of connected-component identity or completeness.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
