---
type: is
id: is-01m7g25t7fsgphrer0krqfxh46
title: "Build T-298's Lean reduction k2m5_of_valid11 here (moh63-dev k2m5-family 355f83e build log: 12 modules, ~6 GB peak per module, 14 min on 2 cores); the Lean subset of think-0h7r, under the item cap; record #973's comment 6897938053"
kind: task
status: in_progress
priority: 2
version: 4
delegate: bold-ritchie-l183
labels:
  - validation
  - result-import
dependencies: []
parent_id: is-01m684vnbc5mmkjn950c3edw3w
hold: null
hold_until: null
created_at: 2026-11-15T16:55:46.667Z
updated_at: 2026-11-15T17:41:16.637Z
started_at: 2026-11-15T16:55:47.704Z
---

## Notes

2026-11-15 17:40Z bold-ritchie-l183: stopped at the measurement, before writing a toolchain or cache; not built. The toolchain measured 3,037,354,159 bytes unpacked (devtools.lean_disk_price, receipts/lean-price/ in the k2m5 packet), and Sqpack/Basic.lean imports all of Mathlib, so the whole 0df444a3 cache (about 6.5 GB) comes with it: 9.54 GB before sources or output, over the 9 GB cap (free 9.75 GB). The closure through Sqpack.Bentz at 659ee62 is blob for blob the one built here on 3 October at about 13 GB resident with swap; the authors' build_full.log leaves it out. #973's comment 6897938053 and the 355f83e read are recorded; T-298 unchanged; think-0h7r re-priced (Lean part about 0.5 CPU-hours, about 11 GB of disk, swap or 24 GB for Sqpack.Bentz). Draft PR #999.
