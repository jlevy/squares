---
type: is
id: is-01m4ezx2k0m0jpqgjpyaxc2zfm
title: Record the first hosted suite_d observation before intake merge
kind: bug
status: closed
priority: 1
version: 3
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m4ekeq41zfgtf5dp8r462n05
hold: null
hold_until: null
created_at: 2026-10-09T00:09:43.263Z
updated_at: 2026-10-09T01:24:05.589Z
started_at: 2026-10-09T00:09:49.470Z
closed_at: 2026-10-09T01:24:05.587Z
close_reason: "The exact first hosted suite_d observation (104.95s, run36939743802/job110628224361/head89855, original1/1/4 shape) replaced expired pending fields without changing143s or enforcement. Actual Astra M–P accepted abb budget99b39f; #434 passed exact-head Packing37864114853, Pages37864114912 and full37864151667, then merged as b810432cccf7849920dda3aad76882f191464eb5. Same accepted budget blob is published through439–460. Broad cohort/repartition calibration stays open as think-t7k5; later163.63s observation remains adverse, not replaced by the historical baseline."
resolution: null
duplicate_of: null
---
The suite_d pending measurement deadline 2026-10-08 expired at midnight UTC, leaving current intake records validation red. Use maintained read_tier_walls on an exact hosted observation at the declared jobs=1/inner_jobs=1/cpus=4 shape; record its real head/run/job/date and measured wall, retain the 143s ceiling and all selection/enforcement policy, remove only the fulfilled pending fields. Astra must review the source delta. Preserve broader think-t7k5 A/B/C cohort and repartition work as open. Land on earliest applicable intake layer, normal-merge into other owning layers, and rerun actual current-head gates.
