---
type: is
id: is-01m5kdrb3bn0addbdjqdby4qhx
title: Match Frontier Survey record status icons to shared tag sizing
kind: task
status: closed
priority: 2
version: 3
spec_path: docs/project/specs/active/plan-2026-10-22-site-navigation.md
delegate: site-followups-ui
labels: []
dependencies: []
parent_id: is-01m5jnsqdwj3t8m7hkbx6mr1m2
hold: null
hold_until: null
created_at: 2026-10-23T03:44:27.753Z
updated_at: 2026-10-23T04:17:28.612Z
started_at: 2026-10-23T03:44:43.514Z
closed_at: 2026-10-23T04:17:28.612Z
close_reason: Implemented in ab238b2f73e60dbe331b2c22e94165e8083de41b, https://github.com/jlevy/squares/pull/743. Shared sans collection-heading role now covers profile sections with Title Case and existing anchors; profile Records/Results/Credits stack above Resources; main directory names use shared bold; category ancestors retain the active underline; Frontier property badges share tag size/height tokens. Focused Chromium checks passed for headings, tallies, directory link weights, category focus/hover, badge geometry, responsive Frontier row centering/scrolling, and 35em/card alignment. Scoped Ruff/Biome passed. Implementation complete; hosted CI, final PR review, and deployment remain coordinator work.
resolution: null
duplicate_of: null
---
User reports Frontier Survey [R], [O], and [=] status icons are too small. Match other tags through shared design tokens, preserving meaning, accessible labels, contrast and compact responsive table alignment. Verify actual rendered table at desktop and mobile; avoid per-glyph hacks.
