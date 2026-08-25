---
title: exp-030 — one-seed n=9 BasinEvent/v3 performance validation
softschema:
  contract: packing.squares:Experiment/v2
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-030
  series: series-000
  title: Time one complete BasinEvent/v3 path at n=9
  date: '2026-08-24'
  hypotheses:
  - H-021
  tier: exploratory
  known_defects:
  - D-126
  subject:
    label: one uniform independent start followed by the audited Python bracket quench
    engine: basin_census.py BasinEvent/v3 and sqpack quench
    engine_commit: 56bf66c
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
    point: 9
    role: positive_control
  method:
    candidate: one fixed independently addressable start under the unchanged v3 regime
    runs_per_condition: 1
    interleaved: false
    operator: openai-codex
    commit: 56bf66c
    dirty: false
    entry_point: explorations/packing/tools/basin_census.py
    command: timeout 60 uv run --frozen --quiet python tools/basin_census.py run --n 9 --seeds 0 --time-budget
      20 --output campaign/series/series-000-smoke-and-calibration/results/exp-030-h-021-n9-basin-event-v3.jsonl
    budget: one seed; 20-second quench; 60-second process cap; retain every stop
    record: campaign/series/series-000-smoke-and-calibration/results/exp-030-h-021-n9-basin-event-v3.jsonl
  effort:
    timebox: 30m result slice; 60s measurement cap
    wall_seconds: 20.06198708305601
    agent_minutes: 5
    stopped_by: criterion
  results:
  - shape: determination
    question: Does one n=9 start traverse generation, quench, independent validation, keying, retention,
      and replay inside the declared performance stop?
    role: outcome
    outcome: criterion_met
    checked_by: 'BasinEvent/v3 replay: 1/1 independently valid event retained; the event is a typed
      20-second time-budget stop with 5,845/5,845 evaluations settled; complete command wall 21.36
      seconds'
  verdict:
    decision: baseline
    primary_criterion: one complete independently replayable event with attributed stage cost
    reason: The complete event path stays below the 30-second profile trigger and retains its nonconverged
      outcome without censorship. D-126 bars frequency or deterministic-work claims, and no additional
      n=9 samples are authorized by this performance cell.
    commit: 56bf66c
---
# exp-030 — the `n = 9` performance cell is complete

BC-007 asks whether the complete event path remains cheap enough to inspect before any
broader sampling at n=9. It changes only the size, the per-seed cap, and the number of
starts from exp-029. The single event is retained and semantically replayed as a valid,
non-admissible time-budget stop at side `3.151852534444`; all 5,845 fixed-point
evaluations settle.

The quench retains 20.062 seconds of wall time, and the complete frozen command takes
21.36 seconds. Across five one-event batches, the median independent screen costs
0.000174 seconds and the median canonical key costs 0.001074 seconds.
Full semantic replay costs 0.001622 seconds in the already-started process; the separate
frozen CLI costs 0.771 seconds including startup.
Keying is about 0.0054% of retained quench wall, so the cell does not trigger a profile.

This result validates the n=9 event and timing path only.
It neither samples the n=9 landscape nor tests return to the proved side-3 grid.
D-126 remains explicit, and the size ladder stops here because BC-008 requires a
source-bound n=10 seeded-pose entry point that does not yet exist.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
