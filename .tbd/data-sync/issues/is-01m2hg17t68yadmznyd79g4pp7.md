---
type: is
id: is-01m2hg17t68yadmznyd79g4pp7
title: "PR #160 review D09: a forged Search ledger at large coordinates is admitted as a valid packing"
kind: bug
status: closed
priority: 2
version: 2
labels: []
dependencies: []
parent_id: is-01m2hb40z4hvrre5f0219zp1m9
created_at: 2026-09-15T02:58:42.117Z
updated_at: 2026-09-15T02:58:53.310Z
closed_at: 2026-09-15T02:58:53.310Z
close_reason: "Fixed on PR #160 in 78c338be: the validity contract gains area-bound and magnitude clauses in TypeScript and Python, Resolve refuses out-of-limit input, and search-scheduler.test.ts refuses the 2^52 grid, 1e17 point, pair, rotated and half-size forgeries on decode, summary and resume."
resolution: null
duplicate_of: null
---
Canonical defect D09 from the 2026-09-14 stack triage. Source finding: #160 R4 (High).

A forged Search ledger at large coordinates was admitted, ranked and resumed as a valid packing. `assessPackingSnapshot` had no bound on coordinate magnitude: near 2^52 a centre plus or minus half a side rounds away, so bounds, walls and pair overlaps all read 0. An n=9 ledger with a 3 by 3 grid at 2^52 + 2 + i was admitted with side 2 (below the proved 3) and became `summarizeSearch`'s best; n=1 at (1e17, 1e17) was admitted with side 0.

Files at `72629c03`: `packages/workbench/src/core/runtime-contracts.ts:128-177`, `src/core/geometry.ts:169-189`, `src/search/validation.ts:231-243`, reached through `decodeSearchOutcomes` and `src/search/scheduler.ts:72-79`; test `tests/search-scheduler.test.ts`.

Related: think-lp1x (area lower bound, whose page readout half is D11), think-i5pg (ledger decoding).
