---
type: is
id: is-01m5ntqg8kza7vn9e3v650vndr
title: Catch up every 'Review pending' result on the profiles (T-073/T-080, T-083/T-084, T-163) and track each pending review's state in its GitHub issue (owner, 24 October)
kind: task
status: in_progress
priority: 2
version: 3
delegate: c-review-pending-1024
labels: []
dependencies: []
parent_id: is-01m5khvjtdjf8q14f59bmd8c1k
hold: null
hold_until: null
created_at: 2026-10-24T02:09:40.627Z
updated_at: 2026-10-24T02:09:50.200Z
started_at: 2026-10-24T02:09:50.200Z
---

## Notes

2026-10-24 coord-intake-1023: OWNER (in conversation, 24 October, verbatim): "can you also check all cases like this one https://squaremath.org/profiles/kevin-fang.html#records where it says Review pending. All cases like that should be caught up. Is that right? Are you merging them and fixing them? I believe all his work should be quick to validate, so I don't see why we should have entries like that on the profile pages."; "There are others that list this as well, and we should review all of the ones that say "review pending" and make sure we've followed up correctly."; "This state of all reviews should be tracked in the GitHub issues."
At main 5664ac1e8, `profile_records.load_record_index().unresolved` holds 5 results: T-073 and T-080 (unordered reported/verified lower-bound priority at 101-105); T-083 and T-084 (unordered verified lower-bound priority at 16 counts k^2-1); T-163 (the family comparison is unassessed, think-kqi1; V2/C1, its next_rung leaving an owner decision between two readings of public recoverability).
