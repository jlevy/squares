---
type: is
id: is-01m4xpwnpsr6echsj2ex1s947k
title: "Validate: wand125 closed form, complete replay4d replay of all 136 records (4,294 CPU-h by the source; HELD)"
kind: task
status: open
priority: 3
version: 1
labels:
  - validation
  - result-import
dependencies: []
parent_id: is-01m4wv28mebp8r7ss9p8r6dgxy
created_at: 2026-10-14T17:20:49.369Z
updated_at: 2026-10-14T17:20:49.369Z
---
Validation part of think-tsox (wand125's closed form s(N) >= a(N) for every non-square N >= 49, T-180 in the 14 October records PR #602, V0/C1 after the 14 October review). HELD by the owner's cap.

## Validation
- Claim: s(N) >= a(N) for every non-square N >= 49 (SPEC.md 1.1) as certified by the 136 records over 34 intervals of release closed-form-v1 (wand125/square-packing eb0fd19, pinned 9a28a84bd55dc124bfa2919bb6c4fb504dda3149; 35 assets, 815,734,366 B, about 18 GB unpacked). It is above the reported lower bound at 156 counts and the verified one at 189; the verified lane moves only on a complete replay here.
- Run: the source's check from problems/closed-form (ASSET.json `check`): `python3 structure/structure_all.py --assets assets`, `(cd checker && cargo +1.86.0 build --locked --release -p replay4d)`, `python3 checker/replay_all.py --assets assets --threads T --jobs J`, with resumable work directories, from the crates retained in packing/resources/web/wand125-closed-form-2026-10-14/ (replay4d 0.1.0; the 1c661b7 revision's 0.1.1 has byte-identical sources and a source hash that covers b3d_sort.rs).
- Cost: 4,294 CPU-h by the source's receipt (receipts/replay.json: one full replay, 269 runs on two machines, summed replay4d cpu_seconds), uncalibrated here; by region straddle 1,628.4, left 1,634.4, top 130.8, right 900.5. About 1,070 h of wall on this four-core host. The calibration bead think-au7j measures the ratio.
- Budget status (owner, 2026-10-14): HELD (> 40 CPU-h, awaiting the owner).
- Possible <= 40 CPU-h subset (proposal only; never to be run without the owner's word): one whole interval, which certifies that interval's bound at every count. Interval 24 [0.485, 0.49] costs 18.32 CPU-h at the source (straddle 8.66, left 6.37, top 0.33, right 2.96) and attains a(N) at 6 counts where a(N) is above the reported lower bound: 130, 154, 180, 208, 238, 270 (evaluation/outputs/counts.tsv). Interval 7 [0.38, 0.4] (28.55 CPU-h) attains it at 151, 177, 205, 266, 300. Interval 34 (49.25 CPU-h) is over the cap and carries only already-proved counts.
- Depends on: think-au7j, the calibration (build and price first); network access to crates.io; 18 GB of scratch disk; the owner's budget.
- Done when: every one of the 136 records ends REPLAY OK with the receipt's root and leaf counts (25 records as the source's 158 pieces, whose tiling the receipt lets a reader check), the structure check passes, and the evidence (same-implementation replay) is registered on T-180; result noted on think-tsox.
- Machine note: 4 CPUs shared with gates; a run > 2 wall-h should be scheduled outside a validation gate. Any interval above is many wall-hours; it needs dedicated hours or another machine.
