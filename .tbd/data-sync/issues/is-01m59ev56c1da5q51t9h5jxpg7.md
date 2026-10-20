---
type: is
id: is-01m59ev56c1da5q51t9h5jxpg7
title: Require source-specific review when reconciling contributor credit joins
kind: bug
status: closed
priority: 1
version: 3
spec_path: docs/project/specs/active/plan-2026-10-10-contributor-profiles.md
delegate: profiles-reconcile-fix
labels: []
dependencies: []
parent_id: is-01m4v4ehd59t1r89qwksx77bmh
hold: null
hold_until: null
created_at: 2026-10-19T06:51:04.267Z
updated_at: 2026-10-19T09:09:19.380Z
started_at: 2026-10-19T06:52:10.618Z
closed_at: 2026-10-19T09:09:19.379Z
close_reason: "Reviewed fixes integrated at b76a24fd29bdab28b5c946adeff88313fd28eb47. Standard packing and publication CI passed; full checkpoint passed with 14 successful jobs and 10 intentional skips: https://github.com/jlevy/squares/actions/runs/39223503977 . Final integration review: https://github.com/jlevy/squares/pull/578#pullrequestreview-5568927630 ."
resolution: null
duplicate_of: null
---
Senior review found automatic label/alias propagation can authorize new source occurrences without source-specific review; reconcile may also overlap retained manual subspans. Reproduce, preserve existing reviewed spans, make new occurrences unresolved candidates, and validate before writing. Review in progress.
