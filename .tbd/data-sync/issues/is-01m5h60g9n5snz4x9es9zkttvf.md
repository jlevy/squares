---
type: is
id: is-01m5h60g9n5snz4x9es9zkttvf
title: "PR #720 A2: check passes an empty all-pairs sample receipt"
kind: bug
status: closed
priority: 2
version: 3
delegate: c-lane-pr-b
labels: []
dependencies: []
parent_id: is-01m5h60etmp9mafa8j0y40ey2h
hold: null
hold_until: null
created_at: 2026-10-22T06:50:37.748Z
updated_at: 2026-10-22T07:48:48.966Z
started_at: 2026-10-22T06:50:48.469Z
closed_at: 2026-10-22T07:48:48.965Z
close_reason: "fixed in 728dc8833: Release.sampled and sample_problems refuse an all-pairs sample that is not the declared counts, an empty one included; test_an_empty_or_disagreeing_all_pairs_sample_is_refused."
resolution: null
duplicate_of: null
---
Low. packing/devtools/beyond_horizon_replay.py:866-881 (_cross_check_problems) objects only to disagreeing sample rows; a receipt with rows [] passes though each README states an all-pairs agreement at a named count. Review: https://github.com/jlevy/squares/pull/720#issuecomment-6334629965 (PR #720, review A, round 1).
