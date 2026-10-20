---
type: is
id: is-01m50ycf6fy4df9p6xnrh1xa3h
title: "PR #626 A2 (suggestion): #521 close_when still waits on two owner answers"
kind: bug
status: closed
priority: 3
version: 3
delegate: tbd-moderate-addresser-ee8en33t
labels: []
dependencies: []
parent_id: is-01m50yc6hrcb9bzwnns4yh4a7k
hold: null
hold_until: null
created_at: 2026-10-15T23:29:30.318Z
updated_at: 2026-10-15T23:41:23.840Z
started_at: 2026-10-15T23:29:47.481Z
closed_at: 2026-10-15T23:41:23.840Z
close_reason: "fixed in 836c95d36 on PR #626: #521 close_when reads 'The evidence entry is on main and the owner has decided the replayed-annotation ask.' Confirmed: check_requests gate 0, --report #521 blockers are the open result and the one queued ask."
resolution: null
duplicate_of: null
---
Suggestion. close_when (packing/campaign/result-requests.yaml:6173) reads 'the owner has answered the two asks', but one ask is now done by the reply's statement of fact. Reword to '...and the owner has decided the replayed-annotation ask'. Review: https://github.com/jlevy/squares/pull/626#pullrequestreview-5541123578
