---
type: is
id: is-01m4e36h18crs5ws6c0fm80afy
title: Review and validate the atlas site cleanups
kind: task
status: in_progress
priority: 2
version: 10
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m4e35s7r1e65r1qmpz250h0p
hold: null
hold_until: null
created_at: 2026-10-08T15:48:04.263Z
updated_at: 2026-10-08T23:21:28.165Z
started_at: 2026-10-08T15:49:07.449Z
---
Review source changes and exported atlas, run focused checks and the change-reachable gate, then commit/push a focused PR and confirm CI. Keep the site cleanup epic open for further requests.

## Notes

Latest full records tier passed all 47 steps in 66.74 seconds; full Ruff/BasedPyright/browser static floors and 67 mandatory Chromium checks pass. n211 records and actual narrowed324PDF independently reviewed clear; both export families pass receipts at v0.5.0-d32a82. Scoped preview generators and current asset/alias/n211 checks pass. Final100PDF visual inspection found legacy lower-only recency suppressing red n11O; minimal shared-flags fix delegated in think-4yfk, Grid geometry unchanged. Broad pre-push validation is paused pending sufficient external scratch space (about 250 MiB free; user asked to free 1 GiB). Full-context PR draft passes description contract but is not published; commit/push and required/complete hosted CI follow the final gate.
