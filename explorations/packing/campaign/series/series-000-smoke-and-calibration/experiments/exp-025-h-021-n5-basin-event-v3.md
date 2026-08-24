---
title: exp-025 — four-seed n=5 BasinEvent/v3 tool validation
softschema:
  contract: packing.squares:Experiment/v1
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-025
  series: series-000
  title: Test complete BasinEvent/v3 receipts at the first non-grid proved case
  date: '2026-08-24'
  hypotheses: [H-021]
  tier: exploratory
  subject:
    label: uniform independent starts followed by the audited Python bracket quench
    engine: basin_census.py BasinEvent/v3 and sqpack quench
    engine_commit: 5ab8dab
    precision: f64_screen
    host_system: macOS arm64, Apple M1 Pro
    selftest_passed: true
  instance: {axis: n, point: 5, role: positive_control}
  method:
    candidate: four fixed independently addressable starts under the unchanged v3 regime
    runs_per_condition: 4
    interleaved: false
    operator: openai-codex
    commit: 5ab8dab
    dirty: false
    entry_point: explorations/packing/tools/basin_census.py
    command: >-
      timeout 60 uv run --frozen --quiet python tools/basin_census.py run --n 5
      --seeds 0-3 --time-budget 10 --output
      campaign/series/series-000-smoke-and-calibration/results/exp-025-h-021-n5-basin-event-v3.jsonl
    budget: four seeds; 10 seconds per quench; 60-second process cap; retain every stop
    record: campaign/series/series-000-smoke-and-calibration/results/exp-025-h-021-n5-basin-event-v3.jsonl
  effort:
    timebox: 30m result slice; 60s measurement cap
    wall_seconds: 14.472714583040215
    agent_minutes: 5
    stopped_by: criterion
  results:
  - shape: determination
    question: >-
      Under the unchanged v3 regime, do all four n=5 starts retain independently valid,
      balanced events or a typed stop without censoring any fixed-point evaluation?
    role: outcome
    outcome: criterion_met
    checked_by: >-
      BasinEvent/v3 replay: 4/4 producer-converged, independently valid, admissible,
      and balanced; 14,219/14,219 fixed-point evaluations settled
  verdict:
    decision: baseline
    primary_criterion: complete independently replayable event outcome for every fixed seed
    reason: >-
      All four events replay as admissible and retain complete fixed-point accounting.
      This validates the n=5 event path; reaching the proved optimum was not required,
      and no endpoint key is promoted to a component.
    commit: 5ab8dab
---
# exp-025 — the `n = 5` event-validation cell is complete

BC-003 moves one size beyond the exact `n=3,4` event controls without changing the
instrument, seeds, per-seed budget, or acceptance screen.
The question is whether the event stack retains a complete, independently valid and
replayable account for every start at the first non-grid proved case.

The criterion is event-level only.
A valid nonoptimal endpoint is a successful tool observation, while any unsettled
fixed-point evaluation is a retained blocker and opens a defect before the campaign
scales further. All four seeds converged and independently validate.
Their receipts account for 14,219 fixed-point evaluations, all settled and none
unsettled, in 14.47 seconds of recorded quench wall time.
Seeds 0 and 1 end at side `2.974873734153` with one shared descriptor; seeds 2 and 3 end
at side `2.828427124746` with distinct descriptors.

Those are three observed event descriptors at two side values, not three terminal
components. Repeated or distinct sides, keys, and contact descriptors do not establish
connected-component identity, path separation, basin measure, or census saturation.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
