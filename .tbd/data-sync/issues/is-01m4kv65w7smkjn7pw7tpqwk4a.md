---
type: is
id: is-01m4kv65w7smkjn7pw7tpqwk4a
title: Align shared Atlas legend color swatches with text
kind: bug
status: in_progress
priority: 2
version: 5
spec_path: docs/project/specs/active/plan-2026-10-08-site-layout-and-navigation.md
delegate: codex@spud10
labels: []
dependencies: []
parent_id: is-01m4ewpe4eqqjvrq6henxdzkh9
hold: null
hold_until: null
created_at: 2026-10-10T21:23:30.810Z
updated_at: 2026-10-10T22:00:07.862Z
started_at: 2026-10-10T21:24:11.328Z
---
Make angle/contact legend swatches square, about the text line height, aligned with adjacent text on homepage and dedicated Atlas. Use shared design styles and preserve responsive wrapping/theme colors. Apply the same square color-swatch shape and comparable text-line sizing/alignment to both published Atlas PDF legends, preserving all legend wording, scientific packing geometry, palettes, evidence badges and upstream print improvements; regenerate the required Atlas SVG/PNG/PDF export families with the targeted builder.

## Notes

Owner approved PDF regeneration after web refinement. Final PDF swatches match adjacent font size: 19/48-unit squares with bold 0.6-em degree labels; web uses 1-em squares and 0.65-em semibold labels near the text baseline. Both PDFs visually inspected clean. All nonlegend SVG geometry and descriptions are exactly unchanged versus the preceding commit; legend wording and evidence badges are unchanged. Stroke-inclusive hue/shade row gaps are 6.78 and 17.13 units; horizontally adjacent keys touch. Both existing PDF legend tests passed in 5.24 seconds. Exports regenerated, publication and final-head CI pending.
