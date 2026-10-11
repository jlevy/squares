---
type: is
id: is-01m2hpfqfmy4x6d02cht4e33yq
title: "Workbench page: one source for the box-first move share"
kind: task
status: closed
priority: 3
version: 2
labels: []
dependencies: []
created_at: 2026-09-15T04:51:28.371Z
updated_at: 2026-10-06T08:35:36.565Z
closed_at: 2026-10-06T08:35:36.565Z
close_reason: |
  Superseded (bead review 2026-10-06, origin/main eb43ffe9a): The code is gone: BOX_FIRST and moveProgress were removed from packages/workbench/src/application.js in 9cca493c1 (2026-09-16, PR #189); box-first staging survives only as a historical comment
resolution: canceled
duplicate_of: null
---
PR #171 review suggestion (non-blocking): `moveProgress` in `packages/workbench/src/application.js` re-derives the box-first start from `BOX_FIRST` instead of reading one declared value, so the stage box's timing is written in two places. A cleanup with no behaviour change. Do it with the stage-box timing decision (think-31ln, whether boxFirst should reserve 32 % of moves whose box never changes size), or as part of moving that logic out of application.js into a typed module under src/animation/.
