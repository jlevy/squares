---
type: is
id: is-01m4xpwnpsr6echsj2ex1s947k
title: "Validate: wand125 closed form, complete replay4d replay of all 136 records (4,294 CPU-h by the source; HELD)"
kind: task
status: open
priority: 3
version: 3
labels:
  - validation
  - result-import
dependencies: []
parent_id: is-01m4wv28mebp8r7ss9p8r6dgxy
created_at: 2026-10-14T17:20:49.369Z
updated_at: 2026-10-15T19:58:21.277Z
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

## Notes

2026-10-14 stage 1-2 (intake lane wand125-cf, branch lane/wand125-cf, commit 252cb563a; not pushed). Packet: packing/resources/web/wand125-closed-form-2026-10-14/ (README.md, register-plan.md, evaluation/, receipts/).

Pin: wand125/square-packing 9a28a84bd55dc124bfa2919bb6c4fb504dda3149 (head, 2026-10-14T09:27:10Z); problems/closed-form added in eb0fd19 (2026-10-13T09:36:19Z), unchanged since. Release closed-form-v1 published 2026-10-13T09:36:02Z, 35 assets, 815,734,366 bytes: all match ASSET.json, API digests and SHA256SUMS; not retained. Bibliography key [wand125 closed form 2026-10-14] (credit wand125, lineage independent: the folder names no method it builds on; cites #295 only for Nagamochi's gap). AI: the commit names Claude Opus 5.5 as co-author; folder prose silent. MIT for the folder.

Claim map: (1) theorem s(N) >= a(N) for every non-square N >= 49 (SPEC.md 1.1) -> one lower-bound entry, scope the 264 non-square counts 50..323; (2) above reported LB at 156 counts (104-116, 125-139, 148-164, 173-191, 201-220, 230-251, 261-284, 294-319; holders Nagamochi T-007 x149, Green DS7 x5, T-080 x2) -> reported lane at 155: at n=125 the earlier pending T-144 (11.26) beats a(125)=11.25457983...; (3) above verified LB at 189 (Karakus T-083 x187, T-080 x2) -> no change until stage 4; (4) s(m^2-1)=s(m^2-2)=s(m^2-3)=m, m>=8: 33 counts equal, all already proved (T-084, T-086, T-064) -> no new entry, older claims gain a sentence; (5) a(N) > Nagamochi's capped F(N) except m^2-1, m^2-2, and > Karakus except m^2-1: stated in the claim. No a(n) above any upper bound; no open case settled.

Checks run here: release custody; the source's structure_all.py/validate_family.py unchanged on all 68 families: ALL STRUCTURE OK, 680 checks, 68 s wall / 44 CPU-s, results equal to the source's receipt, two mutations refused. Finding: the source's receipts/structure.json names validate_family.py sha256 fdd61866..., the published file is 22e55f17.... First-party evaluation/closed_form_bounds.py (sha256 1a430c09...): two exact routes (closed form; the theorem's inequality), every case bound, four controls refused: 19.5 s wall / 17.9 CPU-s; identical to the source's a_of_n.py (30 places) and site table (9 places) at all 3,498 counts to 3600.

Priced, not run: complete replay of 136 records by replay4d, 4,294 CPU-hours (source's receipts/replay.json; uncalibrated here; smallest record 0.27 CPU-h; needs crates.io and a GMP build; 18 GB unpacked) -> waits for an owner budget. Calibration on two smallest records ~1 CPU-h. Mathematical review: own lane; reading list in the packet README. Independent leaf-test checker: a W7 slice.


The parent of this bead is:
---
type: is
id: is-01m4wsqt2sjrksybyz375sarb3
title: "Intake 2026-10-14: evaluate every open upper-bound report per count, in report order, and record only the strongest"
kind: epic
status: in_progress
priority: PNaN
version: 16
delegate: serene-hopper
labels:
  - result-import
… [33 lines omitted]

2026-10-14 calibration (think-au7j, lane/validation-cheap 598c8ab7c). replay4d 0.1.0 replayed intervals 26 and 14 (top records) here: REPLAY OK, at 1.213× and 1.232× the source's CPU, so about 1.22× (1.20–1.25). Measured at nice 10 under load 12–16, so a quiet host may do better.
Cost (calibrated): the full replay is ≈ 5,250 CPU-h here (source: 4,294). The proposed subset, interval 24, is ≈ 22.4 CPU-h here.
Correction: 0.1.1's checker logic is unchanged, but its sources are not byte-identical: main.rs, Cargo.toml and Cargo.lock differ by the version, the env field and the b3d_sort.rs entry. Still HELD under the owner's per-item cap.

2026-10-15, evening intake pass (think-wnsv), lane D (think-ykg6): think-au7j, the calibration this bead depended on, closed on 2026-10-14 with #605, and its result is in the notes above (1.22x the source's CPU; about 5,250 CPU-h here, the interval-24 subset about 22.4 CPU-h). The dependency is removed so the sweep stops reporting it. This bead is HELD by the owner's 40 CPU-h cap and waits only on the owner's budget, and on a machine with 18 GB of scratch; the decision is not among those #543 lists, and no pull request, issue or bead stands for it, so the line below only clears the resolved dependency. The hold stands.

blocked_on: none
