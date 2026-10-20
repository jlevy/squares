---
type: is
id: is-01m4kwdbnpyegmq64y1swnqs95
title: "Browser tools: every bare chromium.launch() honours one browser executable override (SQPACK_CHROMIUM vs SQUARES_BROWSER_EXECUTABLE)"
kind: bug
status: open
priority: 3
version: 3
labels:
  - tooling
dependencies: []
created_at: 2026-10-10T21:44:54.709Z
updated_at: 2026-10-11T07:19:51.529Z
---
Browser tools that call Playwright's `chromium.launch()` with no executable override cannot run in an environment whose installed Chromium build differs from the pinned Playwright's. The 2026-10-10 remote session showed it: /opt/pw-browsers holds chromium_headless_shell-1194, and Playwright 1.62.0 wants -1234. In that container the fast tier's "workbench browser behaviour in Chromium" step (devtools.check_motion_lab_pages) could not run locally. Found by lane L28 of the 2026-10-10 intake pass.

Widened 2026-10-11 from check_motion_lab_pages alone to every bare launch site, per review A3 on jlevy/squares#398 (https://github.com/jlevy/squares/pull/398#pullrequestreview-5482286271). #398 fixed the deployed-site checker's two launches; these remain. Sites on main at 8aba95081, by `git grep -n "chromium.launch("` with no executable_path:

- packing/devtools/check_motion_lab_pages.py:315
- packing/devtools/render_n11_optimality_review.py:553
- packing/devtools/render_n11_threshold_bound_review.py:602
- packages/workbench/tools/workbench_tools/cadence.py:584 (`launch(headless=True)`)
- packages/workbench/tools/workbench_tools/capture_stills.py:329, 352, 380, 434
- packages/workbench/tools/workbench_tools/capture_video.py:435, 484, 822
- packages/workbench/tools/workbench_tools/check_revision6.py:31
- packing/tests/test_render_n11_optimality_review.py:661, 688, 725 (tests; tests/site_browser.launch is the existing helper)
- the retained video spikes under packing/atlas/known-best/video/spikes/ (v1-slideshow/render_review.py, v2-transitions/*); decide whether they are in scope or left as historical

Two names for one override. Settle on one before adding more sites:
- `SQPACK_CHROMIUM` (devtools.render_n11_lower_bounds_explainer_pdf.BROWSER_OVERRIDE): read by about a dozen packing/devtools tools (preview_site.launch_chromium, check_published_site, measure_atlas_views, measure_site_pages, the explainer PDF and math tools, and others), the tests/site_browser tests, and, in the workbench package, smoke_capture.py, benchmark.py and check_candidate.py.
- `SQUARES_BROWSER_EXECUTABLE`: read by the workbench package's arrival_frames.py, check_accessibility.py, check_animate_view.py, check_animation_editor.py, check_layout.py, check_pack_panel.py, check_page_policy.py, check_search_panel.py, check_stage_resize.py, check_transitions.py and layout_gallery.py, and by packing/tests/test_paper_publication.py.

Fix: choose the one name (or accept both through one shared reader), route every site above through it, and add a test per launcher that the override is honoured, on the pattern of tests/test_site_browser.py and test_both_browser_checks_launch_the_chromium_the_environment_names in tests/test_check_published_site.py.
