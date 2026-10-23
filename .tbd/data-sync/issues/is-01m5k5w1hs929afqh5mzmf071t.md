---
type: is
id: is-01m5k5w1hs929afqh5mzmf071t
title: Restore case popover header controls, math pager and responsive visual width
kind: bug
status: closed
priority: 1
version: 5
spec_path: docs/project/specs/active/plan-2026-10-22-site-navigation.md
delegate: navigation-components
labels: []
dependencies: []
parent_id: is-01m5jnsqdwj3t8m7hkbx6mr1m2
hold: null
hold_until: null
created_at: 2026-10-23T01:26:40.440Z
updated_at: 2026-10-23T01:39:26.422Z
started_at: 2026-10-23T01:27:20.756Z
closed_at: 2026-10-23T01:39:26.421Z
close_reason: null
resolution: null
duplicate_of: null
---
Keep case popover expand/close controls in the upper-right independently of previous/next pager links. Render pager n labels using existing mathematical notation. Let the packing visual use the available popover content width with preserved aspect ratio and no mobile overflow. Preserve canonical case URLs and full-page behavior. Validate real n=5 at desktop/mobile and safely refresh Atlas/case leaves and shared assets; coordinator commits/builds.

## Notes

Completed case-header/visual fix and latest News Reset refinement. Original retained n5 test failed at1280: controls_top74.59 instead of46.6 because sticky offset added28px panel padding; diagram capped288/224px. Subtracting padding restores upper-right controls; fetched case figure fills available content width; canonical figure stays compact; details and mathematical prose retain630px reading measure. Pager n labels use existing _math()+SERIF_MATH, with prepared MathML and serif math. News Reset remains right-aligned in SAME row as Topics/Significance on desktop, count below, responsive wrapping. Evidence: SQPACK_SITE_PREVIEW_URL=http://127.0.0.1:8792 python -m pytest tests/test_site_case_records.py::test_the_popovers_cross_stands_in_its_corner_clear_of_the_steps tests/test_site_case_records.py::test_the_popovers_compact_drawing_keeps_its_own_line_weight:7passed7.78s; final n5-only3passed4.43s at1280/390/320 includes full-width/aspect/nooverflow, corner symmetry, math semantics, scroll/reachable close and focus restoration. tests/test_case_pages.py::test_each_record_steps_to_its_neighbours_with_the_sites_arrows:1passed51.79s. tests/test_rung_scale.py::test_rendered_news_topics_share_neutral_surfaces_and_reset_sits_above_count:1passed5.40s (both themes x1280/390/320; Reset same-row condition desktop). Ruff, Biome, probe tsc and BasedPyright0findings. Runtime checkpoint parent pushed cbb421dc1; six final preservation/test/probe files staged for parent followup. Safe non-pruning leaf refreshes: cases4/5/6/10 plus Overview/Atlas/Frontier/News; all four entry leaves verified reference final assets/css/site.3cb3108dc556ba1f.css. Plan/design notes handed to frontier_split. No worker commits or full builds.
