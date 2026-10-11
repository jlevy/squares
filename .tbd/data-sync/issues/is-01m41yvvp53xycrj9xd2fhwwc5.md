---
type: is
id: is-01m41yvvp53xycrj9xd2fhwwc5
title: "CI: the typecheck tier (basedpyright) runs at 85-104% of its 111 s ceiling; fix it by measurement"
kind: bug
status: closed
priority: 1
version: 2
labels:
  - ci
dependencies: []
created_at: 2026-10-03T22:41:27.236Z
updated_at: 2026-10-04T01:57:33.527Z
closed_at: 2026-10-04T01:57:33.527Z
close_reason: Duplicate of think-4w2g (same typecheck-tier ceiling breach on runner variance); data points moved there.
resolution: null
duplicate_of: null
---
On 2026-10-03 basedpyright alone took 93.8 s (run 37157463427, 85%) and about 105 s (run 37153454383, 95%) on passing pull-request runs, against a recorded 76.5 s and a 111 s ceiling. Two runs started at 22:32-22:35 UTC both failed the budget verdict at 114.8 s and 114.9 s with 0 type errors: #328 (AGENTS.md only, run 37158946117) and #323 (run 37158774919). So the tier fails on runner variance rather than on any change. Per OR-17 and OR-14, measure where basedpyright spends its time (per-file timing, incremental cache, or splitting the program) and bring the tier back under its ceiling with margin, or re-record the ceiling on a measurement. Do not raise it unmeasured. Siblings: think-lrs0 (checks tier) and think-t7k5 (behavioral shards).
