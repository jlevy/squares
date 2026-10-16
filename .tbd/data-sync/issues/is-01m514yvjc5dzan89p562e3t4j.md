---
type: is
id: is-01m514yvjc5dzan89p562e3t4j
title: "PR #636 A10: a redundant SETTLED entry the automatic decided branch covers goes unflagged"
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
created_at: 2026-10-16T01:24:24.268Z
updated_at: 2026-10-16T01:24:39.561Z
started_at: 2026-10-16T01:24:39.560Z
---
Low suggestion. default_drawings.py:776-777 flags only regularized and regular-as-published; a SETTLED entry where a strong view is held but not drawn is not flagged. Review: https://github.com/jlevy/squares/pull/636#pullrequestreview-5541598868
