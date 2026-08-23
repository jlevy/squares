---
type: is
id: is-01m0p4askv3n2t3je7mefnhmsd
title: Port sqsearch behind the proposer interface
kind: task
status: open
priority: 1
version: 2
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-22-minimal-packing-toolkit.md
labels: []
dependencies: []
parent_id: is-01m0p4asaeypn1nn54frxj3cx9
created_at: 2026-08-23T01:39:00.858Z
updated_at: 2026-08-23T01:41:01.741Z
---
The existing Rust annealer becomes proposer #1. Critical change: record EVERY quenched local optimum, not only the best per chain - the current engine discards exactly the data the atlas is made of. Keep the counter-based RNG keyed by (seed, chain) and the selftest gate.
