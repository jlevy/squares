---
type: is
id: is-01m0na7h19jnbnw50yv13vgcg4
title: Build and run FrankenSim to verify claims firsthand
kind: task
status: closed
priority: 2
version: 2
spec_path: docs/project/research/research-2026-08-22-frankensim-rust-toolkit-for-square-packing.md
labels: []
dependencies: []
parent_id: is-01m0na7g8gwp6hzhfapbxs2mer
created_at: 2026-08-22T18:02:50.793Z
updated_at: 2026-08-22T18:33:28.031Z
closed_at: 2026-08-22T18:33:28.031Z
close_reason: "Built and tested firsthand. The workspace does NOT resolve at its own recorded constellation pins: fs-ad requires packages named frankentorch-autograd and frankentorch-core, but the pinned FrankenTorch head names them ft-autograd and ft-core, so Cargo fails manifest resolution for every crate. Both deps are optional and off by default, so dropping the two package= renames is a sufficient fix. With it, fs-math/fs-ivl/fs-rand/fs-simd/fs-alloc/fs-evidence/fs-substrate build in 12 s on the pinned nightly and pass 652 tests with 0 failures. The bootstrap tool materialises 6 of 7 siblings (franken_numpy fails a case-folding integrity check) and correctly refuses to repurpose an existing checkout at the wrong head."
---
Compile the workspace or a representative subset, run its tests and any benchmarks, and record what actually works versus what the docs claim.
