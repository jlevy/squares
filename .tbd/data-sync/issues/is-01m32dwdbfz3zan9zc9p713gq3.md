---
type: is
id: is-01m32dwdbfz3zan9zc9p713gq3
title: m6_model F5 and F7 deferred by commit message only, with no tracker (PR 205)
kind: task
status: closed
priority: 3
version: 2
labels: []
dependencies: []
parent_id: is-01m32dvmtc77znp14556p7c5w2
created_at: 2026-09-21T16:48:12.143Z
updated_at: 2026-10-06T08:47:46.833Z
closed_at: 2026-10-06T08:47:46.833Z
close_reason: "Duplicate of think-p8hm (older): both track the m6_model F5 and F7 deferrals from PR 205; F5's early return inside the for-partial loop is still at packing/devtools/bentz2016/m6_model.py ~766 on origin/main."
resolution: duplicate
duplicate_of: is-01m31gq8059s839hxx8ypaf9xr
---
The fix commit says 'F5 and F7 are left as the review filed them'. The disposition confirmed in source that the needs-geometry return at m6_model.py:766 is still at 8-space indent inside the for-partial loop at :745, and that no bead, defect or campaign note exists. The deferral lives only in a commit message body. Conservative in direction, and unexercised at n=32 today because _five_plus_partial is never entered there.
