---
type: is
id: is-01m0nym2spr0w1f57xe3kmsa3j
title: "sqpack-search: annealing and billiard moves, counter-based RNG, basin recording"
kind: task
status: open
priority: 1
version: 3
spec_path: docs/project/specs/active/plan-2026-08-22-minimal-packing-toolkit.md
labels: []
dependencies: []
parent_id: is-01m0p5tswc9s27gb5c1d3da27b
created_at: 2026-08-22T23:59:13.718Z
updated_at: 2026-10-10T22:47:15.644Z
---
RNG keyed by (seed, kernel, chain, index) with O(1) random access so any basin is replayable from its key; fixed-slot reductions in chain order so worker count never changes the answer. Cheap now, near-impossible to retrofit.
