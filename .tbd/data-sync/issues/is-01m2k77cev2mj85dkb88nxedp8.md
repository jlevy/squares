---
type: is
id: is-01m2k77cev2mj85dkb88nxedp8
title: Close the live workbench PR stack in dependency order
kind: task
status: in_progress
priority: 1
version: 8
labels: []
dependencies: []
parent_id: is-01m2h2zv3xg1w4gdy1svjsv1tx
child_order_hints:
  - is-01m2kd6659g8r7svfx9mkb83sf
created_at: 2026-09-15T19:03:15.162Z
updated_at: 2026-09-16T03:28:58.217Z
---
Merge #125, #155, #160, #171, #175, #178, #179, #181, and #180 strictly parent-first. Refresh each child from the exact parent, resolve only evidence-backed conflicts, require clean mergeability and exact-head fast/Page CI at each stopping point, and require a successful deferred checkpoint on the final cumulative leaf before completing the stack. Track the #179 nested-package selector fix and the #181 think-6o9n lifecycle explicitly; do not treat stale green checks as evidence.

## Notes

2026-09-15/16 checkpoint: #125 merged as 0ac0e063; #155 as 031de58d; #160 as
11783761; #171 as 21a68102. #175 final 3d8ef13c is fully green after deterministic
suite sharding, corrected quick-test scope, recorded 150.54s/119.54s hosted means, and
6,111 accounted quick tests; think-ex35 closed. #178 final d0b7ba31 retained its patch
and passed local push 48/78 (6,249/9) plus hosted Packing 35049553885, Page 35049553881,
and mergeability 35049547981. #179 final 4e579aa3 retained d3173cbf,
`**/package.json`, and the nested slideshow regression; local push passed 48/78 with
6,249/9 in 1,080.58s, and hosted Packing 35051380618, Page 35051380652, and
mergeability 35051377927 are green. #181 propagation is active from that exact parent;
#180 remains 1bed9751 and must retain 400e26d9 and the no-overrides floor. Continue
strictly parent-first, never reuse stale green checks, keep think-6o9n open until main,
and require the final cumulative deferred checkpoint before async stack merge.
