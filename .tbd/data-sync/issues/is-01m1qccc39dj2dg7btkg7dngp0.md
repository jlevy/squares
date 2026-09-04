---
type: is
id: is-01m1qccc39dj2dg7btkg7dngp0
title: "F10: assess and port the exact-seam refusal fix in the interval route"
kind: task
status: open
priority: 2
version: 2
labels: []
dependencies: []
parent_id: is-01m1qcc9devr6mz0m6erxswxjc
created_at: 2026-09-04T23:34:37.417Z
updated_at: 2026-09-04T23:41:13.206Z
---
F10 and the box budget. PR 80's BOX_BUDGET = 100,000 per direction fails safe and the four retained verdicts are unchanged under it, but the headroom at the n = 17 top rung is 3.2x (31,103 boxes measured) and the comment naming the largest retained certificate is already wrong (2,097; it is 2,260). Raise it (500,000 gives about 16x) or derive it from the net size, and fix the comment. Confirm the exact-seam mechanism (a leave-edge on an enter-edge that outward rounding cannot close) before porting that part.
