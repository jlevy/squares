---
type: is
id: is-01m2k77cev2mj85dkb88nxedp8
title: Close the live workbench PR stack in dependency order
kind: task
status: open
priority: 1
version: 1
labels: []
dependencies: []
parent_id: is-01m2h2zv3xg1w4gdy1svjsv1tx
created_at: 2026-09-15T19:03:15.162Z
updated_at: 2026-09-15T19:03:15.162Z
---
Merge #125, #155, #160, #171, #175, #178, #179, #181, and #180 strictly parent-first. Refresh each child from the exact parent, resolve only evidence-backed conflicts, require clean mergeability and exact-head fast/Page CI at each stopping point, and require a successful deferred checkpoint on the final cumulative leaf before completing the stack. Track the #179 nested-package selector fix and the #181 think-6o9n lifecycle explicitly; do not treat stale green checks as evidence.
