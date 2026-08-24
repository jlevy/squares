---
type: is
id: is-01m0rrjtq99x8zbzd5hvqxrjcg
title: "The engine is not the bottleneck: do not micro-optimize sqsearch yet"
kind: chore
status: open
priority: 3
version: 3
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-24-packing-engineering-maturity.md
labels:
  - engineering-maturity
dependencies: []
parent_id: is-01m0rrgqj3esjc4jx1fr3qy1ht
created_at: 2026-08-24T02:11:24.520Z
updated_at: 2026-08-24T21:22:13.482Z
---
Measured: 28.7M moves/s at n=11, 16M moves in 0.56s across 4 chains. The whole soundness perimeter's three engine cells cost ~1.7s of a step that ran for 36s.

There ARE real wins available in the move loop, and they should be recorded so nobody re-derives them, but none of them should be done before the quench work (think-y91x):
- Rng::below uses '%' by a runtime bound: one 64-bit division per move. Lemire's multiply-shift removes it and also removes the modulo bias.
- required_side rescans all n squares per move. Maintaining the bbox and rescanning only when the moved square was the extreme makes most moves O(1) on that term.
- local_overlap is evaluated twice per move (old pose and new). Caching a per-square row-sum of pair depths makes the 'old' side O(1), updating the row-sums only on accept -- roughly halving pair-kernel work at the low acceptance rates that dominate late anneal.
- The rotate branch calls cos() and sin() separately; f64::sin_cos() computes both.

Expect these to be worth maybe 1.5-2x on a component that is already three orders of magnitude faster than the thing next to it. Deliberately deferred.
