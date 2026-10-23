---
type: is
id: is-01m5k7hryzkf4jsfzn115887g9
title: Use Lucide Contrast for the shared color-theme control
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
created_at: 2026-10-23T01:56:01.105Z
updated_at: 2026-10-23T02:03:13.688Z
started_at: 2026-10-23T01:56:36.530Z
closed_at: 2026-10-23T02:03:13.688Z
close_reason: Focused shared topic, breadcrumb and Contrast checks passed; final source staged for coordinator.
resolution: null
duplicate_of: null
---
Replace the shared navigation color-theme gear with Lucide Contrast (half-filled black/white circle), using existing pinned icon conventions and shared icon size. Preserve the accessible Color theme name, focus behavior and theme selection. Keep scope to the shared icon surface and focused semantic check.

## Notes

Complete. Focused project-env command: python -m pytest tests/test_rung_scale.py tests/test_site_navigation.py::test_breadcrumb_links_underline_only_on_hover_and_keep_keyboard_focus tests/test_site_navigation.py::test_theme_control_uses_the_shared_contrast_icon_size_and_keeps_its_name -q:27passed14.69s. Actual All Results topic fills/ink match News in both themes; V/C/status/significance colors preserved. Breadcrumb default/hover/focus desktop/mobile and Contrast size/Color theme/menu checks pass. Palette CLI exits0; external shared-topic-palette.txt. Ruff, BasedPyright0findings, probe tsc and Biome clean. Coordinator source checkpoint f490dd026; final tool/test/icon/docs followup staged. Parent/Frontier refresh global manifest CSS/nav refs. No worker commit.
