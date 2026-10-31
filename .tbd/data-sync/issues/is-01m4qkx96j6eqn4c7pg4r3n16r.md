---
type: is
id: is-01m4qkx96j6eqn4c7pg4r3n16r
title: "Import E. Summins: forced double meeters (Theorem FC, SLOT-CROWD) and the forced-cell traction finding (#525)"
kind: task
status: open
priority: 1
version: 6
delegate: null
labels:
  - result-import
dependencies: []
parent_id: is-01m4padgs7fh6ze3tbh57d5ar1
hold: null
hold_until: null
created_at: 2026-10-12T08:33:17.010Z
updated_at: 2026-10-31T11:18:04.288Z
started_at: 2026-10-12T08:52:51.272Z
---
https://github.com/jlevy/squares/issues/525 (2026-10-12T04:12:41Z). Esummins/packing at 651a9a54688341880e9c0dc9fcfc19f2c04cd3cb: writeup/outreach/02-ladder-requirements.md; docs/proofs/{slot_crowds,forced_corners,sideband,wall_torque,wedged_seal,lemma_eps,snap_rule}.md; attempts/A238-k4-benchmark/{notes,results}, A241-row-cascade/results/rows241.md; lean slot_crowd_stmt, fc_transfer_stmt, snap_dead, gate. n-general lemmas about strata, measured traction, one refuted cascade rule; no bound.

## Notes

## Stage 1 triage (2026-10-12, lane intake-esummins, worktree branch intake-esummins from l4 dead83f0e)

- Pin: Esummins/packing 651a9a54688341880e9c0dc9fcfc19f2c04cd3cb (master, committed 2026-10-12T04:11:54Z); head eb3ae15 adds only writeup/outreach/POSTED.md. Issue filed 2026-10-12T04:12:41Z. Licence: code MIT, documents and data CC BY 4.0. AI assistance: produced by Claude under the PI's direction.
- Claims mapped (stage 1 table):
  1. Theorems [T], any n: Lemma SLOT-CROWD (a packing containing the pins of a class S but not those of a closed extension S + p, with p Young-completable, unclipped, not a pin and usable, meets int B_p(m) with >= 2 non-pin squares; proof by teleporting the lone meeter into the slot square) and Theorem FC (the same on the dilated page with pad pi_i = (lambda_max - 1)(i + 1 + 1/sqrt 2)). Lean: `slot_crowd_stmt` and `fc_transfer_stmt` are theorems on std axioms (AUDIT.md); `theorem_FC` itself (Open/TheoremFC.lean) is an axiom, so the full padded statement is prose plus its transfer step in Lean. Where: structural lemmas about strata, not bounds; a method record. No register entry.
  2. Measured [M]: traction = closed one-slot extensions (corners4 0 of 8; k4_08 and k4_11 5 of 7; every k <= 3 class 0); on k4_11 A100's LP-unkillable cells die at the root by geometry in 13 to 16 s. Numerical engine facts; a ledger note at most.
  3. Negative [F]: "every one-slot extension of C dead implies C dead" is unsound (a packing of class exactly C has no (k+1)-th simple square). Correct as stated; a ledger note. Also: the crowd-counting certificate CS does not certify (B2 to B4 FAIL with 30 to 32 exact holes).
  4. Exact statements with Lean names: ONE-TILTED (Lean axiom `one_tilted`; the two-line proof is elementary), WEDGED-SEAL (theorem `wedged_seal` from the axiom `lemma_PUSH`), Lemma EPS (theorems, std), Rule SNAP (`snap_step`, `snap_dead`, `snap_diag_two`, theorems, std). Method record.
- Dependencies on this record: none beyond the windows (T-037 for W'); the lemmas are n-general.
- Hand check here: SLOT-CROWD's argument is sound as stated, given its hypotheses: the slot square at p lies in the container, meets no pin's interior (unclipped), and is interior-disjoint from every square that misses int B_p(m), so replacing the single meeter (or, if none, any non-pin square, which needs n - k >= 1) by the slot square is a packing at the same side containing T's pins; T dead on a window containing m is the contradiction. The pad formula needs the dilation lemma (closed_disjoint_bridge.md B.0): a reviewer should check that a unit square meeting the box at side m lands, after dilation by lambda <= lambda_max, within (lambda_max - 1)(i + 1 + 1/sqrt 2) of its image, which is the slot corner's offset plus a half-diagonal.
- Review route and price: a mathematics-tier review of forced_corners.md section 0 and slot_crowds.md section 2 with the dilation lemma, about two hours; the traction measurement needs no review. The asks (a k-of-m charge pricing "two distinct non-pin meeters of one box"; the row cascade on a bigger machine, which PARAM-FAILed on every anchoring at the lab) are a research request and a compute request for the owner.
- Retained: packet esummins-packing-2026-10-12: writeup/outreach/02-ladder-requirements.md, docs/proofs (slot_crowds, forced_corners, sideband, wall_torque, wedged_seal, lemma_eps, snap_rule, k0_count, corner_seal, ring_swap), attempts/A238-k4-benchmark/{notes/k4_238.md, results summaries}, attempts/A241-row-cascade/{notes, results, code}, the Lean Statements.

## Acknowledgement draft (stage 1; not posted)

@Esummins, thank you. Received: Theorem FC, Lemma SLOT-CROWD, the traction finding and the four local lemmas at [Esummins/packing@651a9a5](https://github.com/Esummins/packing/blob/651a9a54688341880e9c0dc9fcfc19f2c04cd3cb/writeup/outreach/02-ladder-requirements.md), pinned at that commit; the lemma files, the benchmark and cascade notes and the Lean statements are retained here.

What will happen: these are structural lemmas rather than bounds, so no register entry is made; SLOT-CROWD's argument was read here and a short review of Theorem FC's pad against your dilation lemma is priced. Your two asks, a charge that prices two distinct meeters of one box and the row cascade on a larger machine, are requests for new work that the owner will answer.

---
_Generated by [Claude Code](https://claude.ai/code)_

2026-10-12 09:00Z: packet committed on worktree branch intake-esummins at 7d4cc96c1 (not pushed); acquire_source --check PACKET_MATCHES_ITS_CONTRACT; proposed result-requests.yaml and intake-watch.yaml entries in the lane scratch file proposed-entries.yaml (reported to the coordinator), nothing applied to the shared records.

2026-10-31 bold-ritchie-l6 (stalled-bead triage of the 31 October intake pass, think-ztcy): Waits on the owner's accept-or-decline of #525's research and compute request (a k-of-m charge for two distinct non-pin meeters of one box; the row cascade on a bigger machine), listed on #543 under E. Summins' series.
