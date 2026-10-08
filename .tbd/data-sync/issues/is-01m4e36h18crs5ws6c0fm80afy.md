---
type: is
id: is-01m4e36h18crs5ws6c0fm80afy
title: Review and validate the atlas site cleanups
kind: task
status: in_progress
priority: 2
version: 5
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m4e35s7r1e65r1qmpz250h0p
hold: null
hold_until: null
created_at: 2026-10-08T15:48:04.263Z
updated_at: 2026-10-08T21:42:40.408Z
started_at: 2026-10-08T15:49:07.449Z
---
Review source changes and exported atlas, run focused checks and the change-reachable gate, then commit/push a focused PR and confirm CI. Keep the site cleanup epic open for further requests.

## Notes

Final dated exports, receipt checks and independent product review passed before the latest design requests. A broader pre-push run was interrupted on external storage pressure after 90 non-test checks passed; it also found missing Pages inputs (fixed), inherited pytest cache_dir configuration (corrected environment; all four probes now pass), and a genuine portable snapshot byte-cap breach due to retained rigidity metadata. Latest margin, grid-label and swatch-label refinements are in progress. Finish snapshot-budget disposition, regenerate and visually review exports, run the settled pre-push gate, then open/attach a draft PR with completed and in-progress context and require hosted CI plus complete checkpoint at the exact head.
