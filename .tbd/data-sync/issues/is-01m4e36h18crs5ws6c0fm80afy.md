---
type: is
id: is-01m4e36h18crs5ws6c0fm80afy
title: Review and validate the atlas site cleanups
kind: task
status: in_progress
priority: 2
version: 9
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m4e35s7r1e65r1qmpz250h0p
hold: null
hold_until: null
created_at: 2026-10-08T15:48:04.263Z
updated_at: 2026-10-08T23:07:14.117Z
started_at: 2026-10-08T15:49:07.449Z
---
Review source changes and exported atlas, run focused checks and the change-reachable gate, then commit/push a focused PR and confirm CI. Keep the site cleanup epic open for further requests.

## Notes

All source lanes and n211 records are frozen. Three reused subagents cover final static floors, independent record/PDF review, and preview refresh after pinned exports. Independent n211 record review is clear; figure/layout metadata refreshed. Fresh full records tier is running, followed by the data commit and one-line pin, actual PDF exports/visual review, maintained preview generators, final change-reachable pre-push validation, full-context PR, required CI and complete hosted checkpoint at the pushed head. Earlier interrupted broad run is not treated as a pass.
