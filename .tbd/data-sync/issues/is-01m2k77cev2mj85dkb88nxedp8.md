---
type: is
id: is-01m2k77cev2mj85dkb88nxedp8
title: Close the live workbench PR stack in dependency order
kind: task
status: in_progress
priority: 1
version: 6
labels: []
dependencies: []
parent_id: is-01m2h2zv3xg1w4gdy1svjsv1tx
child_order_hints:
  - is-01m2kd6659g8r7svfx9mkb83sf
created_at: 2026-09-15T19:03:15.162Z
updated_at: 2026-09-16T02:26:42.201Z
---
Merge #125, #155, #160, #171, #175, #178, #179, #181, and #180 strictly parent-first. Refresh each child from the exact parent, resolve only evidence-backed conflicts, require clean mergeability and exact-head fast/Page CI at each stopping point, and require a successful deferred checkpoint on the final cumulative leaf before completing the stack. Track the #179 nested-package selector fix and the #181 think-6o9n lifecycle explicitly; do not treat stale green checks as evidence.

## Notes

2026-09-15/16 checkpoint: #125 exact 8884196b merged as 0ac0e063; #155 exact adbaf8a7 merged as 031de58d; #160 exact 07ffdbfb merged as 11783761; #171 exact b7e984b1 merged as 21a68102. #175 was reconstructed after restart, now final at 3d8ef13c: deterministic suite-a/suite-b partition, corrected quick test, recorded hosted means 150.54s/119.54s, 6,111 quick tests accounted for, local pre-push and final automatic packing/Page/mergeability checks green; think-ex35 closed. The one initial Page PDF mismatch was known D-490 host variance and the isolated rerun passed. Current descendant heads remain #178 97d1413b, #179 94bf4e15 (d3173cbf ancestor and nested **/package.json selector preserved), #181 a94a84e8, #180 1bed9751 (400e26d9 ancestor and no-overrides floor preserved). Synthetic parent-first merge through all four returned no textual conflict, but stale green checks will not be reused. Real propagation has begun at #178. Continue strictly parent-first, preserve the #179 nested selector and #180 no-overrides floor, keep think-6o9n open until main, and require the final cumulative deferred checkpoint before async stack merge.
