---
type: is
id: is-01m4e36h18crs5ws6c0fm80afy
title: Review and validate the atlas site cleanups
kind: task
status: in_progress
priority: 2
version: 4
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m4e35s7r1e65r1qmpz250h0p
hold: null
hold_until: null
created_at: 2026-10-08T15:48:04.263Z
updated_at: 2026-10-08T18:51:34.991Z
started_at: 2026-10-08T15:49:07.449Z
---
Review source changes and exported atlas, run focused checks and the change-reachable gate, then commit/push a focused PR and confirm CI. Keep the site cleanup epic open for further requests.

## Notes

Source and export changes are committed through e3c5bbcd6; the final math-formatting follow-up is in flight under think-2uux. Earlier focused source/layout tests and export checks passed. The first broad pre-push run exposed local environment/import and browser bootstrap expectation failures; PYTHONPATH, nested node_modules and the outdated default-Triangle expectation were corrected, with the type floor and affected Node tests then passing. Subsequent full pre-push attempts were interrupted for user-requested font/title/text refinements, so none is recorded as a final gate. Run a fresh pre-push gate on the settled source/export commit with bounded concurrency and external scratch, then create the PR and require all PR CI plus the complete workflow_dispatch checkpoint at that exact pushed head.
