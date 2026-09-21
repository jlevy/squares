---
type: is
id: is-01m31gpjj60pm8ayyh6qw0v2fm
title: fold --check cannot see a variant or corner_clip swap
kind: bug
status: open
priority: 2
version: 1
labels: []
dependencies: []
parent_id: is-01m31gn7263sfhfbq8xfabkh3p
created_at: 2026-09-21T08:18:12.165Z
updated_at: 2026-09-21T08:18:12.165Z
---
PR 207 re-review residual. container_differences in fold_ceiling_family.py:234-260 compares n, outer_side, square_side and half_tangents but not variant or corner_clip, while fold copies them through (folded_record = dict(record)). Measured: differences(clipped_fold, unclipped_fold) == [], so --check reports matches: true for retained bytes declaring a different hypothesis. Concrete here: .../agenda-040/exp-220-n11-96-25-class-family.json:2011-2012 carries both fields at top level. By M3's own argument those two fields say which problem the family is a ceiling for and belong in container_differences.
