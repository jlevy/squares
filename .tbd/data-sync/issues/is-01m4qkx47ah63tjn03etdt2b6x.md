---
type: is
id: is-01m4qkx47ah63tjn03etdt2b6x
title: "Import E. Summins: Conjecture ONE-FLUSH(n), its equivalences, reduction and evidence (#524)"
kind: task
status: open
priority: 1
version: 5
delegate: null
labels:
  - result-import
dependencies: []
parent_id: is-01m4padgs7fh6ze3tbh57d5ar1
hold: null
hold_until: null
created_at: 2026-10-12T08:33:11.914Z
updated_at: 2026-10-23T06:15:58.205Z
started_at: 2026-10-12T08:52:51.261Z
---
https://github.com/jlevy/squares/issues/524 (2026-10-12T04:12:37Z). Esummins/packing at 651a9a54688341880e9c0dc9fcfc19f2c04cd3cb: writeup/outreach/04-simple-square-conjecture.md; docs/proofs/{one_flush,ring_swap,local_lock,...}.md; lean Statements/Open/{OneFlush,LocalLock,RingSwap,RingCapacity,PocketWaste,Realign,Stuck4}.lean; attempts/A226-one-flush/. A conjecture, not a result; the extremal reduction to LOCKED-CROWD-FREE(n) is the theorem claim.

## Notes

## Stage 1 triage (2026-10-12, lane intake-esummins, worktree branch intake-esummins from l4 dead83f0e)

- Pin: Esummins/packing 651a9a54688341880e9c0dc9fcfc19f2c04cd3cb (master, committed 2026-10-12T04:11:54Z); head eb3ae15 adds only writeup/outreach/POSTED.md. Issue filed 2026-10-12T04:12:37Z. Licence: code MIT, documents and data CC BY 4.0. AI assistance: produced by Claude under the PI's direction.
- Claims mapped (stage 1 table):
  1. Conjecture ONE-FLUSH(n): for every n with s(n) < ceil(sqrt n), some optimal packing has a corner box met by at most one square. Where: no register entry (the register holds results; a conjecture is neither a bound nor a theorem). If the owner wants it noted, the place is a methods-survey or literature note (resources README, Contributed Research Packets) or an open-problems line; the packet holds it either way.
  2. Theorems [T], n-general: the four forms equivalent (one_flush.md section 1, ring_swap.md; Lean OneFlush.lean, RingSwap.lean); the extremal reduction to LOCKED-CROWD-FREE(n) (local_lock.md section 1; Lean LocalLock.lean: `no_retreat_of_psiMin` is a theorem on std axioms per AUDIT.md; `exists_optimal_singly_met` and `optimal_psiMin_not_stuck` are theorems from the axiom `locked_crowd_free`; `one_flush` itself is an axiom). Where: structural theorems, not bounds; a method record. A mathematics-tier review is the route if the owner wants the reduction on record.
  3. Negatives [F] with witnesses: every local charge (CROWD-ABOVE: four-crowds at O(eps) above every record, n = 26 to 55 verified), the counting routes (a 9-square force-balanced ring at side 4.11; NO-CLOSURE), torque and handedness invariants, monotone re-alignment, lower tilt bounds (theta_min(s) = 0 on [3.82, 4)), and the PI's second conjecture refuted (n = 5 and n = 10 are optimal with four flush corners, as are 18 later records). Where: a ledger of refuted routes; stays in the packet.
  4. Measured [M]: 0 of 883 free Fritz-John points are four-crowds; no teleport-stuck packing below side 4.0014; 783 of 792 corner swaps strictly side-lowering; 21 of 21 records below ceil(sqrt n) have >= 3 flush corners (Ellsworth's coordinates re-verified by exact SAT). Numerical and survey facts; no record.
- Dependencies on this record: the n = 11 instance uses T-060 and T-112 (the uniqueness form needs every packing at s-hat to be singly met, which T-112's statement gives since Trump's packing has three flush corners); the record survey uses Ellsworth's packings, which the atlas also holds.
- Review route and price: a mathematics-tier review of the extremal reduction (local_lock.md section 1 and LocalLock.lean: the retreat potential Psi, compactness, Fritz-John at a Psi-minimal optimum, the LOCKED residue) and the equivalence lemmas (one_flush.md section 1, ring_swap.md: SWAP, CELLS, RAISE), about half a day; it covers #526's extremal claim as well. The research asks (a threshold certificate conditioned on four doubly-met corners, a family indexed by n, an angle from the charge machinery on LOCKED-CROWD-FREE(n)) are requests for new work, for the owner to accept or decline.
- Retained: packet esummins-packing-2026-10-12: writeup/outreach/04-simple-square-conjecture.md, writeup/outreach_simple_square_conjecture.md, docs/proofs (one_flush, ring_swap, local_lock, ring_capacity, pocket_waste, cross, no_vv, wedged_seal, realign, handedness, k0_count, wall_torque), the Lean Statements/Open files, attempts/A226-one-flush (the 21-record survey, code and Ellsworth SVG data), attempts/A217-torque-probe/results/witnesses217.jsonl (the four-crowd witnesses, stored gzip).

## Acknowledgement draft (stage 1; not posted)

@Esummins, thank you. Received: Conjecture ONE-FLUSH(n) with its equivalences, the extremal reduction, the refuted routes and the survey, at [Esummins/packing@651a9a5](https://github.com/Esummins/packing/blob/651a9a54688341880e9c0dc9fcfc19f2c04cd3cb/writeup/outreach/04-simple-square-conjecture.md), pinned at that commit; the lemma files, Lean statements, witnesses and the survey are retained here.

What will happen: a conjecture is not a result the register holds, so nothing is registered; the extremal reduction and the equivalences are theorems that a mathematics review can read if the owner takes the conjecture into the record's notes, and that review is priced. Your request for a certificate conditioned on four doubly-met corners is a request for new work, which the owner will answer.

---
_Generated by [Claude Code](https://claude.ai/code)_

2026-10-12 09:00Z: packet committed on worktree branch intake-esummins at 7d4cc96c1 (not pushed); acquire_source --check PACKET_MATCHES_ITS_CONTRACT; proposed result-requests.yaml and intake-watch.yaml entries in the lane scratch file proposed-entries.yaml (reported to the coordinator), nothing applied to the shared records.
