---
type: is
id: is-01m3s1c1k2fsdmngp8g5fr8r1s
title: Decide whether a kernel-checked Lean proof counts toward the confirmation rung
kind: task
status: closed
priority: 2
version: 2
labels:
  - packing
  - epistemics
dependencies: []
created_at: 2026-09-30T11:32:04.834Z
updated_at: 2026-10-06T08:41:43.969Z
closed_at: 2026-10-06T08:41:43.969Z
close_reason: "Decided and done: 99b043acd (2026-09-30) 'epistemics: redefine the V and C ladders' counts proof-assistant-checked evidence as machine evidence at rung 3 (epistemics.md C3 row; check_results.py FORMAL_METHOD in _machine_proof_shaped)."
resolution: null
duplicate_of: null
---
The register's first V5 is T-006 (s(13) = 4). It rests on E-n013-evand-casefree-cover-lean-kernel: method proof-assistant-checked, origin replayed-here, built on 2026-09-30 from Evan Daniel's Lean project. check_results.py's MACHINE_METHODS is {exact-algebraic, interval-certified}, so a kernel check derives no confirmation rung above C2 by itself. T-006 reaches C3 only through the separate zmx2 replay of the same cover. Owner question from the review in docs/project/reviews/review-2026-09-30-lean-s13.md (S1): should proof-assistant-checked evidence replayed here count as machine-proof-shaped for C3/C4? It is arguably the strongest confirmation the record can hold: the kernel decides the statement from the definitions. The alternative is to keep V (what kind of check) and C (how many independent replays here) orthogonal, as epistemics.md does now. If it counts, T-006 would be C4 (Lean plus zmx2, different methods). Decide, then update epistemics.md → Confirmation and check_results.py together.
