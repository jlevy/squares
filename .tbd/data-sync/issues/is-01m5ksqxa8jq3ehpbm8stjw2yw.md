---
type: is
id: is-01m5ksqxa8jq3ehpbm8stjw2yw
title: "Validate: Hosono's Lean kernel proof of s(59) = 8 (T-235), full build (~862 CPU-h by the source's receipt; HELD)"
kind: task
status: open
priority: 3
version: 1
labels:
  - validation
  - result-import
dependencies: []
parent_id: is-01m5khvjtdjf8q14f59bmd8c1k
created_at: 2026-10-23T07:13:56.552Z
updated_at: 2026-10-23T07:13:56.552Z
---
Validation part of think-xk3f (Hiroaki Hosono's Lean kernel proof that s(59) = 8, a formalization of T-066; no issue; GitHub tracking jlevy/squares#536 and #544). Created by c-lean-1023 under the 23 October intake epic, as the lane rules allow; it serves think-xk3f.

## Validation
- Claim: `SquarePacking.s59_eq_8 : minSide 59 = 8` in wand125/square-packing at f9a77b7d38fd60144b78fe290c94f841ab626156, `problems/square-lower-bounds/certificates/k2m5_n59_L8/lean/`, on Evan Daniel's ZMTreeM/CovM/le_minSide_mixed at evand/square-packing 1718a580e5de2fac7e1a5535e98f11ba447d312e, cover n59_mixed_cover_8.txt (SHA-256 6f4d2b64...). Checker: Lean v4.33.1's kernel, Mathlib 0df444a3. Packet: packing/resources/web/wand125-n59-lean-kernel-2026-10-11/.
- Run: the source's lean/README.md steps from the staged library at 1718a580 (all 19 closure modules retained byte for byte in the 7 October evand packet): build Pts and Attain; `run_s59.py` over 290 batches, comparing the generated files with SOURCES.sha256 (fetched at the pin); `mk_s59_cov.py`; build Cov and S59Lower; `lake env lean Axioms59.lean`, accepting only the three standard axioms.
- Cost: about 862 CPU-hours by the source's retained receipt (receipts/kernel_tasks.jsonl.gz): 94.04 generation, 767.87 Part files, 0.48 Roots.
- Budget status: HELD, above the owner's 40 CPU-hour item cap; it also needs 9.8 GB per Part process and 35 GB for Cov and S59Lower, above a 15 GB host.
- Possible subset under the cap (proposed; runs on the owner's word): `lake build Sqpack.S59T.Pts` alone, deciding the data facts (no duplicate atoms, D4 invariance, total below 59) in Lean, under an hour; it decides no covering and moves no rung.
- Depends on: think-xk3f's packet; an owner budget and a large machine for the full run.
- Done when: a build and axiom receipt is committed on a branch this bead names and registered on T-235, or the owner dispositions the build.
- Machine note: not this host for the full run.

blocked_on: none
