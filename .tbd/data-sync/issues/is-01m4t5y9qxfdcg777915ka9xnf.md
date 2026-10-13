---
type: is
id: is-01m4t5y9qxfdcg777915ka9xnf
title: "PR #549 B3: 53, 54, 178 call a 36-place round-up the bound exactly / exact side"
kind: bug
status: closed
priority: 2
version: 3
delegate: claude-code@vm
labels: []
dependencies: []
parent_id: is-01m4t5xyswh7ea30knxw766epz
hold: null
hold_until: null
created_at: 2026-10-13T08:26:53.565Z
updated_at: 2026-10-13T08:55:02.761Z
started_at: 2026-10-13T08:54:59.805Z
closed_at: 2026-10-13T08:55:02.760Z
close_reason: "fixed in 296a0dd2b: rounded sides are written as rounded up at 36 places, never exactly"
resolution: null
duplicate_of: null
---
Medium. register_regularized_bounds.py:1053, :838, :187-193; n-053.md, n-054.md, n-178.md. Review B https://github.com/jlevy/squares/pull/549#pullrequestreview-5500740106.
