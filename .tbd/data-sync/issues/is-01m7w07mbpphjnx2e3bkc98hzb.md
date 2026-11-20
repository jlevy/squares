---
type: is
id: is-01m7w07mbpphjnx2e3bkc98hzb
title: "Import #1038: Özden's s(228) <= 15.596043116632 (jazivxt's Boxed In coordinates) at kenaznia-doga/s228-upper-bound-1559604311 46ab8bf; option D against T-301"
kind: task
status: in_progress
priority: 1
version: 5
delegate: i1038
labels: []
dependencies: []
parent_id: is-01m7khxdfnc5tynb8cjr4z7862
hold: null
hold_until: null
created_at: 2026-11-20T08:12:42.230Z
updated_at: 2026-11-20T09:17:34.042Z
started_at: 2026-11-20T08:13:34.461Z
---

## Notes

2026-11-20T08:22Z lane i1038: control plan written before any replay or control ran, SHA-256 a8b9a8c6014168a4d750b1e1e9d98899d5abfc7e11877ec7436a2c194a8d61e1 (controls-plan-1038.md, to be retained in the packet's receipts/). Before it: only sha256sum, devtools.contraction_margin and devtools.measure_identity read the certificate. Option D measured (devtools.contraction_margin): T-301's margin 3.487511e-09 (1 - lambda* 2.389354e-10); the certificate gains 4.289025e-09 on T-301, 1.2298 times the margin, so it is below T-301 shrunk to first contact: a new result under think-b0w5. Identity: nearest centres pair it one to one with T-301 under the identity of the box; 86 squares beyond 1e-3, 47 beyond 1e-2, 5 beyond a tenth (largest 0.238), turns up to 1.956 degrees. Own margin 4.39e-22.

2026-11-20T09:40Z lane i1038: stages 1-3 done on branch claude/intake-2026-11-20-import-1038, draft PR #1045 (head b30ff10152). Packet ozden-s228-upper-bound-2026-11-18; replay both routes, 11 sharp controls as the hashed plan stated (plan retained as receipts/controls-plan-1038.md). Registered as T-334 (provisional, coordinator's assignment after #1024 T-328..330 and c2 T-331..333); check_results contiguity fails on this branch only until those merge. Option D: 1.2298 x T-301's margin, 8.015e-10 below T-301 contracted -> new result. Identity: one to one with T-301 (5 squares beyond 0.1). Credit (provisional on review): found_by Ono (arrangement, measured, as T-314), improved_by jazivxt, certificate Özden; bib credit 'Ozden after jazivxt, Levy'. Held: project's think-17ex solved view at 228, 9.66e-14 below the certificate, stays a think-4z8z candidate (think-frl5 precedent). Kaggle unreachable (proxy 403). Next: map r1038's review (think-3ape) when merged, then adopt at 228 in the pass of the merge day, regularize, stamp_landed, release_pin.
