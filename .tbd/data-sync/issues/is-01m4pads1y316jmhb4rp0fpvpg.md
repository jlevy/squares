---
type: is
id: is-01m4pads1y316jmhb4rp0fpvpg
title: "Intake 2026-10-11 reads: comments on #419, #413 and #485; #494 and #495 entered; watched repositories evand, ry-xu, wand125, itsnaka, franciscouzo, Guzhou0806 (no issue)"
kind: task
status: closed
priority: 1
version: 4
delegate: claude-code@vm
labels:
  - result-import
dependencies: []
parent_id: is-01m4padgs7fh6ze3tbh57d5ar1
hold: null
hold_until: null
created_at: 2026-10-11T20:28:17.342Z
updated_at: 2026-10-12T23:39:32.438Z
started_at: 2026-10-11T20:28:28.469Z
closed_at: 2026-10-12T23:39:32.437Z
close_reason: "Delivered in PR #512 (merged 2026-10-12): the 2026-10-11 comment and watched-repository reads recorded, #494 and #495 entered in result-requests.yaml; follow-ups are think-wop1, think-xk3f, think-0ayk."
resolution: null
duplicate_of: null
---
Unread comments: #419 evand 6104596297 (Lean binding for #419's exact forms at 6bbae37; exact verified_upper_bound requested at 41 quadratic counts; owner think-63vx), #413 wand125 6104576642 (rows 1, 2, 3, 15, 27, 33 have kernel certificates, admission #495; owner think-x4v4/think-nmfl). Enter #494 (think-lkbe) and #495 (think-nmfl) in result-requests.yaml with triage pending, held with think-x4v4. Watch reads: evand/square-packing 675a5ea (18 commits), ry-xu/square_packing 9535d65 (cube records), wand125/square-packing 04fbef0 (22 commits), itsnaka/squish-certs 56fa71f, franciscouzo/square-packing 337078c, Guzhou0806/n40-square-packing 6a65957.

## Notes

## Lane E of the 2026-10-11 intake pass (Claude Opus 5.5): the reads

Branch worktree-agent-ac898de73570860b2, from main 3a5a91a90. Records changed: packing/campaign/result-requests.yaml (#419, #413, #485, #494, #495) and packing/campaign/intake-watch.yaml (seven reads). check_requests: 53 issues, every id resolves; check_bead_tree ok.

**#419, evand 6104596297 (2026-10-11T02:25:18Z).** Mapped as lean-packs-binding-2026-10-11 (queued, bead think-63vx) and a queued ask (bead think-63vx): exact a + b sqrt d as the verified upper bound at 41 counts (35 with sqrt 2, 6 with (k + sqrt 7)/2). Read at evand/square-packing 6bbae37: lean/Sqpack/Exact/Packs/ holds 258 modules with SHA256SUMS and a README; each proves packs : exists s, peval pS s = 0, Sa <= s <= Sb, Packs n s; the 62 quadratic ones also packs_closed and minSide_le_closed through quadOK (lean/Sqpack/ExactQuad.lean, 7d047a9). Price from the author's table (search/exact/lean_batch/results.md at 6bbae37): all 258 modules 37,107 s (10.3 process-hours); the 41 of the ask 7,559 s (2.1 process-hours), longest n = 148 at 294 s; n = 129 and 146 need chunk 10 (chunks of 25 exceed 14 GB). No Lean build here. read_through moved to 02:25:18Z. Draft acknowledgement: "Thank you: the Lean binding at 6bbae37 is the theorem the 9 October updates said was missing. It is mapped in this issue's record as evidence about the configurations this issue reports, and your request for the exact quadratic side as the verified upper bound at the 41 counts is queued with the build that would confirm it (about 2.1 process-hours by your timings, with the axiom receipt and a reading of the Packs and minSide definitions); nothing changes in the register until that build runs here."

**#413, wand125 6104576642 (02:22:21Z).** Mapped as kernel-rows-2026-10-11 (queued, bead think-nmfl, blocked_on think-x4v4): rows 1, 2, 3, 15, 27, 33 have kernel certificates, filed as #495 (m5181696, m5177920, m2031888, m459873, m4000256, m6160481); row 4 still stalls under the kernel. think-nmfl added to the entry's beads; read_through moved; the notes say rows 1-3 would get the kernel route the first queued ask names a branch-and-bound route for.

**#494 (evand, 00:58:50Z), think-lkbe.** Entered with triage done: one result, wallchain-width1-negative, a float negative for the n17 hard tail (X-052 2.5), no certificate and no claim on a bound, queued for recording beside X-052 2.5 (bead think-lkbe, blocked_on think-x4v4); nothing to replay. Draft acknowledgement: "Thank you for posting the negative. It is recorded as a method result for the n = 17 hard tail, in floating point with no certificate, and will be noted beside X-052 section 2.5 when the n = 17 intake resumes, so that the width-1 relaxation is not repeated. Nothing in the register changes."

**#495 (wand125, 02:09:47Z, comments 02:10:04Z and 04:50:49Z), think-nmfl.** Entered with triage done: kernel-certificates-15 (masks listed) and kernel-certificate-m4003392 (batch4), each not registered (census-ledger candidates), queued, bead think-nmfl, blocked_on think-x4v4. Price by the author's verifier column: 13,622 s for the 15 plus 3,411 s for m4003392, about 4.7 CPU-hours of full-mode replay, plus custody of 837 MB (batch3) and 167 MB (batch4) of hosted objects: owner budget. Draft acknowledgement: "Received, thank you: fifteen kernel certificates from this repository's producer at 657cc48, each passed in full mode by the standing verifier at blob be8135f6e, hosted as data/n17-kernel-batch3-v1, and a sixteenth, m4003392, as data/n17-kernel-batch4-v1, with the one rewritten receipt field disclosed. They are recorded for admission to certified-sub-patterns.yaml by the route #472's took (custody of the hosted objects and receipts, a fresh full-mode replay under a listed verifier, about 4.7 CPU-hours by your timings, and the census counting), held with the n = 17 intake; your note on H-342 and the octagon core is passed to that block."

**#485** is think-tln9's (its notes).

**Watched repositories** (reads in intake-watch.yaml, read_on 2026-10-11):
- evand/square-packing, two reads. Through 6bbae37 (bead think-63vx): 1b9dd35 and 6bbae37 commit the 258 Packs modules (#419), including Packs/N17.lean, the module the ea1a2f2 read said no commit added yet (#375's n = 17 exact form stays held under think-x4v4); cd55295 is #494's wallchain code and a nagqe CAD test of Nagamochi's Lemma 1 (no bound). Through 675a5ea (bead think-0ayk, new): 060c1a1 merges wand125's PR #6, Valid7 in the Lean kernel (root modules from wand125's release data/valid7-lean-certs-v1, not rebuilt by evand), a kernel route to T-064's finite premise; 6a8b384 adds raw exact certificates converting the 16 records posted since 10 October (#500, #501, #503, #504, #505, #506's counts), none his own, whose imports think-ga3m, think-e59i, think-0zd4, think-4znu, think-dzre and think-om5l own; the Mondrian composer and site data. New certificates of his own: none. PR #509 (think-csds, open) vendors search/regularize and search/exact at 675a5ea.
- wand125/square-packing, two reads. Through 23e3186 (bead think-wop1, new): mixed_n31_L59775, s(31) >= 2391/400 = 5.9775 on the 2,073-direction net, above n = 31's registered 2381/400 and #446's reported 597/100; the author's pre-publication sqverify_fast run took 7,277 s. Through 04fbef0 (bead think-xk3f, new): f9a77b7, a Lean kernel proof of s(59) = 8 on Evan Daniel's mixed checker at 1718a58, new evidence for T-066; grid packing certificates for upper bounds the record holds; triangle, domino, hexagon, right-isosceles and rectangle problems out of scope; site. No n17 work past #495 and #413.
- franciscouzo/square-packing through 337078c (bead think-om5l): f311f08 (n175 rewritten to 13.767119024201, 1.70e-6 below T-140's; 308, 343, 380 added; 340, 376, 378, 379 rewritten) and 337078c (#506's values); the #506 lane's triage already lists 175, 308, 340 and 343 as imports of their own.
- itsnaka/squish-certs through 56fa71f (bead think-ga3m): aeacc6c is #500's submission; bd0c72e and 56fa71f are README links.
- ry-xu/square_packing through 9535d65 (no bead): cube packing records n = 34-36 in three dimensions, out of scope.
- Guzhou0806/n40-square-packing: head 6a65957 is the new packet's pin; no read.

New beads (parent think-mq0k, label result-import): think-wop1 (P2, s(31) >= 2391/400), think-xk3f (P3, s(59) = 8 Lean proof for T-066), think-0ayk (P3, Valid7 in the Lean kernel for T-064).
