---
type: is
id: is-01m4e36h18crs5ws6c0fm80afy
title: Review and validate the atlas site cleanups
kind: task
status: in_progress
priority: 2
version: 15
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m4e35s7r1e65r1qmpz250h0p
hold: blocked
hold_until: null
created_at: 2026-10-08T15:48:04.263Z
updated_at: 2026-10-09T01:53:45.105Z
started_at: 2026-10-08T15:49:07.449Z
---
Review source changes and exported atlas, run focused checks and the change-reachable gate, then commit/push a focused PR and confirm CI. Keep the site cleanup epic open for further requests.

## Notes

Reviewed source and freshly regenerated composite exports are committed at clean checkpoint 7900aafad on codex/atlas-triangle-default in the isolated atlas-cleanups worktree. Data commit 9695fbdd4b6f4f2216c82b3d79aedc60f118a9d2 and isolated pin commit 0a79d624 stamp both export families v0.5.0-9695fb with October 8, 2026 data. Current website passes 82 mandatory Chromium checks with zero skips and 17 focused containment checks; PDF builder passes 20 tests; n211 horizontal reflection passes 26 focused checks, exact verification and replay. All 324 frontmatter and 811 enforced datasets pass schema validation. Actual dated PDFs were independently rendered and inspected, with no clipping or collisions; retained composite and PDF byte checks are green. Fresh maintained preview has all nine canonical assets and both legacy PDF aliases byte-equal, Medium Triangle default, Grid option and current n211 motion facts. Finder is raised with the latest 324 PDF selected. Human approved the original local preview server; it is running on localhost:8799 and root HTTP headers return200, but automated browser navigation remains tool-rejected. Full current edit took524.71s with all source floors green and one failure: historical URL preservation against advanced main b810432cc, whose PR434 changes complete source/evidence for n68/n105/n292. Edit timing also exceeds its reported240s ceiling at an off-reference allocation. Records-current passed45/47 in62.54s; invalid Ruff boolean environment is now corrected, and upstream history mismatch remains. Suite-D declaration repair is independently reviewed and committed under think-pvtr; later measured performance debt stays think-t7k5. think-mcca owns complete upstream integration, awaiting explicit local-merge approval after automatic review rejected the merge under confirm-session policy. No rebase or partial-record workaround. Full push gate, push, PR and exact-head hosted CI remain pending. Full-context PR draft and unique current evidence are retained externally. Epic remains open.
