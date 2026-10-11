---
type: is
id: is-01m45m6x68t479v0ssh5azqrrw
title: "Owner decision: behavioural-lane capacity for the n17 stack (5th shard or ~9% higher ceilings)"
kind: task
status: open
priority: 1
version: 1
spec_path: docs/project/reviews/review-2026-10-02-n17-bulk-exclusion-design.md
labels: []
dependencies: []
parent_id: is-01m45eykfctkcn3vxwx3dxmn7f
created_at: 2026-10-05T08:52:12.616Z
updated_at: 2026-10-05T08:52:12.616Z
---
Stack 357 fails only shard budget verdicts: #347 adds ~10% to the lane (133.9 recorded test-s; 30 files). Stack median 4-shard sum 505.5 s vs main 464 s; on slow runners ~558 s of 570 s ceilings (97.9%). 16/24 stack cohorts had a shard over ceiling vs 2/27 on main. Restoring main's suite-file-costs.json fails suite_files check (>10% unrecorded). Options: (1) 5th shard via suite_files record --shards 5 + suite-e job; (2) raise ceilings ~9% (A/D ~143, B/C ~168); (3) reduce #347's added cost. In all cases re-record from hosted cohort (#354 run 37283307487 attempts 1-2; #347 run 37280874035) — needs artifact download (think-skka). Side note: pack() tie-break puts the largest file on shard A (131 s); tie-break toward largest capacity is a main-side fix. Analysis scripts in the coordinator scratchpad (shardpredict.py etc.).
