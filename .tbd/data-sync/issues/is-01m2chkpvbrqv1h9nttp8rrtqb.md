---
type: is
id: is-01m2chkpvbrqv1h9nttp8rrtqb
title: Define an exact public seed domain and mixing contract
kind: bug
status: open
priority: 2
version: 2
spec_path: docs/project/specs/active/plan-2026-09-11-workbench-from-spike-to-product.md
labels: []
dependencies:
  - type: blocks
    target: is-01m2chahf57z4w9tj5gehbs0td
parent_id: is-01m28p7h39vcykq99dgjmvwv98
created_at: 2026-09-13T04:50:03.754Z
updated_at: 2026-09-13T05:00:45.990Z
---
Review R5: JS computes state.seed * 0x9e3779b1 as Number before integer conversion; accepted seeds 79049217 and 29207060 alias at base17. Use explicit bounded integer seed semantics and integer-safe mixing, preserve seed0 behavior, record actual seed, and test browser/Node replay plus boundary seeds. Existing campaigns used small seeds; their contamination is not established.
