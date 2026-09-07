---
type: is
id: is-01m1x429njx0y04ye6gge85pma
title: "PR106 R4: investigate sweep timing baseline rejection at 54 seconds"
kind: bug
status: open
priority: 2
version: 2
labels: []
dependencies: []
parent_id: is-01m1x3eetb4hcjncmd2y7xqsfa
created_at: 2026-09-07T05:04:45.227Z
updated_at: 2026-09-07T05:09:42.123Z
---
PR106 commit 4cf85d90. CI run 34085213884 attempt1: all four sweeps passed, but wall54.00s was below stale threshold64.23s (=0.6*107.05s baseline). Unchanged failed-job rerun attempt2 passed at95.73s. No gate settings changed. This is wider hosted timing variability than the four-sample reference set. D-472 and development.md name a baseline-band follow-up think-be1s, but that ID is unavailable in current synced tracker. Preserve this observation for the next W5 calibration block; it is not a failing check on the final PR.
