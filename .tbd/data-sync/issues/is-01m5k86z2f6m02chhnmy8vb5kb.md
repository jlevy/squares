---
type: is
id: is-01m5k86z2f6m02chhnmy8vb5kb
title: Apply common document guidelines and Title Case to site headings
kind: task
status: closed
priority: 1
version: 3
spec_path: docs/project/specs/active/plan-2026-10-22-site-navigation.md
delegate: site-followups-ui
labels: []
dependencies: []
parent_id: is-01m5jnsqdwj3t8m7hkbx6mr1m2
hold: null
hold_until: null
created_at: 2026-10-23T02:07:35.502Z
updated_at: 2026-10-23T04:17:28.596Z
started_at: 2026-10-23T03:44:43.489Z
closed_at: 2026-10-23T04:17:28.596Z
close_reason: Implemented in ab238b2f73e60dbe331b2c22e94165e8083de41b, https://github.com/jlevy/squares/pull/743. Shared sans collection-heading role now covers profile sections with Title Case and existing anchors; profile Records/Results/Credits stack above Resources; main directory names use shared bold; category ancestors retain the active underline; Frontier property badges share tag size/height tokens. Focused Chromium checks passed for headings, tallies, directory link weights, category focus/hover, badge geometry, responsive Frontier row centering/scrolling, and 35em/card alignment. Scoped Ruff/Biome passed. Implementation complete; hosted CI, final PR review, and deployment remain coordinator work.
resolution: null
duplicate_of: null
---
After the current navigation checkpoint is stabilized and pushed, apply common-doc-guidelines systematically to rendered pages and their source/templates. Audit heading Title Case, including profile sections such as Credited work on Joshua Levy; fix source generators rather than generated output, preserve URL anchors, document justified exceptions and validate representative pages.
