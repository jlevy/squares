---
type: is
id: is-01m2k77cev2mj85dkb88nxedp8
title: Close the live workbench PR stack in dependency order
kind: task
status: in_progress
priority: 1
version: 15
labels: []
dependencies: []
parent_id: is-01m2h2zv3xg1w4gdy1svjsv1tx
child_order_hints:
  - is-01m2kd6659g8r7svfx9mkb83sf
  - is-01m2m5zjmj7dsycs1x6yxwcwwt
  - is-01m2m6xx00sabcq5zqkrneavd0
  - is-01m2m6y4gw224dgrwf37bgqnhd
  - is-01m2mab5h55dh53sd1gtw5prjh
created_at: 2026-09-15T19:03:15.162Z
updated_at: 2026-09-16T07:36:41.558Z
---
Merge #125, #155, #160, #171, #175, #178, #179, #181, and #180 strictly parent-first. Refresh each child from the exact parent, resolve only evidence-backed conflicts, require clean mergeability and exact-head fast/Page CI at each stopping point, and require a successful deferred checkpoint on the final cumulative leaf before completing the stack. Track the #179 nested-package selector fix and the #181 think-6o9n lifecycle explicitly; do not treat stale green checks as evidence.

## Notes

Parent-first merge pass advanced: #175 -> 05157c33, #178 -> 6e212693, #179 -> 8484d616, #183 -> 4ef41be3, and #181 -> 398e59e4. PR #181 merged only after full senior review, final-parent reconciliation, a hosted geometry regression-control failure was fixed with file-backed probes, and exact-head required/visual CI was fully green. #180 is next; its senior review found opacity-zero Motion Lab pages could falsely pass, tracked as open think-7z01, and a delegated implementation/re-review lane is fixing it before restack and merge.
