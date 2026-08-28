---
title: exp-021 — supervised n=3 BasinEvent/v3 trust-boundary calibration
softschema:
  contract: packing.squares:Experiment/v2
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-021
  series: series-000
  title: The first BasinEvent/v3 derives a scientifically admissible terminal event
  date: '2026-08-24'
  hypotheses:
  - H-021
  tier: exploratory
  subject:
    label: uniform independent start followed by the audited Python bracket quench
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
    candidate: one independently addressable start with full-pose and fixed-point receipt retention
    runs_per_condition: 1
    interleaved: false
    operator: openai-codex
    commit: 8f20908
    dirty: false
    entry_point: explorations/packing/tools/basin_census.py
    command: timeout 30 uv run --frozen --quiet python tools/basin_census.py run --n 3 --seeds 1 --time-budget
      10 --output campaign/series/series-000-smoke-and-calibration/results/exp-021-h-021-n3-basin-event-v3.jsonl
    budget: one seed; 10 seconds for the quench; 30-second process cap; stop on replay failure
    record: campaign/series/series-000-smoke-and-calibration/results/exp-021-h-021-n3-basin-event-v3.jsonl
  effort:
    timebox: 30m implementation slice; 30s measurement cap
    wall_seconds: 1.8969770000549033
    agent_minutes: 15
    stopped_by: criterion
  results:
  - shape: determination
    question: Does one supervised n=3 run retain a complete fixed-point receipt from which scientific
      event admissibility is independently derived?
    role: outcome
    outcome: criterion_met
    checked_by: BasinEvent/v3 semantic replay, independent sqpack.verify screen, balanced 2037 = 2037
      + 0 fixed-point receipt, and forged-claim rejection
  verdict:
    decision: baseline
    primary_criterion: independently replayable scientifically admissible terminal event
    reason: The retained event is producer-converged, independently valid, has all 2,037 fixed-point
      evaluations accounted for and settled, and rejects a forged all-probes-accounted flag. This
      calibrates the event trust boundary but does not decide H-021's component-classification claim.
    commit: 8f20908
---
# exp-021 — the first admissible retained basin event

The supervised `n = 3`, seed 1 run reached side `2.000000000000001` in 1.90 seconds.
Its independent geometry screen checked all three pairs and accepted the pose; the
reported side is within the declared `1e-10` screen of the independently recomputed
required side.

The producer routed every fixed-point evaluation through one audited call path.
The retained receipt contains 2,037 evaluations, all 2,037 settled and none unsettled,
with 2,328 LP solves in total.
BasinEvent/v3 derives `all_probe_evaluations_accounted_for: true`, scientific
admissibility, and the empty blocker list from those counts, convergence, and the
independent pose screen.
Changing only the retained all-probes flag to false makes semantic replay refuse the
event.

This result closes the D-165 event trust boundary.
It does not turn an endpoint key into a connected component, estimate basin mass, or
decide H-021. Those remain separate classification and sampling steps.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
