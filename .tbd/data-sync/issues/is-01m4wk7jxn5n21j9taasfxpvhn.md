---
type: is
id: is-01m4wk7jxn5n21j9taasfxpvhn
title: "Import evand: s(339) <= 18.926898900357, s(364) <= 19.583782203951, s(375) <= 19.882451030482, beyond the case corpus (#584)"
kind: task
status: open
priority: 1
version: 9
delegate: null
labels:
  - result-import
dependencies: []
parent_id: is-01m4padgs7fh6ze3tbh57d5ar1
hold: null
hold_until: null
created_at: 2026-10-14T06:57:38.228Z
updated_at: 2026-10-23T06:16:16.766Z
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

## Stage 2 and the stage 4 replay, 2026-10-14, lane ostashev (branch claude/wizardly-meitner-wqn4x3-intake-1014-ostashev, head 8d396177b)

Packet packing/resources/web/evand-compositions-2026-10-13 (source key [Daniel compositions 2026-10-13], evidence E-evand-584-compositions-report): 12 comp2 files, LICENSE, CREDITS.md retained (14 files, 454,778 bytes); checkers pinned to the issue-399 packet, search/exact/README.md to the issue-489 packet, PACKER.md by digest. claims.json and beyond-horizon-claims.json frozen against main aeef99ef0 (unchanged on f73e9de13).

Importer: devtools.upper_bound_reports accepts a declaration requesting only beyond-horizon counts; register-plan then emits evidence, source row and beyond-horizon rows, no results.yaml entry (tests).

certify --workers 1: 9 jobs, all 3 positives pass and all 6 controls refused on both routes, 1,160,892 pair decisions, 477.89 route CPU s, 12m49s at load 9-11; least wall >= 5.00e-21, pair >= 9.99e-21. check --replay: 9 jobs equal, 8m39s.

Register plan: scratchpad register-plan-evand-compositions-2026-10-13.yaml (evidence, source row, three beyond-horizon rows at 18.926898900357, 19.583782203951, 19.882451030482, assurance reported until review).

## Stage 1 acknowledgement posted, 2026-10-14

https://github.com/jlevy/squares/issues/584#issuecomment-6165052968 (states the pin, the retained and replayed certificates with controls refused, and the comparison at each count; the earlier draft above was not posted as written).

Registered on 2026-10-14 in the 14 October records PR (branch claude/wizardly-meitner-wqn4x3-records-1014): #584's 339, 364 and 375 as beyond-horizon rows in report order (339 superseded by #586).

2026-10-16 ~06:45Z user-eb-intake-residue (lane A, think-mu5v): #584's final comment, rendered from main e2e018f32 with check_requests --draft 584 (greeting added). Checked first: the last reply is more than a day old with no author comment since, nothing the author asked for is queued, no think-l3oo decision touches it, and main and the deployed site (result pages read 06:30Z, deployment e2e018f32) state what it states. NOT POSTED: this session's permission system refused the GitHub comment and the close (auto-mode classifier, external system writes), so the post, the close and the record of the reply under #584's replies (kind final, with state/closed) are owed by whoever posts it. To post: gh api repos/jlevy/squares/issues/584/comments -X POST -F body=@FILE, then gh api repos/jlevy/squares/issues/584 -X PATCH -f state=closed -f state_reason=completed. Draft:

@evand, thank you. Where this request stands in the record on `main`.

**Not registered.**

- s(339) <= 18.926898900357, s(364) <= 19.583782203951 and s(375) <= 19.882451030482, by exact rational certificates: Beyond the n <= 324 corpus: rows of the evand-compositions-2026-10-13 source.

**On `main`.** [`packing/frontier/RESULTS.md`](https://github.com/jlevy/squares/blob/main/packing/frontier/RESULTS.md).

Nothing you asked for is queued, so this issue is closed with this comment.

---
_Generated by [Claude Code](https://claude.ai/code)_

Correction (user-eb-intake-residue, 2026-10-16T05:47Z by date -u): the '~06:xxZ' times in this lane's notes of 16 October are about an hour late; they were written between 05:30Z and 05:47Z. The site pages were read at about 05:35Z. No condition changes: every last reply named is still more than a day old.
