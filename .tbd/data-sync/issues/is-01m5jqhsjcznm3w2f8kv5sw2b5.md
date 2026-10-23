---
type: is
id: is-01m5jqhsjcznm3w2f8kv5sw2b5
title: Integrate and validate navigation across all site page families
kind: task
status: in_progress
priority: 2
version: 3
spec_path: docs/project/specs/active/plan-2026-10-22-site-navigation.md
delegate: navigation-integration
labels: []
dependencies: []
parent_id: is-01m5jnsqdwj3t8m7hkbx6mr1m2
hold: null
hold_until: null
created_at: 2026-10-22T21:16:24.523Z
updated_at: 2026-10-23T00:07:08.506Z
started_at: 2026-10-22T21:28:25.411Z
---
After PR733 merges, apply shared parent/breadcrumb metadata to articles, records, profiles, papers, chapters and workbench; reconcile registry/build/freshness inputs; verify links, keyboard/mobile/no-JS, theme and browser layouts; build the complete site and review the standalone navigation PR. Include the five focused profile/popover/footer follow-up beads.

## Notes

Integration checklist for latest live-review requirements: complete shared assets and all generated page families; verify one Recent Results table and seven-day/earlier-row interaction including no-JavaScript and hash navigation; verify dedicated Verification page, Project Epistemics button/breadcrumb and legacy archive-fragment forwarding; confirm 35em alignment, canonical labels, homepage heading exceptions, standalone breadcrumb omission, menu placement and chevron endpoints. Rebuild the local preview and audit links/URL registry and paper navigation. Previous checkpoint Pages CI passed; current changes and known stale-test fixes require a new pushed checkpoint and green current-head CI. Do not reuse obsolete build or prior-commit validation as evidence for latest source.
