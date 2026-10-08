---
type: is
id: is-01m4e36h18crs5ws6c0fm80afy
title: Review and validate the atlas site cleanups
kind: task
status: in_progress
priority: 2
version: 7
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m4e35s7r1e65r1qmpz250h0p
hold: null
hold_until: null
created_at: 2026-10-08T15:48:04.263Z
updated_at: 2026-10-08T22:24:56.728Z
started_at: 2026-10-08T15:49:07.449Z
---
Review source changes and exported atlas, run focused checks and the change-reachable gate, then commit/push a focused PR and confirm CI. Keep the site cleanup epic open for further requests.

## Notes

The final pre-push run was interrupted at 38 percent without observed failures to implement the latest user revision: PDF credits should contain only deduplicated canonical names, with no bracketed citations. Prior source, browser, schema, export and preview checks remain recorded as scoped evidence, not a completed final gate. Refresh the credits, their focused tests and documentation, regenerate canonical exports and preview assets, review the actual PDF, then complete the pre-push gate before committing and opening the full-context PR. Continue hosted PR CI and the complete checkpoint at the pushed head.
