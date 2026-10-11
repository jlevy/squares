---
type: is
id: is-01m3txn7c2rh3zyjh7x42e9z5r
title: "Verification at a Glance: one ladder diagram in a special-purpose tabular layout, not three cards"
kind: feature
status: closed
priority: 2
version: 2
spec_path: docs/project/specs/active/plan-2026-09-29-github-pages-overview.md
labels: []
dependencies: []
parent_id: is-01m3p52z585a2zb9jmy19b0r96
created_at: 2026-10-01T05:05:40.223Z
updated_at: 2026-10-01T07:14:57.629Z
closed_at: 2026-10-01T07:14:57.628Z
close_reason: "Done in c7a7890d4 and 414d595ab on claude/overview-page-impl (jlevy/squares#255, pushed at 158820d9d); checked in the built site on 2026-10-01. One .site-ladders diagram: three columns, a row per level with level 5 at the top, each cell a chip, a count and a two-line description; ARIA table roles on divs; three columns from 716 px, stacked by ladder below; every rung one height."
resolution: null
duplicate_of: null
---
Owner, 2026-10-01: 'let's make it a diagram that doesn't look like three cards, but rather a special-purpose tabular layout'. Replace the three rubric cards with one diagram: columns Significance, Verification, Confirmation (significance first, think-ucon); one row per level so the rungs of the three ladders line up; each cell a rung chip (saturation rising with the level, think-nxfd), a two-line description (think-olap) and the count of results at that level; no eyebrow labels (think-v7kg). It is its own component in the design system, not the shared data table and not a card grid, readable on a phone. Supersedes the card form of think-v7kg, think-ucon and think-olap, whose requirements it carries.
