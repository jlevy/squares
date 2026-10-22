---
type: is
id: is-01m5h60h4dwkxcv9emzfs6x74a
title: "PR #720 A3: a deletion row's controls are assumed, not checked"
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
created_at: 2026-10-22T06:50:38.604Z
updated_at: 2026-10-22T06:50:48.958Z
started_at: 2026-10-22T06:50:48.958Z
---
Low. packing/devtools/beyond_horizon_replay.py:424-425, 803-807, docstring 32-33. Nothing refuses a deletion row whose certificate has no whole row in the release. Review: https://github.com/jlevy/squares/pull/720#issuecomment-6334629965 (PR #720, review A, round 1).
