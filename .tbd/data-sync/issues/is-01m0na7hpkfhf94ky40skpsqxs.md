---
type: is
id: is-01m0na7hpkfhf94ky40skpsqxs
title: Survey the author's other Rust repositories
kind: task
status: closed
priority: 2
version: 2
spec_path: docs/project/research/research-2026-08-22-frankensim-rust-toolkit-for-square-packing.md
labels: []
dependencies: []
parent_id: is-01m0na7g8gwp6hzhfapbxs2mer
created_at: 2026-08-22T18:02:51.475Z
updated_at: 2026-08-22T18:33:27.714Z
closed_at: 2026-08-22T18:33:27.714Z
close_reason: "Recorded in the FrankenSim research doc. Architecture: 166 crates / 1.89M LOC Rust in a seven-layer workspace (L0 SUBSTRATE to L6 HELM) with layer discipline, determinism class and unsafe-capsule registration all enforced by a custom xtask rather than by convention. Performance practices worth taking: thin LTO with codegen-units=1 (not fat, for determinism), no global target-feature with per-kernel FMA capsules instead (the libm-fma trap costs ~1 GFLOP/s on baseline x86-64), a strict det:: elementary-function layer with declared ULP budgets and cross-ISA golden hashes, lint-enforced bans on platform libm and on powi(|n|>3), golden hashes coupled to semantic-surface versions, and a roofline harness with measured machine axes, median-plus-IQR dispersion and a baseline-promotion protocol that refuses a loaded host. Siblings: asupersync (cancel-correct concurrency, 44 criterion benches behind an opt-in feature, 766 cargo-fuzz targets) and frankenscipy (fsci-opt local optimisers, forbid(unsafe_code)) are the two that matter here; all eight repos carry an OpenAI/Anthropic rider on their MIT licence."
---
Identify dicklesworthstone's other Rust work and pull out reusable libraries, patterns, or benchmarking practices relevant to a compute-heavy search workload.
