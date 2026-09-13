---
type: is
id: is-01m2chkpvbrqv1h9nttp8rrtqb
title: Define an exact public seed domain and mixing contract
kind: bug
status: in_progress
priority: 2
version: 7
spec_path: docs/project/specs/active/plan-2026-09-11-workbench-from-spike-to-product.md
labels:
  - workbench-roadmap
  - workbench-phase-1
dependencies:
  - type: blocks
    target: is-01m2chahf57z4w9tj5gehbs0td
  - type: blocks
    target: is-01m2ckzvnsawqg79z9ybspc3yt
  - type: blocks
    target: is-01m29bhrhcs1zrcbfbhgwbb86n
  - type: blocks
    target: is-01m2chr65cx0jhfd1gsmx3r31y
parent_id: is-01m28p7h39vcykq99dgjmvwv98
created_at: 2026-09-13T04:50:03.754Z
updated_at: 2026-09-13T06:17:28.341Z
---
Review R5: JS computes state.seed * 0x9e3779b1 as Number before integer conversion; accepted seeds 79049217 and 29207060 alias at base17. Use explicit bounded integer seed semantics and integer-safe mixing, preserve seed0 behavior, record actual seed, and test browser/Node replay plus boundary seeds. Existing campaigns used small seeds; their contamination is not established.
