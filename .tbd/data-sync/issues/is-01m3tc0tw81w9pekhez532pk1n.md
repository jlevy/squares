---
type: is
id: is-01m3tc0tw81w9pekhez532pk1n
title: "Site tables: the row is the unit, with whole-row hover and click opening that row's popover and no per-cell expansion"
kind: feature
status: closed
priority: 2
version: 2
spec_path: docs/project/specs/active/plan-2026-09-29-github-pages-overview.md
labels: []
dependencies: []
parent_id: is-01m3p52z585a2zb9jmy19b0r96
created_at: 2026-09-30T23:57:26.268Z
updated_at: 2026-10-01T04:50:47.637Z
closed_at: 2026-10-01T04:50:47.636Z
close_reason: Done in dad5a3bc8 and 04a4d0568 on claude/overview-page-impl (jlevy/squares#255, pushed at d078a2020); checked in the built site at http://localhost:8000 on 2026-10-01. Recent Results, all-results, awaiting replay and frontier rows open one popover each through row_detail and overview/row-popover.js; no td contains details; documented in paper-design.md.
resolution: null
duplicate_of: null
---
Owner, 2026-09-30: every table row that has a hover must not use individual cell expansion. The whole row takes the hover, is clickable (and keyboard-focusable, Enter/Space to open), and opens one popover for that row, the same popover component the cards use. Make this the design system's one pattern for detail on a table row, documented in paper-design.md, and apply it to every site table with row detail: Recent Results on the homepage, all-results.html, and any other table that expands a cell today (overview_sections' <details> in the result cell; the replay table). Without scripts, the row's detail stays reachable (a link to its record or a visible fallback).
