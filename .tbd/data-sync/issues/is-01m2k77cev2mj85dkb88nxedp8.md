---
type: is
id: is-01m2k77cev2mj85dkb88nxedp8
title: Close the live workbench PR stack in dependency order
kind: task
status: in_progress
priority: 1
version: 5
labels: []
dependencies: []
parent_id: is-01m2h2zv3xg1w4gdy1svjsv1tx
child_order_hints:
  - is-01m2kd6659g8r7svfx9mkb83sf
created_at: 2026-09-15T19:03:15.162Z
updated_at: 2026-09-15T20:47:27.395Z
---
Merge #125, #155, #160, #171, #175, #178, #179, #181, and #180 strictly parent-first. Refresh each child from the exact parent, resolve only evidence-backed conflicts, require clean mergeability and exact-head fast/Page CI at each stopping point, and require a successful deferred checkpoint on the final cumulative leaf before completing the stack. Track the #179 nested-package selector fix and the #181 think-6o9n lifecycle explicitly; do not treat stale green checks as evidence.

## Notes

2026-09-15 checkpoint: #125 exact 8884196b merged as 0ac0e063; #155 exact adbaf8a7 merged as 031de58d; #160 exact 07ffdbfb merged as 11783761; #171 exact b7e984b1 merged as 21a68102. #175 exact ef907d8c remains the sole stack blocker: two hosted runs passed all 6,096 tests but exceeded the 275-second suite ceiling (280.83s and 278.93s); a dedicated efficiency lane is diagnosing and fixing the cost without weakening CI. #178 exact 97d1413b, #179 exact 94bf4e15, and #181 exact a94a84e8 are clean and fully green. #179 retains the nested package.json selector fix. #180 was propagated from #181, locally fully validated, and pushed at exact head 1bed9751; hosted checks are running. Continue strictly parent-first after #175 is green. Keep think-6o9n open until #180 reaches main, and require the final cumulative deferred checkpoint.
