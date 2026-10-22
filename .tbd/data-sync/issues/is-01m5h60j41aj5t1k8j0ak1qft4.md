---
type: is
id: is-01m5h60j41aj5t1k8j0ak1qft4
title: "PR #720 A4: seed_credit and _jobs bypass read_retained_bytes; the test asserts .is_file()"
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
created_at: 2026-10-22T06:50:39.617Z
updated_at: 2026-10-22T07:48:50.094Z
started_at: 2026-10-22T06:50:49.434Z
closed_at: 2026-10-22T07:48:50.093Z
close_reason: "fixed in 728dc8833: seed_credit reads through read_retained_text, _jobs orders by count without stat(), the table test asserts presence through read_retained_bytes."
resolution: null
duplicate_of: null
---
Low. packing/devtools/beyond_horizon_replay.py:373-376, 437-441; packing/tests/test_beyond_horizon_replay.py:85. Review: https://github.com/jlevy/squares/pull/720#issuecomment-6334629965 (PR #720, review A, round 1).
