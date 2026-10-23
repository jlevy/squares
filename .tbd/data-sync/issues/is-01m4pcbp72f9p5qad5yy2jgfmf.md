---
type: is
id: is-01m4pcbp72f9p5qad5yy2jgfmf
title: "Import wand125: the Lean kernel proof of s(59) = 8 (f9a77b7), a proof-assistant route for T-066 (no issue)"
kind: task
status: in_progress
priority: 3
version: 4
delegate: c-lean-1023
labels:
  - result-import
dependencies: []
parent_id: is-01m4padgs7fh6ze3tbh57d5ar1
hold: null
hold_until: null
created_at: 2026-10-11T21:02:06.049Z
updated_at: 2026-10-23T08:27:52.487Z
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
