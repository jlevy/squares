---
type: is
id: is-01m4e36h18crs5ws6c0fm80afy
title: Review and validate the atlas site cleanups
kind: task
status: in_progress
priority: 2
version: 6
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m4e35s7r1e65r1qmpz250h0p
hold: null
hold_until: null
created_at: 2026-10-08T15:48:04.263Z
updated_at: 2026-10-08T22:15:34.574Z
started_at: 2026-10-08T15:49:07.449Z
---
Review source changes and exported atlas, run focused checks and the change-reachable gate, then commit/push a focused PR and confirm CI. Keep the site cleanup epic open for further requests.

## Notes

All requested layout, title, legend, credit, rigidity, label, bound-display and export-name changes are implemented and frozen. Final independent source and real-PDF visual review is clear, including the accessible recent-result description. Canonical exports use v0.5.0-72924f; both export families and all nine preview assets pass receipts. Mandatory Chromium: 67 passed, zero skips; all 324 case documents and 811 datasets pass declared schemas. The final pre-push gate is running with two pytest processes and bounded external scratch at the refreshed origin/main 91ca9b824; earlier interrupted runs are not passing gates. Commit/push the settled changes, open and attach a full-context draft PR, then continue PR CI and complete hosted checkpoint at the exact pushed head.
