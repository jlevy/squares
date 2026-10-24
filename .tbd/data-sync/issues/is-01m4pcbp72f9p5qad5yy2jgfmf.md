---
type: is
id: is-01m4pcbp72f9p5qad5yy2jgfmf
title: "Import wand125: the Lean kernel proof of s(59) = 8 (f9a77b7), a proof-assistant route for T-066 (no issue)"
kind: task
status: open
priority: 3
version: 8
delegate: null
labels:
  - result-import
dependencies: []
parent_id: is-01m4padgs7fh6ze3tbh57d5ar1
hold: null
hold_until: null
created_at: 2026-10-11T21:02:06.049Z
updated_at: 2026-10-24T09:16:49.611Z
started_at: 2026-10-23T06:19:00.079Z
---
Found in the 2026-10-11 intake read of wand125/square-packing (think-q655); nothing on GitHub asked. Commit f9a77b7 (2026-10-11T01:42:37Z) adds problems/square-lower-bounds/certificates/k2m5_n59_L8/lean/: a generated Lean proof, theorem s59_eq_8 : minSide 59 = 8 and s59_ge_8, axioms [propext, Classical.choice, Quot.sound], no sorry and no native_decide, on Evan Daniel's mixed-measure checker (ZMTreeM.checkM, CovM, le_minSide_mixed) used unchanged at evand/square-packing 1718a580e5de2fac7e1a5535e98f11ba447d312e, over the cover n59_mixed_cover_8.txt (SHA-256 6f4d2b64...): 6,400 root cells in 290 batches, 43,154 generated files not stored (SOURCES.sha256 lists them; receipts/kernel_tasks.jsonl.gz the kernel tasks).

This is new evidence for T-066 (s(59) = 8, V3/C3 on zmx2's full replay; its claim says "It has no Lean statement"): a proof-assistant route for the lower half. Runbook row: new evidence about a registered entry, no new entry; retain the lean/ directory at f9a77b7 in a packet, read the statement binding (minSide, the cover's digest against the retained 2026-10-01 copy), and price a kernel rebuild from the generator before any rung moves (C5 needs a replay here with an axiom receipt and two expert formalization reviews). Compare think-f2bm (the same author's Lean proof of point-only s(21) = 5, bearing on T-055).

## Notes

2026-10-12, GitHub tracking (owner's request that the pass's remaining work be tracked as GitHub issues): https://github.com/jlevy/squares/issues/536. Tracker https://github.com/jlevy/squares/issues/544.

2026-10-23, c-lean-1023 (stages 1 to 3), branch claude/intake-2026-10-23-lean-sources.

Stage 1. Pin: wand125/square-packing f9a77b7d38fd60144b78fe290c94f841ab626156 (2026-10-11T01:42:37Z). Licence MIT (problems/square-lower-bounds/LICENSE; LICENSE.md says folders keep their licence). Claim: SquarePacking.s59_eq_8 : minSide 59 = 8 and s59_ge_8, no hypothesis, source-reported axioms [propext, Classical.choice, Quot.sound], no sorry or native_decide; cover n59_mixed_cover_8.txt (SHA-256 6f4d2b64..., equal to the retained 2026-10-01 copy decompressed); 43,444 generated files not stored, SOURCES.sha256 lists them. Library evand/square-packing 1718a580: all 19 closure modules (devtools.lean_closure; no kernel escapes) have the blobs of the 7 October evand packet's copies, so the library is already retained. The README's receipts/final_build.log is not in the tree; kernel_tasks.jsonl.gz has task, seconds and peak memory, no exit status: 94.04 h generation, 767.87 h Part files (max 9.8 GiB), 0.48 h Roots.
Claim map: a formalization of T-066 (Result Kinds, 13 October), so a new entry instead of the triage's evidence update: T-235, formalization, proves_kind optimality, V0/C0, draft S2; evidence E-n059-wand125-lean-kernel-report; T-066's claim no longer says "no Lean statement" and names T-235.
Stage 2. Packet packing/resources/web/wand125-n59-lean-kernel-2026-10-11/ (13 retained incl. the original gzip receipt; SOURCES.sha256 and INDEX.json pinned by digest; 5 pinned identical), key [wand125 n59 Lean kernel 2026-10-11]. The intake-watch read through 04fbef0 no longer names this bead. Packet pushed at 918d780b0; records at 1e22df80f (merged with main at 9ba8e7a85).
Price: about 862 CPU-hours (the receipt), 9.8 GB per Part and 35 GB for Cov/S59Lower: held above the cap and the host. Subset: build Pts.lean alone (data facts; no rung). Validation bead think-cs9x.
Stage 4 review: owed, from the packet.
2026-10-24 c-stage7-1024 (think-9i18, PR https://github.com/jlevy/squares/pull/787): #536's ask is marked done, with a note: the packet wand125-n59-lean-kernel-2026-10-11 (lean/ at f9a77b7, on main since #750, 2c58b6373), its README's read of the statement binding (s59_eq_8 : minSide 59 = 8, minSide and Packs from S32.lean at 1718a580), the evidence entry E-n059-wand125-lean-kernel-report under T-235 rather than T-066 (T-066's claim names T-235), and the rebuild priced at about 862 CPU-hours, held (think-cs9x). results stays [] because mapping a result to T-235 (V0/C0) would make the issue unsettled against a close_when that asks only for the packet, the entry and a price. check_requests --report: #536 closeable. Closing reply drafted for the coordinator: /tmp/claude-0/-home-user-squares/f8504540-2b5a-5f78-8968-eb4ffa4c4b64/scratchpad/stage7-1024/reply-536.md. After it is posted and recorded with the close, the record names this bead on no open issue. This bead still holds T-235's stage 4 review (C1, per its next_rung): a search finds no other bead for it (PR #770 proposes tracking issue #783), so it should not close on #536's close alone; the full build stays with think-cs9x.

2026-10-24 coord-intake-1024: released. #536's closing reply (the lost scratch draft reply-536.md) is re-drafted from main with check_requests --draft 536 after #787 merges (think-9i18's stage 7). This bead keeps T-235's stage 4 review.

2026-10-24 coord-intake-1024: #536 closed 2026-10-24T09:16:30Z with its final reply https://github.com/jlevy/squares/issues/536#issuecomment-6382429802 (posted after Pages run 40080362391 verified 6808d293a's deploy); the record rides think-mdfr's records PR. This bead keeps T-235's stage 4 review (tracked on #783).
