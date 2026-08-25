---
title: exp-022 — complete the four-seed n=3 BasinEvent/v3 calibration
softschema:
  contract: packing.squares:Experiment/v2
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-022
  series: series-000
  title: The remaining n=3 starts all produce admissible BasinEvent/v3 observations
  date: '2026-08-24'
  hypotheses:
  - H-021
  tier: exploratory
  subject:
    label: uniform independent starts followed by the audited Python bracket quench
    engine: basin_census.py BasinEvent/v3 and sqpack quench
    engine_commit: 8f20908
    assurance: numerically-checked
    method: numerical-f64
    precision:
      binary_bits: 53
      rounding: nearest-even
    tolerance: unrecorded-historical
    migration_annotation: '2026-08-25: the v1 artifact identified float64 arithmetic but did not retain
      one experiment-wide acceptance tolerance.'
    host_system: macOS arm64, Apple M1 Pro
    selftest_passed: true
  instance:
    axis: n
    point: 3
    role: positive_control
  method:
    candidate: three remaining independently addressable starts with complete receipts
    runs_per_condition: 3
    interleaved: false
    operator: openai-codex
    commit: 8f20908
    dirty: false
    entry_point: explorations/packing/tools/basin_census.py
    command: timeout 60 uv run --frozen --quiet python tools/basin_census.py run --n 3 --seeds 0,2,3
      --time-budget 10 --output campaign/series/series-000-smoke-and-calibration/results/exp-022-h-021-n3-basin-event-v3-completion.jsonl
    budget: three seeds; 10 seconds per quench; 60-second process cap; stop on replay failure
    record: campaign/series/series-000-smoke-and-calibration/results/exp-022-h-021-n3-basin-event-v3-completion.jsonl
  effort:
    timebox: 30m result slice; 60s measurement cap
    wall_seconds: 6.274342125048861
    agent_minutes: 6
    stopped_by: criterion
  results:
  - shape: determination
    question: Do the three remaining n=3 starts produce independently valid events with every fixed-point
      evaluation retained and settled?
    role: outcome
    outcome: criterion_met
    checked_by: 'BasinEvent/v3 replay: 3/3 producer-converged, independently valid, admissible, and
      balanced; 8,364/8,364 fixed-point evaluations settled'
  verdict:
    decision: baseline
    primary_criterion: admissible terminal-event fraction for the remaining n=3 starts
    reason: All three events are admissible and replayable. Combined with exp-021, the fixed four-seed
      n=3 block is 4/4 admissible; this still does not classify endpoint components or decide H-021.
    commit: 8f20908
---
# exp-022 — complete the `n = 3` event calibration

Seeds 0, 2, and 3 all converged and passed independent geometry and semantic replay in
6.27 seconds total.
Their receipts contain 8,364 fixed-point evaluations, all settled and
none unsettled. Together with seed 1 in exp-021, the fixed four-seed v3 block is 4/4
scientifically admissible at the event level.

Seeds 0, 1, and 3 reach side 2 within the declared floating-point screen.
Seed 2 again reaches the valid nonoptimal side `2.3627357977946724` with a clean free
pass. This is evidence that the producer has more than one terminal outcome under the
declared regime; it does not establish whether the nonoptimal endpoint is isolated,
identify its connected terminal component, or measure its basin mass.

The largest v3 n=3 event took 2.41 seconds.
The retained historical n=4 block took 13.32 seconds for four seeds, so the next n=4 v3
cell is conservatively budgeted at 10 seconds per seed and 60 seconds for the process.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
