---
type: is
id: is-01m3qzn1k3708fhtrsw1mqdgvk
title: "W5: remove repeated ancestry construction from snapshot accounting"
kind: task
status: closed
priority: 1
version: 3
spec_path: docs/project/reviews/review-2026-09-29-validation-parallelism.md
labels: []
dependencies: []
parent_id: is-01m1sx5m1p5868jhwcdzfkvada
created_at: 2026-09-30T01:42:48.162Z
updated_at: 2026-10-06T08:35:00.023Z
closed_at: 2026-10-06T08:35:00.023Z
close_reason: |
  Done (bead review 2026-10-06, origin/main eb43ffe9a): run_negative_controls.in_pruned_roots on origin/main walks the ancestor chain once against a frozenset of prune roots; before/after timings 6.23 s -> 0.74 s retained under session-164-validation and described in review-2026-09-29-validation-parallelism.md
resolution: null
duplicate_of: null
---
CI36655332600 spent13.45s in the snapshot-accounting test. A scoped local baseline took6.23s. Traversal pruning gave6.30s and was discarded. cProfile localized21.8/22.9 instrumented test seconds to323185 repeated Path.is_relative_to ancestry constructions. Replace root-by-root scans with one ancestor walk and hashed root membership, preserving exact Path semantics, required evidence and all snapshot limits. Same local test now0.74s; verify equivalence, link/result copy-back and cache controls; retain timings and rerun only affected tests. Hosted shard timing still needs confirmation; no broad local suite.
