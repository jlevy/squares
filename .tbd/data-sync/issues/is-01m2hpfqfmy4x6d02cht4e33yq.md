---
type: is
id: is-01m2hpfqfmy4x6d02cht4e33yq
title: "Workbench page: one source for the box-first move share"
kind: task
status: open
priority: 3
version: 1
labels: []
dependencies: []
created_at: 2026-09-15T04:51:28.371Z
updated_at: 2026-09-15T04:51:28.371Z
---
PR #171 review suggestion (non-blocking): `moveProgress` in `packages/workbench/src/application.js` re-derives the box-first start from `BOX_FIRST` instead of reading one declared value, so the stage box's timing is written in two places. A cleanup with no behaviour change. Do it with the stage-box timing decision (think-31ln, whether boxFirst should reserve 32 % of moves whose box never changes size), or as part of moving that logic out of application.js into a typed module under src/animation/.
