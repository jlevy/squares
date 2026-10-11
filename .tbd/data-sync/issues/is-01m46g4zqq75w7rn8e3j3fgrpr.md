---
type: is
id: is-01m46g4zqq75w7rn8e3j3fgrpr
title: "Import wand125 #366 s(18) >= 47/10 (finer net, 43050ed) and think-4qit s(66) >= 843/100 (d73ce20): sqverify_fast reads a declared net, replay, review"
kind: task
status: closed
priority: 1
version: 6
delegate: claude-code@vm
labels:
  - result-import
dependencies: []
parent_id: is-01m46g4yac7ewc22drc7twjhy5
child_order_hints:
  - is-01m471mzy4w6jycg53h50v68zc
hold: null
hold_until: null
created_at: 2026-10-05T17:00:29.815Z
updated_at: 2026-10-06T02:41:31.338Z
started_at: 2026-10-05T17:06:29.900Z
closed_at: 2026-10-06T02:41:31.338Z
close_reason: Done in jlevy/squares#369 (merged 34e87a86b); verdict replies posted 2026-10-06
resolution: null
duplicate_of: null
---

## Notes

2026-10-05 22:00 lane B, after the replays and the review:
- n18: bundle driver full replay 17:16-21:40Z, exit 0, ALL_ANGLES_VERIFIED_AND_REPLAYED 416/416; compare (fixed for DN-1) FULL_REPLAY_MATCHES_SHIPPED. T-096 at V3/C3 (a8d2934a5); n = 18 verified lower 939/200 -> 47/10, consumers followed.
- n66: sample of 12/201 directions via mixed-replay, all REPLAYED and matching (4,628 CPU-s); sqverify-fast all 201. T-097 at V0/C1, verified stays 421/50. Complete replay is think-0fkt (15.5 CPU-h, held for budget).
- Review b40996152 (claude -p tbd-strong, byte-identical, accepted, DN-1 blocking fixed at f17e341de; DN-2, DN-4..DN-7, DN-9 fixed at 910b6b12c; DN-3 by the census commit; DN-8 for the #366 reply; DN-10 nothing to do).
- think-4qit is subsumed: its import (packet, row, audit, fetch, registration as T-097, review) is done here; the coordinator closes it.
