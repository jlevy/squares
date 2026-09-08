---
type: is
id: is-01m1w1x0nx4kytkxzncp25t9ae
title: "PR #98 review R6: _oracle_against_sweep empty-cells shape fragility"
kind: bug
status: closed
priority: 2
version: 3
labels: []
dependencies: []
parent_id: is-01m1w1w81t7vmr0gem6d91wg8b
created_at: 2026-09-06T19:07:40.605Z
updated_at: 2026-09-06T19:16:34.391Z
closed_at: 2026-09-06T19:16:34.391Z
close_reason: "Fixed: reshape(-1, 2) on the cells array."
resolution: null
duplicate_of: null
---
packing/tests/test_fractional_generate.py:156 np.asarray(cells)[:,0] fails on empty cells. Fix: reshape(-1, 2) or precondition comment.
