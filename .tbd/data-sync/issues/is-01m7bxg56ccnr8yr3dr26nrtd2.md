---
type: is
id: is-01m7bxg56ccnr8yr3dr26nrtd2
title: "Price and run the full replay of #973's Valid11 and Lean reduction (k2m5-family 2c0b1b9): zmx2 sweep, coverage dumps, tight-tile jobs, Lean build"
kind: task
status: open
priority: 2
version: 4
labels:
  - validation
  - result-import
dependencies: []
parent_id: is-01m7bwabjnw739a8whwmhq1sre
created_at: 2026-11-14T02:17:04.972Z
updated_at: 2026-11-14T06:54:53.460Z
---
Priced full replay of Mohsen Khalili and Sara Gharabaghi's s(k^2 - 5) = k (jlevy/squares#973), held above the import lane's budget; the import is think-2vgx (lane L145, 14 November 2026).

## Validation
- Claim: Valid11, every closed unit square in [0,11]^2 has mass >= 1 under certificate/sol_exact_box11.txt (SHA-256 d259fed5...12099), and the Lean reduction k2m5_of_valid11 : Valid11 -> forall k >= 10, minSide (k^2 - 5) = k; source moh63-dev/k2m5-family at 2c0b1b9979bcb67d92eb215366dc5ee19286c1d8, retained in packing/resources/web/moh63-dev-k2m5-family-2026-11-13 (tight_tile/cov.tar.xz pinned by digest only); checkers Evan Daniel's zmx2 (e2bb84e9) and qx2_zm.py (6294052a, with zeromargin.py 3cb95fb7) at evand/square-packing@659ee62, and the authors' Tight-Tile checker (tight_tile/).
- Run: from packing/, devtools.replay_k2m5_family stage/build, then (1) zmx2 --columns 0-54 (cert0 and the 55-column first-order D4 sweep; the lane ran a sample); (2) the 75 coverage dumps of tight_tile/run_cov.sh with --uncert-cap 100000000 and ZMX2_PRINT_ALL, which verify.sh --full does not re-run, compared with cov.tar.xz; (3) root9632 (done in the lane); (4) the 308 + 15 tight-tile jobs and the 3 out_fix reruns (tight --jobs ...), then cov_check.py on the regenerated dumps and outputs; (5) the Lean build: Daniel's lean/ at 659ee62 (toolchain leanprover/lean4:v4.33.1, lake exe cache get), then lean -o for Grid10 Fam10 InstData InstFam InstC1..InstC7 Inst in order, one per process, and #print axioms k2m5_of_valid11 accepting only propext, Classical.choice, Quot.sound; (6) the source's audit_zmx2.py on the regenerated sweep and dumps.
- Cost: about 313 CPU-hours at the source's recorded speed (zmx2 sweep 12.6, coverage dumps 18.3, root 9632 0.5, tight-tile jobs 279.8, controls about 1, Lean build an estimate of 2 to 5 with about 10 GB of disk for the toolchain and Mathlib cache and about 6 GB of memory per kernel-check module by the source); scaled by this host's measured speed in the lane's sample, see the notes. Basis: the source's recorded seconds (verification/logs/zmx2_box11/col*.out, tight_tile/cov/r*.out, tight_tile/out*/ "secs") and the lane's sample.
- Budget status: held (above the import lane's 4 CPU-hour box and the owner's 40 CPU-hour item cap); the zmx2 sweep and dumps alone (about 31 CPU-hours at source speed) and the Lean build fit under the item cap.
- Possible subset under the cap: (a) the Lean build (a few CPU-hours, disk permitting); (b) the zmx2 sweep's remaining columns and the 75 coverage dumps (about 31 CPU-hours at source speed); (c) the tight-tile jobs, about 280 CPU-hours, the bulk, or a stratified sample of them.
- Depends on: an owner budget; a hosted data release of tight_tile/cov.tar.xz (8.7 MB, over the per-blob ceiling) before receipts that compare against it are cited; the stage 4 review (think-h10k).
- Done when: every part's receipts are in the packet and compare root for root and job for job with the source's records, controls refused, a replayed-here evidence entry for Valid11 and one for the Lean build are registered, and T-298's unfinished_confirmations entry is removed.
- Machine note: single-threaded processes; the tight-tile jobs are Python and embarrassingly parallel (run_all2.sh NP), the largest job about 18 CPU-hours; the Lean modules need about 6 GB of memory each, one at a time.

## Notes

2026-11-14 06:55Z coordinator: #973 is answered and closed (T-298 merged in #974). This replay is held for the owner's budget decision, about 145 to 180 CPU-hours (up to about 320) plus the Lean build on a host with at least 24 GB; it closes only the second half of F2.
blocked_on: the owner's budget decision
