---
type: is
id: is-01m5k0vqb7h3a15ntqvb15fz23
title: Toggle earlier Recent Results rows within one table
kind: task
status: closed
priority: 2
version: 4
spec_path: docs/project/specs/active/plan-2026-10-22-site-navigation.md
delegate: navigation-components
labels: []
dependencies: []
parent_id: is-01m5jnsqdwj3t8m7hkbx6mr1m2
hold: null
hold_until: null
created_at: 2026-10-22T23:59:07.097Z
updated_at: 2026-10-23T00:13:52.424Z
started_at: 2026-10-23T00:00:13.636Z
closed_at: 2026-10-23T00:13:52.423Z
close_reason: One-table progressive disclosure implemented and real-page desktop/mobile, keyboard, fragment, empty-history and no-script checks passed; existing table Node tests36passed. Full-build integration remains parent responsibility.
resolution: null
duplicate_of: null
---
Implement an accessible Earlier results toggle for one Recent Results table with two row groups, showing the latest seven days initially, exposing all rows without JavaScript, and retaining shared design and popovers.

## Notes

Implemented in existing overview/table.js and overview/results.css with no new asset filename. One native table has current and earlier tbody groups; the boundary button controls only the older group, updates aria-expanded/label/chevron, preserves Enter/Space semantics, restores focus before hiding focused older content, opens the legacy earlier boundary for initial/hashchange navigation, and disappears/disabled when no older rows exist. Recent tables bypass generic table sorting to preserve arrival order. Existing prepaint bootstrap collapses the earlier group before paint; without JavaScript all rows remain visible and the inactive control is hidden. Desktop table and mobile result-row cards retain their native responsive displays. Canonical result-row fragment IDs intentionally remain on Results Archive; Recent ordinary links reach complete canonical record articles.

Evidence: uv run --frozen --all-extras --group dev python -m pytest tests/test_site_navigation.py::test_recent_table_disclosure_preserves_native_rows_keyboard_and_no_script_access -q: 1 passed in 15.56s using the actual recent_results_page producer at1280/390/320, Enter/Space/aria/label/icon, same-document and direct-load legacy boundary, no-history state, and no-JavaScript every-older-row visibility at1280/320. node --test tests/node/overview_table/table.test.mjs tests/node/overview_table/filters.test.mjs:36 passed. Overview tsc passed; Biome table.js/results.css clean. Scoped basedpyright site_navigation.py and test_site_navigation.py:0 errors/0 warnings. Design contract/link updated in paper-design.md; plan maintained by landings. Parent owns full rebuild, budgets, CI and commits.
