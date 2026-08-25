---
type: is
id: is-01m0vwd8ej4f7j45jk54mqmtxx
title: Make trajectory rendering honor or reject rotation and container changes
kind: bug
status: closed
priority: 2
version: 3
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-24-deterministic-svg-rendering-toolkit.md
labels:
  - packing
  - validity
  - not-session-010
dependencies: []
parent_id: is-01m0tzzrpy2hcdcjs6ncbx7b0d
created_at: 2026-08-25T07:15:59.570Z
updated_at: 2026-08-25T07:24:42.553Z
closed_at: 2026-08-25T07:24:42.552Z
close_reason: Trajectory rendering now validates translation-only, fixed-container frames and rejects rotation, shape-offset, and container changes with controls.
resolution: null
duplicate_of: null
---
PR 25 advertises general trajectory animation with rotation and union viewport, but the implementation animates translations of final-frame polygons and derives layout only from the final frame. Implement the contract or explicitly reject trajectories with angle/container changes; add controls. Found during pre-session-010 upstream review.
