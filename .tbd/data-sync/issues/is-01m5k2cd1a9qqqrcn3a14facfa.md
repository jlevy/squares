---
type: is
id: is-01m5k2cd1a9qqqrcn3a14facfa
title: Use shared significance segments on Results Archive
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
created_at: 2026-10-23T00:25:42.183Z
updated_at: 2026-10-23T00:42:17.853Z
started_at: 2026-10-23T00:25:50.320Z
closed_at: 2026-10-23T00:42:17.852Z
close_reason: Shared Archive significance segments and URL adapters are implemented; actual desktop/mobile selection/reload/history/legacy/project/V-C/no-JS checks2passed, existing deep-link/default regressions6passed, Node37passed.
resolution: null
duplicate_of: null
---
Replace Results Archive significance minimum dropdown with inline S1 through S5 multiselect segments using same shared styling as News/homepage choosers. Preserve current default coverage, existing query links including exact significance project links and threshold links, history/back/reset behavior, counts and no-JavaScript access. Keep other rating filters unchanged. Document selection semantics and verify focused browser behavior.

## Notes

Implemented S1-S5 native multiselect segments in Results Archive, using the shared site-tabs/site-chooser-small styling already used by News and homepage Grid/Triangle. Every S level starts selected; noncontiguous selection is OR within S and composes by AND with existing V/C and other facets. The generic table constructs a one-of filter from pressed segment buttons and skips hidden legacy S adapters. Initial exact s=N, comma-separated s=1,3,5 and legacy s-min/s-max intersection links remain meaningful without rewriting the initial address. A segment click preserves unrelated parameters and fragments, writes canonical s values (s=none for empty selection, omits s for all), and Back/Forward restore segments/counts. Bare-page load resets all levels. Hidden S adapters remain hidden; V/C controls unchanged. With JavaScript disabled every row is available and controls are omitted. Project tallies now start from the actual Resources catalogue and assert selected S segments instead of the obsolete visible At significance control. Design policy updated in paper-design.md; plan maintained by landings.

Evidence from packing with task environment: python -m pytest tests/test_site_result_filters.py::test_significance_segments_preserve_selection_legacy_links_and_history -q -x --tb=short: 2 passed in117.83s (1280/390 actual page, noncontiguous/reload/counts/history/none/default/min/max/exact/project/V-C/no-JS). Requested existing project-tally/home-query/default-helper cases: 6 passed49.82s. node --test tests/node/overview_table/table.test.mjs tests/node/overview_table/filters.test.mjs:37 passed; existing36 plus noncontiguous/empty membership. Overview tsc and scoped Python source/test BasedPyright:0 errors/0 warnings; Ruff and Biome clean. Review caught an initially missed readFilters edit and selector-blind Node fixture; both corrected before source-ready. Parent owns source commits, full rebuild and current-head CI.
