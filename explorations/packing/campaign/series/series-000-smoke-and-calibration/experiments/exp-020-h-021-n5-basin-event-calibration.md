---
title: exp-020 — replayable n=5 basin stopping events
softschema:
  contract: packing.squares:Experiment/v2
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-020
  series: series-000
  title: The first n=5 full-pose event block remains promotion-blocked
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
    point: 5
    role: positive_control
  method:
    candidate: four independently addressable uniform starts with full-pose retention
    runs_per_condition: 4
    interleaved: false
    operator: openai-codex
    commit: 79910a9
    dirty: false
    entry_point: explorations/packing/tools/basin_census.py
    command: timeout 60 uv run --frozen --quiet python tools/basin_census.py run --n 5 --seeds 0-3
      --time-budget 10 --output campaign/series/series-000-smoke-and-calibration/results/exp-020-h-021-n5-basin-events.jsonl
    budget: four seeds; 10 seconds per quench; 60-second process cap; stop on replay failure
    record: campaign/series/series-000-smoke-and-calibration/results/exp-020-h-021-n5-basin-events.jsonl
  effort:
    timebox: 60s
    wall_seconds: 14.82109770795796
    agent_minutes: 5
    stopped_by: dependency
  results:
  - shape: determination
    question: Does the current quench produce scientifically admissible terminal events for all four
      n=5 positive-control starts?
    role: outcome
    outcome: invalid
    checked_by: 'BasinEvent/v2 replay: 4/4 poses independently valid and producer-converged, but 0/4
      scientifically admissible because D-165 leaves initial probes unaccounted'
  verdict:
    decision: blocked
    primary_criterion: scientifically admissible terminal-event fraction
    reason: The block retains two repeated side values and full poses, but it finds no proved optimum
      and D-165 makes all four events ineligible for component classification.
    commit: 79910a9
---
# exp-020 — the first bounded `n=5` event block

All four deterministic starts produced independently valid, replayable poses and carried
the producer’s convergence flag.
Two ended at side 2.828427124746 and two at side 2.974873734153; none reached the proved
optimum 2.707106781187. The archive contains three geometric keys and three contact
keys.

Repeated sides are not repeated components.
The side-2.8284 pair has two distinct geometric descriptors, while the side-2.9749 pair
shares one.
No connectivity test has yet decided whether a descriptor split is geometric,
combinatorial, or merely a slice through one terminal family.

All four events remain promotion-blocked by D-165. They add complete examples and timing
evidence for the n=5 identity work; they do not count basins and do not support coverage
or unseen-mass inference.

The four quenches took 14.82 seconds, with per-seed times from 2.93 to 4.90 seconds.
The cost increase from `n=4` remains modest, so a later fixed instrument can revisit
this cell cheaply. Until then, additional seeds would multiply blocked examples rather
than increase scientific coverage.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
