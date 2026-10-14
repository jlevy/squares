---
type: is
id: is-01m4xpw60d6b166a3xvv0n8rn2
title: "Validate: wand125 closed form, calibration replay of the two smallest replay4d records with the build (~1 CPU-h)"
kind: task
status: in_progress
priority: 2
version: 4
delegate: serene-hopper-vcheap
labels:
  - validation
  - result-import
dependencies:
  - type: blocks
    target: is-01m4xpwnpsr6echsj2ex1s947k
parent_id: is-01m4wv28mebp8r7ss9p8r6dgxy
hold: null
hold_until: null
created_at: 2026-10-14T17:20:33.292Z
updated_at: 2026-10-14T17:32:14.103Z
started_at: 2026-10-14T17:32:14.102Z
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
