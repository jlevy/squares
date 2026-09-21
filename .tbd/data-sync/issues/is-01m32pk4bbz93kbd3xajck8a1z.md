---
type: is
id: is-01m32pk4bbz93kbd3xajck8a1z
title: packing-ledger check measures deadlines against the HEAD commit's timestamp, not the wall clock
kind: bug
status: open
priority: 2
version: 1
labels: []
dependencies: []
parent_id: is-01m32dvmtc77znp14556p7c5w2
created_at: 2026-09-21T19:20:25.194Z
updated_at: 2026-09-21T19:20:25.194Z
---
Found 2026-09-21 while closing session-150.

A delegation whose deadline_at was unexpired at the moment it was authored expired the instant it was committed, because the checker judges deadlines against the HEAD commit's timestamp rather than the current time. So the act of committing a record can invalidate a clock that was honest when written.

Fixed honestly in that instance by marking the retention lane completed, since its deliverable genuinely was done -- not by moving the clock.

This is the same family as think-3umt: the ledger's clock rules are load-bearing and their reference point is unstated. A record author cannot tell, from the rules as written, whether 'unexpired' means now or at commit time, and the two differ by exactly the time it takes to finish writing the record.
