---
type: is
id: is-01m4xpw60d6b166a3xvv0n8rn2
title: "Validate: wand125 closed form, calibration replay of the two smallest replay4d records with the build (~1 CPU-h)"
kind: task
status: closed
priority: 2
version: 7
delegate: serene-hopper-vcheap
labels:
  - validation
  - result-import
dependencies: []
parent_id: is-01m4wv28mebp8r7ss9p8r6dgxy
hold: null
hold_until: null
created_at: 2026-10-14T17:20:33.292Z
updated_at: 2026-10-15T19:59:00.373Z
started_at: 2026-10-14T17:32:14.102Z
closed_at: 2026-10-14T20:27:03.070Z
close_reason: "replay4d built, and intervals 26 and 14 replayed at 1.22x the source's CPU; on main with #605 (77fa15c7e). T-180's basis text is in the post-#602 records bead; think-wu73 carries the calibrated cost."
resolution: null
duplicate_of: null
---
Validation part of think-tsox (wand125's closed form, T-180 in the 14 October records PR #602). The first step of any replay4d replay: it builds the checker and prices the 4,294 CPU-h full replay on this host. Not record-changing by itself.

## Validation
- Claim: two records of closed-form-v1 (wand125/square-packing eb0fd19, pinned 9a28a84bd55dc124bfa2919bb6c4fb504dda3149): interval 26 [0.495, 0.5] region top (4,158 roots, 32,828 leaves; 0.27 CPU-h at the source) and interval 14 [0.435, 0.44] region top (3,861 roots, 91,343 leaves; 0.28 CPU-h), the two smallest of the 136 in receipts/replay.json; and the ratio of this host's CPU to the source's, which the full-replay bead think-wu73's price needs.
- Run: from the retained crates in packing/resources/web/wand125-closed-form-2026-10-14/square-packing/problems/closed-form/checker/ (Cargo.lock, locked): `cargo +1.86.0 test --locked --release -p seam4d_core -p replay4d` and `cargo +1.86.0 build --locked --release -p replay4d`; fetch release closed-form-v1 assets interval_0.495_0.5.tar.gz (4,754,979 B, SHA-256 93406cf4...51f7) and interval_0.435_0.44.tar.gz (8,328,896 B, a0e14933...f456), check them against ASSET.json and SHA256SUMS, and run `replay4d family.json top.rec --region X0 X1 Y0 Y1 --threads 1 --out summary.json` on each top record (or `checker/replay_all.py --assets assets --only 26` restricted to the top region). Record the printed source hash and the B3_PLAIN_RF setting (review finding F3). Keep the receipts in the packet (receipts/calibration/) and the archives outside Git.
- Cost: about 1 CPU-h: 0.55 CPU-h for the two records by the source's receipt (receipts/replay.json, results[].cpu_hours), plus the build: the Rust 1.86.0 toolchain, the locked crates from crates.io and GMP built from source (register-plan.md, Validation, Priced).
- Budget status (owner, 2026-10-14): runnable (<= 40 CPU-h).
- Possible <= 40 CPU-h subset: n/a (runnable as a whole).
- Depends on: network access to crates.io and the Rust toolchain host from the session (environment). No owner decision. Optionally after the 1c661b7 check (think-4wgw), so that the build can also be compared with replay4d 0.1.1.
- Done when: both records end `REPLAY OK` with the receipt's root and leaf counts, a receipt with CPU s, wall s, binary digest and source hash is kept in the packet, and the ratio to the source is written into think-wu73's Cost line.
- Machine note: 4 CPUs shared with gates; a run > 2 wall-h should be scheduled outside a validation gate. Under an hour of wall including the build.

## Notes

2026-10-14 validation lane vcheap (serene-hopper-vcheap), branch lane/validation-cheap, commit 598c8ab7c (with 99d1864dc for the gate; not pushed).

Build: rustup toolchain 1.86.0 (rustc 1.86.0 05f9846f8, minimal; rustup also self-updated). Checker trees restored in scratch from the 9a28a84 packet (0.1.0) and the 1c661b7 packet (0.1.1), each matched to its manifest by sha256sum -c (14 files). cargo +1.86.0 fetch/test/build --locked, -j 2, shared target: 28 tests pass on each (4 + 23 + 1); test 0.1.0 229.2 CPU-s incl. GMP/MPFR from source; builds 12.6 and 13.3 CPU-s; binaries d52b8d88... (0.1.0), fb84677b... (0.1.1). Build total 269 CPU-s.

Custody: interval_0.495_0.5.tar.gz 93406cf4...51f7, interval_0.435_0.44.tar.gz a0e14933...f456, SHA256SUMS 2e31850c... downloaded 17:33:34Z by release URL (gh API not enabled for that repo); equal ASSET.json; members pass their SHA256SUMS; plain files.

Replays, replay4d 0.1.0, --threads 1, B3_PLAIN_RF unset, two at once at nice 10 (load avg 12-16, ~42% of a core each):
- interval 26 [0.495, 0.5] top: REPLAY OK, 4,158 roots, 32,828 leaves; 1,178.9 CPU-s = 0.3275 h vs source 0.27 -> 1.213; wall 2,171.8 s.
- interval 14 [0.435, 0.44] top: REPLAY OK, 3,861 roots, 91,343 leaves; 1,241.7 CPU-s = 0.3449 h vs source 0.28 -> 1.232; wall 2,241.0 s.
Family digest, record digest, roots and leaves per kind equal intervals.json; printed source hash 92002e0e....
MEASURED RATE: 1.223 x the source's CPU (0.6724 / 0.55; 1.20 to 1.25 at the source's two decimals; measured under load). Complete replay: 4,294 x 1.223 = about 5,250 CPU-h here; interval 24 subset 18.32 -> about 22.4 CPU-h.

Controls on interval 26 top: first two roots alone REPLAY BAD (2) on 0.1.0 and 0.1.1 (u-range does not cover 90 degrees; root intervals not partitions); 20 leaves --leaves REPLAY OK on both; leaf 0 relabelled CORE1:Tx -> CORE REPLAY BAD (1) on 0.1.0. 0.1.1 printed f8cafeab... and env.B3_PLAIN_RF unset. Controls 6.9 CPU-s.

Total 0.75 CPU-h (build 269 s + replays 2,421 s + controls 7 s). Receipts: packing/resources/web/wand125-closed-form-2026-10-14/receipts/calibration/ (runs.json, logs, replay4d summaries, controls.json, calibration.json by devtools.audit_wand125_closed_form calibrate; 120 KB); archives and records stay in scratch. Packet README section "The Calibration Replay"; calibration-plan.md for the records lane (T-180 basis, V-wand125-replay4d note, optional sample entry).

Remaining: the ratio written into think-wu73's Cost line (proposed text in calibration-plan.md, "think-wu73"). Not done here because editing think-wu73 needs a claim, which would mark a held bead in progress; left to the coordinator. Bead left open for that step.
