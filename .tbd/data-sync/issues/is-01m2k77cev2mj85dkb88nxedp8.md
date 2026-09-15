---
type: is
id: is-01m2k77cev2mj85dkb88nxedp8
title: Close the live workbench PR stack in dependency order
kind: task
status: in_progress
priority: 1
version: 3
labels: []
dependencies: []
parent_id: is-01m2h2zv3xg1w4gdy1svjsv1tx
created_at: 2026-09-15T19:03:15.162Z
updated_at: 2026-09-15T19:46:43.145Z
---
Merge #125, #155, #160, #171, #175, #178, #179, #181, and #180 strictly parent-first. Refresh each child from the exact parent, resolve only evidence-backed conflicts, require clean mergeability and exact-head fast/Page CI at each stopping point, and require a successful deferred checkpoint on the final cumulative leaf before completing the stack. Track the #179 nested-package selector fix and the #181 think-6o9n lifecycle explicitly; do not treat stale green checks as evidence.

## Notes

2026-09-15 checkpoint: dependency order remains #125 -> #155 -> #160 -> #171 -> #175 -> #178 -> #179 -> #181 -> #180. #125 exact 8884196b is CLEAN with fast/Page green and three of four deferred jobs green; exhaustive-tier is still running. #155 exact adbaf8a7 is fully green. #160 exact 07ffdbfb is fully green after all 6,042 tests passed on the third run; the previous retry exceeded the 275-second wall ceiling by 1.09 seconds without a test failure. #171 exact b7e984b1 is fully green. Propagation heads #175 ef907d8c, #178 97d1413b, and #179 94bf4e15 are pushed with independent local invariants and focused/browser/package/record gates green; hosted checks are running. #179 retains the nested package.json selector fix. #181 propagation is in progress; keep think-6o9n open until final #180 reaches main. Merge only parent-first by exact SHA; run the final cumulative deferred gate on #180.
