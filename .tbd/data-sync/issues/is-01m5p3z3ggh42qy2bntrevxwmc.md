---
type: is
id: is-01m5p3z3ggh42qy2bntrevxwmc
title: "PR #770: apply the owner's 'Credit both' answer and open the nine tracking issues"
kind: task
status: closed
priority: 2
version: 4
delegate: c-fin-770-1024
labels: []
dependencies: []
parent_id: is-01m5ntqg8kza7vn9e3v650vndr
hold: null
hold_until: null
created_at: 2026-10-24T04:51:06.895Z
updated_at: 2026-10-24T07:30:01.217Z
started_at: 2026-10-24T04:51:26.723Z
closed_at: 2026-10-24T07:30:01.217Z
close_reason: "PR #770 merged 2026-10-24T07:14:46Z (11d0ab06b): 'Credit both' applied and tracking issues #772-#780 (and #782-#786) opened"
resolution: null
duplicate_of: null
---

## Notes

2026-10-24 c-fin-770-1024: done on PR #770 (branch claude/intake-2026-10-24-review-pending), head 294fbfc08, hosted CI green (Packing validation 40066029993, Certificate page 40066029901, Branch mergeability 40066026169; 31 passed, 28 skipped).
- Commits: cdb03eb9c merge main af9c9e850 (#745, #759); 3b4406002 "Credit both (Recommended)" (classify_records patch, negative control first, live assertions, rule in result-import.md Several Reports at One Count and contributors README); f28c0b00d the nine tracking issues in result-requests.yaml and owner-bead links on T-036, T-046, T-087, T-112; 49da5d7e0 merge main 2c58b6373 (#771, #750); d00606803 re-pin DATA_REVISION to 49da5d7e; 294fbfc08 papers' no-change record re-measured (69 files byte-identical, links pinned to 2c58b637).
- Tracking issues (intake label): T-036 #772, T-046 #773, T-087 #774, T-112 #775, T-142 #776, T-143 #777, T-144 #778, T-179 #779, T-192 #780. check_requests --pending: 43 pending, 0 with no tracking issue; 12 not stating their present state (the nine, owed an acknowledgement after the merge, plus T-153, T-154, T-233).
- Owner beads created under think-ezt8: think-o9kd (T-036 C3), think-sb7a (T-046 C3), think-ysr9 (T-112 C3). Existing owners reused, not duplicated: think-wcex (T-046 C1), think-gtjq (T-087 C2).
- Record index at the head: 126 current, 0 unassessed, unresolved empty. Overview build before/after the patch at cdb03eb9c: 4 files differ (hiroaki-hosono.html, hakan-karakus.html, profiles/index.html, resources.html); no page says Review pending.
- Drafts kept outside the tree in the review-pending scratch: draft-issue-603.md (think-494l as T-163's next route, no CPU; T-236's Lean build the other), draft-issue-294.md (both entries credited, post after merge), draft-issue-295.md (unposted, as recommended).
- Validation: packing-validate --records --jobs 2 --inner-jobs 1 at 294fbfc08, 53 of 111 passed, none failed (197 s); 13 focused modules, 485 passed.
