---
type: is
id: is-01m0nrjzvt5eh2rdjg2srwrst3
title: Build an open annealer on jagua-rs and point the modern search stack at s(n)
kind: task
status: open
priority: 3
version: 1
spec_path: docs/project/research/research-2026-08-22-packing-11-unit-squares.md
labels: []
dependencies: []
parent_id: is-01m0nrjz7jn0q1ktm5n7bhxbwm
created_at: 2026-08-22T22:13:46.490Z
updated_at: 2026-08-22T22:13:46.490Z
---
Records are set by one closed-source annealer run by one person. jagua-rs already solves the collision detection under MPL-2.0 with continuous rotation; the annealing layer is comparatively simple. Copy the determinism discipline from the FrankenSim study (counter-based RNG keyed by (seed, kernel, tile, index), fixed-slot reductions) so basin statistics are reproducible. Separately: the AlphaEvolve benchmark ecosystem is active, open, and has never been aimed at squares-in-squares.
