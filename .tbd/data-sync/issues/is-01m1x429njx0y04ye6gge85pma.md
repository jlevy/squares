---
type: is
id: is-01m1x429njx0y04ye6gge85pma
title: "PR106 R4: investigate sweep timing baseline rejection at 54 seconds"
kind: bug
status: open
priority: 2
version: 1
labels: []
dependencies: []
parent_id: is-01m1x3eetb4hcjncmd2y7xqsfa
created_at: 2026-09-07T05:04:45.227Z
updated_at: 2026-09-07T05:04:45.227Z
---
PR106 commit 4cf85d90, CI run 34085213884 sweeps: all four checks passed, but 54.00s vs 107.05s baseline failed stale_ratio 0.6. Reviewing prior calibration and rerunning unchanged failed job before deciding whether a baseline correction is justified.
