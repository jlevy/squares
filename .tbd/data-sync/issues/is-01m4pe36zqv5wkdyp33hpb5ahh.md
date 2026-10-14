---
type: is
id: is-01m4pe36zqv5wkdyp33hpb5ahh
title: Survey wand125 and evand repositories for unimported results and proofs (2026-10-11)
kind: task
status: closed
priority: 1
version: 5
delegate: claude-code@vm
labels:
  - result-import
dependencies: []
parent_id: is-01m4padgs7fh6ze3tbh57d5ar1
hold: null
hold_until: null
created_at: 2026-10-11T21:32:25.463Z
updated_at: 2026-10-12T23:38:31.101Z
started_at: 2026-10-11T21:32:33.200Z
closed_at: 2026-10-12T23:38:31.101Z
close_reason: Survey of wand125 and evand repositories (2026-10-11) delivered in the bead notes; candidates routed to their owning lanes, nothing further to import.
resolution: null
duplicate_of: null
---

## Notes

## Survey of wand125 and evand repositories, 2026-10-11 (lane X, Claude Opus 5.5)

Heads read (blobless clones, no author code run):

- wand125/square-packing 04fbef0d4e8fc33d628c7fe626605e7fbbbf3250 (2026-10-11T11:29Z), the merged home of ten repositories; INDEX.json read whole (445 square-lower-bounds certificates).
- evand/square-packing 675a5eaa8712542daac8b4515b0f69ad7044df44 (2026-10-11T16:34Z); every .cert file outside batch/ and raw/ parsed, plus the 324 regularize lists.
- wand125/n11-optimality-lean main ee96259 and split 8126ef4 (2026-10-02); wand125/square-packing-1 (fork of evand's; branches valid7-followup 4eb59c4, wand125/valid7-kernel 45d8c39, wand125/mixed-checker 8ce6b6c, wand125-links-merged-repo af70592); evand PRs #5 (closed), #6 (merged 060c1a1), #7 (open).
- Archived and moved (MOVED.json, no content past the merge): square-packing-bounds, square-packing-density-bounds, valid7-independent-check, square-packing-tools, n17-certificates, n17-bb-verifier, squares-in-triangle, squares-in-domino, squares-in-hexagon; evand/square-packing-12.
- Not square packing: wand125 solving-dosello, agd and older repos; evand open-math-problems (a tier list; no packing result), manifold-math and the rest. No gists with packing content.

Method: scratch scripts compared every INDEX.json claim (with monotone closure n <= 324) against each case record's reported and verified lower bound and every register claim; every evand certificate side against the case upper bounds and every register `s(n) <= v` claim, exactly in Fractions. The one apparent drop (n = 51 list side 5.2e-17 below the 16-digit decimal) is 7.7e-20 above the exact form (16+5 sqrt 2)/3, so not an improvement.

### New or partly owned (ranked by value / cost)

1. think-eth9 (new, P2). #446's best values at n = 19, 20, 26, 27: 1931/400, 393/80, 1111/200, 1131/200 (mixed_n19_L48275, mixed_n20_L49125, mixed_n26_L5555 at 61e37d5; mixed_n27_L5655 at bf85d6b). Above each case's lower bound by 1/400, 3/400, 1/100, 23/2000 and above T-103..T-106. Held only as evidence and #446 entries; no register entry, unlike n = 28, 29, 30 (T-142, T-132, T-143). Registration: minutes (records lane). Replay: about 13-18 CPU-hours (3.3-4.5 per certificate, from the T-142/T-143 measurements), think-ndvg's budget.
   Overlap: think-dc0p (in_progress since 2026-10-06, no label, no notes) titles the n = 19 value with three others from square-packing-bounds f8e0178; #446 (PR #450, think-ndvg) superseded it, and its T-109/T-113/T-114 references use a branch's numbering. It looks stale: close it as superseded by think-ndvg and think-eth9, if its owner agrees.
2. think-oyd4 (new, P3). Evan Daniel's Lean `s12_ge_15680_3951` (S12HLower.lean, 513bb66, 2026-09-28), hypothesis-free, three standard axioms by the source. A proof-assistant route for T-049, whose next_rung says none exists. Retained in the evand-exact-and-local-reports-2026-10-07 packet, cited nowhere. Price: generator 39 min on one core, then a build of 7.3 CPU-hours (6 h 31 min wall on 2 cores, up to 30.6 GB RSS), plus Mathlib. No Lean here.
3. think-0ayk (existing): new evidence. wand125's open PR #7 on evand (4eb59c4, 2026-10-11T05:59Z) proves ValidTilt7 from the pose tree without the Face module (generated, 47 GB to build), adds LebMassBridge, and prices the kernel rebuild of the 9,800 roots at about 6,650 CPU-hours (10,700 with generation). This is the price think-0ayk asks for. evand's static review (tasks/pr6-valid7-kernel/review-2026-10-10.md) flags forged root names as the risk and proposes an allowlist audit. A sample of 50-100 roots is about 70 process-hours by evand's estimate.

No quick items: none of these is an exact certificate or a finite check that runs in minutes here.

### Known and owned: status confirmed at the heads above

- think-wop1: mixed_n31_L59775 unchanged since 23e3186; 2391/400 is INDEX's best at n = 31, above the case value 2381/400 by 1/40.
- think-xk3f: k2m5_n59_L8/lean unchanged since f9a77b7. evand's own zm_mixed depth-34 sweep of the s(59) cover is paused at 33,725/102,400 roots (about 127 CPU-hours in total; TODO.md). Not a result.
- think-0ayk: V7 unchanged since 45d8c39 (merged 060c1a1); PR #7 above.
- think-63vx: lean/Sqpack/Exact/Packs unchanged since 6bbae37.
- think-f2bm: point_n21_L5/lean unchanged since the 7400660 merge.
- think-jtlq: search/tilings unchanged since 49907ec (964, 1092, 1228).
- think-r333, think-i85v, think-nd7g: n29 22a23c8, n28 36b85b9, n30 ff9f269 and n122 a9f76c3 unchanged; T-144's 563/50 reaches n = 126 by monotonicity (above the case's 11.24695).
- think-x4v4, think-nmfl: problems/n17 unchanged since 89676bc. Releases data/n17-kernel-batch3-v1 (837 MB) and batch4-v1 (167 MB) are #495's; data/n17-m4000256-v1 is 59 GB.
- All other INDEX bounds equal or fall below the record (n = 11, 32, 40, 60, 78, 96 below).
- No evand certificate is below the record. The 375 certificates (big1, polish) are beyond the horizon (think-1545, think-a4wq); trio126, hunt1-3, sw2, dc1, rd1 and s292_fix0a are equal or above. The n = 110 minima are at or above the record.

### Nothing to import (recorded so the next survey starts here)

- wand125's n11 Lean (lean/n11-optimality; split 8126ef4 has `sorry` units): partial, and T-060's notes already state it. Unchanged since 2026-10-02.
- tools/packing_check (cac504b): two exact checkers for algebraic packings (degree <= 3 irreducibility in method 1), used here only on grid packings. A candidate route for think-720n, not a claim.
- tools/general_pose_tree: T-059. The sqverify-net and fn1 verification folders are already in packets.
- Out of scope (container not a square): triangle (including the 10-11 s△(37) = 9 + 2/√3), right-isosceles, domino, hexagon and rectangles F_k. The rectangles' a = b ends reproduce known records.
- evand: Lean s3_eq_2, s16_ge_4, s5_ge_2_leb (trivial); Lean s11_ge_3040_797 (below T-037); unavoid13 (p(3) = 7, no half-turn-symmetric 13-point set for [0,4]^2: a method result, not a bound); S6_SKELETON, S6_LOCAL and BRANCH (negatives). GREEN_FIG34 (a703d67, 2026-10-01Z) is already credited in review-2026-10-02-green-ds7-theorem9 (G9-3); its 4.44 and 4.484 are below the record. S20_LB is superseded and reviewed 2026-10-05. The raw/ certificates of 6a8b384 are exact conversions of the #500-#506 posts, owned by those lanes. The 00ad611 Mondrian rebuild of s(126) states no new side.

Not read: wand125 and evand release assets (none downloaded; the brief's disk limits); the generated Lean roots of PR #6 and #7; notes/ and tasks/ beyond the files named.
