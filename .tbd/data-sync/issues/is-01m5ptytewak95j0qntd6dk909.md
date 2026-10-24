---
type: is
id: is-01m5ptytewak95j0qntd6dk909
title: "PR #789 (merge): dedicated correctness review B of beyond_horizon_replay.claim_map_walk_sources and the declared_rows corpus exclusion"
kind: task
status: closed
priority: 1
version: 4
delegate: c-rev-789b-1024
labels: []
dependencies: []
parent_id: is-01m5khvjtdjf8q14f59bmd8c1k
hold: null
hold_until: null
created_at: 2026-10-24T11:32:54.875Z
updated_at: 2026-10-24T11:57:25.115Z
started_at: 2026-10-24T11:33:01.391Z
closed_at: 2026-10-24T11:57:25.114Z
close_reason: "Review B (correctness) posted https://github.com/jlevy/squares/pull/789#issuecomment-6383901035: approve after B1 (High, deferred to think-lyf9 blocking think-gn29) and B2 (Medium, fixed in the PR); B3-B5 Low; rows and verdicts hold."
resolution: null
duplicate_of: null
---

## Notes

2026-10-24 c-rev-789b-1024: Review B (correctness, round 1) published at https://github.com/jlevy/squares/pull/789#issuecomment-6383901035 against head 3773d6025, base f354a34f5. Verdict: approve after B1 and B2 are dispositioned (B1 may be deferred with a bead that blocks think-gn29). B1 High: the 23:38:42Z push also publishes 99 sides at 325-1024 credited to Kaggle notebook authors (87 certificates, 12 recipes), 1.46e-4 to 6.60e-2 below main e5c1c64e3; nothing walks, records or tracks them, against the watched-repository rule PR A applies to the 10 unrequested rows and think-6r5p applies at 304; 46 of them overlap 43f666c's 126 counts. B2 Medium: the corpus exclusion hides a recorded corpus count from every replay check (C8). B3-B5 Low; B6, B7 suggestions. Scratch: rev-789b/ (tools/, others-below-main-964ee2b.tsv, review-B.md). Not synced (brief).
