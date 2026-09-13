---
type: is
id: is-01m229c25xgrtk9hh5nd1brnxn
title: Add calibration and held-out presets within Search
kind: feature
status: open
priority: 2
version: 7
spec_path: docs/project/specs/active/plan-2026-09-11-workbench-from-spike-to-product.md
labels:
  - packing
  - workbench-roadmap
  - workbench-phase-5
dependencies:
  - type: blocks
    target: is-01m2cm04t1enrq3zreb3rjjhpd
parent_id: is-01m2b7n9tyq13n0zw4tkq4rfss
created_at: 2026-09-09T05:13:40.284Z
updated_at: 2026-09-13T05:43:49.529Z
---
Phase 5: use the shared Search scheduler for known-record parameter sweeps and a fixed tuning/held-out partition declared before the campaign starts. Record the partition in the campaign manifest and reference it from every run; replay/resume preserves it. Report both best individual arrangement and configuration-level distributions/hit rates under equal work, plus held-out scores. Acceptance: no tuning on held-out outcomes, explicit cohort labels and seed blocks, exact manifest replay, same Pack run API. No separate Calibrate tab. Coordinate older think-wffa as research-acceptance follow-up, not duplicate UI work.

## Notes

2026-09-12 plan disposition: Calibrate becomes a parameter-sweep/held-out preset within deferred Search (think-vhgz), using the same single-run API. Do not implement a fourth tab or a separate optimization loop. New source belongs in top-level packages/workbench/ after current cleanup and extraction phases.
