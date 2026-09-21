---
type: is
id: is-01m32dwdbfz3zan9zc9p713gq3
title: m6_model F5 and F7 deferred by commit message only, with no tracker (PR 205)
kind: task
status: open
priority: 3
version: 1
labels: []
dependencies: []
parent_id: is-01m32dvmtc77znp14556p7c5w2
created_at: 2026-09-21T16:48:12.143Z
updated_at: 2026-09-21T16:48:12.143Z
---
The fix commit says 'F5 and F7 are left as the review filed them'. The disposition confirmed in source that the needs-geometry return at m6_model.py:766 is still at 8-space indent inside the for-partial loop at :745, and that no bead, defect or campaign note exists. The deferral lives only in a commit message body. Conservative in direction, and unexercised at n=32 today because _five_plus_partial is never entered there.
