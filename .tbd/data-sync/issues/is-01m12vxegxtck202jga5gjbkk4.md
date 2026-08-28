---
type: is
id: is-01m12vxegxtck202jga5gjbkk4
title: Add a sound single-square escape screen for packing play
kind: feature
status: open
priority: 2
version: 2
labels: []
dependencies: []
parent_id: is-01m12zjr144a4kg6rnv1t0pm6n
created_at: 2026-08-28T00:22:02.515Z
updated_at: 2026-08-28T01:26:21.946Z
---
A one-sided rigidity screen is cheap and immediately useful. Translating one square by eps*d with the rest fixed shifts each SAT projection interval exactly by eps*(d.n), so a square has play iff some direction makes a zero-gap axis of every active blocker strictly increase. Feasibility is piecewise-constant between the critical angles where d.n = 0, so one interior direction per arc is a complete search rather than a sample. Built over sqpack.verify primitives and sqpack.witness.materialize_witness, roughly 120 lines, full corpus in under three minutes.

A hit certifies play; a miss proves only that that one square cannot be translated, so it cannot establish rigidity. Prototype results: n=27, 38 and 67 each have exactly two movable squares, symmetric pairs sliding along a 45-degree diagonal by 0.1213, 0.3284 and 0.2426 (n=27 is 3/sqrt(2)-2, n=38 is 2sqrt(2)-5/2), stable across tolerance 1e-12 to 1e-6. 25 records carry a certified movable square. No record flagged rigid: true shows any play. n=10 is proved optimal and still has two rattlers, so rigidity and optimality are independent.

Note a naive clearance or contact-count heuristic finds nothing: every square in every packing touches something, and the loose ones slide tangentially rather than floating.
