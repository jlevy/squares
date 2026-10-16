---
type: is
id: is-01m514yvjc5dzan89p562e3t4j
title: "PR #636 A10: a redundant SETTLED entry the automatic decided branch covers goes unflagged"
kind: bug
status: closed
priority: 3
version: 3
delegate: ecstatic-edison-636-review-a
labels:
  - regularization
dependencies: []
parent_id: is-01m514y11gd146dzhmnf7ke508
hold: null
hold_until: null
created_at: 2026-10-16T01:24:24.268Z
updated_at: 2026-10-16T02:07:16.301Z
started_at: 2026-10-16T01:24:39.560Z
closed_at: 2026-10-16T02:07:16.301Z
close_reason: "Fixed (PR #636 A10) in 288a1a520: a SETTLED entry where the layer's held strong view decides the count fails the gate. Test: test_a_settled_entry_the_layer_decides_unaided_fails_the_gate."
resolution: null
duplicate_of: null
---
Low suggestion. default_drawings.py:776-777 flags only regularized and regular-as-published; a SETTLED entry where a strong view is held but not drawn is not flagged. Review: https://github.com/jlevy/squares/pull/636#pullrequestreview-5541598868
