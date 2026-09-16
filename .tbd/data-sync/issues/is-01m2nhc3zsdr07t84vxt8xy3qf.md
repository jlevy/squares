---
type: is
id: is-01m2nhc3zsdr07t84vxt8xy3qf
title: Stabilize Animate physical trajectories and enforce frame-continuity budgets
kind: bug
status: in_progress
priority: 1
version: 4
spec_path: docs/project/specs/active/plan-2026-09-11-workbench-from-spike-to-product.md
delegate: codex@spud10
labels:
  - workbench
  - animation
dependencies: []
parent_id: is-01m2m2zmky0p8gw5m4zctfnfex
hold: null
hold_until: null
created_at: 2026-09-16T16:39:04.951Z
updated_at: 2026-09-16T18:43:10.220Z
started_at: 2026-09-16T16:49:14.497Z
---
Current main a4f801e8 still runs Animate styles B/C with one semi-implicit Euler step per stored frame. Pack calls forceLawSubsteps, but buildTrajectory does not. On the current corpus at 16→17 with the rigid preset and default anneal, the current path reaches 0.3699 square widths per stored step, 0.7399 second difference, 945 direction reversals, and 0.6484 penetration; using the helper-required two finer steps reduces those to 0.1617, 0.0754, 0 reversals, and 0.0558. At 89→90 the current path has 7,832 reversals; two finer steps reduce that to 3. The 0.3699 displacement is maxSpeed × timestep and 0.7399 is a cap-to-cap reversal, proving the teleporting is solver ringing plus the clamp, not missing renderer interpolation.

Implement the immediate stable spring path in Animate: derive sufficient substeps for every active force law, integrate within each stored interval while preserving stored-frame count, deterministic seeking, and base playback timing; tune damping/clamps if necessary to meet think-4uu3's motion targets. Commit the measurement as a maintained probe and gate rigid/default/sticky paths on maximum displacement, reversal/jerk, penetration, deterministic replay, and trajectory cost, including n=17 and a crowded case such as n=90. The existing tests that only unit-test forceLawSubsteps are insufficient. The durable projection/constraint solution remains think-r2qd.

## Notes

Engine commit 9cca493c adds adaptive Animate integration, raw/corrected traces, monotonic snap landing, integration receipts/warnings, deterministic headless kinetics, and safe tween default. The exact frozen 48-cell matrix on that commit remains outside physical continuity budgets: examples include Physics n=17 balanced reversal 0.03899 (>0.03), Physics n=90 balanced max step 0.20534 (>0.1), and Bodies n=90 balanced max step 0.23095. Keep open. Next experiment should add a named Bodies member/rotational response normalization or equivalent control, then rerun the frozen matrix; do not hide produced motion with renderer smoothing.
