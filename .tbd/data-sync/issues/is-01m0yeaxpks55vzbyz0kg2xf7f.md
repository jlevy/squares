---
type: is
id: is-01m0yeaxpks55vzbyz0kg2xf7f
title: Implement setup-only snapping and editor group behavior
kind: task
status: open
priority: 1
version: 2
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
updated_at: 2026-08-26T07:08:02.214Z
---
Build the deterministic editor state reducer and SAT-based snap candidate selection. Support individual and temporary-group translation, centroid rotation, deterministic group merging, reset, snapping toggle, overlap marking, and complete release of editor group metadata at run start. Cover edge, vertex, wall, arbitrary-angle, and tie cases test-first.
