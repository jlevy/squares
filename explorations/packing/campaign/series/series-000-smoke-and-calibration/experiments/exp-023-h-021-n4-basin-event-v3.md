---
title: exp-023 — four-seed n=4 BasinEvent/v3 calibration
softschema:
  contract: packing.squares:Experiment/v2
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-023
  series: series-000
  title: Three of four n=4 starts are admissible and one fails closed
  date: '2026-08-24'
  hypotheses:
  - H-021
  tier: exploratory
  known_defects:
  - D-171
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
    point: 4
    role: positive_control
  method:
    candidate: four independently addressable starts with complete receipts
    runs_per_condition: 4
    interleaved: false
    operator: openai-codex
    commit: 8f20908
    dirty: false
    entry_point: explorations/packing/tools/basin_census.py
    command: timeout 60 uv run --frozen --quiet python tools/basin_census.py run --n 4 --seeds 0-3
      --time-budget 10 --output campaign/series/series-000-smoke-and-calibration/results/exp-023-h-021-n4-basin-event-v3.jsonl
    budget: four seeds; 10 seconds per quench; 60-second process cap; retain every stop
    record: campaign/series/series-000-smoke-and-calibration/results/exp-023-h-021-n4-basin-event-v3.jsonl
  effort:
    timebox: 30m result slice; 60s measurement cap
    wall_seconds: 12.505728166084737
    agent_minutes: 8
    stopped_by: criterion
  results:
  - shape: determination
    question: Do all four n=4 positive-control starts produce independently valid, admissible BasinEvent/v3
      terminal observations?
    role: outcome
    outcome: criterion_missed
    checked_by: 'BasinEvent/v3 replay: 4/4 valid, 3/4 producer-converged and admissible, with one
      typed unsettled fixed-point evaluation retained for seed 3'
  verdict:
    decision: baseline
    primary_criterion: admissible terminal-event fraction at the n=4 positive control
    reason: Three events reach the proved side and are admissible. Seed 3 fails closed on one post-check
      rejection after the bounded repair, so the cell is 3/4 admissible and cannot support a complete-map
      claim.
    commit: 8f20908
---
# exp-023 — the `n = 4` event calibration fails closed once

Seeds 0, 1, and 2 reach side 2, pass the independent geometry screen, and retain only
settled fixed-point evaluations.
Seed 3 stops at side `2.0218239546404626` when one evaluation returns a successful HiGHS
solution whose pair row 16 residual is still `4.209e-10` after the single bounded D-164
repair. The event retains 3,865 settled evaluations, one unsettled evaluation, both
explicit promotion blockers, and the independently valid stopping pose.

The four events cost 12.51 seconds and replay without ambiguity.
The result improves the historical v2 producer-convergence count from 2/4 to 3/4, but
the current positive-control cell remains incomplete.
D-171 owns diagnosis of the exact failing evaluation; this round does not weaken the
screen, add retries after seeing the result, or infer a component from an endpoint key.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
