---
type: is
id: is-01m5k9qf3pntdwp0q0c5jhmz4h
title: Move profile tallies above Resources and stack them vertically
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
created_at: 2026-10-23T02:34:04.778Z
updated_at: 2026-10-23T04:17:28.604Z
started_at: 2026-10-23T03:44:43.504Z
closed_at: 2026-10-23T04:17:28.604Z
close_reason: Implemented in ab238b2f73e60dbe331b2c22e94165e8083de41b, https://github.com/jlevy/squares/pull/743. Shared sans collection-heading role now covers profile sections with Title Case and existing anchors; profile Records/Results/Credits stack above Resources; main directory names use shared bold; category ancestors retain the active underline; Frontier property badges share tag size/height tokens. Focused Chromium checks passed for headings, tallies, directory link weights, category focus/hover, badge geometry, responsive Frontier row centering/scrolling, and 35em/card alignment. Scoped Ruff/Biome passed. Implementation complete; hosted CI, final PR review, and deployment remain coordinator work.
resolution: null
duplicate_of: null
---
Next PR only, per owner request after current navigation PR lands. On individual profiles (example Oscar Fitzharding), place Records, Results, Credits summary above Resources; each metric on its own line rather than middle-dot separators. Preserve order, links, significance parentheticals and shared tally styling; apply to all profile pages. Do not include in current stabilization PR737.
