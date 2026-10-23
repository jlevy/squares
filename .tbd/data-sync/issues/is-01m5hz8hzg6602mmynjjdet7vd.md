---
type: is
id: is-01m5hz8hzg6602mmynjjdet7vd
title: "Polkovskyi's unclaimed n204.cert (12fc4667) is 1.48e-11 below T-229 and equals the project's regularized view: record it under his credit"
kind: task
status: open
priority: 2
version: 3
labels:
  - result-import
dependencies: []
created_at: 2026-10-22T14:11:56.015Z
updated_at: 2026-10-23T00:36:20.108Z
---
Found by the stage 4 lane c-lane-stage4-1022 (22 October 2026) while regularizing T-229 after adoption.

Evan Daniel's regularizer, run by the project on T-229's 204 witness, reaches s(204) <= 14808642830513087197802415708703/10^30, 1.48e-11 below T-229's claimed side (882663895519250432/59604644775390625). That side is byte-for-byte the header side of Polkovskyi's other 204 file, `certificates/n204.cert`, in Mishapolk/square-packing-records at 12fc4667 (first committed at 1851c2c, 2026-10-22T05:29:48Z, unless the packet's receipts say otherwise). The mishapolk-issue719-2026-10-22 packet pins that file by digest only, and #719 claims `n-204.cert`.

Mishapolk/square-packing-records is a watched repository, so `n204.cert` is Polkovskyi's report dated by its first commit whatever the issue claims (the same rule as Couzo's unclaimed watched publications, think-tmwt). So the project's regularized view is NOT a project result under the Register Candidates row 3; it reproduces an earlier publication and the credit is Polkovskyi's.

The stage 4 PR (claude/intake-2026-10-22-stage4) does not register it; it records the candidate and its equality with n204.cert in the 204 settlement/README and the PR body.

To do, after #719's reply question 4 ("which 204 file do you claim") is answered or after a reasonable wait:
- Derive and replay n204.cert (derived-only custody, no licence), both maintained routes and sharp controls; confirm the exact side and that it equals the regularizer's.
- Record it under Polkovskyi's credit, dated by its first commit: either T-229 states the smaller side at 204 (if he names it, or by the watched-publication rule), or a new entry at V0/C0. The project's regularizer run is corroborating evidence (an independent route to the same side), not a credit.
- Then stage 4 for that side and adoption at 204 (House Rule).
- Check the earlier-publications receipt and #719's ledger for whether n204.cert should already appear as an earlier/same-commit publication at 204 (#722 review A2: same-commit sides keep the smaller).

blocked_on: think-xyhn

## Notes

2026-10-22 18:40Z coord-intake-1021b (from #725 review A, A2, https://github.com/jlevy/squares/pull/725#issuecomment-6348041004): correction to this bead's dating. The path certificates/n204.cert was first committed at 8bb41af5 (13 October) with a LARGER side and changed at 70a033f0 (14 October); the side equal to the project's regularized view first appears at 1851c2c7 (2026-10-22T05:29:48Z), the same commit that first published n-204.cert, the file T-229 cites. So the report to record is n204.cert's side dated by 1851c2c7 (the first commit holding THAT side), not by the path's first commit; 'earlier publication' is true only against the project's regularizer run. #722 review A2's rule (a commit's least side per count) also applies at this commit: 1851c2c7 published both n-204.cert and n204.cert, and n204.cert is the smaller.

2026-10-23 c-lane-sweep-1023a. The author claimed the lower file on #719, comment 6350348588 (2026-10-22T20:15:57Z), answer 3: "We claim the lower certified bound (1.48 x 10^-11 lower), which passed both of your exact routes." So this bead's wait on the answer is over, and #725 (T-229 adopted at 204) merged at 2026-10-23T00:23:18Z (e929137a8).
- The file: certificates/n204.cert at 12fc466, SHA-256 9c5dabc8f2456b0c90650eac5794918c5e52ff90d9e817bd215c9816a88f3e7d (the mishapolk-issue719-2026-10-22 packet's sources.json binds it by digest only), header side 14808642830513087197802415708703/10^30, 1.4809e-11 below T-229's 882663895519250432/59604644775390625 (exact, Fraction). The path is gone at 814fbe9 and at the head 17cc220.
- #719's requests entry now carries it as result n204-lower, queued, bead think-h01y (claude/intake-bookkeeping-2026-10-23).
- Licence: 17cc220 adds an MIT LICENSE (copyright Mykhailo Polkovskyi); the comment says it covers every certificate and lets "jlevy/squares retain and redistribute the raw certificate files in your packets". The file is not in 17cc220's tree, so retaining its bytes rests on the comment's grant; derived facts, as the #719 packet keeps, need none.
- How to record it: T-229 is now V3/C3 and adopted at n-204.cert's side, so restating T-229 would void its review's stated bound. Recommended: a new entry at 204 (a refinement of T-229's packing, credited as T-229 is), dated by 1851c2c, then stage 4 and adoption by the house rule; the stage 4 regularizer run is corroborating evidence, not credit. The coordinator chooses.
- The reply draft that announces this step: replies/stage4-1022/719-reply-v2.md.
blocked_on: none
