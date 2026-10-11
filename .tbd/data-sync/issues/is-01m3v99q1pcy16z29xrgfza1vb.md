---
type: is
id: is-01m3v99q1pcy16z29xrgfza1vb
title: "Homepage survey: hover keeps the packing's black lines; only the background tint changes"
kind: task
status: closed
priority: 2
version: 4
spec_path: docs/project/specs/active/plan-2026-09-29-github-pages-overview.md
labels: []
dependencies: []
parent_id: is-01m3p52z585a2zb9jmy19b0r96
created_at: 2026-10-01T08:29:05.970Z
updated_at: 2026-10-01T09:13:43.512Z
closed_at: 2026-10-01T09:13:43.511Z
close_reason: "ddcdcd6bf, merged into jlevy/squares#264: the atlas cell's drawing names its own ink, so the link's hover colour no longer reaches the strokes; the hover wash is unchanged; test_site_drawing_hover pins it in light and dark (10 passed)."
resolution: null
duplicate_of: null
---
Owner, 2026-10-01: hover on the survey on the homepage hides the black lines on the graphics. This doesn't look good. Don't do that. Just overlay with the hover background color change as you currently do. Find what the hover rule does to the tile's SVG (an opaque background painted over the strokes, a fill change on the squares, a blend mode, or a z-order overlay) and make the hover tint sit behind or beneath the strokes so every line stays at full black; check the frontier page's grid for the same fault; pin with a browser test that samples a stroke pixel with and without hover.

## Notes

Cause: the atlas grid's drawings are stroked in currentColor read from the cell's link, and KPress's .kpress a:hover (0,2,1) outranks .kpress .site-atlas-cell (0,2,0), so hover turned every line to the link's lighter accent (light: rgb(17,24,39) -> rgb(15,118,110); dark: rgb(232,237,243) -> rgb(110,197,188)). Fix on branch claude/site-polish-2-survey, commit ddcdcd6bf (not pushed): .site-atlas-cell svg names its own ink in packing/devtools/templates/site.css; the wash stays the cell's background. Pinned by packing/tests/test_site_drawing_hover.py (probe tests/probes/site_drawing_hover/drawing.js), 10 passed in Chromium, 4 fail with the declaration removed. Hero link and frontier thumbnails measured and not affected. paper-design.md Atlas grid entry updated.
