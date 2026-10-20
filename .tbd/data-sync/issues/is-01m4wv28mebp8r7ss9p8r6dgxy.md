---
type: is
id: is-01m4wv28mebp8r7ss9p8r6dgxy
title: "Import wand125: the closed-form lower bound s(N) >= a(N) for every non-square N >= 49 (closed-form-v1, eb0fd19), with its Rust replay checker (no issue)"
kind: task
status: in_progress
priority: 1
version: 11
delegate: serene-hopper
labels:
  - result-import
dependencies: []
parent_id: is-01m4wsqt2sjrksybyz375sarb3
child_order_hints:
  - is-01m4xpw60d6b166a3xvv0n8rn2
  - is-01m4xpw72p25ttba77475p8s6n
  - is-01m4xpwnpsr6echsj2ex1s947k
hold: null
hold_until: null
created_at: 2026-10-14T09:14:32.462Z
updated_at: 2026-10-18T08:51:44.401Z
started_at: 2026-10-14T09:14:41.667Z
---
Found by the 2026-10-14 watch survey (think-fxs7): wand125/square-packing problems/closed-form (eb0fd19, 2026-10-13T09:36Z): s(N) >= a(N) for every non-square N >= 49, with a Rust replay checker; gives s(k^2-1), s(k^2-2), s(k^2-3) = k for k >= 8 without Nagamochi's lemma. The survey's own evaluation of a(N) from intervals.json (50-digit decimals, not the author's checker) beats the reported lower bound at 156 counts (104-116, 125-139, 148-164, 173-191, 201-220, 230-251, 261-284, 294-319) and the verified lower bound at 189. Stages 1-2, a priced replay of the author's checker, and a mathematical review of the theorem.

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
priority: P1
version: 16
delegate: serene-hopper
labels:
  - result-import
dependencies: []
child_order_hints:
  - is-01m4wsratj3p9crt698720cq6f
  - is-01m4wsrbkd61qxbpgxphckpd6v
  - is-01m4wsrcd61weyq0xjpyk4xbqv
  - is-01m4wsrd9g7qg370shbzjs41wr
  - is-01m4wsreb5h5x2ppve9gsy2d32
  - is-01m4wt3k2f29pznyxes56xh69e
  - is-01m4wt4ehr9401mzvgm1n3br4v
  - is-01m4wv278cdppm9155311gb6y5
  - is-01m4wv27yed1e2wfnq55h1avr0
  - is-01m4wv28mebp8r7ss9p8r6dgxy
  - is-01m4wv298hea3eq4fmf0qpvqw1
  - is-01m4x2z8wp9dzqk43j4gxdwr79
  - is-01m4xmr0fhhynbfzj5vj0sh358
  - is-01m4xmr1psrjaabyjsp60ccn67
hold: null
hold_until: null
created_at: 2026-10-14T08:51:21.304Z
updated_at: 2026-10-14T16:43:20.665Z
started_at: 2026-10-14T08:51:46.973Z
---
Owner's request in session 0132qkwt8gAB9vM3aQcCJLsQ (branch claude/serene-hopper-xxh80m, off origin/main f73e9de13): review every outstanding GitHub issue for intake; build one per-n ledger across all open reports; at each count, walk the reports in the order they reached the record, and record a report only where it is stronger than the record and every earlier report; a report an earlier, stronger (or equal) report already beats is not recorded unless there is a key reason, which the ledger names; track every item as beads; comment progress on the issues; finish with a summary table of every intake item, recorded or not, and why.

Coordination: the stages 1-3 imports of #521-#596 are held by the 2026-10-14 lanes of think-mq0k (session 01UXZs37jGv5vqVGADH7Gkn8, branches claude/wizardly-meitner-wqn4x3-intake-1014-*). This epic does not retain, register or renumber anything those lanes own: it supplies the ledger's verdicts to them, owns what no bead owns, and posts the progress comments. Message sent to that session 2026-10-14T08:5xZ.


2026-10-14 sweep (triage, read only): wand125 1c661b7 (12:17Z), one commit past cfcheck's 746e2c5, publishes replay4d 0.1.1. Its source_hash now covers b3d_sort.rs (f8cafeab..., 11 files; was 92002e0e..., 10 files at 9a28a84, both recomputed). Results record env.B3_PLAIN_RF, and receipts/structure.json's validate_family_sha256 is regenerated from fdd61866... to 22e55f17..., the published script's hash. b3d_sort.rs (23be1db0...) and validate_family.py are byte-identical at both commits. It answers #600 questions: Q1 yes; Q2 from 0.1.1 on (the existing 4,294 CPU-h receipts are still 0.1.0, though the file is unchanged); Q3 for future runs only. A later-revision packet retains pin 1c661b7, the 7 changed files and b3d_sort.rs, and notes that the replay receipts are at 0.1.0. No new release: closed-form-v1 (2026-10-13) stands.

## Validation backlog (2026-10-14, owner's cap: hold anything > 40 CPU-h)

Validation beads: think-au7j, the replay4d build and calibration on the two smallest records (~1 CPU-h, runnable); think-4wgw, the 1c661b7 later revision's source hashes and structure digest (<0.1 CPU-h, runnable); think-wu73, the complete replay of 136 records (4,294 CPU-h by the source, HELD; depends on think-au7j; a proposed subset is one interval, e.g. interval 24 at 18.32 CPU-h). The whole backlog is think-lh7d.

2026-10-18 W1 intake (think-xmxb): PR667 A9 notification: wand125/square-packing 3dbb4b5 (read through fbc5fc4ca042843481ec6cd3686153cfc7cd72a2) adds closed-form Lean layerA, conditional on34 LocalCovers intervals. Finite layerB not proved there. New evidence for T-180, not complete confirmation. Retain and map this source; no rebuild here.
