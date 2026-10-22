---
type: is
id: is-01m5h60fj2d5s7zjcqp7x7w3rv
title: "PR #720 A1: earlier rows' superseded_by skips the backlog reports now first in report order (77 counts)"
kind: bug
status: in_progress
priority: 2
version: 2
delegate: c-lane-pr-b
labels: []
dependencies: []
parent_id: is-01m5h60etmp9mafa8j0y40ey2h
hold: null
hold_until: null
created_at: 2026-10-22T06:50:36.994Z
updated_at: 2026-10-22T06:50:47.963Z
started_at: 2026-10-22T06:50:47.963Z
---
Medium. packing/devtools/beyond_horizon_replay.py:741-772 (planned_supersessions, coverage_problems), packing/frontier/source-coverage.yaml (e.g. 11301-11307 at 464). 77 start rows (couzo-verified-bounds-2026-10-14 69, couzo-certificates-2026-10-14 6, evand-fresh-compositions-2026-10-14 1, fang-excess-theorem-2026-10-13 1) still name #678 (48), #686 (21) or #715 (8) although #670/#675/#672/#666 beat them first. Coordinator prefers fix (a): repoint to the first backlog report, held by planned_supersessions/coverage_problems. Review: https://github.com/jlevy/squares/pull/720#issuecomment-6334629965 (PR #720, review A, round 1).
