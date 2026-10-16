---
type: is
id: is-01m50ydwrbd03y6ah6athxpk5n
title: "PR #627 A1: T-188/T-189/T-190 claim records frozen before #614 moved the houses (T-182 at 211, T-183 at 237)"
kind: bug
status: closed
priority: 2
version: 3
delegate: ecstatic-edison-address-627
labels: []
dependencies: []
parent_id: is-01m50yc0efcxyyh72mesjv7t15
hold: null
hold_until: null
created_at: 2026-10-15T23:30:16.971Z
updated_at: 2026-10-16T00:13:32.969Z
started_at: 2026-10-15T23:30:44.851Z
closed_at: 2026-10-16T00:13:32.969Z
close_reason: fixed in d79f526f2 (houses T-182/T-183, read_at_main 22a67ce4a, refrozen claims, margins restated); tests in 942feaa77
resolution: null
duplicate_of: null
---
High. PR #627, review A (https://github.com/jlevy/squares/pull/627#pullrequestreview-5541077630). packing/frontier/results.yaml T-188 (rationale, notes, next_rung), T-189, T-190; acquisition/report.json of couzo-verified-bounds-2026-10-14, couzo-certificates-2026-10-14, couzo-n237-2026-10-15 (houses, read_at_main c4c690a3e). Fix: houses T-182 at 211 and T-183 at 237, T-149 and T-140 into pending, read_at_main at or after d33de8b10, refreeze with check-claims --write, restate margins (T-188 9.29e-6 below T-182; T-189 and T-190 1.01e-4 below T-183).
