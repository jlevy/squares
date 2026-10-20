---
type: is
id: is-01m50yctwg3f43p8cjs8xwg089
title: "PR #630 A3 (suggestion): smaller unadopted entries named on #562 but not on #564, #503, #504"
kind: bug
status: closed
priority: 3
version: 3
delegate: tbd-moderate-addresser-ee8en33t
labels: []
dependencies: []
parent_id: is-01m50ycgh45vrr9zhdqy32kexy
hold: null
hold_until: null
created_at: 2026-10-15T23:29:42.288Z
updated_at: 2026-10-15T23:41:25.042Z
started_at: 2026-10-15T23:29:47.507Z
closed_at: 2026-10-15T23:41:25.034Z
close_reason: "fixed in 0b14d0dea on PR #630: #564 notes record that the final reply names T-181 and not T-186 (1.787e-19 smaller at 302, recomputed with Fraction; not adopted) and that no reply is owed. Confirmed: check_requests gate 0, --report #564 closed and settled, records tier exit 0."
resolution: null
duplicate_of: null
---
Suggestion. #562's final reply (result-requests.yaml:7336) names smaller unadopted entries; #564 (:7403, T-186 at 302), #503 (:5340, T-174 at 207) and #504 (:5510, T-174 at 153) leave them out. A note in the #564 entry's notes saying the omission is deliberate would stop the next pass treating it as owed. Review: https://github.com/jlevy/squares/pull/630#pullrequestreview-5541123708
