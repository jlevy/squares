---
type: is
id: is-01m4ezx2k0m0jpqgjpyaxc2zfm
title: Record the first hosted suite_d observation before intake merge
kind: bug
status: in_progress
priority: 1
version: 2
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m4ekeq41zfgtf5dp8r462n05
hold: null
hold_until: null
created_at: 2026-10-09T00:09:43.263Z
updated_at: 2026-10-09T00:09:49.470Z
started_at: 2026-10-09T00:09:49.470Z
---
The suite_d pending measurement deadline 2026-10-08 expired at midnight UTC, leaving current intake records validation red. Use maintained read_tier_walls on an exact hosted observation at the declared jobs=1/inner_jobs=1/cpus=4 shape; record its real head/run/job/date and measured wall, retain the 143s ceiling and all selection/enforcement policy, remove only the fulfilled pending fields. Astra must review the source delta. Preserve broader think-t7k5 A/B/C cohort and repartition work as open. Land on earliest applicable intake layer, normal-merge into other owning layers, and rerun actual current-head gates.
