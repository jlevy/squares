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
  effort:
    timebox: 30m result slice; 90s measurement cap
    wall_seconds: 38.627748667029664
    agent_minutes: 5
    stopped_by: criterion
  results:
  - shape: determination
    question: >-
      Under the unchanged v3 regime, do all four n=7 starts retain independently
      replayable events or typed stops without censoring validity or termination evidence?
    role: outcome
    outcome: criterion_met
    checked_by: >-
      BasinEvent/v3 replay: 4/4 independently valid balanced outcomes retained; 1/4
      producer-converged and admissible; 3/4 are typed time-budget stops; all 18,286
      fixed-point evaluations settled
  verdict:
    decision: baseline
    primary_criterion: complete independently replayable event outcome for every fixed seed
    reason: >-
      The complete block retains and replays without a launch-path failure. Three
      time-budget stops make the cell unsuitable for basin-frequency or completeness
      claims under D-126, and endpoint keys remain observations rather than components.
    commit: ce84ef6
---
# exp-028 — the `n = 7` event-validation cell is complete

BC-005 advances one size after the complete n=6 retention replication.
The instrument, seeds, per-seed budget, validity screen, typed blockers, and replay
contract remain unchanged.

All four events are independently valid and replay.
Seed 1 converges at side `3.199999999999` and is admissible.
Seeds 0, 2, and 3 hit the time budget at valid sides `3.209153843824`, `3.148250012242`,
and `3.167825251585`; each remains non-admissible with `producer_not_converged`. Their
receipts account for 18,286 fixed-point evaluations, all settled and none unsettled, in
38.63 seconds of quench wall time.

This completes the n=7 event-retention cell without finding a new launch-path defect.
The 1/4 admissible rate is not a basin-frequency estimate: D-126 makes the wall-clock
work budget load-dependent, and endpoint descriptors are not component identities.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
