---
type: is
id: is-01m5ntqg8kza7vn9e3v650vndr
title: Catch up every 'Review pending' result on the profiles (T-073/T-080, T-083/T-084, T-163) and track each pending review's state in its GitHub issue (owner, 24 October)
kind: task
status: in_progress
priority: 2
version: 6
delegate: c-review-pending-1024
labels: []
dependencies: []
parent_id: is-01m5khvjtdjf8q14f59bmd8c1k
child_order_hints:
  - is-01m5p3z3ggh42qy2bntrevxwmc
hold: null
hold_until: null
created_at: 2026-10-24T02:09:40.627Z
updated_at: 2026-10-24T04:51:06.895Z
started_at: 2026-10-24T02:09:50.200Z
---

## Notes

2026-10-24 coord-intake-1023: OWNER (in conversation, 24 October, verbatim): "can you also check all cases like this one https://squaremath.org/profiles/kevin-fang.html#records where it says Review pending. All cases like that should be caught up. Is that right? Are you merging them and fixing them? I believe all his work should be quick to validate, so I don't see why we should have entries like that on the profile pages."; "There are others that list this as well, and we should review all of the ones that say "review pending" and make sure we've followed up correctly."; "This state of all reviews should be tracked in the GitHub issues."
At main 5664ac1e8, `profile_records.load_record_index().unresolved` holds 5 results: T-073 and T-080 (unordered reported/verified lower-bound priority at 101-105); T-083 and T-084 (unordered verified lower-bound priority at 16 counts k^2-1); T-163 (the family comparison is unassessed, think-kqi1; V2/C1, its next_rung leaving an owner decision between two readings of public recoverability).

2026-10-24 c-review-pending-1024: draft PR https://github.com/jlevy/squares/pull/770 (branch claude/intake-2026-10-24-review-pending, head de63099d5 at opening; labels intake, S2).
- Review pending, at main 5664ac1e8 and at the heads of #745, #750, #756 and #757: the same 5 unassessed results everywhere. The label shows for T-073, T-080 and T-163, on profiles/kevin-fang.html, profiles/hiroaki-hosono.html, both of their rows in profiles/index.html, and the squarepack-certs and wand125/square-packing-bounds cards of resources.html. profiles/hakan-karakus.html lists T-083 and T-084 under "Facet comparisons awaiting review", with no label.
- T-163 settled: record_scope.assessment, recomputed by cases/asymptotic/deficiency_family.py on every read. Current: strictly the smallest at k = 15-68 and 70-75, tied with Ryu's earlier Theorem 1.3 at 69 and 76. The ledger's and the rationale's "15 <= k <= 78" were against Ryu's Theorem 1.4 only, and are now qualified. V2 kept: the note is public now (DOI 10.5281/zenodo.23463481), so V2's premise is gone, but V3 needs a cited entry (think-494l or think-dgrc). next_rung and composition now say so.
- T-073/T-080 and T-083/T-084: one report each, so report order cannot decide. Decision bead think-33u4; option A patch saved in the lane's scratchpad.
- check_requests --pending: 46 pending; 9 with no tracking issue (none at S4 or above); 6 with a stale or held issue. Stage 7 rule added. Drafts for #603, #294 and #295 are in the lane's scratchpad, not posted.

2026-10-24 coord-intake-1023: OWNER ANSWERS (in conversation). On a pair of register entries from one report (T-073/T-080, T-083/T-084), the owner selected "Credit both (Recommended)": when the tied entries carry identical attribution, both are credited as current (option A, the 11-line change to classify_records). On the nine pending results with no tracking issue (T-036, T-046, T-087, T-112, T-142, T-143, T-144, T-179, T-192), the owner selected "Open all nine (Recommended)": one issue per result, labelled intake, stating its current review state, updated at every change, and closed when the review lands.
