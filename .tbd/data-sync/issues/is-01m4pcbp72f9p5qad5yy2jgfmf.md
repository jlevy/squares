---
type: is
id: is-01m4pcbp72f9p5qad5yy2jgfmf
title: "Import wand125: the Lean kernel proof of s(59) = 8 (f9a77b7), a proof-assistant route for T-066 (no issue)"
kind: task
status: open
priority: 3
version: 2
labels:
  - result-import
dependencies: []
parent_id: is-01m4padgs7fh6ze3tbh57d5ar1
created_at: 2026-10-11T21:02:06.049Z
updated_at: 2026-10-12T07:54:42.558Z
---
Found in the 2026-10-11 intake read of wand125/square-packing (think-q655); nothing on GitHub asked. Commit f9a77b7 (2026-10-11T01:42:37Z) adds problems/square-lower-bounds/certificates/k2m5_n59_L8/lean/: a generated Lean proof, theorem s59_eq_8 : minSide 59 = 8 and s59_ge_8, axioms [propext, Classical.choice, Quot.sound], no sorry and no native_decide, on Evan Daniel's mixed-measure checker (ZMTreeM.checkM, CovM, le_minSide_mixed) used unchanged at evand/square-packing 1718a580e5de2fac7e1a5535e98f11ba447d312e, over the cover n59_mixed_cover_8.txt (SHA-256 6f4d2b64...): 6,400 root cells in 290 batches, 43,154 generated files not stored (SOURCES.sha256 lists them; receipts/kernel_tasks.jsonl.gz the kernel tasks).

This is new evidence for T-066 (s(59) = 8, V3/C3 on zmx2's full replay; its claim says "It has no Lean statement"): a proof-assistant route for the lower half. Runbook row: new evidence about a registered entry, no new entry; retain the lean/ directory at f9a77b7 in a packet, read the statement binding (minSide, the cover's digest against the retained 2026-10-01 copy), and price a kernel rebuild from the generator before any rung moves (C5 needs a replay here with an axiom receipt and two expert formalization reviews). Compare think-f2bm (the same author's Lean proof of point-only s(21) = 5, bearing on T-055).

## Notes

2026-10-12, GitHub tracking (owner's request that the pass's remaining work be tracked as GitHub issues): https://github.com/jlevy/squares/issues/536. Tracker https://github.com/jlevy/squares/issues/544.
