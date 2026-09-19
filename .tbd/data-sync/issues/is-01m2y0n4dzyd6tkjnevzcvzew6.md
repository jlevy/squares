---
type: is
id: is-01m2y0n4dzyd6tkjnevzcvzew6
title: "PR200 review R5: prevent concurrent covering-queue writers"
kind: bug
status: open
priority: 2
version: 1
labels: []
dependencies: []
parent_id: is-01m2y07hq7kkss9qh386q3h912
created_at: 2026-09-19T23:40:04.411Z
updated_at: 2026-09-19T23:40:04.411Z
---
run_covering_queue.py:218-232 checks for final run JSON but has no reservation/host lease. Two simultaneous walk_queue calls both start the same missing probe and write identical output prefixes; reproduced with a barrier-backed runner. Add atomic exclusion for queue execution and output ownership, refuse the second generator, and test concurrent starts.
