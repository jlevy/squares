---
type: is
id: is-01m5kdrskqhn653hpxf6vrjntr
title: Underline the active top-level navigation category on descendant pages
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
created_at: 2026-10-23T03:44:42.614Z
updated_at: 2026-10-23T04:17:28.618Z
started_at: 2026-10-23T03:44:55.335Z
closed_at: 2026-10-23T04:17:28.618Z
close_reason: Implemented in ab238b2f73e60dbe331b2c22e94165e8083de41b, https://github.com/jlevy/squares/pull/743. Shared sans collection-heading role now covers profile sections with Title Case and existing anchors; profile Records/Results/Credits stack above Resources; main directory names use shared bold; category ancestors retain the active underline; Frontier property badges share tag size/height tokens. Focused Chromium checks passed for headings, tallies, directory link weights, category focus/hover, badge geometry, responsive Frontier row centering/scrolling, and 35em/card alignment. Scoped Ruff/Biome passed. Implementation complete; hosted CI, final PR review, and deployment remain coordinator work.
resolution: null
duplicate_of: null
---
Show the shared active-tab underline on Results, Learn, or About whenever any descendant page is current. Preserve one category dropdown trigger, non-page categories, selected item semantics and keyboard focus styling; Overview and News stay active on their own pages. Verify profile, result, article and top-level pages.
