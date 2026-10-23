---
type: is
id: is-01m3x1fagrtcdtyfv1bcj0jtx1
title: "Import wand125: the Lean proof of its point-only s(21) = 5 (bears on T-055)"
kind: task
status: in_progress
priority: 3
version: 3
delegate: c-lean-1023
labels:
  - packing
  - result-import
dependencies: []
parent_id: is-01m3wvgebtkjqb3km59h7768zx
hold: null
hold_until: null
created_at: 2026-10-02T00:50:50.004Z
updated_at: 2026-10-23T08:27:49.858Z
started_at: 2026-10-23T06:18:59.491Z
---
Found by triage of wand125/square-packing-bounds at 1a25a5ed, requested by no issue: a hypothesis-free Lean proof of the point-only s(21) = 5 (upstream commit 77636c63, 2026-09-29). By the runbook a claim in scope that no request mentions is its own import. Evidence update to T-055; no new entry expected.

## Notes

2026-10-23, c-lean-1023 (stages 1 to 3), branch claude/intake-2026-10-23-lean-sources.

Stage 1. Pin: wand125/square-packing-bounds 77636c63f45a90d9a829417a1722a3bf9bfef37d (2026-09-29T07:16:17Z), zero-margin/ unchanged to the archived head 069f3276; the moved copy at wand125/square-packing e48de243 lacks data-sha256.txt, so the archived repository is pinned. Licence MIT (root LICENSE), Daniel's library MIT. Claim: SquarePacking.n21pts_eq_5 : minSide 21 = 5 and n21pts_ge_5, no hypothesis, source-reported axioms [propext, Classical.choice, Quot.sound]; certificate n21-capture-one.txt (SHA-256 9f631fba..., retained gz in the 2026-09-28 packet); 66 generated files (88 MB) not published, data-sha256.txt lists them. Library: evand/square-packing 6aa82ba4; devtools.lean_closure reads its closure (Basic, Chord, ZeroMargin, D4, Cover, S32Data, S32, BoxTree, ZMTree; no kernel escapes) and every file, plus gen_zmtree.py and zeromargin.py, is retained byte for byte in earlier evand packets; the four SHA-256 the build script pins agree.
Claim map: since 13 October a proof-assistant proof of a result the record holds is a formalization (epistemics.md, Result Kinds), so the triage's "evidence update to T-055, no new entry" became a new entry: T-234, formalization, proves_kind optimality, V0/C0, draft S2; evidence E-n021-wand125-zero-margin-lean-report; T-055's notes name it.
Stage 2. Packet packing/resources/web/wand125-n21-zero-margin-lean-2026-09-29/ (8 retained files, 3 pinned identical), key [wand125 n21 zero-margin Lean 2026-09-29], coverage entry wand125-n21-zero-margin-lean-2026-09-29. Packet pushed at 918d780b0; records at 1e22df80f (merged with main at 9ba8e7a85).
Price: 6 to 12 CPU-hours (central 9; generation about 2.4, kernel about 7, from the source's M4 run), near 6 GB per part, about 10 GB of disk for toolchain and cache. Not run: above the lane's 2 CPU-hour single-run limit and this host had 5.2 GB free disk. Validation bead think-tpbd (runnable under the 40 CPU-hour cap).
Stage 4 review: owed, from the packet (coordinator starts it).
