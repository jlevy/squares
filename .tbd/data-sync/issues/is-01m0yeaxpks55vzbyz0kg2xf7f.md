---
type: is
id: is-01m0yeaxpks55vzbyz0kg2xf7f
title: Implement setup-only snapping and editor group behavior
kind: task
status: closed
priority: 1
version: 4
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-25-generalized-motion-lab.md
labels:
  - packing
  - visualization
  - motion-lab
dependencies:
  - type: blocks
    target: is-01m0yebd9ks8n9kjn3adq8npdv
parent_id: is-01m0yd38q3mxynbc38k3gyxt7f
created_at: 2026-08-26T07:07:46.242Z
updated_at: 2026-08-26T08:04:07.019Z
closed_at: 2026-08-26T08:04:07.008Z
close_reason: Implemented the pure setup editor reducer with deterministic SAT edge snaps, corner-to-corner vertex snaps, wall snaps, temporary group merging, group translation and centroid rotation, snapping toggle, reset, overlap/outside diagnostics, and a release function that emits only an unconstrained QuenchRequest. Edge, vertex, wall, arbitrary-angle, tie, rejection, and release tests pass; fast validation passed (158 tests).
resolution: null
duplicate_of: null
---
Build the deterministic editor state reducer and SAT-based snap candidate selection. Support individual and temporary-group translation, centroid rotation, deterministic group merging, reset, snapping toggle, overlap marking, and complete release of editor group metadata at run start. Cover edge, vertex, wall, arbitrary-angle, and tie cases test-first.
