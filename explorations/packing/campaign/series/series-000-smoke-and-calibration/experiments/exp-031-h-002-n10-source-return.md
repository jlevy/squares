---
title: exp-031 — source-bound n=10 known-answer return
softschema:
  contract: packing.squares:Experiment/v1
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-031
  series: series-000
  title: Test four source-bound returns to the proved n=10 side
  date: '2026-08-24'
  hypotheses: [H-002]
  tier: exploratory
  known_defects: [D-126]
  subject:
    label: deterministic perturbations of the published Göbel n=10 packing
    engine: basin_census.py BasinEvent/v3 and sqpack quench
    engine_commit: dab797c
    precision: f64_screen
    host_system: macOS arm64, Apple M1 Pro
    selftest_passed: true
  instance: {axis: n, point: 10, role: positive_control}
  method:
    candidate: four fixed perturbations of source fixture gobel10-svg-v1 at scale 1e-4
    runs_per_condition: 4
    interleaved: false
    operator: openai-codex
    commit: dab797c
    dirty: false
    entry_point: explorations/packing/tools/basin_census.py
    command: >-
      timeout 90 uv run --frozen --quiet python tools/basin_census.py run --n 10
      --seeds 0-3 --time-budget 15 --start-source gobel10-svg-v1
      --perturbation-scale 1e-4 --output
      campaign/series/series-000-smoke-and-calibration/results/exp-031-h-002-n10-source-return.jsonl
    budget: four seeds; 15 seconds per quench; 90-second process cap; retain every stop
    record: campaign/series/series-000-smoke-and-calibration/results/exp-031-h-002-n10-source-return.jsonl
  lease: {expires: '2026-08-24T19:21:00Z', host: local-m1-pro}
  results:
  - shape: determination
    question: >-
      Do all four declared source perturbations converge to independently valid n=10
      endpoints within 1e-12 of the proved side, with complete balanced receipts?
    role: outcome
    outcome: invalid
    checked_by: pending BasinEvent/v3 semantic replay and analytic-side comparison
  verdict:
    decision: in-progress
    primary_criterion: >-
      Four of four retained events are producer-converged, scientifically admissible,
      independently valid, fully accounted, and within 1e-12 of 3 + sqrt(2)/2.
    reason: >-
      Preregistered before the four-event measurement. A fully retained typed stop is a
      criterion miss even if its endpoint reaches the proved side; an outer timeout or
      missing event invalidates the round rather than censoring the failed seed.
---
# exp-031 — preregistered `n = 10` source-return control

BC-008 is a known-answer tool control, not a landscape sample.
Each start is a deterministic `1e-4` perturbation of the full Göbel pose reconstructed
from Kingbird’s primary SVG and bound in the event by source URL and SHA-256. The
proposer, quench, independent screen, event contract, and `1e-12` side criterion are
frozen before these four outcomes are observed.

The verdict is intentionally stricter than “the endpoint has the right side.”
Every seed must also report producer convergence, balanced fixed-point accounting,
independent validity, and semantic replay.
A valid optimal-side event stopped by its local budget is useful negative evidence but
misses the control. If the outer 90-second process cap prevents all four events from
being retained, the round is invalid and resumes only from the missing seeds under a new
preregistration.

This round does not reopen H-002’s refuted universal claim.
It tests the narrower local known-answer behavior that the quench must reproduce before
the campaign trusts more distant starts.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
