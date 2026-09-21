---
type: is
id: is-01m31gqc74pvscra842qpp180a
title: doubled_net docstring imprecision in interval.py
kind: bug
status: open
priority: 3
version: 1
labels: []
dependencies: []
parent_id: is-01m31gn7263sfhfbq8xfabkh3p
created_at: 2026-09-21T08:18:38.434Z
updated_at: 2026-09-21T08:18:38.434Z
---
PR 206 re-review, new Low introduced by 9a19d393. The L2 replacement docstring says doubled_net 'yields the net's own arc [0, pi/4]', but rotation_from_half_tangent only enforces t in [0,1), i.e. theta in [0, pi/2), so the forward net is not confined to [0, pi/4]. It also credits 'the guard below' with making the property true by construction, when the actual enforcement is Rotation.__post_init__ (interval.py:304-306), which it never mentions. The stated conclusion - every rotation lies in [0, pi/2] - is still correct.
