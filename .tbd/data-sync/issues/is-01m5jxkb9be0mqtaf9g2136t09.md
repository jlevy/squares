---
type: is
id: is-01m5jxkb9be0mqtaf9g2136t09
title: Align frontend browser tests with reviewed navigation and page ownership
kind: task
status: closed
priority: 2
version: 4
spec_path: docs/project/specs/active/plan-2026-10-22-site-navigation.md
delegate: sol-frontend-tests
labels: []
dependencies: []
parent_id: is-01m5jnsqdwj3t8m7hkbx6mr1m2
hold: null
hold_until: null
created_at: 2026-10-22T23:02:06.889Z
updated_at: 2026-10-22T23:12:26.859Z
started_at: 2026-10-22T23:02:14.022Z
closed_at: 2026-10-22T23:12:26.858Z
close_reason: null
resolution: null
duplicate_of: null
---
Fix directory-route validation and mechanical browser-test expectations for Accounts order, View All Results actions, removed homepage film, and selected learning previews. Preserve behavior, accessibility, link destinations, geometry and numerical checks; root owns case-popover geometry and components owns headroom. No product/runtime changes.

## Notes

Updated only assigned tests/probe: declared directory index aliases (including Workbench), Accounts header and sort-column indices, stable archive data selector with preserved filter/fragment routing, Recent Results keyboard destination at desktop/mobile/320px, three selected learning cards, current action labels, standalone Videos native playback under reduced motion, viewport bounds and About page title. Shared heading style comparison now includes both margins. Focused run: 11 passed and 3 stale assertions failed; corrected only obsolete Videos 52rem homepage cap and moved About Documentation content expectation; affected four-case rerun passed 94.54s. Union covers all 14 selected cases. Ruff and Biome checks pass; git diff --check passes. Coordinator committed source in dfde0c3cc and follow-up d3df6a7e76f89d39b2f2b51c36e9820bcebc9003. Evidence: /Volumes/spud-ext2/agent-scratch/site-navigation-20261022/frontend-mechanical-tests.log and frontend-mechanical-rerun.log. No runtime changes, commit or push by this worker.
