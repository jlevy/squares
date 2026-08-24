---
title: exp-019 — replayable n=4 basin stopping events
softschema:
  contract: packing.squares:Experiment/v1
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-019
  series: series-000
  title: The first n=4 full-pose event block remains promotion-blocked
  date: '2026-08-24'
  hypotheses: [H-021]
  tier: exploratory
  known_defects: [D-165]
  subject:
    label: uniform independent starts followed by the Python bracket quench
    engine: basin_census.py BasinEvent/v2 and sqpack quench
    engine_commit: ee3acc1
    precision: f64_screen
    host_system: macOS arm64, Apple M1 Pro
    selftest_passed: true
  instance: {axis: n, point: 4, role: positive_control}
  method:
    candidate: four independently addressable uniform starts with full-pose retention
    runs_per_condition: 4
    interleaved: false
    operator: openai-codex
    commit: 16829c9
    dirty: false
    entry_point: explorations/packing/tools/basin_census.py
    command: >-
      timeout 60 uv run --frozen --quiet python tools/basin_census.py run --n 4
      --seeds 0-3 --time-budget 10 --output
      campaign/series/series-000-smoke-and-calibration/results/exp-019-h-021-n4-basin-events.jsonl
    budget: four seeds; 10 seconds per quench; 60-second process cap; stop on replay failure
    record: campaign/series/series-000-smoke-and-calibration/results/exp-019-h-021-n4-basin-events.jsonl
  effort:
    timebox: 60s
    wall_seconds: 13.321588165941648
    agent_minutes: 5
    stopped_by: dependency
  results:
  - shape: determination
    question: >-
      Does the current quench produce scientifically admissible terminal events for all
      four n=4 positive-control starts?
    role: outcome
    outcome: invalid
    checked_by: >-
      BasinEvent/v2 replay: 4/4 poses independently valid, 2/4 producer-converged, 0/4
      scientifically admissible because D-165 leaves initial probe failures unaccounted
  verdict:
    decision: blocked
    primary_criterion: scientifically admissible terminal-event fraction
    reason: >-
      The block retains two exact side-2 endpoints and two explicit cell-cycle stops,
      but D-165 makes all four ineligible for terminal-component classification.
    commit: 16829c9
---
# exp-019 — the first bounded `n=4` event block

The four deterministic starts produced four independently valid, replayable poses in
13.32 seconds of measured quench wall time.
Two runs carried the producer’s convergence flag and reached side 2, the proved optimum.
The other two stopped on explicit fixed-cell cycles at sides 2.038794768854 and
2.209948126046.

The archive contains three geometric keys and three contact keys.
Exact classification already proves that the optimal `n=4` quotient is one point; the
two optimum descriptors agree.
The two nonoptimal stopping events are examples for quench diagnosis, not evidence of
two additional terminal components.

As in exp-018, all four events are scientifically promotion-blocked by D-165. Their
poses, reasons, validity screens, and timings are durable, while H-021’s denominator
remains undefined.

Per-seed wall times range from 1.63 to 4.45 seconds.
Moving from `n=3` to `n=4` increased this four-seed block from 10.02 to 13.32 seconds,
still far below the validity work that blocks a larger campaign.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
