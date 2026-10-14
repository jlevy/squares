---
type: is
id: is-01m4wk7jxn5n21j9taasfxpvhn
title: "Import evand: s(339) <= 18.926898900357, s(364) <= 19.583782203951, s(375) <= 19.882451030482, beyond the case corpus (#584)"
kind: task
status: in_progress
priority: 1
version: 3
delegate: claude-code@vm
labels:
  - result-import
dependencies: []
parent_id: is-01m4padgs7fh6ze3tbh57d5ar1
hold: null
hold_until: null
created_at: 2026-10-14T06:57:38.228Z
updated_at: 2026-10-14T07:18:41.423Z
started_at: 2026-10-14T06:57:50.383Z
---
https://github.com/jlevy/squares/issues/584 (2026-10-13T14:31:16Z, unedited). evand/square-packing at 231d41df7a03fccd89aa6e9ef5a540348a8214cc, search/packer/candidates/comp2_n339, n364, n375 (.cert, .exact.txt, .input.txt, .json). All three counts lie beyond n = 324: verified beyond-horizon rows in source-coverage.yaml, as #506. Stages 1-2 and the stage 4 replay through devtools.upper_bound_reports, intake lane ostashev of 2026-10-14.

## Notes

Issue: https://github.com/jlevy/squares/issues/584 (opened 2026-10-13T14:31:16Z by evand, label intake added 2026-10-14T04:38Z). Body never edited; no comments as of 2026-10-14T07:00Z. evand's commit fc094b1 references the issue. New issue #596 (evand, 2026-10-14T06:51Z: 365, 370, 460, beyond the corpus, at 622cd2e) cross-references it; #596 is not in this lane.

## Stage 1 triage, 2026-10-14, intake lane ostashev (branch claude/wizardly-meitner-wqn4x3-intake-1014-ostashev from main aeef99ef0)

Pin: evand/square-packing 231d41df7a03fccd89aa6e9ef5a540348a8214cc (committed 2026-10-13T14:24:04Z), the commit the issue names; its three .cert SHA-256 match. The head when retrieved (2026-10-14T07:01Z), 622cd2e, holds the same twelve comp2 files and the same checkers (it adds #596's fresh_* files). MIT licence (LICENSE, CREDITS.md).

Claims the release makes, and their register map:
1. s(339) <= 18.926898900357, s(364) <= 19.583782203951, s(375) <= 19.882451030482 (12 places rounded up; exact sides 18.92689890035674158973360842897, 19.583782203950834292109305759091, 19.882451030481246819527281665997). All three lie beyond the case corpus: no register entry; three beyond-horizon rows in source-coverage.yaml (verified after review, as #506's).
2. Corollaries by Friedman's L-step: s(403) <= 20.583782203951, s(414) <= 20.882451030482 "and so on up the chains". The author asks no rows; no certificate files for them at the pin. Not registered.
3. The packer log (PACKER.md, pinned by digest) also records s(325)/s(326) <= 130/7 (withdrawn there as beaten by the L-step) and s(414) <= 20.8984034740 (beaten by the 375 corollary). No certificate at the pin; no claim made by the issue. Not registered.
4. KKT / reduced Hessian / MILP: numerical evidence as the source says; not registered.
5. Lineage: two-piece compositions (Ellsworth s(171) style, Ostashev #562/#575 style): 339 from two crops of Ostashev's #575 s(304); 364 = BuddenPing's (PingYou Ltd) s(146) of #566 (refinement of Barnett's #505) + Schadt's s(50); 375 from crops of SQUISH's s(88) and Xu's s(129). Claude (Claude Code) assistance disclosed, directed and reviewed by Evan Daniel.

Who else holds each value (frozen in acquisition/claims.json against main aeef99ef0; grid 19 at 339, 20 at 364 and 375):
- 339: current beyond-horizon row couzo-certificates-2026-10-11 (T-152's release, verified) 18.929433883808, below by 2.535e-3; Couzo #583 18.927383638495, below by 4.847e-4; Couzo #586 18.925319360704 is SMALLER, by 1.580e-3 (#586 cites this issue as its comparison). Smallest: #586.
- 364: row couzo-extended-range-reports-2026-10-08 19.597249391207239 (reported), below by 1.347e-2. Couzo's head b85dee2 n364.cert 19.597249391226 is above too. No open report. Smallest: this certificate.
- 375: row couzo-certificates-2026-10-11 19.906335145009, below by 2.388e-2; Couzo #561 19.901618621328, below by 1.917e-2; Couzo's 4596670 / b85dee2 n375.cert 19.893906534236 (no issue; identical bytes at both commits), below by 1.146e-2. Smallest: this certificate.
- No other open report (#562, #575, #564, #566-#569, #570, #573, #582, #593) names 339, 364 or 375. Open PRs #585, #587, #591 touch no beyond-horizon row here.

Importer: devtools.upper_bound_reports refused a declaration that requests nothing inside the horizon; this lane relaxes that (register-plan then plans evidence, the source row and beyond-horizon rows, and no register entry), with tests.

Validation plan (priced): evand-cert adapter; both maintained exact routes, --workers 1: 9 jobs at n = 339..375, about 30-45 min each pass at load 12-15. Source checkers pinned against the issue-399 packet, not run. Review: records lane, as for #506.

## Draft acknowledgement (not posted)

Thank you, Evan. We received the three certificates at evand/square-packing 231d41d (search/packer/candidates/comp2_n339, n364 and n375), and the three SHA-256 values match the files there. All three counts lie beyond the n <= 324 case corpus, so they go to the source register's beyond-horizon rows rather than to a register entry, as #506's did. We will retain the commit, read each certificate exactly, decide each packing with a duplicate-square and an outside-container control on our two maintained exact routes, and compare each side with the rows and reports at its count. At 339, Francisco Couzo's #586 (18.925319360704) is now below this side; at 364 and 375 this side is below everything we hold. We register no rows for the L-step corollaries at 403 and 414, as you asked.
