---
type: is
id: is-01m4ymttngabkttp59yea87pj5
title: "Validation (#610, think-ribz): build lean/S95Lower.lean on Sqpack 1718a58, held on memory (25 GB peak, host has 15 GB)"
kind: task
status: in_progress
priority: 3
version: 2
delegate: bold-ritchie-l5
labels:
  - validation
  - result-import
dependencies: []
parent_id: is-01m4padgs7fh6ze3tbh57d5ar1
hold: null
hold_until: null
created_at: 2026-10-15T02:04:06.191Z
updated_at: 2026-10-31T05:00:29.509Z
started_at: 2026-10-31T05:00:29.508Z
---
Held validation item for the #610 import (think-ribz): build the source's Lean wrapper lean/S95Lower.lean on Evan Daniel's Sqpack.

## Validation
- Claim: theorem s95_eq_10 (hcov : S95Cover) : minSide 95 = 10, with axioms propext, Classical.choice and Quot.sound, from bengreff/s95-certificate at dd7297d06adc664268c65005369b895e4ded7547 (lean/S95Lower.lean, lean/S95T_Pts.lean.gz, generator lean/mk_lean.py, build_summary.txt), retained in packing/resources/web/bengreff-s95-certificate-2026-10-15/. The data facts pts_nodup, pts_d4, segs_d4 and wsum_lt are proved by decide +kernel; S95Cover, the covering statement (CovM on centres [0,5]^2, u in [0,1/2]), is a hypothesis.
- Run: obtain Sqpack at evand/square-packing 1718a58 (no packet retains it; think-ilwc owns that read) with its lean-toolchain (Lean v4.33.1) and Mathlib pin; elan toolchain install; lake exe cache get; place the retained S95T_Pts.lean (gunzip) at Sqpack/S95T/Pts.lean and S95Lower.lean at Sqpack/S95Lower.lean, or regenerate both with python3 -I lean/mk_lean.py COVER LEANROOT 95 (it imports gen_zmmtree from Sqpack's scripts/) and compare with the retained bytes; lake build Sqpack.S95Lower under devtools.replay_receipt with /usr/bin/time -v for peak memory; then #print axioms SquarePacking.s95_eq_10. The packet's receipts/programs/lean_data_binding.py already binds the generated data to the cover.
- Cost: 20 min 35 s wall and 25,305,596 KB (25.3 GB) peak resident memory at the source (8,726 jobs, build_summary.txt); about 1 CPU-hour of build on a comparable machine, plus a Mathlib cache download of about 5 GB and about 10 GB of disk. The #594 build (S76Lower.lean) was 15 min 21 s at the source and was not built here either.
- Budget status: held on the machine, not the cap: this host has 15 GB of memory, below the 25 GB peak; the CPU cost is well under 40 CPU-h.
- Possible subset under the cap: none on this host. On a machine with at least 32 GB, the whole build runs.
- Depends on: think-ilwc (Sqpack at 1718a58 retained and read), a 32 GB machine, and the owner's word on where to run it.
- Done when: the build succeeds from retained bytes, #print axioms lists only propext, Classical.choice and Quot.sound, and the receipt (toolchain, Mathlib revision, peak memory, wall) is committed in the packet.
- What it would raise: no V or C rung. It would check in the kernel the cover's data facts and the reduction le_minSide_mixed from S95Cover to minSide 95 = 10, a conditional formalization; V5 needs S95Cover itself proved in Lean (wand125's kernel-discharge route for s(59) at the same Sqpack, think-xk3f; unpriced) and an expert formalization review.
- Machine note: memory-bound (25 GB); cannot share this host.
