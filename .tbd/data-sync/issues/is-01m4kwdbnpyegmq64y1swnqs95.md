---
type: is
id: is-01m4kwdbnpyegmq64y1swnqs95
title: "Browser tools that ignore the executable override: check_motion_lab_pages and the rest, under one override name"
kind: bug
status: open
priority: 3
version: 2
labels:
  - tooling
dependencies: []
created_at: 2026-10-10T21:44:54.709Z
updated_at: 2026-10-11T07:17:49.081Z
---
Several browser tools call playwright's chromium.launch() with no executable override, so in a container whose installed Chromium build differs from the pinned Playwright's (2026-10-10 remote session: /opt/pw-browsers holds chromium_headless_shell-1194, Playwright 1.62.0 wants -1234) they cannot run locally. check_published_site's two launches honour SQPACK_CHROMIUM since #398.

Sites still ignoring it on main 8aba95081 (from #398's review A3):
- packing/devtools/check_motion_lab_pages.py:315 (blocks the fast tier's 'workbench browser behaviour in Chromium' step locally; found by lane L28 of the 2026-10-10 intake pass)
- packing/devtools/render_n11_optimality_review.py:553
- packing/devtools/render_n11_threshold_bound_review.py:602
- packages/workbench/tools/workbench_tools/cadence.py:584 (launch(headless=True))
- packages/workbench/tools/workbench_tools/capture_stills.py:329, 352, 380, 434
- packages/workbench/tools/workbench_tools/capture_video.py:435, 484, 822
- packages/workbench/tools/workbench_tools/check_revision6.py:31

Settle the name first: the workbench package reads both SQPACK_CHROMIUM (smoke_capture.py, benchmark.py, check_candidate.py) and SQUARES_BROWSER_EXECUTABLE (arrival_frames.py, check_accessibility.py, check_animate_view.py, check_animation_editor.py and others). Standardise on one, route the sites above through preview_site.launch_chromium or the same override, and test that each honours it.
