---
type: is
id: is-01m5kdvhzprx6akg8y6cmbva6j
title: Bold main person-name links in Contributor Profiles table
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
created_at: 2026-10-23T03:46:13.109Z
updated_at: 2026-10-23T04:17:28.625Z
started_at: 2026-10-23T03:46:40.609Z
closed_at: 2026-10-23T04:17:28.625Z
close_reason: Implemented in ab238b2f73e60dbe331b2c22e94165e8083de41b, https://github.com/jlevy/squares/pull/743. Shared sans collection-heading role now covers profile sections with Title Case and existing anchors; profile Records/Results/Credits stack above Resources; main directory names use shared bold; category ancestors retain the active underline; Frontier property badges share tag size/height tokens. Focused Chromium checks passed for headings, tallies, directory link weights, category focus/hover, badge geometry, responsive Frontier row centering/scrolling, and 35em/card alignment. Scoped Ruff/Biome passed. Implementation complete; hosted CI, final PR review, and deployment remain coordinator work.
resolution: null
duplicate_of: null
---
Bold every main person-name link on Contributor Profiles directory. Apply shared style to primary profile links only; accounts and resource links retain normal weight. Preserve full names, surname sorting, keyboard focus and row navigation.
