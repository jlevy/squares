---
type: is
id: is-01m514yt3mhmdckj5xgm0v8mdy
title: "PR #636 A8: the lapse lifecycle (carried unchanged; names a view two witnesses back after a second re-housing)"
kind: bug
status: in_progress
priority: 3
version: 2
delegate: ecstatic-edison-636-review-a
labels:
  - regularization
dependencies: []
parent_id: is-01m514y11gd146dzhmnf7ke508
hold: null
hold_until: null
created_at: 2026-10-16T01:24:22.772Z
updated_at: 2026-10-16T01:24:37.215Z
started_at: 2026-10-16T01:24:37.207Z
---
Low suggestion. regularize_axis_components.py:2076-2077. Fix: say in the schema that lapsed is the last strong view that lapsed, or replace it on the next re-housing and drop it when settled. Review: https://github.com/jlevy/squares/pull/636#pullrequestreview-5541598868
