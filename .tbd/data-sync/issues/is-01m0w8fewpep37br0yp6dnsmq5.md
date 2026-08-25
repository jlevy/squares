---
type: is
id: is-01m0w8fewpep37br0yp6dnsmq5
title: New defect totals left synopsis controls and open-defect inventory stale
kind: bug
status: closed
priority: 2
version: 2
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-23-overnight-cartography-run.md
delegate: codex-root
labels: []
dependencies: []
parent_id: is-01m0vr7g27g67p699aepcdksxd
created_at: 2026-08-25T10:46:54.601Z
updated_at: 2026-08-25T10:52:13.481Z
closed_at: 2026-08-25T10:52:13.481Z
close_reason: Fixed and regression-checked in pushed checkpoint a9330d6; the 99.08-second normal gate passes all 31 steps and 62 mutation controls.
resolution: null
duplicate_of: null
---
After recording D-275 through D-280, the complete gate found three record drifts: controls.yaml still targeted old defect/gate aggregates, SYNOPSIS omitted the current 93 no-regression count, and contained D-280 was absent from the open-defect inventory. Reconcile exact generated facts and rerun focused controls before the replacement gate.
