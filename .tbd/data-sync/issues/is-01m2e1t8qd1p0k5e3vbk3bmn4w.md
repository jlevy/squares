---
type: is
id: is-01m2e1t8qd1p0k5e3vbk3bmn4w
title: "R3: reject extra coordinator artifacts at run-root snapshot"
kind: bug
status: open
priority: 1
version: 1
spec_path: docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md
labels: []
dependencies: []
parent_id: is-01m2dzxxp9raxnvx21zk6mawes
created_at: 2026-09-13T18:52:30.316Z
updated_at: 2026-09-13T18:52:30.316Z
---
Exact-head verifier review at 878e18d0 found snapshot accepts an added profile-4-run.json at baseline. Define and enforce the coordinator run-root path contract before recording an immutable baseline.
