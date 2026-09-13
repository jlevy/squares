---
type: is
id: is-01m2cv9b743e0nphgkb8swxewf
title: "PR #157 review DOC-04: the PR cost summary omits available scoped evidence"
kind: bug
status: closed
priority: 2
version: 2
labels:
  - n11
dependencies: []
parent_id: is-01m2cv7affzce4qkz704rp2kvv
created_at: 2026-09-13T07:39:09.924Z
updated_at: 2026-09-13T18:18:51.912Z
closed_at: 2026-09-13T18:18:51.911Z
close_reason: Transferred to canonical PR157-DOC-04 think-i17o. The corrected PR body is prepared; canonical issue stays in progress until final source and validation are recorded and the body is published.
resolution: duplicate
duplicate_of: is-01m2cv670mx6yhq3q7tx37581b
---
The PR body reports 13 files and +1448/-54, but the reviewed head changes 22 files and +3482/-712. Five dedicated agent rollups report 434 assistant turns, 269 tool calls, 5 errors and 1978.818s of summed overlapping agent spans. The generated branch block is unavailable because the logs retain another branch label; the refreshed shared parent log's Sep 4-12 span cannot be allocated wholly to this PR. Fix per OR-9: refresh the final diff and separate session-clock estimates, dedicated agent observations, shared-log limits, and the unmeasured new review work.
