---
title: exp-018 — replayable n=3 basin stopping events
softschema:
  contract: packing.squares:Experiment/v2
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-018
  series: series-000
  title: The first n=3 full-pose event block remains promotion-blocked
  date: '2026-08-24'
  hypotheses:
  - H-021
  tier: exploratory
  known_defects:
  - D-165
  subject:
    label: uniform independent starts followed by the Python bracket quench
    engine: basin_census.py BasinEvent/v2 and sqpack quench
    engine_commit: ee3acc1
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
    candidate: four independently addressable uniform starts with full-pose retention
    runs_per_condition: 4
    interleaved: false
    operator: openai-codex
    commit: ee3acc1
    dirty: false
    entry_point: explorations/packing/tools/basin_census.py
    command: timeout 60 uv run --frozen --quiet python tools/basin_census.py run --n 3 --seeds 0-3
      --time-budget 10 --output campaign/series/series-000-smoke-and-calibration/results/exp-018-h-021-n3-basin-events.jsonl
    budget: four seeds; 10 seconds per quench; 60-second process cap; stop on replay failure
    record: campaign/series/series-000-smoke-and-calibration/results/exp-018-h-021-n3-basin-events.jsonl
  effort:
    timebox: 60s
    wall_seconds: 10.024809541995637
    agent_minutes: 12
    stopped_by: dependency
  results:
  - shape: determination
    question: Does the current quench produce scientifically admissible terminal events for all four
      n=3 positive-control starts?
    role: outcome
    outcome: invalid
    checked_by: 'BasinEvent/v2 replay: 4/4 poses independently valid, 3/4 producer-converged, 0/4
      scientifically admissible because D-165 leaves initial probe failures unaccounted'
  verdict:
    decision: blocked
    primary_criterion: scientifically admissible terminal-event fraction
    reason: The block retains useful stopping evidence, including two exact side-2 endpoints, but
      D-165 forces all four events to remain ineligible for component classification.
    commit: ee3acc1
---
# exp-018 — the first bounded `n=3` event block

The four deterministic starts produced four independently valid, replayable poses in
10.02 seconds of measured quench wall time.
Three runs carried the producer’s convergence flag; two of those reached side 2, the
proved optimum. The fourth run stopped on an explicit fixed-cell cycle at side
2.020073763260. The remaining producer-converged run ended at the nonoptimal side
2.362735797795.

The raw archive contains three geometric keys and three contact keys.
Those are descriptors, not component counts.
The exact topology says the two side-2 rows belong to the known optimal moduli space,
while the present event contract deliberately refuses to infer connectivity from either
hash.

No event is scientifically admissible under the current quench.
D-165 proves that an initial failed cell solve can still become a dummy angle objective,
so BasinEvent/v2 records `scientifically_admissible_terminal_event: false` and names
D-165 as the blocker.
This round therefore calibrates cost and preserves examples; it does not advance H-021’s
classification denominator.

Measured per-seed wall times range from 2.27 to 3.08 seconds.
At this size, event generation is cheap enough that validity—not throughput—is the
binding constraint.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
