---
type: is
id: is-01m2k77cev2mj85dkb88nxedp8
title: Close the live workbench PR stack in dependency order
kind: task
status: closed
priority: 1
version: 17
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
updated_at: 2026-09-16T10:03:36.257Z
closed_at: 2026-09-16T10:03:36.256Z
close_reason: "The named workbench stack is fully merged parent-first through #180 at a4f801e8. Every leaf used current-parent exact-head required/Page evidence; the final cumulative leaf also passed deep run 35078581840. Remaining CI reconciliation moved to think-97we under think-xfqk."
resolution: null
duplicate_of: null
---
Merge #125, #155, #160, #171, #175, #178, #179, #181, and #180 strictly parent-first. Refresh each child from the exact parent, resolve only evidence-backed conflicts, require clean mergeability and exact-head fast/Page CI at each stopping point, and require a successful deferred checkpoint on the final cumulative leaf before completing the stack. Track the #179 nested-package selector fix and the #181 think-6o9n lifecycle explicitly; do not treat stale green checks as evidence.

## Notes

Live workbench stack closed parent-first: #125, #155, #160, #171, #175 (05157c33), #178 (6e212693), #179 (8484d616), #181 (398e59e4), and #180 (a4f801e8) are merged. #183 (4ef41be3) was reconciled between the no-JS leaves. Final leaf #180 merged only after exact-head required/Page CI and deep run 35078581840 were fully green on verified synthetic merge 699b84b6. Post-stack CI reconciliation think-97we moved to CI epic think-xfqk and remains open.
