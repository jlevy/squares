---
type: is
id: is-01m4vexn6tszcfdhr44q9v3zh1
title: "PR #588 A1: simplification kind does not survive T-154's later rungs; derivation falls to superseded at C2/C3"
kind: bug
status: closed
priority: 2
version: 3
delegate: claude-code@vm
labels: []
dependencies: []
parent_id: is-01m4vex5amc35y6f4zqamve8q6
hold: null
hold_until: null
created_at: 2026-10-13T20:23:04.154Z
updated_at: 2026-10-13T20:51:02.297Z
started_at: 2026-10-13T20:23:22.509Z
closed_at: 2026-10-13T20:51:02.295Z
close_reason: "fixed in d3cfe11 and 9ab8f8d: simplification's stated relations stand in for KIND_DIRECTIONS; T-154 C1/C2-C3/adopted pinned by test_a_simplification_keeps_a_standing_through_its_later_rungs; next_rung and epistemics.md Result Kinds sentence"
resolution: null
duplicate_of: null
---
Severity Medium. PR #588 review https://github.com/jlevy/squares/pull/588#pullrequestreview-5509274657, finding A1. Where: packing/devtools/render_recent_results.py:555-562, packing/devtools/check_standing.py:111,117-121,248-282, packing/frontier/results.yaml:17465,17595-17612, epistemics.md:413.
