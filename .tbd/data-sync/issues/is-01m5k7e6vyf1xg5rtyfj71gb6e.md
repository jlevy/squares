---
type: is
id: is-01m5k7e6vyf1xg5rtyfj71gb6e
title: Reconcile math probe imports after upstream navigation integration
kind: bug
status: in_progress
priority: 1
version: 2
spec_path: docs/project/specs/active/plan-2026-10-22-site-navigation.md
delegate: navigation-root
labels: []
dependencies: []
parent_id: is-01m5k19kqedc9vp30sk9wm3s5f
hold: null
hold_until: null
created_at: 2026-10-23T01:54:04.282Z
updated_at: 2026-10-23T01:54:19.083Z
started_at: 2026-10-23T01:54:19.081Z
---
The upstream attribute-order regression imports _MEASURE_MATH while this branch exposes MEASURE_MATH as the applied probe. Preserve the upstream regression and update its import/use; run the focused regression and typecheck.
