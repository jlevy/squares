---
type: is
id: is-01m4wc2gjm8dj8rtfv2xmb2k9s
title: "Import Francisco Couzo: 154, 156, 176, 211, 237, 241, 271, 302 and beyond-horizon 338-382 (#561, #570, #583, #586)"
kind: task
status: in_progress
priority: 1
version: 9
delegate: claude-code@vm
labels:
  - result-import
dependencies: []
parent_id: is-01m4padgs7fh6ze3tbh57d5ar1
hold: null
hold_until: null
created_at: 2026-10-14T04:52:31.956Z
updated_at: 2026-10-16T03:23:49.101Z
started_at: 2026-10-14T04:52:38.993Z
---
Francisco Couzo (franciscouzo/square-packing) reports exact rational upper-bound certificates in four issues filed 12-13 October 2026: #561 at 0fa0e0de (156, 176, 237, 271; beyond the corpus 338, 344, 375, 376, 378), #570 at 1b31bc90 (154, 379; superseded by #583 and #586), #583 at 45966700 (154, 211, 241, 302; 339, 379, 380, 381, 382) and #586 at b85dee2b (updates #583: 154, 339, 379, 380, 382 and precision refinements at 211 and 241). Stages 1, 2 and the stage 4 replay of the 2026-10-14 intake lane couzo (think-mq0k), on branch claude/wizardly-meitner-wqn4x3-intake-1014-couzo.

## Notes

GitHub issues: https://github.com/jlevy/squares/issues/561, /570, /583, /586 (Francisco Couzo, franciscouzo). Read 2026-10-14T04:44Z: no comments and no body edits on any of the four (GraphQL userContentEdits = 0); each carries the `intake` label (added 2026-10-14T04:38Z).

## Stage 1: triage

**Pins.** Repository https://github.com/franciscouzo/square-packing, head of master at retrieval b85dee2b964e7f7fb9f765227e60c44cdcd3aa4d (2026-10-13T17:30:53Z). No licence file or reuse terms.

- #561 (filed 2026-10-12T18:55Z) pins 0fa0e0de2ef0b414655e871b1baffcfe0d33c815 (2026-10-12T18:26:28Z) for its nine certificates; its replay script, manifest and receipt are at e9eb44b (18:35:46Z) under publications/20261012/, deleted at 06d8db2. All nine SHA-256 digests the issue states match the files at 0fa0e0d.
- #570 (2026-10-12T23:19Z) pins 1b31bc907d2d881c6962739b6b40cd10b1cd5a9c, which GitHub does not serve (API 422 "No commit found"; raw 404): never pushed, or rewritten. Its n154 digest 5335cb3b... is the n154.cert of 4596670 (#583's), so #570's 154 is #583's certificate. Its n379 (ac463682..., 19.953542593650) is not retrievable; #583 and #586 supersede it.
- #583 (2026-10-13T14:11Z) pins 45966700cf15d3f42e064fd6da51fcb9a5def2be (2026-10-13T13:53:57Z).
- #586 (2026-10-13T17:37Z) pins b85dee2b (the head); it updates #583 at 154, 339, 379, 380, 382 and tightens 211 and 241; 302 and 381 are unchanged since 4596670.

**Every claim of the releases, latest certificate per count** (exact sides rounded up at 12 places):

| n | latest certificate | named by | earlier prints by the same author |
| --- | --- | --- | --- |
| 154 | 12.921206577133 (b85dee2) | #586 | #570 = #583 12.922499814643 |
| 156 | 12.979165853835 (a7067d7, unchanged to head) | #561 | |
| 176 | 13.807637226803 (93570ef) | none | #561 13.807637227056 |
| 211 | 14.993558913975 (b85dee2) | #586 | #583 14.993558914123 |
| 237 | 15.902947773659 (unchanged to head) | #561 | |
| 241 | 15.987117095151 (b85dee2) | #586 | #583 15.987117095169 |
| 271 | 16.948992356452 (unchanged to head) | #561 | |
| 302 | 17.870013850405 (4596670) | #583 | |
| 338 | 18.906332809853 (unchanged to head) | #561 | |
| 339 | 18.925319360704 (b85dee2) | #586 | #583 18.927383638495 |
| 344 | 18.993724693587 (b85dee2) | none | #561 18.993741872920 |
| 375 | 19.893906534236 (4596670) | none | #561 19.901618621328 |
| 376 | 19.904068025747 (4596670) | none | #561 19.904949736499 |
| 378 | 19.942519693846 (b85dee2) | none | #561 19.942536155970 |
| 379 | 19.953531362123 (b85dee2) | #586 | #570 19.953542593650, #583 19.953531531603 |
| 380 | 19.961611078672 (b85dee2) | #586 | #583 19.973553606628 |
| 381 | 19.974977397657 (4596670) | #583 | |
| 382 | 19.987713157610 (b85dee2) | #586 | #583 19.988600568289 |

The head also holds 304 at #506's side (no new claim; Ostashev #575 17.929427758076 is smaller there) and 364 at 19.597249391226 (evand #584's 19.583782203951 is smaller).

**Map to the register (stage 1 table).** Two packets, one per pinned subject: couzo-certificates-2026-10-12 (0fa0e0d, #561, nine requested) and couzo-certificates-2026-10-13 (b85dee2, #583 + #586, nine requested; 176, 344, 375, 376, 378 compared and named by no issue, each an import of its own). In-horizon: one upper-bound entry per packet (156, 176, 237, 271; 154, 211, 241, 302). Beyond the horizon: tracked rows (338, 344, 375, 376, 378 from #561; 339, 379, 380, 381, 382 from #583/#586), each superseding the couzo-certificates-2026-10-11 row at its count except 382, which has none. #570's and #583's superseded prints: no entry; they stay in the packet READMEs.

**Who else holds each value** (main at aeef99ef0; every other register entry at each in-horizon count is above its case ceiling; PRs #585, #587, #591 change no ceiling at these counts: #585 edits the n-154, n-156, n-176 and n-211 case records' drawing credits, #587 is T-156 at 290, #591 is the atlas):

- 154: case T-136 (SQUISH) 12.9230702023; #552 evand 12.922566401934 (exact); #593 Mishapolk 12.9224998146424 (exact, from 46f638c). Smallest: #586, by 1.29e-3 below #593.
- 156: case T-149 (Ostashev) 12.9791726136; #593's certificate has this certificate's exact side. Smallest: tie Couzo #561 = Mishapolk #593 (Couzo first).
- 176: case T-151 (SQUISH) 13.8128562533; #575 Ostashev and #593 13.795872318436 (same exact side). Smallest: #575 (= #593), 1.18e-2 below Couzo.
- 211: case T-149 14.9963367213; #575 14.993694186583; #593 same exact side as #586. Smallest: tie Couzo #586 = Mishapolk #593; #575 above by 1.35e-4.
- 237: case T-140 (Couzo #488) 15.9029496077; #593 15.902705057866. Smallest: #593, 2.43e-4 below #561.
- 241: case T-098 15.9881324395; #575 15.987134249051; #593 same exact side as #586. Smallest: tie #586 = #593; #575 above by 1.72e-5.
- 271: case T-151 16.9491166878; #593 same exact side as #561. Smallest: tie.
- 302: case T-146 17.8720298491; #564 BuddenPing 17.870275382734; #593 17.870275382555. Smallest: #583, 2.62e-4 below #593.
- 338, 344, 376, 378: only the #506 rows. Smallest: Couzo (#561 at 338; head certificates at 344, 376, 378, named by no issue, below #561's by 1.72e-5, 8.82e-4, 1.65e-5).
- 339: #584 evand 18.926898900357. Smallest: #586, 1.58e-3 below.
- 375: #584 evand 19.882451030481. Smallest: #584, 1.15e-2 below Couzo's head certificate and 1.92e-2 below #561's.
- 379: Smallest: #586. 380: #586, 1.52e-2 below Kevin Fang's 078789a. 381: #583, 1.99e-3 below Fang's 078789a and 1.06e-2 below mstrmg #582. 382: #586, 1.77e-3 below Fang.

#593's 16-place prints are '%.16f' renderings of binary64 values (all eight checked); the comparison reads them with the new `binary64` rounding. Exact sides of #593, #575, #584 and Fang's certificates were read from files fetched at the pinned commits (digests equal to those the issues state) and are not retained.

**Priced validation plan.** Both maintained exact routes of upper_bound_reports (sqpack exact witness verifier and the independent rational corner checker), positive + duplicate-square + outside-container per count: 9 counts (27 jobs) for the #561 packet, 14 counts (42 jobs) for the b85dee2 packet. #506's 45 jobs at n = 175-381 took 2,540 route CPU s; priced here at about 1 hour of one worker for certify and the same again for check --replay. No job near 30 minutes. No source program is run (the author's replay.py fetches over the network and was not run). Third exact route (check_half_angle_area) and the mapped W2 review are stage 4's review lane.

## Draft acknowledgement (not posted)

Thank you, Francisco. We have received #561, #570, #583 and #586 and retained the certificates at the commits they pin: 0fa0e0de for #561, and b85dee2b for #583 and #586, which is also the head of your repository. #570's commit 1b31bc90 is not available on GitHub; its 154 certificate is byte-identical to the one #583 pins, and #583 and #586 supersede its 379, so we will take #570's claims through #583 and #586. We will replay every certificate at both pins on this repository's two exact routes, compare each count with the case records and the other open reports (Evan Daniel #552 and #584, Daniil Ostashev #575, BuddenPing #564, Mishapolk #593 and Miles Gray #582), and reply with the result. Five certificates at b85dee2, at 176, 344, 375, 376 and 378, are newer than the ones #561 names and appear in no issue; we will compare them too, and tell us if you would like them registered. We will keep the construction credits you list for each count.

## Lane couzo, resumed after the container restart (2026-10-14, from 05:24Z)

**Stage 2.** Packets couzo-certificates-2026-10-12 (0fa0e0de, nine certificates, all requested by #561) and couzo-certificates-2026-10-13 (b85dee2b, 14 certificates: nine requested by #583/#586, and 176, 344, 375, 376, 378 named by no issue, compared only). acquire_source --check: PACKET_MATCHES_ITS_CONTRACT for both. Importer change: rounding `binary64` for #593's '%.16f' prints, with a test.

**Open PR #574 (PingYou Ltd / BuddenPing, opened 2026-10-13T00:13Z), found on resume and added as a pending report in both packets.** Its numerical-refinements claims state Couzo's #561 certificates at 156, 237 and 271, Ostashev's #575 at 176, and the case ceilings at 211 (T-149), 241 (T-098) and 304 (T-152), each tightened so the side is smaller by about one part in 1e20 (1.3e-19 to 1.8e-19); at 302 an exact algebraic side 17.87027538255505966957... Not read or replayed here. Effect: at 156, 176 and 271 #574 is the smallest stated side, undecided only against #593's binary64 prints; 237 stays #593; 211, 241, 302 stay Couzo (#574 above). Not on the coordinator's list of PRs; flagged to the coordinator.

**Stage 4 replay (both maintained exact routes, --workers 1).**
- #561 packet: 27 jobs, 9 positives pass both routes, 18 controls refused on both; 2,519,208 pair decisions, 601.97 route CPU s, 939.01 job wall s, longest 97.82 s. certify decided 26 jobs 05:01Z-05:15Z before the restart; the 27th by decide-job; certify --finished admitted the receipt. check --replay: all 27 equal, 18 min 17 s.
- b85dee2 packet: 42 jobs, 14 positives pass, 28 controls refused; 4,444,044 pair decisions, 1,473.51 route CPU s, 2,536.72 job wall s, longest 157.79 s. certify decided 28 jobs 05:28Z-05:58Z (stopped by the 30-minute background limit); the other 14 by decide-job 06:07Z-06:21Z; certify --finished admitted the receipt. check --replay: all 42 equal, 34 min 3 s.
- Margins: exact optima clear walls by exactly 5e-21 and pairs by just under 1e-20; rational witnesses clear walls by exactly 1e-15 and pairs by 7.3e-13 to 7.6e-11.

**Register plans** kept for the records lane (register-plan output of both packets). The beyond-horizon rows are 338, 344, 375, 376, 378 (#561) and 339, 379, 380, 381, 382 (#583/#586); at 344, 375, 376 and 378 the b85dee2 certificates no issue names are smaller than #561's, and at 375 evand #584 is smaller than both.

**Committed and pushed** as f8ecf2173fa69c32729e1251cdeb96a6c3007f74 on claude/wizardly-meitner-wqn4x3-intake-1014-couzo (no PR). Checks: tests/test_upper_bound_reports.py 201 passed; the six other importer-dependent modules 87 passed; tests/test_check_half_angle_area.py 153 passed; packing-validate --records 50 of 50 steps passed. Records-lane work (T-NNN, evidence, coverage rows, bibliography, resources README, case records) not done here, by the brief.

## Stage 1 acknowledgement posted (2026-10-14)

The draft above was rewritten before posting to state only what was measured: the pins, the replay on both exact checkers (23 certificates, 69 jobs, controls refused), and the comparison with the current register entry at each count (case ceiling, or the #506 row above 324; the grid at 382). No T-NNN id or rung; it asks Couzo whether the five unrequested b85dee2b certificates (176, 344, 375, 376, 378) should be registered.

- Main reply, #586: https://github.com/jlevy/squares/issues/586#issuecomment-6163323439
- Pointer, #561: https://github.com/jlevy/squares/issues/561#issuecomment-6163323684
- Pointer, #570: https://github.com/jlevy/squares/issues/570#issuecomment-6163324127
- Pointer, #583: https://github.com/jlevy/squares/issues/583#issuecomment-6163324490

Registered on 2026-10-14 in the 14 October records PR (branch claude/wizardly-meitner-wqn4x3-records-1014): T-161 (#561 at 156, 176, 237, 271), T-164 (b85dee2's 176), T-171 (#570's 154), T-181 (#583 at 211, 241, 302) and T-182 (#586 at 154, 211, 241, regularizing T-181's at 211 and 241), all V0/C0, with beyond-horizon rows in report order.

Renumbered on 14 October at review A3 of #602 (records PR, branch claude/wizardly-meitner-wqn4x3-records-1014): Kevin Fang's theorem, T-178 above, is now T-163, at Theorem 1's first commit (6028f31, 12 October); T-163 to T-177 above are now T-164 to T-178. T-179 to T-184 keep their ids.

2026-10-16 ~03:40Z ecstatic-edison-replies-stack, PR #637 review A4 (https://github.com/jlevy/squares/pull/637#pullrequestreview-5542558537). Held reply on #570: `check_requests --report` lists #570 as reply due (T-172 is V3/C3, confirmed, and E-couzo-583-certificate-report reviewed, where the follow-up of 14 October stated V0/C0 and recorded) and closeable with a final comment. The coordinator held it out of the 16 October replies (think-wnsv, 15 October ~22:00Z: "#570 (owner decision on rows without retained certificate)"; think-py1e's brief: "Not on #574 #570 ..."): #570's 379 certificate is in no reachable commit of the source, is not retained and has no row. What releases it: the owner's decision on that, or the owner's instruction to post. Until then a pass that finds #570 due does not post it; #570's entry in packing/campaign/result-requests.yaml notes the same hold (PR #637). #561, #583 and #586, which this bead also answers, were closed with their final replies on 16 October.
