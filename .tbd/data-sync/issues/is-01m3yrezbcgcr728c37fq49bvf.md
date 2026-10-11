---
type: is
id: is-01m3yrezbcgcr728c37fq49bvf
title: "Independent fast measure verifier: a clean-room, high-performance checker for net-direction and continuous-angle certificates"
kind: epic
status: open
priority: 1
version: 17
labels:
  - verifiers
dependencies: []
parent_id: is-01m3yrdxte02c7bnygkke34ct4
child_order_hints:
  - is-01m3yssz1abf448yycr6hj6nr9
  - is-01m3ystaq4ef5xmnmf4f802x3n
  - is-01m3ystck294q971jb9d2war1h
  - is-01m3ystff276btdyf2nxewyzyc
  - is-01m3yt01stqppbqjedb0xe3d61
  - is-01m3yt043ad0fdz31rfe5spgyx
  - is-01m3yt067qc3s5wfdc6586gebv
  - is-01m3z564t0yxdye6gt6hzsjww5
  - is-01m3z566ftxbm195y6f68b3chw
  - is-01m415rr01msa2hqba0pqxhczx
created_at: 2026-10-02T16:51:50.251Z
updated_at: 2026-10-03T20:45:20.628Z
closed_at: 2026-10-03T20:38:31.238Z
close_reason: null
resolution: null
duplicate_of: null
---
Owner requirement: an independent implementation of the verifier, made extremely fast. Slice 1 (running): spec from the reviews' mathematics, clean-room protocol producing an independence record, profile of verify.cpp / mixed_rotated_verify.cpp / unified_linear_verify.cpp, slice plan. Slice 2: Rust engine for rectangle-density certificates (f64 outward-rounded intervals, exact-rational fallback near threshold via sqpack.rectangle_density, spatial index, incremental bounds, batched evaluation, reuse across net directions), validated against every replayed rectangle certificate and all mutation controls. Slice 3: points and segments (mixed, linear). Slice 4: continuous-angle (zmx2-family) covers. Slice 5: adversarial review; record each passing certificate as confirming evidence with verifier_relation independent-implementation. Ships in the stacked PR on top of #298 (slices that finish later may follow in their own PR). Not a rung change: an attribute beside the rung (epistemics.md, Confirmation).

## Notes

Spec + profile: claude/lane-w1-verifier-spec (beads think-s333, think-fcxx closed; think-r07y adversarial reviews, think-3ok2 independence audit open). Implementation: claude/lane-w2-fast-verifier-wip (local agent W2 running; crate packing/sqverify_fast, experiment-loop registry, INDEPENDENCE.md). Clean-room rule: implementers must not read authors' checker code nor W1's dirty-side files (research-2026-10-02-author-checker-profile.md, attribution/, profile script). Headline benchmark vs verify.cpp to be run on an idle cloud runner.

2026-10-02 23:10 UTC: Milestone A complete (claude/lane-w2-fast-verifier-wip @67d7179fe): all 27 replayed rectangle-density certificates (24 wand125 + 3 Tokoharu) verify at 201 directions; every mutation control refused; SOUNDNESS.md and INDEPENDENCE.md current; gate step `measure verifier Rust (sqverify-fast)` wired. Loaded-host CPU vs verify.cpp: whole rect_n32_L595 1,457 s vs 33.7 s (43x); six single directions 28.8x. Kept: exact-admission speedup, inherited derivative bounds, branch-free rounding; 7 experiments rejected (in the ledger). Next: headline on idle runner (bench session, branch claude/bench-sqverify-fast-headline), release-build audit with fault injection (think-na5a), Milestone B points/segments (think-4vf7), verify.cpp timing at any direction (think-j1pd), Lemma R7.
- 2026-10-03 00:30 idle-host headline (branch claude/bench-sqverify-fast-headline, 4-CPU Xeon 2.1 GHz, load ~1): whole certificates rect_n32_L595 verify.cpp 1359.5 CPU-s vs sqverify-fast 28.0 (48.6x), rect_n31_L592 2127.5 vs 39.7 (53.6x); per-direction sample 33.7x (14-35x per cell), same verdicts, node counts within a few percent (the gain is per-box cost).
- 2026-10-03 Milestone B done (claude/lane-w2-fast-verifier-wip @717e4f8ca; think-4vf7 closed): formats M and L, point/segment lemmas B1-B3, direction-0 branch and bound (Z1, Z2), release audit reclassifies every item; all 6 replayed mixed/linear certificates verify at 201 directions; all controls refused; fault injection caught. CPU vs the authors' recorded replays: n76 13,096 s -> 758 s (17x), n101 27,669 s -> 128 s (216x), per-direction 22-29x on n65, n83, n84, n85. Finding: the authors' recorded n76 direction-0 minimum 1.0075130 is below the true vertex minimum 1.0075339 (conservative, not wrong). Next: census over every retained certificate; adversarial review (think-r07y) by a separate lane; independence audit and evidence (think-3ok2); Milestone C (continuous-angle zmx2 family).
