---
type: is
id: is-01m4kv65w7smkjn7pw7tpqwk4a
title: Align shared Atlas legend color swatches with text
kind: bug
status: in_progress
priority: 2
version: 4
spec_path: docs/project/specs/active/plan-2026-10-08-site-layout-and-navigation.md
delegate: codex@spud10
labels: []
dependencies: []
parent_id: is-01m4ewpe4eqqjvrq6henxdzkh9
hold: null
hold_until: null
created_at: 2026-10-10T21:23:30.810Z
updated_at: 2026-10-10T21:45:24.660Z
started_at: 2026-10-10T21:24:11.328Z
---
Make angle/contact legend swatches square, about the text line height, aligned with adjacent text on homepage and dedicated Atlas. Use shared design styles and preserve responsive wrapping/theme colors. Apply the same square color-swatch shape and comparable text-line sizing/alignment to both published Atlas PDF legends, preserving all legend wording, scientific packing geometry, palettes, evidence badges and upstream print improvements; regenerate the required Atlas SVG/PNG/PDF export families with the targeted builder.

## Notes

Owner review on 2026-10-10 requested a WEB-ONLY refinement before any further PDF regeneration: smaller 1em color squares, larger degree labels, close alignment to the visible text baseline. Current live CSS uses 1em squares (17.46875px), 0.65em labels (11.362px), baseline row alignment and a -0.1em upward swatch offset; 90°/45° text measures 15.09375px and fits. Four existing-probe desktop/mobile homepage/Atlas checks and screenshots passed; live preview http://127.0.0.1:8766/ uses site.89de311e10b826e6.css. Only shared CSS and its existing geometry probe changed. PDF/SVG/PNG exports and print generator are untouched in this iteration; further PDF work and Git publication wait for owner web review. Durable visual evidence: atlas-swatch-alignment/web-refinement in the task visualization directory.
