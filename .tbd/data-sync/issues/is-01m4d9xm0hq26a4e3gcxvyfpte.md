---
type: is
id: is-01m4d9xm0hq26a4e3gcxvyfpte
title: "n17: reconcile the current reported #413 patterns with admitted, tail and pilot obligations"
kind: task
status: in_progress
priority: 2
version: 7
spec_path: docs/project/reviews/review-2026-10-07-n17-issue-coordination.md
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m3xkd6zmq1jqwtn628h2k7zy
hold: paused
hold_until: null
created_at: 2026-10-08T08:26:18.000Z
updated_at: 2026-10-13T00:55:33.170Z
started_at: 2026-10-08T16:08:23.148Z
---
Current #413 reconciliation retains 33 reported rows: two unmodified standing FULL, two parallel standing-node checks plus fast, eighteen fast-only and eleven computed. Existing reviewed disposition: https://github.com/jlevy/squares/issues/413#issuecomment-6065911258 . Draft #454 preserves corrections 6064272233/6064443079. Against the frozen #404 60-entry baseline, the conditional union is 2,234 orbits / 17,604 states; only row 23 reaches the hard tail (one orbit / eight states), and none matches the first eight. All 35 contributor classes including #358 remain unadmitted. The metadata join is implemented/reviewed. Remaining work: complete certificate availability/custody; original cell, frame, cap, independent closed-angle and guard joins; standing FULL replay; canonical D4 marginal admission. Row 23 is Computed with availability unknown; rows 3/4 need standing replay; row 33's huge certificate remains an ungenerated estimate. Preserve the frozen pilot order. No new admission or bound.

## Notes

October 9 handoff reconciliation: the current Description supersedes stale source/CI/224MiB approval next-action wording in historical Notes. All actual execution receipts and historical failures remain retained. Main3213 is unchanged; no source edits, target computations, CI dispatches, merges or draft promotions occurred in this pass. Status and dependency map: https://github.com/jlevy/squares/issues/405 . Original complete source handoff: https://github.com/jlevy/squares/pull/404#issuecomment-6075532731 . Supporting issue updates: https://github.com/jlevy/squares/issues/400#issuecomment-6076664631 and https://github.com/jlevy/squares/issues/445#issuecomment-6076662312 .

2026-10-13 owner decision: suspended pending Overbeck's proof that s(17) = L (#557; registered as T-153 by #560, credited by #571), which likely subsumes new s(17) research. Resumes only if the owner lifts the suspension, for example if T-153's replays and reviews find a gap or the candidate is withdrawn. Reconciliation of #413's reported n17 patterns with admission, tail and pilot obligations; new s(17) research on this project's route.
