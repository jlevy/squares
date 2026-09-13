---
type: is
id: is-01m2dz5kzv8k9e1yq06017ngah
title: "F6: bind calibration phases, exits, tasks and process identities to lifetimes"
kind: bug
status: open
priority: 1
version: 5
spec_path: docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md
labels:
  - n11
  - calibration
  - admission
dependencies: []
parent_id: is-01m2b884a8xfyybgtpfr4rdwgv
child_order_hints:
  - is-01m2e19mwtk6gne1hxvwpap4bk
  - is-01m2e19ncq107301gs2q7rg8b6
  - is-01m2e19nqwvrfv91ak14mra1hj
created_at: 2026-09-13T18:06:16.570Z
updated_at: 2026-09-13T18:43:55.541Z
---
Check worker elapsed, observed exit, external lifetime, final readback, phase and task bounds, route order, and child PID distinctness; retain valid parallel and serial controls.

## Notes

Exact-head 7e4d2487 independent review accepted original F6 controls but REFUSED three further lifetime/topology classes: nested/preflight/cleanup clocks (think-txmw), raw/exact task positions against sequential phases (think-7yq0), and a two-process supervisor-child parent cycle (think-rcju). Full readback controls and source lines are in docs/project/reviews/review-2026-09-13-n11-bc329-reader-rereview.md. No positive profile.
