---
type: is
id: is-01m5hz8hzg6602mmynjjdet7vd
title: "Polkovskyi's unclaimed n204.cert (12fc4667) is 1.48e-11 below T-229 and equals the project's regularized view: record it under his credit"
kind: task
status: open
priority: 2
version: 1
labels:
  - result-import
dependencies: []
created_at: 2026-10-22T14:11:56.015Z
updated_at: 2026-10-22T14:11:56.015Z
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
