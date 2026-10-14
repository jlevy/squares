---
type: is
id: is-01m4wv28mebp8r7ss9p8r6dgxy
title: "Import wand125: the closed-form lower bound s(N) >= a(N) for every non-square N >= 49 (closed-form-v1, eb0fd19), with its Rust replay checker (no issue)"
kind: task
status: in_progress
priority: 1
version: 5
delegate: serene-hopper
labels:
  - result-import
dependencies: []
parent_id: is-01m4wsqt2sjrksybyz375sarb3
hold: null
hold_until: null
created_at: 2026-10-14T09:14:32.462Z
updated_at: 2026-10-14T10:07:31.210Z
started_at: 2026-10-14T09:14:41.667Z
---
Found by the 2026-10-14 watch survey (think-fxs7): wand125/square-packing problems/closed-form (eb0fd19, 2026-10-13T09:36Z): s(N) >= a(N) for every non-square N >= 49, with a Rust replay checker; gives s(k^2-1), s(k^2-2), s(k^2-3) = k for k >= 8 without Nagamochi's lemma. The survey's own evaluation of a(N) from intervals.json (50-digit decimals, not the author's checker) beats the reported lower bound at 156 counts (104-116, 125-139, 148-164, 173-191, 201-220, 230-251, 261-284, 294-319) and the verified lower bound at 189. Stages 1-2, a priced replay of the author's checker, and a mathematical review of the theorem.

## Notes

2026-10-14 stage 1-2 (intake lane wand125-cf, branch lane/wand125-cf, commit 252cb563a; not pushed). Packet: packing/resources/web/wand125-closed-form-2026-10-14/ (README.md, register-plan.md, evaluation/, receipts/).

Pin: wand125/square-packing 9a28a84bd55dc124bfa2919bb6c4fb504dda3149 (head, 2026-10-14T09:27:10Z); problems/closed-form added in eb0fd19 (2026-10-13T09:36:19Z), unchanged since. Release closed-form-v1 published 2026-10-13T09:36:02Z, 35 assets, 815,734,366 bytes: all match ASSET.json, API digests and SHA256SUMS; not retained. Bibliography key [wand125 closed form 2026-10-14] (credit wand125, lineage independent: the folder names no method it builds on; cites #295 only for Nagamochi's gap). AI: the commit names Claude Opus 5.5 as co-author; folder prose silent. MIT for the folder.

Claim map: (1) theorem s(N) >= a(N) for every non-square N >= 49 (SPEC.md 1.1) -> one lower-bound entry, scope the 264 non-square counts 50..323; (2) above reported LB at 156 counts (104-116, 125-139, 148-164, 173-191, 201-220, 230-251, 261-284, 294-319; holders Nagamochi T-007 x149, Green DS7 x5, T-080 x2) -> reported lane at 155: at n=125 the earlier pending T-144 (11.26) beats a(125)=11.25457983...; (3) above verified LB at 189 (Karakus T-083 x187, T-080 x2) -> no change until stage 4; (4) s(m^2-1)=s(m^2-2)=s(m^2-3)=m, m>=8: 33 counts equal, all already proved (T-084, T-086, T-064) -> no new entry, older claims gain a sentence; (5) a(N) > Nagamochi's capped F(N) except m^2-1, m^2-2, and > Karakus except m^2-1: stated in the claim. No a(n) above any upper bound; no open case settled.

Checks run here: release custody; the source's structure_all.py/validate_family.py unchanged on all 68 families: ALL STRUCTURE OK, 680 checks, 68 s wall / 44 CPU-s, results equal to the source's receipt, two mutations refused. Finding: the source's receipts/structure.json names validate_family.py sha256 fdd61866..., the published file is 22e55f17.... First-party evaluation/closed_form_bounds.py (sha256 1a430c09...): two exact routes (closed form; the theorem's inequality), every case bound, four controls refused: 19.5 s wall / 17.9 CPU-s; identical to the source's a_of_n.py (30 places) and site table (9 places) at all 3,498 counts to 3600.

Priced, not run: complete replay of 136 records by replay4d, 4,294 CPU-hours (source's receipts/replay.json; uncalibrated here; smallest record 0.27 CPU-h; needs crates.io and a GMP build; 18 GB unpacked) -> waits for an owner budget. Calibration on two smallest records ~1 CPU-h. Mathematical review: own lane; reading list in the packet README. Independent leaf-test checker: a W7 slice.
