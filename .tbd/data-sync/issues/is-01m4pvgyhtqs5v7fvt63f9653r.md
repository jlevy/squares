---
type: is
id: is-01m4pvgyhtqs5v7fvt63f9653r
title: Evaluate wand125's sqverify_continuous (f30cc2c) as an independent route for T-145 and s(40) > 3359/500 (#533)
kind: task
status: in_progress
priority: 2
version: 4
delegate: c-review-sqvc-1023
labels:
  - result-import
dependencies: []
parent_id: is-01m4padgs7fh6ze3tbh57d5ar1
hold: null
hold_until: null
created_at: 2026-10-12T01:27:07.066Z
updated_at: 2026-10-23T06:43:56.790Z
started_at: 2026-10-23T06:43:56.790Z
---
Found in the 2026-10-12 read of wand125/square-packing for the 2026-10-11 intake pass (think-58lu); nothing on GitHub asked. Commit f30cc2cf345a3a3f6af778925f354d9ec979868b (2026-10-12T01:00:19Z; its author name is Hiroaki Hosono), "tools: sqverify_continuous, sqverify_fast with a continuous-angle mode (v3)", the head and the only commit past the 04fbef0 read, adds tools/sqverify_continuous/ (31 files changed, all under it apart from INDEX.json and two lines each of tools/README.md and tools/THIRD_PARTY_NOTICES.md).

**What it is.** The independent continuous-angle mode wand125 described, unpublished, in his review of #485's s(40) > 3359/500 (https://github.com/jlevy/squares/issues/485#issuecomment-6111583905), now published at v3, source_sha256 1266a8b90f9a355d74772e211a7b9a52d0236b0d33cc4113d2f897d8a1044f33 (Cargo.toml, Cargo.lock, build.rs and src/*.rs; v2 a8668d70..., used in the review, differs by cargo fmt and three clippy fixes, and the n = 40 runs were redone with v3). `sqverify-fast --continuous --core B --tau T` proves that every closed square of side B in K = [0, L]^2, at every centre and every angle, captures mu(P) >= tau of a D4-symmetrized rectangle density, checks n tau > M exactly, and concludes s(n) > L/B. Method (lemmas C1 to C6 of sqverify_fast/CONTINUOUS.md): reduction to theta in [0, pi/4], t = tan(theta/2), centre (L/2 + uE(t), L/2 + vE(t)), (u, v) in [0, 1]^2; for t in [eps, T] (default eps = 10^-7, T = 83/200) an outward-rounded binary64 branch and bound over (u, v, t) boxes in 86 root ranges, with monotone angle enclosures (C2), a concave-section trapezoid lower bound at the path centre for every t of the box (C3), interval-only inside/outside classification (C4) and translation-derivative extension to the box (C5); for t in [0, eps] the concentric axis-aligned square of side A, A W(eps) <= B checked exactly, decided by the crate's exact event sweep (C6). Exit 0 VERIFIED, 1 REFUSED, 2 admission or premise error; a refused root reports an exact rational capture at its stopping pose. Trust base: the lemmas, rustc and IEEE 754 binary64; not formally verified.

**Its n = 40 examples (README, v3, Ubuntu 24.04, 6 threads, 44 minutes for all five).** c6715: T-145's density (Guzhou0806/n40-square-packing 71c97d0 certificate/certified_candidate.json, wand125's rect_n40_L67, 480 orbits), B = 199529/200000, tau = 4999/5000: VERIFIED, 86/86 roots, 110,877,174 nodes, 1,167 s; s(40) > 1340000/199529. c6718: the 6.718 density (6a65957e, 685 orbits), B = 3350/3359: VERIFIED, 118,717,888 nodes, 1,355 s; s(40) > 3359/500. Controls refused: each with every weight x 985/1000 (1 s each, exact capture below tau at a refused pose), and c6718 at B = 3348/3359 (97 s; least exact capture at a refused pose 0.99856, below tau). examples/n40/prepare.py fetches both densities over the network by commit and SHA-256 (71011d03... and 984fcd3a...), both retained here (guzhou-n40-continuous-pose-2026-10-10 and guzhou-n40-new-supports-2026-10-11 packets), so a replay here runs it with the fetch replaced.

**Licence.** The repository root LICENSE.md: no single licence, each folder keeps its own; tools/LICENSE is MIT (Copyright 2026 wand125). PROVENANCE.md: the crate code is MIT (upstream by Joshua Levy, wand125's changes under the repository's MIT); the upstream documentation copies (README.md, SOUNDNESS.md, INDEPENDENCE.md, independence-record.yaml) stay CC BY 4.0 to Joshua Levy, the squares project; CONTINUOUS.md, PROVENANCE.md, README.md, patches/ and examples/ are wand125's (MIT). Retainable in full.

**What it reuses from this repository's sqverify-fast.** The crate is tools/fine_net_verifier/sqverify_fast (this repository's packing/sqverify_fast at dee22b88, whose src/ tree 75e1fdf5 is the one the two reviews of 3 October accepted at 4ddf37d9c, plus wand125's own proof_net change, branch commit fe12e036) with the continuous mode added (patches/continuous.diff, 1,367 lines). Read here by Git blob id at f30cc2c: axis.rs (d7d18baf), exact.rs (9b4aafd9), interval.rs (1a10aa8f), oracle.rs (e4e7c5ef), rotated.rs (7fd03b33) are byte for byte this repository's at both dee22b88 and 910b6b12c (the reviewed declared-net source d97758bb); rotated_tests.rs equals dee22b88's. certificate.rs (1bbefbd8) is wand125's proof_net admission, equal to neither dee22b88's (657ef08f), f007d7afd's (9e12447e) nor 910b6b12c's (8937b493): the declared-net review's fixes DN-2, DN-4 to DN-6 and DN-9 are not in it. New: src/slab.rs (786 lines), src/slab_tests.rs (284), main.rs's options and run function (61779ec3 against 0f64e6d3), lib.rs's `pub mod slab;`. So relationship_to_generator against Guzhou0806's kernel (continuous_pose.cpp) is independent code with no shared file, but its author read that kernel while reviewing T-145 before writing this mode, and the outline is the same (branch and bound over (u, v, t), concave sections, translation derivatives, axis patch near t = 0): independent code, not an independent method, as PROVENANCE.md says. Against this repository's first-party route it is shared-components (interval arithmetic, admission and D4 expansion, the exact axis sweep, the exact oracle). It is the W7 slice GC-4 of the 10 October review (docs/project/reviews/review-2026-10-10-guzhou-n40-continuous-pose-bound.md) names, written outside the project on this repository's crate; think-gpe0 is the first-party epic it bears on.

**What it could support.** For T-145 (s(40) > 1340000/199529, V3/C3 by the producer's kernels re-run here: same-implementation) and for the 6.718 claim (think-tln9, retained and audited, not registered, whose slab replay waits on an owner budget): a second, code-distinct decision of the continuous cover, the first by code other than the producer's (GC-4). Recorded beside the rung, not a condition of it (result-import.md stage 4). Not: a distinct method, any rung 4, OBSTRUCTION.md, novelty or optimality.

**Price.**
1. Retain: a packet of tools/sqverify_continuous/ at f30cc2c (28 files, about 8,950 lines of source, tests and documents; MIT and CC BY 4.0), with its acquisition record. Minutes.
2. Soundness review (W2, a mapped review under docs/project/reviews/): lemmas C1 to C6 against src/slab.rs (786 lines) and the run function in main.rs, the root-range coverage and the split rule, the near-axis premise A W(eps) <= B and the use of axis.rs with core A over [L/2, L - A/2]^2, the downward-rounded acceptance against up(tau), and the certificate.rs difference from 910b6b12c (whether the continuous path reaches any proof_net code, and whether admission of a format T candidate there is the reviewed admission). The 10 October review of continuous_pose.cpp (195 lines read) is the model and the specification; about one review lane, a few agent-hours.
3. Build: cargo build --release --locked, minutes; check source_sha256 = 1266a8b9...; cargo test --release (its slab property tests and the upstream suite).
4. Replay here, --threads 1 on this host: c6718 about 1,355 s x 6 = at most 8,130 CPU-s (2.3 CPU-hours) and c6715 at most 7,002 CPU-s (1.9 CPU-hours) by the README's 6-thread walls, the three controls about 10 CPU-minutes; at most about 4.4 CPU-hours in all (44 minutes x 6). Each claim is measured in CPU-hours, so the replay waits for a budget the owner sets (result-import.md, Running an Intake Pass). Node counts do not depend on the thread count, so the receipts compare row for row with the README's.
5. Controls this repository adds: the 99/100 or 985/1000 mass control at every root range, and a mutated certificate refused by every checker that accepted the original (stage 4).

blocked_on: owner budget for the continuous-angle replay (about 4.4 CPU-hours for both n = 40 claims and their controls), after the soundness review

## Notes

2026-10-12, GitHub tracking (owner's request that the pass's remaining work be tracked as GitHub issues): https://github.com/jlevy/squares/issues/533 (review and replay of sqverify_continuous; the replay budget line is on https://github.com/jlevy/squares/issues/543). Tracker https://github.com/jlevy/squares/issues/544.
