---
type: is
id: is-01m5r6x0j12j7arpqj9e8fwvr3
title: "Validate: Daniel's Lean proof of c*(k) <= 4 ceil(sqrt(2k-7)) - 1 (RyuLayers at aa12b98), kernel build and axiom receipt (<1 CPU-h, ~10 GB disk)"
kind: task
status: open
priority: 3
version: 1
labels:
  - validation
  - result-import
dependencies: []
parent_id: is-01m5khvjtdjf8q14f59bmd8c1k
created_at: 2026-10-25T00:20:52.929Z
updated_at: 2026-10-25T00:20:52.929Z
---
Validation part of think-f8py (Evan Daniel's Lean proof of c*(k) <= 4 ceil(sqrt(2k - 7)) - 1 for every k >= 7, the asymptotic register's reported row under '[Daniel k2-minus-c Lean 2026-10-18]'); no issue. Created by c-import-797-1024 under the 23 October intake epic, as the brief allows.

## Validation
- Claim: `UnitSquarePacking.Ryu.packs_sub_4sqrt2_layers` and `packs_layers` (lean/Sqpack/RyuLayers.lean, first at 4b456feee16e25e4831326a2bad5ced2122881b7, unchanged at the pin) in evand/square-packing at aa12b989aa7d4244c57ea6c3b06bb36318bd41ea. Checker: Lean v4.33.1's kernel, Mathlib 0df444a360eaa60ab8c11dca51a86af692955474 (lake-manifest.json). Packet: packing/resources/web/evand-k2-minus-c-lean-2026-10-18/ (closure receipt receipts/lean-closure.json: ten project modules, Mathlib the only outside import, no kernel-escape token).
- Run: stage `lean/` from the packet and the copies its acquisition record names (identical_to); `lake exe cache get`; `lake build Sqpack.RyuLayers`; a probe `#print axioms UnitSquarePacking.Ryu.packs_sub_4sqrt2_layers`, accepting only propext, Classical.choice and Quot.sound. Optionally `Sqpack.RyuFill` for the +5 milestone packs_sub_4sqrt2.
- Cost: under 1 CPU-hour, an estimate priced from the T-236 bead (think-dgrc: RyuBound's seven modules under 0.5 CPU-hours); this closure adds RyuFill, RyuEnds and RyuLayers (about 47 KB of Lean, maxHeartbeats 4000000 on packs_layers). The source's verify.sh says about 5 minutes from a cold Mathlib cache on 16 cores for the whole Ryu line, the staircase modules included. No build log is published.
- Budget status: runnable within a lane's 2 CPU-hour single run, but gated on disk: the toolchain and Mathlib cache need about 9-10 GB, which the importing lane's host lacked on 24 October (about 13-16 GB free, shared by four lanes).
- Possible subset: none needed; the build is one target.
- Depends on: the packet (the #797/think-f8py records PR); a host with about 10 GB free.
- Done when: a build log and the axiom probe output are committed as receipts in the packet on a branch this bead names, and the asymptotic row's note says CHECKED BY KERNEL BUILD HERE in place of REPORTED IN LEAN, or the owner dispositions it.
- Machine note: no certificates and no generated modules; memory is that of `import Mathlib`, a few GB. It can share the host with a gate.
