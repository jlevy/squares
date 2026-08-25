---
title: exp-029 — four-seed n=8 BasinEvent/v3 tool validation
softschema:
  contract: packing.squares:Experiment/v2
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-029
  series: series-000
  title: Test complete BasinEvent/v3 retention and replay at n=8
  date: '2026-08-24'
  hypotheses:
  - H-021
  tier: exploratory
  known_defects:
  - D-126
  subject:
    label: uniform independent starts followed by the audited Python bracket quench
    engine: basin_census.py BasinEvent/v3 and sqpack quench
    engine_commit: 69c6008
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
    point: 8
    role: positive_control
  method:
    candidate: four fixed independently addressable starts under the unchanged v3 regime
    runs_per_condition: 4
    interleaved: false
    operator: openai-codex
    commit: 69c6008
    dirty: false
    entry_point: explorations/packing/tools/basin_census.py
    command: timeout 120 uv run --frozen --quiet python tools/basin_census.py run --n 8 --seeds 0-3
      --time-budget 10 --output campaign/series/series-000-smoke-and-calibration/results/exp-029-h-021-n8-basin-event-v3.jsonl
    budget: four seeds; 10 seconds per quench; 120-second process cap; retain every stop
    record: campaign/series/series-000-smoke-and-calibration/results/exp-029-h-021-n8-basin-event-v3.jsonl
  effort:
    timebox: 30m result slice; 120s measurement cap
    wall_seconds: 38.004218124900945
    agent_minutes: 5
    stopped_by: criterion
  results:
  - shape: determination
    question: At the upper edge of H-021's intended small-n range, do all four starts retain independently
      replayable events or typed stops without censoring evidence?
    role: outcome
    outcome: criterion_met
    checked_by: 'BasinEvent/v3 replay: 4/4 independently valid events retained; 1/4 producer-converged
      and admissible; two typed time-budget stops and one typed unsettled cell-cycle stop; 16,341/16,342
      fixed-point evaluations settled'
  verdict:
    decision: baseline
    primary_criterion: complete independently replayable event outcome for every fixed seed
    reason: The complete block retains and replays without a launch-path failure. Three typed stops
      make the cell unsuitable for basin-frequency or completeness claims under D-126, and endpoint
      keys remain observations rather than components.
    commit: 69c6008
---
# exp-029 — the `n = 8` event-validation cell is complete

BC-006 tests the upper edge of H-021’s declared small-n classifier range without
changing the instrument, seeds, per-seed budget, validity screen, blockers, or replay
contract. Every attempted seed became one replayable event, admissible or blocked.

All four endpoints independently validate.
Seed 0 converges at side `3.000000000000004` and is admissible.
Seed 1 stops at side `3.001495814083` after one of 16,342 fixed-point evaluations
reports an adjacent-objective cell cycle; the event retains both
`producer_not_converged` and `unsettled_fixed_point_evaluation`. Seeds 2 and 3 hit the
time budget at sides `3.493924749807` and `3.248875584058`.

The four quenches retain 38.004 seconds of wall time.
Across five repeated four-event batches, the median independent screen costs 0.000684
seconds and the median canonical key computation costs 0.004956 seconds.
Full semantic replay costs 0.007029 seconds in the already-started process; the separate
frozen CLI replay costs 0.713 seconds including startup.
Canonicalization is about 0.013% of retained quench wall at n=8, so it is not yet the
loop bottleneck.

These timings diagnose the loop; they do not change the event verdict.
The three typed stops make this cell too censored for landscape statistics.
D-126 continues to prohibit basin-frequency inference from wall-clock-censored starts,
and endpoint descriptors are not connected components.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
