---
type: is
id: is-01m2k77cev2mj85dkb88nxedp8
title: Close the live workbench PR stack in dependency order
kind: task
status: in_progress
priority: 1
version: 2
labels: []
dependencies: []
parent_id: is-01m2h2zv3xg1w4gdy1svjsv1tx
created_at: 2026-09-15T19:03:15.162Z
updated_at: 2026-09-15T19:15:53.864Z
---
Merge #125, #155, #160, #171, #175, #178, #179, #181, and #180 strictly parent-first. Refresh each child from the exact parent, resolve only evidence-backed conflicts, require clean mergeability and exact-head fast/Page CI at each stopping point, and require a successful deferred checkpoint on the final cumulative leaf before completing the stack. Track the #179 nested-package selector fix and the #181 think-6o9n lifecycle explicitly; do not treat stale green checks as evidence.

## Notes

2026-09-15 checkpoint: live dependency order is #125 -> #155 -> #160 -> #171 -> #175 -> #178 -> #179 -> #181 -> #180. #125 head 8884196b is CLEAN with exact-head fast and Pages green; deferred run 35012089923 is in progress after an independently reviewed Pages dependency fix. #155 head adbaf8a7 has merged exact #125, resolved its sole SYNOPSIS conflict from artifacts, passed the complete records tier locally, and is running hosted gates. #179 head d3173cbf fixes nested package.json browser-floor selection with 14 focused tests; it remains conflict-red only because ancestors are not yet propagated. Reopen think-6o9n before refreshing #181, keep it open until #180 merges, then close it. Run the final cumulative deferred gate on #180.
