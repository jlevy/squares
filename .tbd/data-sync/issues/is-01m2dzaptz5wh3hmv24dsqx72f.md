---
type: is
id: is-01m2dzaptz5wh3hmv24dsqx72f
title: "Coordinator: bound disjoint phase durations by worker lifetime"
kind: bug
status: open
priority: 1
version: 2
spec_path: docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md
labels:
  - n11
  - calibration
  - admission
dependencies: []
parent_id: is-01m2b883ztxn7qazs98bndea6b
hold: blocked
hold_until: null
created_at: 2026-09-13T18:09:03.326Z
updated_at: 2026-09-13T18:13:03.248Z
---
Independent exact-head review at fc3e314 found raw_seconds 100 with worker_elapsed_seconds 1 accepted. Check each phase and the sum of guaranteed disjoint worker phases against worker lifetime and exit ordering without summing overlapping parent phases.
