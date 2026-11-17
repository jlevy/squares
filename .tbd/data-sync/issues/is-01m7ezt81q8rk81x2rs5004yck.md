---
type: is
id: is-01m7ezt81q8rk81x2rs5004yck
title: "Import #992: Miguel Lara's s(977) <= 17 + 21/sqrt(2) (45-degree central diamond of 441 + four corner staircases of 134), beyond the horizon; decided by devtools.diamond_staircases; not recorded (Couzo #763 row below)"
kind: task
status: closed
priority: 2
version: 8
delegate: bold-ritchie-l179
labels:
  - intake
  - result-import
dependencies: []
parent_id: is-01m684vnbc5mmkjn950c3edw3w
hold: null
hold_until: null
created_at: 2026-11-15T06:55:16.022Z
updated_at: 2026-11-15T09:59:36.626Z
started_at: 2026-11-15T06:55:17.600Z
closed_at: 2026-11-15T09:59:36.625Z
close_reason: "#992 taken in as not recorded (#994, 538b7833a; Couzo #763 row below the claim), answered and closed; reply recorded in #995 (91acf2022)."
resolution: null
duplicate_of: null
---

## Notes

L175 (bold-ritchie-l175), 2026-11-15: controls plan stated before any run of the construction, in scratch l175-notes: controls-plan-n977.md SHA-256 7cbe1f461f002ed510f5ebc7f6d29975a8d6af25239bac00ca38db52cba0c891, hashed 07:05:48Z; one positive at contact, 2 gross and 3 sharp controls on both algebraic routes (sqpack.witness.exact_verify, devtools.check_algebraic_witness_independent), and the Göbel comparison stated in advance. Source: larasmiguel/square-s977 head 26d5695abca2f8a005856e3c1ddc47171d661e9b (clone 07:00Z), no commit named in the issue; the head's three commits after the issue (06:24:24Z-06:24:28Z) acknowledge Göbel and disclaim novelty. Standing row at 977: couzo-issue763-2026-10-23, 31.765989508190, below the claim's 17 + 21/sqrt 2, so the report-order rule does not record it.

L175 2026-11-15 07:50Z: draft PR https://github.com/jlevy/squares/pull/994, head 9afcb4781. Not recorded: the ledger upper-bounds-992-20261115 reads Couzo's #763 row at 977, 31.765989508190, 8.33e-2 below the claim. Construction decided exactly on both maintained routes over Q(sqrt 2) by the new devtools.diamond_staircases (receipts/exact-decision.json, six controls as planned). Göbel: the side is the L-border of the (15, 21) square of 921 (982), which goebel_construction omits (think-7j3i); the author's layout is the (16, 21) arrangement cut to 134 per staircase. L174's review (b0604bf68) read at 07:40Z after this lane's determination was pushed, merged and mapped; agrees; S1 proposed. Licence follow-up think-cszb; display defect think-526p. stamp_landed: nothing to stamp; release_pin --check: pin already the last data commit. Next: hosted CI, the coordinator's merge, then the stage 7 reply on #992 with the review's six questions.

L179 (bold-ritchie-l179) 2026-11-15 09:45Z: recorded #992's final reply (issuecomment-6892360714, jlevy, 09:30:33Z; issue closed as completed 09:30:34Z, after #994 merged as 538b7833a and Pages run 43697866071 passed): kind final, reported n977-diamond-staircases with no id (#900), state closed 2026-11-15, read_through 09:30:33Z; think-cszb stays in the entry beads, not the reply's. Draft PR https://github.com/jlevy/squares/pull/995, head 78adb1d5f. check_requests: #992 settled, no reply due; --github 0 differences; make intake does not list #992 under Needs Action; records tier exit 0; 13 test files 515 passed; release_pin --check: pin already the last data commit (e9b8ab184), no re-pin; no-public-change record 2026-11-15-bold-ritchie-l179-992-reply.yaml. Left open for the coordinator to close after merge.
