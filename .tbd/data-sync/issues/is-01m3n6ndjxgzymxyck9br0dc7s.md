---
type: is
id: is-01m3n6ndjxgzymxyck9br0dc7s
title: "Replay evand's Lean builds: s(13) = 4 and s(32) = 6 reported kernel-checked with no hypothesis (a V5 candidate), s(21)'s reduction, and the small s(11)/s(12) bounds"
kind: task
status: in_progress
priority: 2
version: 3
labels:
  - packing
  - wand125-update
  - low-n
dependencies: []
parent_id: is-01m3n5wh72rsqd2z97m8v1vv4q
created_at: 2026-09-28T23:47:37.180Z
updated_at: 2026-09-30T20:18:10.510Z
---
evand/square-packing at 6aa82ba reports s(13) = 4 and s(32) = 6 kernel-checked hypothesis-free (commits 6e1223c, 92cc5bb: a generic box-tree verifier ZMTree in Lean), s(21) = 5 reduced in Lean to the zm_mixed D4 checker statement, and s(12) >= 35/9, 3920/997 and s(11) >= 3040/797 kernel-checked. epistemics.md's V5 is 'proof-assistant checked': building the Lean project here (elan, Mathlib cache or a full build) and running lake env lean Axioms.lean would support V5 for s(13) and s(32) if the statements are the standard ones. Decide after Session 161's Lane 2 reports whether the toolchain and Mathlib cache are reachable from this environment.

## Notes

2026-09-30 progress (branch claude/determined-goldberg-ura2ed, PR jlevy/squares#249):

- Toolchain reachable: elan 4.2.4, leanprover/lean4:v4.33.1, Mathlib 0df444a3; `lake exe cache get` fetched all 8,690 Mathlib files from lakecache.blob.core.windows.net in six minutes. Setup and results table: packing/resources/web/evand-square-packing-2026-09-28/README.md, "Lean, built here on 30 September"; logs in receipts/lean/.
- DONE, s(13) = 4: `SquarePacking.s13_eq_4 : minSide 13 = 4` built (6,255 s wall, 3,978 s CPU), depending only on propext, Classical.choice, Quot.sound. Recorded as E-n013-evand-casefree-cover-lean-kernel; T-006 is now V5/C3, the register's first V5. Independent review: docs/project/reviews/review-2026-09-30-lean-s13.md.
- DONE, default target + Axioms.lean: built; all 101 printed lines are standard axioms or a subset. That includes s21_eq_five_of_checker and s32_eq_six_of_checker (implications from a checker hypothesis, not values) and s(12) >= 35/9, 3920/997 (both below the registered s(12) bound).
- PARTIAL, s(11) >= 3040/797: points file and 22 of 48 parts built; part 22 exceeds the 6 GB per-process guard. Below the registered s(11) bounds (Wang and Li's strict bound, now T-061, and T-060's exact s(11) = T), so no register change is waiting on it.
- NOT STARTED, s32_eq_6 hypothesis-free: the source's 96-part layout needs > 6 GB per process. Plan from a 12-root probe: regenerate as ~320 parts of ~19 chunks, 14-28 CPU-hours, ~4 GB per process, generator 8-10 GB. It would put the s(32) = 6 entry at V5. It waits for the s(21)/s(45) zm_mixed re-sweeps (think-l6la) to free the CPU.
- Open question for the owner: think-74kl (whether a kernel check counts toward C).
