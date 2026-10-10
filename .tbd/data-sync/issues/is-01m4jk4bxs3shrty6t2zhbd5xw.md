---
type: is
id: is-01m4jk4bxs3shrty6t2zhbd5xw
title: "Import Mishapolk: 28 packings below the register at n = 84-306 (#470)"
kind: task
status: in_progress
priority: 1
version: 4
delegate: claude-code@vm
labels:
  - result-import
dependencies: []
parent_id: is-01m4jk37jkzx9bzdws5jj72qg7
hold: null
hold_until: null
created_at: 2026-10-10T09:43:28.441Z
updated_at: 2026-10-10T10:52:28.316Z
started_at: 2026-10-10T09:49:27.753Z
---
Issue https://github.com/jlevy/squares/issues/470 (opened 2026-10-09, errata 2026-10-09). Corrected certificates at Mishapolk/square-packing-records dd3da5c (the 4e1a601 square-199 and square-263 overlapped, found by squarepacker's 60-digit check). Decimal pose files rounded up to 12 decimals; n = 105 closed form withdrawn; n = 88 ties SQUISH at 12 decimals. Needs rational witnesses or a declared dilation before any exact replay. Stages 1-3.

## Notes

2026-10-10 stage 1-2 lane (intake W1, branch worktree-agent-af22382952a5d839e; tool commit 7ae63ff73 + allowlist 899bdecd1, packet commit 115d07d1d).

PIN DISCREPANCY: the issue's errata pin dd3da5c7b39f3796d19e0970bc2350ef9ea14ad has 39 hex digits; the GitHub API answers 422 "No commit found". The corrected certificates are at dd3da5c753c5ded6cb3b89476193b7b801005415 (tree db3e1d43e22924153213d7a50ed085febadf2eb0, committed 2026-10-09T08:56:05Z): shares the first 8 digits, is main/HEAD (ls-remote), is the only commit after 4e1a601 changing square-199.txt and square-263.txt, and its 28 pose files have exactly the 28 SHA-256 digests the issue lists. Commits: 4e1a601 07:20Z (28 poses), 2b76e6f 08:26Z (343-360), 06b484b 08:47Z (132, 267), dd3da5c 08:56Z (199, 263 re-quenched). square-199.svg and square-263.svg were not updated and still draw the 4e1a601 poses. No licence file: derived-only custody.
PACKET: packing/resources/web/mishapolk-decimal-poses-2026-10-09 (96 files pinned only; acquire_source --check passes) with receipts/decimal-pose-margins.json (30 in-horizon poses) and receipts/decimal-pose-margins-4e1a601-control.json.

CLAIMS IN THE RELEASE: the issue's 28 (S_n = printed side rounded up at 12 places; all 28 equal the files), plus 132 (S=11.986956226066) and 267 (16.838828608296) in README and certificates/ but not in the issue, plus 18 poses at 343-360 whose printed sides are all >= 19.000000000004, above the grid bound s(n) <= 19 for n <= 361 (beyond the corpus and above a trivial bound: no action). README misprints 349-358 as 19.000000000004 (files: 19.143 to 19.265). #476 cites Mishapolk 132/267 as 11.986956226077/16.838828608311, matching neither file.

FORMAT: decimal centre-angle poses in Ellsworth's text format ("s: S", "Square K: x=X, y=Y, deg=D"), box [-s/2, s/2]^2, 16 decimals (36 at 132, 199, 263, 267). Not exact witnesses.
MEASUREMENT (devtools.decimal_pose_margins, interval arithmetic at 60 digits; receipt check reproduced in 4.5 s): at the printed side 11 are proved packings (86, 88, 103, 105, 132, 153, 179, 199, 258, 263, 267) and 19 are not: 12 with overlapping pairs (deepest -1.28e-15 at 127) and 17 with corners outside (deepest -1.20e-15 at 306). With centres dilated by lambda = S_n/s to the issue's 12-decimal ceiling, all 30 are proved packings; least pair gap >= 6.6e-16 (238), least wall >= 4.7e-16 (84). Control: the 4e1a601 square-199/263 are proved not packings at s and at their ceilings; deepest 199 pairs 15-35 -5.0127e-10 and 24-35 -2.3122e-12, 263 -1.3612e-6 (173-246, 192-246), 130 pairs: matches squarepacker's comment.
EXACT WITNESS REQUIRES: centres dilated about the box centre by lambda = S_n/s (exact rational) and each angle replaced by a rational half-angle tangent (>= 30 digits moves no corner by more than ~1e-29, far inside every margin), then the two-route exact replay; or sqpack.witness.promote_rational on a Witness/v2 decimal center-angle (degrees, container-centre origin) with max_side_increase S_n - s. No exact witness built yet.

CLAIM MAP (S_n vs case verified ceiling at main 657cc4861 and pending reports):
smallest known: 103 (10.679232047362, 1.487e-10 below Ryan Xu 10.6792320475106793), 258 (16.563448002138, 1.154e-12 below SQUISH 16.5634480021391540).
below case, beaten by an EARLIER Couzo certificate (T-128 #451 / T-130 #460, 2026-10-08): 84, 86, 105, 175, 270 (T-130); 108, 127, 131, 180, 306 (T-128). Printed sides sit 4.6e-16 (127) to 7.9e-12 (175) above those certificates, and 1.3e-7 above T-130 at 270.
below case, beaten only LATER: 132 and 267 by #476 (Couzo 2026-10-09T20:28Z, started from Mishapolk's 132), 302 and 303 by #481 (SQUISH 21:23Z; #476 also smaller at 303); 131 and 270 also beaten by #481.
not below the case's verified ceiling (no action, stays in packet): 88 (+7.53e-13 vs Gupta; the issue's tie is with SQUISH's display), 130, 153, 154, 179, 199, 207, 208, 209, 236, 237, 238, 239, 263. Printed sides at 130, 208, 238, 239 lie within 1e-15 of Gupta's sides; the replaced 4e1a601 199 printed Gupta's side cut at 16 places. Sides compared only; poses not compared; no priority finding.
Register action proposed: one upper-bound entry whose scope covers the 16 counts below the case ceiling (84, 86, 103, 105, 108, 127, 131, 132, 175, 180, 258, 267, 270, 302, 303, 306) at the S_n values, standing pending adoption at 103 and 258 only; or a narrower entry at 103 and 258 with the rest recorded as superseded reports. Coordinator's call. The issue's lineage does not name Siddharth Gupta.

PRICE: interval measurement of all 30: 4.5 s. Exact witness construction plus two-route replay with controls: comparable to the Couzo #451 run (24 jobs, 1,340 squares, 6.6 min serial); for 103 and 258 alone, under a minute.

## Draft acknowledgement (2026-10-10, not posted; the owner posts it)

Thank you for the corrected files. The pin in the errata, dd3da5c7b39f3796d19e0970bc2350ef9ea14ad, has 39 hex digits and names no commit; we pinned Mishapolk/square-packing-records at dd3da5c753c5ded6cb3b89476193b7b801005415, your current main, whose 28 files have exactly the digests you list. Please say if you meant another commit. We also recorded the poses at 132 and 267, and at 343-360; the latter are all above 19, and s(n) <= 19 holds for every n <= 361 by the grid. We measured the 30 poses at n <= 324 with interval arithmetic at their printed digits. At the printed side, 19 overlap or cross the wall by up to about 1.3e-15 (rounding of the last printed digit). With the centres scaled to your 12-decimal ceilings, all 30 are proved packings. Against the record and the other pending reports, your ceiling is the smallest known side at n = 103 and 258. At 84, 86, 105, 108, 127, 131, 175, 180, 270 and 306, Francisco Couzo's exact certificates of 8 October (#451, #460) are smaller. At 88, 130, 153, 154, 179, 199, 207, 208, 209, 236, 237, 238, 239 and 263 the ceiling is not below the record's bound. At 132, 267, 302 and 303 later reports (#476, #481) are smaller. Next we will build exact rational witnesses at your ceilings and replay them by two exact routes. The repository has no licence, so we keep digests and derived measurements rather than the files. Where a pose started from a published packing, please name it so the credit can.
