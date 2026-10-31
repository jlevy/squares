---
type: is
id: is-01m685njhfc113wb8prbg15npb
title: "Import Mishapolk: 14 upper bounds at N in [105, 308] (#846), with the 23 October watched certificates e386aab-fbc1749 (no issue)"
kind: task
status: in_progress
priority: 1
version: 4
delegate: bold-ritchie-l2
labels:
  - result-import
dependencies: []
parent_id: is-01m684vnbc5mmkjn950c3edw3w
child_order_hints:
  - is-01m687bj11pzvr48e6pm14abna
hold: null
hold_until: null
created_at: 2026-10-31T05:07:11.535Z
updated_at: 2026-10-31T05:49:50.272Z
started_at: 2026-10-31T05:07:23.528Z
---
Issue jlevy/squares#846 (Mishapolk, 2026-10-30T05:46:42Z): 14 certificates at Mishapolk/square-packing-records 52aa267 (committed 2026-10-30T05:40:00Z): Category A at 130 (a 2e-14 dilation of Couzo's #843 packing, 2.08e-12 below it), 182 and 268; Category B at 105, 146, 156, 204, 211, 229, 241, 260, 299, 304, 308. Triage by exact header sides: 182, 268 and 304 are above the case's house, 260 above #844/#845, 299 above Daniel's #824 update, 204 ties T-231, and 211 and 241 restate the source's own e386aab files; 105, 130, 146, 156, 229 and 308 lie below every earlier report (by 1e-21 to 1e-41 but at 130). The 15 commits past the 7e82c64 read also publish, with no issue, certificates at 88, 126, 152, 154, 155, 183, 211, 227, 236, 237, 241 and 271, each about 1e-19 below its case's house (e386aab to fbc1749, 2026-10-23T23:36Z to 23:56Z), ties at 105, 204 and 270, an index-only 303, and small-N certificates at 11 to 41 (ab8e833) above each case's record. Stage 1-3 and the stage 4 replay in the 2026-10-31 intake pass, lane L2 (think-3guf); review and adoption follow.

## Notes

2026-10-31 bold-ritchie-l2: stages 1-3 and the stage 4 replay on branch claude/bold-ritchie-xo28us-upper: packets mishapolk-issue846-2026-10-30 and mishapolk-1023-refinements-2026-10-30 at 52aa267; both maintained exact routes accept all 27 certificates and refuse the gross and sharp controls; identity vs each house (one to one at every recorded count; at 105, 146, 156, 229, 308 and 155, 211, 236, 237, 271 nothing beyond 1e-9). Ledger upper-bounds-843-846-20261031: from the 23 October commits it records 154, 155, 183, 211, 227, 236, 237, 241, 271 (T-252) and not 88, 126 (above T-193's exact sides, which the ledger now reads count by count), 152 (undecided against T-122's exact side, printed at 24 places) or 204, 270 (ties); from #846 it records 105, 130, 146, 156, 229, 308 (T-258) and not 182, 268, 304 (above the houses), 260, 299 (above #845 and the #824 update), 204 (tie), 211, 241 (restate e386aab). Registered at V0/C0 (ids may be renumbered at merge). Review and adoption: think-ikku. Owner decision to raise: whether in-corpus sub-print re-certifications are restatements, as think-fwa9 rules beyond 324. DRAFT import reply for #846, to render from main after the merge: received the 14 certificates at 52aa267 (MIT); each 12-place print is its header rounded up; at 204, 211 and 241 the exact fractions in the issue's table are not the files' headers, and at 268 the printed denominator has an extra digit (ask which file states 1598711709514999999999999999999/10^29 at 241, informational); both routes accept every certificate with gross and sharp controls refused; the ledger records 105, 130, 146, 156, 229, 308 as refinements (T-258, credited to each packing's finder, Polkovskyi for the refinement) and not the other eight, with the reason for each; the 23 October certificates are recorded from their commits (T-252); the review and adoptions are queued (think-ikku).
