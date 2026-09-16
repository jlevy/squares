---
type: is
id: is-01m2nhycvy9kh5cht5e3a0dn08
title: Expose Animate kinetics as a deterministic headless trace and scoring CLI
kind: feature
status: closed
priority: 1
version: 5
spec_path: docs/project/specs/active/plan-2026-09-11-workbench-from-spike-to-product.md
delegate: codex@spud10
labels:
  - workbench
  - animation
dependencies: []
parent_id: is-01m2m2zmky0p8gw5m4zctfnfex
hold: null
hold_until: null
created_at: 2026-09-16T16:49:03.869Z
updated_at: 2026-09-16T20:40:08.752Z
started_at: 2026-09-16T16:49:14.516Z
closed_at: 2026-09-16T20:40:08.752Z
close_reason: "Completed and merged in PR #189 at merge commit 035d84c6. Exact-head hosted Packing and Pages aggregates passed; the deterministic headless kinetics CLI, shared browser/CLI settings, and bounded square-to-container delay are on main."
resolution: null
duplicate_of: null
---
The animation model must be understandable and tunable without rendering a browser. Build a committed CLI over the same trajectory generator and presets used by the workbench. It must emit machine-readable per-frame trajectories plus summary metrics for displacement, velocity, acceleration/jerk, direction reversals, penetration/overlap, contacts and neighbour gaps, endpoint error, deterministic replay, work/substeps, and runtime. Named solver, law, annealing, timing, instance, and seed inputs must map exactly to browser controls, and JSON output must be stable enough for regression tests and later search scoring. Add positive and negative controls, including a synthetic cap-to-cap ringing trace that proves the reversal guard fires. Document the metric units and use the CLI to measure at least n=17 and a crowded case such as n=90 across the shipped approaches and presets. The visual layer is a consumer, not the measurement authority.

## Notes

Implemented at engine commit 9cca493c: shared deterministic Node CLI, raw/corrected/presented trajectories, displacement/reversal/geometry/endpoint/work/runtime metrics, replay guards, negative controls, browser/CLI configuration parity, and pre-allocation frame plus 250,000 aggregate pose-sample bounds. Local package check passed 177 tests and Chromium contract passed 1,323 seeks. Close only after the PR merges green.
