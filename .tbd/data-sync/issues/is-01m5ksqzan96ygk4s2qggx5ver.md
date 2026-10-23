---
type: is
id: is-01m5ksqzan96ygk4s2qggx5ver
title: "Validate: Daniel's Lean proofs of Fang's Theorems 1-2 (T-236) and Ryu's Theorem 1.4, builds and axiom receipts (~2-3.5 CPU-h)"
kind: task
status: open
priority: 3
version: 1
labels:
  - validation
  - result-import
dependencies: []
parent_id: is-01m5khvjtdjf8q14f59bmd8c1k
created_at: 2026-10-23T07:13:58.613Z
updated_at: 2026-10-23T07:13:58.613Z
---
Validation part of think-57ei (Evan Daniel's unconditional Lean proofs of Kevin Fang's Theorems 1 and 2, a formalization of T-163) and think-ahr2 (his Lean proof of Ryu's Theorem 1.4, the asymptotic register's row); no issue. Created by c-lean-1023 under the 23 October intake epic, as the lane rules allow; it serves both.

## Validation
- Claim: `UnitSquarePacking.FangGlue.theorem1`, `theorem2` (FangFinal.lean, first at f4883b41) and `UnitSquarePacking.Ryu.packs_sub_8sqrt`, `packs_sub_8b` (RyuBound.lean) in evand/square-packing at 8475bdf41571c59c8c240aedaddc48e19e0e4707. Checker: Lean v4.33.1's kernel, Mathlib 0df444a3. Packet: packing/resources/web/evand-fang-ryu-lean-2026-10-18/.
- Run: stage `lean/` from the packet and the copies it names; `lake exe cache get`; `lake build Sqpack.RyuBound`; `python3 search/exact/fang_pieces.py` (the generated modules, 6.4 MB); `build_chunks.sh Sqpack.Exact.Fang.<piece> 1` for the 18 pieces; `lake build Sqpack.FangFinal`; a probe printing the axioms of theorem1, theorem2 and packs_sub_8sqrt, accepting only the three standard axioms.
- Cost: Ryu under 0.5 CPU-hours (seven modules, no certificates; an estimate from size). Fang about 1.5 to 3 CPU-hours: the pieces in about 19 minutes wall at 8 chunks in parallel at the source, at most about 2.5 CPU-hours, and a minute of generation (tasks/fang-gluing/README.md, 17 October).
- Budget status: Ryu runnable within a lane's 2 CPU-hour single run; Fang at or above it, under the owner's 40 CPU-hour item cap. Both need about 10 GB of free disk for the toolchain and Mathlib cache, which the lane's host lacked on 23 October (5.2 GB).
- Possible subset: the Ryu build alone.
- Depends on: the packet; the stage 4 review.
- Done when: receipts are committed on a branch this bead names, registered as a `replayed-here` entry on T-236 for Fang and as a CHECKED BY COMPUTATION note on the asymptotic row for Ryu, or the owner dispositions them.
- Machine note: at most about 8 GB per Fang chunk with the sweep-line cut, so one chunk at a time; never a plain `lake build Sqpack.FangFinal` from scratch (every chunk at once reached 120 of 125 GB at the source).

blocked_on: none
