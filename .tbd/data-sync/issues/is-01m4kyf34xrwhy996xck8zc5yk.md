---
type: is
id: is-01m4kyf34xrwhy996xck8zc5yk
title: "PR #462 B1: separate shared-runner timing advisories from rendering gates"
kind: bug
status: in_progress
priority: 1
version: 2
spec_path: docs/project/specs/active/plan-2026-10-08-site-layout-and-navigation.md
delegate: ci_timing_stabilization
labels: []
dependencies: []
parent_id: is-01m4ky07tt9a0s334a3cvzyfb3
hold: null
hold_until: null
created_at: 2026-10-10T22:20:48.668Z
updated_at: 2026-10-10T22:21:24.457Z
started_at: 2026-10-10T22:21:24.456Z
---
Performance Review B1, High: native overview rendering repeatedly exceeded the unchanged 300ms longest task threshold at one head (310/307/302ms), attributed to native initial frames without script work before Grid/fonts; shared runner absolute one-sample timings lack an attributable noise envelope. Add explicit report-only timing for ordinary shared CI, keep default enforcement and CLS/visibility/resource/trace restyle guards blocking, preserve thresholds and measurements. Review artifact pending from atlas_performance_review.
