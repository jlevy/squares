---
type: is
id: is-01m5mpxq11dhpbe4m22msf60t5
title: "PR #748 A3: verified_lane_review_problems counts any review or read whatever its verdict or kind"
kind: bug
status: closed
priority: 2
version: 3
delegate: c-gates-1023
labels: []
dependencies: []
parent_id: is-01m5mpx469084wmghw63k1vasv
hold: null
hold_until: null
created_at: 2026-10-23T15:43:55.425Z
updated_at: 2026-10-23T16:50:17.158Z
started_at: 2026-10-23T15:44:48.867Z
closed_at: 2026-10-23T16:50:17.158Z
close_reason: "Fixed in 1165f88bd: accepting_review and informally-verified reads only; test_a_review_that_does_not_accept_the_mathematics_does_not_count. Disposition https://github.com/jlevy/squares/pull/748#issuecomment-6370073707."
resolution: null
duplicate_of: null
---
packing/devtools/check_results.py:1592, :1536. Severity Low. Review A of PR #748: https://github.com/jlevy/squares/pull/748#issuecomment-6368647934.
