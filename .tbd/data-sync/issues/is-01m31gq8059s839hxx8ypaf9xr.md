---
type: is
id: is-01m31gq8059s839hxx8ypaf9xr
title: Track the F5 and F7 deferrals from the PR 205 review
kind: task
status: open
priority: 3
version: 1
labels: []
dependencies: []
parent_id: is-01m31gn7263sfhfbq8xfabkh3p
created_at: 2026-09-21T08:18:34.112Z
updated_at: 2026-09-21T08:18:34.112Z
---
PR 205 re-review. The fix commit aed8638d declares 'F5 and F7 are left as the review filed them', but no bead, defect or campaign note exists - the deferral lives only in a commit message body. F5: the needs-geometry return in m6_model.py:766 is still at 8-space indent inside the for-partial loop at :745, so _five_plus_partial abandons the line after the first qualifying partial. Direction is conservative and at n=32 the branch is never entered, so it is unexercised today. F7: parallel implementations across the two models.
