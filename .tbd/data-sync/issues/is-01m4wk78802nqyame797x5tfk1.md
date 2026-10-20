---
type: is
id: is-01m4wk78802nqyame797x5tfk1
title: "Import dostashev: s(129) <= 11.870013850405, s(204) <= 14.808663234387, s(303) <= 17.909958291070 (#562)"
kind: task
status: in_progress
priority: 1
version: 6
delegate: claude-code@vm
labels:
  - result-import
dependencies: []
parent_id: is-01m4padgs7fh6ze3tbh57d5ar1
hold: null
hold_until: null
created_at: 2026-10-14T06:57:27.296Z
updated_at: 2026-10-14T14:50:14.193Z
started_at: 2026-10-14T06:57:53.843Z
---
https://github.com/jlevy/squares/issues/562 (2026-10-12T19:10:14Z, unedited). dostashev/square-packing at fe43a64ecf2581cdbd11830e8a5be0989746c5d3, records/n0129, n0204, n0303 (.sqcert, .sqpk). Stages 1-2 and the stage 4 replay through devtools.upper_bound_reports, intake lane ostashev of 2026-10-14.

## Notes

Issue: https://github.com/jlevy/squares/issues/562 (opened 2026-10-12T19:10:14Z by dostashev, label intake added 2026-10-14T04:38Z). Body never edited (GraphQL userContentEdits empty); no comments as of 2026-10-14T07:00Z.

## Stage 1 triage, 2026-10-14, intake lane ostashev (branch claude/wizardly-meitner-wqn4x3-intake-1014-ostashev from main aeef99ef0)

Pin: dostashev/square-packing fe43a64ecf2581cdbd11830e8a5be0989746c5d3 (committed 2026-10-12T17:19:33Z), the commit the issue names; its six SHA-256 match the files there. The head has moved to b909e1b (2026-10-13T03:03:29Z, issue #575); 883aa4b (2026-10-12T20:25:20Z) rewrote the 129, 204 and 303 files in canonical form at the same exact sides (measured here with the sqcert adapter: equal), so the issue's bytes are pinned, not the head's. MIT licence.

Claims the release makes, and their register map:
1. s(129) <= 11.87001385040446434457885353928463864242, s(204) <= 14.80866323438695656647099008094596479529, s(303) <= 17.90995829106990798159574108139873608005 (issue, 38 places rounded up; README 15 places). Bounds of one kind at several counts in one release: one new entry whose scope is 129, 204, 303.
2. README at the pin also prints s(176) <= 13.808663234386957 (fc4bec4), which the issue does not ask for (Couzo improved it from this packing, #561; #575 has the author's smaller 176). Below the case ceiling (T-151) but above #561, #575 and #593: compared in the packet, not registered, not replayed.
3. The commit also holds #528's 175, 232, 264 (unchanged since a8db6ff, think-em0b) and #501's 155, 156, 211 (unchanged since c3d17ab, T-149): no new claim.
4. KKT exact first-order optimum of each contact topology (60 digits, load-bearing squares scaled by 1 + 1e-20): a local-optimality report, not a bound; recorded as reported, not registered.
5. Rectangle packings (44 in (h+3) x h, h = 5.80866...; 62 in (h+6) x h, h = 5.90995...; 163 in (h+3) x h, h = 11.87001...): no s(n) claim; stay in the packet.
6. Lineage: 204/303 compositions of the new rectangles; 129 a cut-out of a rectangle cut from the s(302) house (Chaoweeraprasit, Daniel's regularization), laid out like Xu's s(129), tilted band different. AI assistance stated (AI agents wrote and ran search, composition and verification code).

Who else holds each value (frozen in acquisition/claims.json against main aeef99ef0):
- Every register upper-bound entry at 129, 204 and 303 with a reader (T-101, T-113, T-115, T-125, T-127, T-146 at 129; T-101 at 204; T-098, T-113, T-134, T-136, T-138, T-146 at 303) was rebuilt here and is above the certificate; T-056 and T-092 at 303 have no reader and print larger sides; T-155 at 204 is T-101's side.
- 129: case T-146 (ry-xu, improved by Evan Daniel) 11.8720298490811800; below by 2.016e-3. #593 (Mishapolk) prints 11.8700138504044652: below its print.
- 204: case Kingbird 14.82287565553229 (27/2 + sqrt(7)/2), verified by T-101/T-155 at 14.822875655532295295...; below by 1.421e-2. #593 prints 14.8086632343869571: below its print.
- 303: case T-146 (Chaoweeraprasit, improved by Daniel) 17.9130654627385324; below by 3.107e-3. #593 prints 17.9099582910699091: below its print. Couzo's head 303 (b85dee2) 17.917365675353 is above.
- #593's certificates at Mishapolk/square-packing-records 46f638c (fetched to scratch, SHA-256 matching the issue) state at 129, 204 and 303 exactly these sides rounded up at 30 places (above by 3.6e-31, 3.5e-32, 2.6e-31); its 16-place prints are binary64 renderings, not those sides.
- No other open report of this pass (#561, #570, #583, #586, #564, #566-#569, #573, #582, #584) names 129, 204 or 303. Open PRs #585, #587, #591 change no bound lane at these counts (they add regularization drawing metadata to n-129, n-204, n-303).

Validation plan (priced): sqcert adapter exists; both maintained exact routes (upper_bound_reports certify, then check --replay), --workers 1: 9 jobs, priced from #528's 9 jobs (26 min at load 15-20). Third exact route (check_half_angle_area IMPORTS roster) is the records lane's. Source programs (C++ GMP sqverify, mpmath cross-check) pinned against the #501 packet, not run. W2 review as for #501.

## Draft acknowledgement (not posted)

Thank you, Daniil. We received the three certificates at dostashev/square-packing fe43a64 (records/n0129, n0204 and n0303), and the six SHA-256 values match the files there. We will retain that commit, read each .sqcert exactly, and decide each packing with a duplicate-square and an outside-container control on our two maintained exact routes, then on a third exact route in review. We will compare each side with the record at its count and with the other reports open at it. We note that your head, b909e1b, rewrites these three files in canonical form at the same exact sides; we keep the bytes this issue names. We will also keep the 176 composition in the packet, unregistered, as you asked.

## Stage 2 and the stage 4 replay, 2026-10-14, lane ostashev (branch claude/wizardly-meitner-wqn4x3-intake-1014-ostashev, head 8d396177b, rebased on main f73e9de13)

Packet packing/resources/web/dostashev-compositions-2026-10-12 (source key [Ostashev compositions 2026-10-12], evidence E-ostashev-562-certificate-report): README, LICENSE and records/n0129, n0176, n0204, n0303 retained (10 files, 564,351 bytes); 36 files pinned identical to the #501 packet, #528's 175/232/264 by digest only. acquire_source --check passes. claims.json frozen against main aeef99ef0 (unchanged when rewritten on f73e9de13).

certify --workers 1: 9 jobs (129, 204, 303), all 3 positives pass and all 6 controls refused on both routes, 448,290 pair decisions, 363.99 route CPU s, 7m38s wall at load 10-14; least wall clearance >= 5.00e-21, pair >= 4.99e-21 on both routes. check --replay: 9 jobs equal, 7m04s. The unrequested 176 is compared, not replayed (3 jobs, about 3 min).

Register plan: scratchpad register-plan-dostashev-compositions-2026-10-12.yaml (T-NNN over 129, 204, 303; published 2026-10-12).

## Stage 1 acknowledgement posted, 2026-10-14

https://github.com/jlevy/squares/issues/562#issuecomment-6165052232 (states the pin, the retained and replayed certificates with controls refused, and the comparison at each count; the earlier draft above was not posted as written).

Registered on 2026-10-14 in the 14 October records PR (branch claude/wizardly-meitner-wqn4x3-records-1014): T-162 at 129, 204 and 303, V0/C0, S3.
