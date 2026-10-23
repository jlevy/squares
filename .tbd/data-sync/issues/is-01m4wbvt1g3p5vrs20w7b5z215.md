---
type: is
id: is-01m4wbvt1g3p5vrs20w7b5z215
title: "Import BuddenPing: s(146) <= 12.5837822039508342919134679370511513667729, refining T-150 (#566)"
kind: task
status: closed
priority: 1
version: 7
delegate: claude-code@vm
labels:
  - result-import
dependencies: []
parent_id: is-01m4padgs7fh6ze3tbh57d5ar1
hold: null
hold_until: null
created_at: 2026-10-14T04:48:52.272Z
updated_at: 2026-10-23T06:12:34.224Z
started_at: 2026-10-14T04:49:01.069Z
closed_at: 2026-10-23T06:12:34.224Z
close_reason: "Tracker audit 2026-10-23 (c-audit-b-1023, think-ioqe), checked by coord-intake-1023: STALE-CLAIM + DONE. #566 closed 2026-10-15. T-168 is V3/C3 confirmed. check_requests: closed."
resolution: null
duplicate_of: null
---
https://github.com/jlevy/squares/issues/566 (BuddenPing, opened 2026-10-12T22:38Z; updated 2026-10-12T23:41Z). BuddenPing/square-packing-certificates 820b9ffb11dd602d735f7a03cd472db98a2d3bb6, n146.cert.json and pingyou-n146-rational.yaml; a further refinement of Robert Barnett's T-150 at 146; credit PingYou Ltd. Intake lane pingyou of 2026-10-14.

## Notes

## 2026-10-14 intake lane pingyou (stages 1, 2 and the stage 4 replay)

Branch `claude/wizardly-meitner-wqn4x3-intake-1014-pingyou`, commit `680123806` (pushed; no PR). Packet `packing/resources/web/pingyou-n146-refinement-2026-10-12/`. Resumed after a container restart: the predecessor lane's packet, declaration and first five receipts were kept and checked; n272 and n261 were certified and all seven replayed again here.

### Stage 1 triage

- **Read:** issue #566 (opened 2026-10-12T22:38Z; title and body replaced 23:41Z, and a comment at 23:41Z saying so; no other comments).
- **Pin:** BuddenPing/square-packing-certificates `820b9ffb11dd602d735f7a03cd472db98a2d3bb6`, committed 2026-10-12T23:41:08Z (tree `32adc0e3`); every file of the scope has the same blob at the head 318ab94 (2026-10-12T23:46:52Z) at retrieval 2026-10-14T04:47Z.
- **Claim:** s(146) <= 12.5837822039508342919134679370511513667729 as printed; exact side 6291891101975417145956733968525575683386443086533905641519426925380587272252740885402451051/5000000000000000000000000000…, rounded up at 16 places 12.5837822039508343. First committed 2026-10-12T23:41:08Z.
- **Other claims of the release:** none at other counts in this scope. Later, outside it: PR #574 (BuddenPing/squares head 4c319c2, open) and the GitHub releases at tags data/pingyou-* on 318ab94 state smaller certificates at all seven of this pass's PingYou counts; an import of their own, not owned here (see the packet README).
- **Licence:** none (no licence file at the pin; GitHub detects none; the release READMEs grant nothing for the source's own files). Derived-only custody: no upstream byte retained.
- **Register action:** a new entry: a later certificate that improves T-150's value at 146 (Barnett's refinement of Xu's packing); T-150 keeps its claim.
- **Who else holds the value (frozen in acquisition/claims.json at main aeef99ef0):** case T-150 (ry-xu, improved by Robert Barnett), below by 2.119e-13; T-101 (#375) below by 1.713e-02; T-125 (#432) below by 7.356e-08; T-146 (no issue) below by 7.346e-08; #593 below by 2.113e-13; PR #574 undecided by 4.545e-69; smallest undecided among this certificate and PR #574: their prints do not order them. Open PRs #585 (regularized-drawing credit), #587 (T-156 at 290) and #591 (regularized view by default) state no side at this count. evand's #584 builds its s(364) from this certificate's packing whole, S* = s(146) + 7, so #584's 364 rests on #566.
- **Credit:** Credit PingYou Ltd (https://github.com/BuddenPing/square-packing-certificates) with this further refinement, as the source asks, of Robert Barnett's refinement (T-150, issue 505) of Ryan Xu's packing of 146 (ry-xu, issue 432); the source credits Evan Daniel with the contact-solver source and the earlier n146 regularization.
- **AI assistance:** the issue and comments state nothing about AI assistance; no pinned file states anything about AI assistance (scanned, packages included); the standing statement on record is the author's #503 answer of 2026-10-12T17:57Z for the n207 and n153 solutions: 'Both solutions were AI assisted by "PY", an unreleased agentic AI offering by PingYou Ltd.'; the certificate's provenance and the package's construction records name machine-local paths under a directory named ChatGPT (paths, not a statement).
- **Validation plan and price:** both maintained exact routes (sqpack exact_verify and check_rational_witness_independent) through devtools.upper_bound_reports, a positive and two controls, --workers 1; measured 16-17 s per job (11 route CPU s). No source program needs to run. Stage 4 review and a third route (check_half_angle_area) remain.

### Stage 2 and the stage 4 replay

- Packet written by acquire_source; fact derived and held to the source's witness. certify --workers 1 52 s wall: 3 jobs, 1 positive passes both routes, 2 controls refused by both; 63,510 pair decisions, 32.7 route CPU s, longest job 16.69 s; a fresh check --replay 48 s wall, equal to the retained rows.
- register-plan (printed, nothing written; full output kept in the lane's scratch): T-NNN at V0/C0, scope [146], proposed significance 2, published 2026-10-12, evidence E-pingyou-566-certificate-report, credit 'PingYou Ltd after Xu, Barnett, Daniel, Levy', lineage builds-on-project, source key [PingYou n146 refinement 2026-10-12]. Shared records not edited.

### Draft acknowledgement (not posted)

@BuddenPing, thank you. We have the n146 certificate from your update of 12 October, pinned at 820b9ff (n146.cert.json, SHA-256 a88ede7e…). We retain it as derived exact facts, and this project's two maintained exact routes have decided it with both controls. A review and the registration follow, and a reply from main will say what was registered. PR #574 states a further n146 certificate; it is a separate import.

Posted (stage 1 acknowledgement, 2026-10-14): https://github.com/jlevy/squares/issues/566#issuecomment-6162867895

Registered on 2026-10-14 in the 14 October records PR (branch claude/wizardly-meitner-wqn4x3-records-1014): T-167 at 146, V0/C0, regularizing T-150.

Renumbered on 14 October at review A3 of #602 (records PR, branch claude/wizardly-meitner-wqn4x3-records-1014): Kevin Fang's theorem, T-178 above, is now T-163, at Theorem 1's first commit (6028f31, 12 October); T-163 to T-177 above are now T-164 to T-178. T-179 to T-184 keep their ids.
