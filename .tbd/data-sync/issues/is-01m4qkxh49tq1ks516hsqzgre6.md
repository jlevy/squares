---
type: is
id: is-01m4qkxh49tq1ks516hsqzgre6
title: "Import E. Summins: geometry-before-LP toolkit for stratum trees, exact-rational leaf rules, 7.2x on closed nodes (#527)"
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
created_at: 2026-10-12T08:33:25.129Z
updated_at: 2026-10-31T11:18:18.313Z
started_at: 2026-10-12T08:52:51.295Z
---
https://github.com/jlevy/squares/issues/527 (2026-10-12T04:12:50Z). Esummins/packing at 651a9a54688341880e9c0dc9fcfc19f2c04cd3cb: writeup/outreach/05-toolkit.md; attempts/A211-coarse-tree/code/ (the live engine), A202, A203, A213, A214, A215/results/benchmark215.md, A221/notes/lane221.md; the frozen verifiers verify_case.py v1/v3/v4/v5 and verify_swap232.py. A method, not a bound: measured speed-ups; tree-node kills are exact-rational traces with no verifier clause.

## Notes

## Stage 1 triage (2026-10-12, lane intake-esummins, worktree branch intake-esummins from l4 dead83f0e)

- Pin: Esummins/packing 651a9a54688341880e9c0dc9fcfc19f2c04cd3cb (master, committed 2026-10-12T04:11:54Z); head eb3ae15 adds only writeup/outreach/POSTED.md. Issue filed 2026-10-12T04:12:50Z. Licence: code MIT, documents and data CC BY 4.0. AI assistance: produced by Claude under the PI's direction.
- Claims mapped (stage 1 table):
  1. Method: the geometry-before-LP toolkit for stratum trees (stage 0 closed-form rules, the CSP on pieces, multibox cores K' and the clip cascade, the leaf rules corner cover, no-room with lane and pocket-rooted covers, named split, role split, pocket branching, SNAP, EPS; inheritance across runs and start-node shards; integer polycore and C kernels). Where: a methods-survey item (resources README's method sources) and the packet; no register entry.
  2. Measured [M]: 7.22x geometric-mean speed-up over 11 closed nodes (A215 benchmark215.md), 5.0x on 68 no-room nodes (A221, 4,685 s to 934 s), 0 regressions over 314 replayed rows; the n = 17 costs. Engine measurements on their machine; no record.
  3. Soundness: each rule's soundness is a prose lemma in docs/proofs (forced_corners, slot_crowds, sideband, noroom and A189, corner_seal, lemma_eps, snap_rule, boxed_windows, guardline_clause, wedged_seal, k0_count, wall_torque); in Lean, `noroom_leaf`, `theorem_G`, `windows_clause_kill`, the snap_* and EPS theorems and `role_split` are theorems on std axioms, while `lemma_CT` (the clip tree), `lemma_A189_noroom` and `lemma_CORNER_COVER` are axioms (AUDIT.md). The lab states there is no verifier clause for a tree node: every tree kill in #522's scoreboard trees and #523's descent is a trace of exact-rational tests that is replayable but not independently verified.
  4. Frozen verifiers: verify_case.py v1 (retained; committed-bytes sha256 1574ddbd..., the quoted 521cb01fe656 is the CRLF digest), v3 (polygon cores, rests on a certificate clause PolycoreExemptSound), v4 (boxed windows, Theorem W, Lean end to end), v5 (guard lines, Theorem G, a soundness bug found by external review and fixed per their status sheet), verify_swap232.py; certs/verify_measure.py and verify_certificate.py (retained).
- Dependencies on this record: none; the one hard-coded n = 11 body (tree209.noroom_at with m = 11 - len(roles)) they report as unsound at n > 11 and replaced in A243.
- Review route and price: the ask is a review of one leaf rule end to end; no-room with the pocket-rooted cover (A189's lemma, A221's Lemma POCKET-DEAD and POCKET-INHERIT, the trace format in a coarsetree211 certificate) is the right first one: a mathematics-tier review of about one day, reading noroom.md, lane221.md and one retained trace. A tree-node verifier clause (their second ask, "in your verifiers.yaml terms") would be a W7 tool of the lab's or this project's making, only if the owner adopts the method. The sqverify-fast question is the owner's: sqverify-fast decides measure certificates on declared nets, and the lane cover is a float witness search for no-room (about 98 per cent of a lane run), a different object, so it is not a drop-in.
- Retained: packet esummins-packing-2026-10-12: writeup/outreach/05-toolkit.md, attempts/A211-coarse-tree/code (the live engine, 82 files), A202 and A203 (BRIEF, code, notes), A213 and A214 (BRIEF, code, notes, tests; the C kernel's build/ directory pinned by the commit), A215/results, A221/notes/lane221.md, the frozen verifiers, docs/proofs.

## Acknowledgement draft (stage 1; not posted)

@Esummins, thank you. Received: the geometry-before-LP toolkit, its leaf rules, kernels and benchmarks at [Esummins/packing@651a9a5](https://github.com/Esummins/packing/blob/651a9a54688341880e9c0dc9fcfc19f2c04cd3cb/writeup/outreach/05-toolkit.md), pinned at that commit; the engine's code, the benchmark results, the lemma files and the frozen verifiers are retained here.

What will happen: a toolkit is a method rather than a result, so no register entry is made; the soundness review of one leaf rule you ask for, no-room with the pocket-rooted cover, is priced as a review of about a day, and the owner decides whether to run it. On sqverify-fast: it decides measure certificates on declared nets, which is a different object from your lane cover, so it is not a drop-in replacement.

---
_Generated by [Claude Code](https://claude.ai/code)_

2026-10-12 09:00Z: packet committed on worktree branch intake-esummins at 7d4cc96c1 (not pushed); acquire_source --check PACKET_MATCHES_ITS_CONTRACT; proposed result-requests.yaml and intake-watch.yaml entries in the lane scratch file proposed-entries.yaml (reported to the coordinator), nothing applied to the shared records.

2026-10-31 bold-ritchie-l6 (stalled-bead triage of the 31 October intake pass, think-ztcy): Waits on the owner's accept-or-decline of #527's requests: a one-leaf-rule review, about one agent-day, which also gates #523's n = 19 climb, and whether an exact sqverify-fast sweep can replace the lane cover.
