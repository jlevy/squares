---
type: is
id: is-01m4qkxdf84mtkxqgh33e5edhb
title: "Import E. Summins: k = 0 at n = 11, theorems, ten refuted routes with witnesses, measured facts (#526)"
kind: task
status: in_progress
priority: 1
version: 4
delegate: claude-code@vm
labels:
  - result-import
dependencies: []
parent_id: is-01m4padgs7fh6ze3tbh57d5ar1
hold: null
hold_until: null
created_at: 2026-10-12T08:33:21.384Z
updated_at: 2026-10-12T08:58:05.219Z
started_at: 2026-10-12T08:52:51.284Z
---
https://github.com/jlevy/squares/issues/526 (2026-10-12T04:12:45Z). Esummins/packing at 651a9a54688341880e9c0dc9fcfc19f2c04cd3cb: writeup/outreach/03-k0-status.md; docs/proofs/{k0_route,ring_swap,one_flush,local_lock,swap_leaf,k0_count,...}.md; attempts/A217-torque-probe/results/witnesses217.jsonl; A232 verify_swap232.py. K0-FREE and SWAP/CELLS (Lean, standard axioms), the extremal reduction, ten negatives with witnesses, measured facts; k0_00 not closed. n = 11 is settled by T-060 and T-112; nothing here moves the case.

## Notes

## Stage 1 triage (2026-10-12, lane intake-esummins, worktree branch intake-esummins from l4 dead83f0e)

- Pin: Esummins/packing 651a9a54688341880e9c0dc9fcfc19f2c04cd3cb (master, committed 2026-10-12T04:11:54Z); head eb3ae15 adds only writeup/outreach/POSTED.md. Issue filed 2026-10-12T04:12:45Z. Licence: code MIT, documents and data CC BY 4.0. AI assistance: produced by Claude under the PI's direction.
- Claims mapped (stage 1 table):
  1. Theorems [T]: K0-FREE (a corner box met by <= 1 square exchanges at the same side into a flush corner), SWAP and CELLS (Lean `swap_packing`, `cells_swap`: theorems on std axioms per AUDIT.md, in Open/RingSwap.lean); the extremal reduction (shared with #524; `no_retreat_of_psiMin` std, the two corollaries from the axiom `locked_crowd_free`); local facts at a locked corner (PUSH and HOLD are the axiom `lemma_PUSH`; ONE-TILTED the axiom `one_tilted`; NO-VV, CROSS-PLANAR, CEIL, FLUSH with `flush_eleven_four` from the axiom `lemma_FLUSH`); n = 11: `fourcrowd_dead_of_step_kill` (theorem, std): STEP on the window plus the k1 kill excludes four-crowds. Where: structural theorems at a settled count (T-060, T-112 hold the value and uniqueness); a method record; no register entry.
  2. Negatives [F], ten routes each with a witness (torque sign rule, 12 > 11 count, sweep count, click monotonicity, capacity counts and NO-CLOSURE, handedness sums, OPPOSE, tilt floors, local charges, pocket waste). Where: a ledger of refuted routes; valuable as a record of what does not work, stays in the packet (03-k0-status.md section 2 is the table).
  3. Measured [M]: 0 of 883 free Fritz-John points are four-crowds; no teleport-stuck packing below 4.0014; every four-crowd witness has an improving corner swap (783 of 792 strictly lowering); crowd rings below 4 hold one square. Numerical; no record.
  4. The n = 11 form: STEP on the eleven converged-alive k0 cells (swap-leaf verifier verify_swap232.py, retained; the leaf cannot fire on the cells since ten roles are unboxed) and the normal-ring chain (A258 to A281) with open links (pair3 not started, STRIP2 budgeted about 5,000 CPU-h, FLOAT2 and CAP-2 axioms). Status: k0_00 is not closed; this is a gap in the lab's programme, not in the record.
- Note at the pin: attempts/A275-k0-knowledge/ holds only BRIEF.md (5.7 KB); the "1,103-line compilation" (72 [T], 17 [T-computed], 21 [M], 38 [F], 18 [C]) that 03 cites is not in the tree at this commit. A question for the lab.
- Dependencies on this record: T-060 and T-112 settle n = 11; nothing here moves the case. Their window W' uses T-037.
- Review route and price: the extremal reduction's review is the one priced in think-s1ru (#524), about half a day, and covers this issue's theorem claim; K0-FREE, SWAP and CELLS are elementary exchange lemmas (an hour to read with the Lean statements). The asks (a field certificate on [31/8, s0] conditioned on four doubly-met corners, with the 193 held four-crowds and 40 window-shaped crowds in witnesses217.jsonl as adversaries; compute for pair3 and STRIP2) are a research request and a compute request for the owner; STRIP2 at about 5,000 CPU-h is far outside any budget on record.
- Retained: packet esummins-packing-2026-10-12: writeup/outreach/03-k0-status.md, docs/proofs (k0_route, ring_swap, one_flush, local_lock, swap_leaf, k0_count, wall_torque, two_grains, handedness, cross, no_vv, realign, ring_capacity, pocket_waste, drain_flow_k0, noroom, flat_x), attempts/A217-torque-probe/results/witnesses217.jsonl (gzip), attempts/A232-swap-leaf/code/verify_swap232.py, attempts/A275-k0-knowledge/BRIEF.md, the Lean Statements/Open files.

## Acknowledgement draft (stage 1; not posted)

@Esummins, thank you. Received: the k = 0 status at n = 11, its theorems, the refuted routes with their witnesses and the measured facts, at [Esummins/packing@651a9a5](https://github.com/Esummins/packing/blob/651a9a54688341880e9c0dc9fcfc19f2c04cd3cb/writeup/outreach/03-k0-status.md), pinned at that commit; the lemma files, the swap-leaf verifier, the four-crowd witnesses and the Lean statements are retained here.

What will happen: n = 11 is settled in this record by T-060 and T-112, so nothing here is registered; the theorems and the ledger of refuted routes are retained as your record, and the extremal reduction's review is priced with the conjecture's. One question: `attempts/A275-k0-knowledge/` holds only `BRIEF.md` at the pinned commit, so the compilation the note cites is not in the retained tree. Your request for a field certificate conditioned on four doubly-met corners is a request for new work that the owner will answer.

---
_Generated by [Claude Code](https://claude.ai/code)_

2026-10-12 09:00Z: packet committed on worktree branch intake-esummins at 7d4cc96c1 (not pushed); acquire_source --check PACKET_MATCHES_ITS_CONTRACT; proposed result-requests.yaml and intake-watch.yaml entries in the lane scratch file proposed-entries.yaml (reported to the coordinator), nothing applied to the shared records.
