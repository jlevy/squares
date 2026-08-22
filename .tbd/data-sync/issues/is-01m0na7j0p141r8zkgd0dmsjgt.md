---
type: is
id: is-01m0na7j0p141r8zkgd0dmsjgt
title: Assess transfer to a square-packing toolkit
kind: task
status: closed
priority: 2
version: 2
spec_path: docs/project/research/research-2026-08-22-frankensim-rust-toolkit-for-square-packing.md
labels: []
dependencies: []
parent_id: is-01m0na7g8gwp6hzhfapbxs2mer
created_at: 2026-08-22T18:02:51.798Z
updated_at: 2026-08-22T18:33:28.353Z
closed_at: 2026-08-22T18:33:28.353Z
close_reason: "Assessed with two measured experiments rather than by reading. fs-ivl's interval arithmetic proves 41 of 55 pairs of Trump's packing strictly separated and cannot settle 14 - a set identical pair-for-pair to the zero-gap contacts our own exact verifier finds, so two unrelated implementations agree exactly. fs-ivl's exact orient2d additionally shows the published 16-digit coordinates are not a valid packing: 8 pairs have no separating axis, overlapping by about 1e-16. fs-rand's counter-based streams are bit-identical across three traversal orders with O(1) seek to 2^63. Recommendation: adopt the designs, not the code - a filtered exact-predicate kernel staged like fs-ivl but over algebraic rather than f64 arithmetic, counter-based RNG keyed by logical work identity, fixed-slot tile reductions, the three-class determinism taxonomy, the powi/libm lints, and the roofline measurement discipline."
---
Decide what to adopt, adapt, or ignore for exact verification, large-scale stochastic search, and proof support; propose a concrete architecture.
