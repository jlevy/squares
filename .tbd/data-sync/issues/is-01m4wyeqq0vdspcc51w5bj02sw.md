---
type: is
id: is-01m4wyeqq0vdspcc51w5bj02sw
title: "check_half_angle_area: the radians half-angle floor disagrees with the importer at extreme angles (PR 598 review A9)"
kind: bug
status: open
priority: 3
version: 1
labels: []
dependencies: []
created_at: 2026-10-14T10:13:46.847Z
updated_at: 2026-10-14T10:13:46.847Z
---
Review A9 on PR 598: _decided_floor uses an absolute error bound, so theta = 1.0e-500 or 3.1 is refused by the third route while upper_bound_reports.half_angle_tangent_radians decides it; the importer has no RADIANS_LIMIT. Use a relative bound and share the limit. No retained fact is affected.
