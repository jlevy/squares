---
type: is
id: is-01m514yhd4ap4smz23e1d3gw1j
title: "PR #636 A4: witness identity is weaker than stated; bind SETTLED to source.path and source.revision too"
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
created_at: 2026-10-16T01:24:13.860Z
updated_at: 2026-10-16T01:24:33.062Z
started_at: 2026-10-16T01:24:33.061Z
---
Low. default_drawings.py:447-459,:481-485,:759-760. witness.id is per-n so the id comparison cannot fire on re-housing; SETTLED binds only (source.key, side). Fix: add source.path and source.revision (where present) to witness_identity and Settled; say what the id comparison checks. Review: https://github.com/jlevy/squares/pull/636#pullrequestreview-5541598868
