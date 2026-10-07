---
type: is
id: is-01m41c9wf2h05agc5kv2hmy425
title: "Integrity ceremony: remove the digest pins in four n = 11 tools inherited from main"
kind: task
status: open
priority: 3
version: 4
spec_path: docs/project/reviews/review-2026-10-02-n17-bulk-exclusion-design.md
delegate: claude-code@vm
labels:
  - integrity
dependencies: []
parent_id: is-01m3xkd6zmq1jqwtn628h2k7zy
hold: null
hold_until: null
created_at: 2026-10-03T17:17:03.841Z
updated_at: 2026-10-03T22:35:53.005Z
started_at: 2026-10-03T22:35:45.146Z
---
The merge of origin/main at f864a576a brought in four n = 11 tools written on main
before OR-16’s amendment reached it.
Each hashes its own source or pins digests of retained objects:
- check_n11_optimality_d4_incidence.py (5 sites)
- check_n11_optimality_local_two_radius.py (6)
- select_n11_field_minimum.py (4)
- n11_optimality_overview_figures.py (7, up from 1) They are recorded in
  devtools/integrity-ceremony.yaml as inherited.
  Apply OR-16 as amended: identify by Git revision and path, keep pins only at real
  boundaries (the publisher’s archived objects), and lower the baseline with --update.
  Coordinate with main, which owns these files, so the change does not fight upstream
  edits.

## Notes

2026-10-03, fourth merge of main (e8aee5177): it brought in plan_valid9_replay.py,
main’s ValidTilt9 replay planner.
Its 6 sites pin the record and cover by digest, as plan_valid7_replay.py does.
They are recorded as inherited in integrity-ceremony.yaml (302b085ef) and belong to this
bead’s review.
