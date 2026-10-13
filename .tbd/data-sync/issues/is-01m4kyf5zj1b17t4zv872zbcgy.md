---
type: is
id: is-01m4kyf5zj1b17t4zv872zbcgy
title: "PR #462 B2: wait for Atlas container height animations in retained probes"
kind: bug
status: closed
priority: 2
version: 3
spec_path: docs/project/specs/active/plan-2026-10-08-site-layout-and-navigation.md
delegate: ci_timing_stabilization
labels: []
dependencies: []
parent_id: is-01m4ky07tt9a0s334a3cvzyfb3
hold: null
hold_until: null
created_at: 2026-10-10T22:20:51.568Z
updated_at: 2026-10-12T23:39:33.102Z
started_at: 2026-10-10T22:21:30.184Z
closed_at: 2026-10-12T23:39:33.102Z
close_reason: "Delivered in PR #462 (merged 2026-10-11): measure_atlas_views move.js and settled.js wait for .site-atlas-cells container animations as well as cells (774d2dbb4)."
resolution: null
duplicate_of: null
---
Performance Review B2: packing/devtools/probes/measure_atlas_views/move.js and settled.js only select site-atlas-cell animations, so new site-atlas-cells height-only moves can finish sampling early. Wait for container plus cell animations; preserve moved tile counts. Review artifact pending from atlas_performance_review.
