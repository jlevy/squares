---
type: is
id: is-01m50ye4qbkg6xbdvbnxg1hand
title: "PR #616 A1 (https://github.com/jlevy/squares/pull/616#issuecomment-6189327252): rows recorded as current are beaten by the 4e4c8ce index and nothing a reader sees says so"
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
created_at: 2026-10-15T23:30:25.131Z
updated_at: 2026-10-16T00:13:37.507Z
started_at: 2026-10-15T23:30:50.623Z
closed_at: 2026-10-16T00:13:37.506Z
close_reason: "fixed in d79f526f2: notes and source notes say the 4e4c8ce index beats 238 and 7 current rows; PR body corrected"
resolution: null
duplicate_of: null
---
Blocking. #616 review A (https://github.com/jlevy/squares/pull/616#issuecomment-6189327252), carried by PR #627 (review B, B1). results.yaml T-188 notes (beyond-horizon paragraph), T-189 notes (supersedes the row it beats), T-190 notes (rewrites 341 rows), source-coverage.yaml notes of couzo-verified-bounds-2026-10-14 and couzo-certificates-2026-10-14, the PR body. Fix: one sentence each that 4e4c8ce's index is smaller at those rows; correct the PR body; note in think-yfoo.
