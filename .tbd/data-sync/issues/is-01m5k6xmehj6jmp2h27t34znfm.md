---
type: is
id: is-01m5k6xmehj6jmp2h27t34znfm
title: Share neutral topic chips between All Results and News
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
created_at: 2026-10-23T01:45:01.124Z
updated_at: 2026-10-23T02:03:13.670Z
started_at: 2026-10-23T01:45:41.884Z
closed_at: 2026-10-23T02:03:13.669Z
close_reason: Focused shared topic, breadcrumb and Contrast checks passed; final source staged for coordinator.
resolution: null
duplicate_of: null
---
Apply the accepted News topic vocabulary (shared neutral gray surface and corresponding readable colored topic ink in light/dark themes) to All Results table topic tags such as Upper bound and Optimality. Preserve verification/confirmation/status/significance rung colors and filter behavior. Identify the semantic topic column; reuse shared tokens rather than introducing a parallel palette. Validate rendered topic colors and unchanged rung colors, then stage for coordinator; no worker commits/full build.

## Notes

Complete. Focused project-env command: python -m pytest tests/test_rung_scale.py tests/test_site_navigation.py::test_breadcrumb_links_underline_only_on_hover_and_keep_keyboard_focus tests/test_site_navigation.py::test_theme_control_uses_the_shared_contrast_icon_size_and_keeps_its_name -q:27passed14.69s. Actual All Results topic fills/ink match News in both themes; V/C/status/significance colors preserved. Breadcrumb default/hover/focus desktop/mobile and Contrast size/Color theme/menu checks pass. Palette CLI exits0; external shared-topic-palette.txt. Ruff, BasedPyright0findings, probe tsc and Biome clean. Coordinator source checkpoint f490dd026; final tool/test/icon/docs followup staged. Parent/Frontier refresh global manifest CSS/nav refs. No worker commit.
