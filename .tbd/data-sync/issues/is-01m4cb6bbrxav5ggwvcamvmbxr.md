---
type: is
id: is-01m4cb6bbrxav5ggwvcamvmbxr
title: "PR #427 A6 — High: the structure reader cannot consume the new rational witnesses."
kind: bug
status: open
priority: 1
version: 1
labels: []
dependencies: []
parent_id: is-01m4cb68shtz5h0braprdqj1qb
created_at: 2026-10-07T23:29:18.200Z
updated_at: 2026-10-07T23:29:18.200Z
---
Review https://github.com/jlevy/squares/pull/427#pullrequestreview-5449633758 head83748.

**A6 — High: the structure reader cannot consume the new rational witnesses.**
`packing/devtools/known_structure.py:60` passes corner strings directly to `float`; its
return also passes the exact side directly to `float`. Hosted suite D reaches the newly
selected n=199 witness and raises `ValueError` on `42298529743377/4398046511104`. The
workbench’s record-reference path therefore cannot read an admitted current witness.
Its tolerance test also constructs `Decimal` from rational strings, which would fail
after only the production reader is fixed.

**Fix:** parse admitted rational scalars exactly before converting to the diagnostic
float representation, covering corners, centers and side as applicable.
Update `packages/workbench/tests/test_record_reference_tolerance.py:87` and its
corner/center references to support both decimal and fraction strings.
Preserve the conversion-error and record-tolerance assertions; exercise at least the
actual n=199 witness and a rotated rational square.
