---
type: is
id: is-01m5ksqq0fznqex7x78tm0ph82
title: "Validate: Hosono's zero-margin Lean proof of s(21) = 5 (T-234), build and axiom receipt (6-12 CPU-h estimate)"
kind: task
status: open
priority: 3
version: 1
labels:
  - validation
  - result-import
dependencies: []
parent_id: is-01m5khvjtdjf8q14f59bmd8c1k
created_at: 2026-10-23T07:13:50.094Z
updated_at: 2026-10-23T07:13:50.094Z
---
Validation part of think-f2bm (Hiroaki Hosono's hypothesis-free Lean proof that s(21) = 5, a formalization of T-055's point-only route; no issue). Created by c-lean-1023 under the 23 October intake epic, as the lane rules allow; it serves think-f2bm.

## Validation
- Claim: `SquarePacking.n21pts_eq_5 : minSide 21 = 5` in wand125/square-packing-bounds at 77636c63f45a90d9a829417a1722a3bf9bfef37d, `point_n21_L5/lean/zero-margin/`, on Evan Daniel's Lean library and `gen_zmtree.py` at evand/square-packing 6aa82ba457e9eaeaaa3af0833600f27f91a2fce3, certificate `n21-capture-one.txt` (SHA-256 9f631fba...). Checker: Lean v4.33.1's kernel, Mathlib 0df444a3. Packet: packing/resources/web/wand125-n21-zero-margin-lean-2026-09-29/.
- Run: stage `s12/` at 6aa82ba4 from the retained evand packets (every closure file is retained byte for byte; receipts/evand-library-closure-6aa82ba4.json lists them), then `build_zero_margin.sh` with its clone replaced by the staged tree: regenerate the 64 parts, compare with data-sha256.txt, `lake exe cache get`, build the parts one or two at a time and `Sqpack.N21PtsLower`, and `lake env lean N21PtsAxiomsZ.lean`. Accept only `[propext, Classical.choice, Quot.sound]` for `n21pts_eq_5`.
- Cost: 6 to 12 CPU-hours, central 9: generation 1,459 s on 6 workers and the kernel check about 3.5 h wall at 2 parts on the source's Apple M4 under load (its README); an estimate, not a receipt.
- Budget status: runnable under the owner's 40 CPU-hour item cap; above the 2 CPU-hour single run a writer lane of the 23 October pass may start, so it needs the coordinator's word, and a host with about 10 GB of free disk for the toolchain and Mathlib cache (the lane's host had 5.2 GB on 23 October).
- Possible subset: none needed under the cap; the generation alone (about 2.4 CPU-hours) checks data-sha256.txt and decides nothing.
- Depends on: think-f2bm's packet (pushed on claude/intake-2026-10-23-lean-sources); the stage 4 review.
- Done when: a build and axiom receipt is committed on a branch this bead names and registered as a `proof-assistant-checked`, `replayed-here` entry on T-234 (same-implementation: the source's recipe), or the owner dispositions it.
- Machine note: near 6 GB per part; one part at a time fits a 15 GB host. Not alongside a validation gate.

blocked_on: none
