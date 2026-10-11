---
type: is
id: is-01m1stehnxfjd4g4h6wpe9p1bx
title: "Explainer: the published Markdown mentions a control it does not have, and carries less of Figure 7 than the page"
kind: bug
status: open
priority: 3
version: 2
labels: []
dependencies: []
created_at: 2026-09-05T22:18:57.597Z
updated_at: 2026-10-06T08:29:02.885Z
---
Measured 2026-09-05. The Markdown edition otherwise stands on its own: one image (Figure 1, same 196-char alt), Figures 2-7 as caption-only paragraphs whose captions state what the figure shows rather than deferring to it, no 'see Figure 3' pattern, and every pointer-only instruction correctly stripped by the screen-only spans.

Two gaps. Line 60 reads 'The chooser under each figure switches every figure between the two at once', a reference to an interactive control the Markdown edition does not have; in the HTML that sentence is inside a screen-only span, in the .md it is unconditional. And Figure 7's data is thinner than the HTML's: the rendered SVG's aria-label enumerates all five points (K=10 gives 0, K=30 gives 0.3256, K=60 gives 0.82113, K=90 gives 0.907055, K=180 gives 1.00006) where the Markdown caption gives only the summary, and the .md carries only the 19/5 variant's caption so the 381/100 series is absent entirely.

## Notes

2026-10-06 (bead review): gap 1 is fixed on origin/main (render_n11_lower_bounds_explainer strips multi-line screen-only spans; test_no_screen_only_prose_survives_into_the_published_document). Gap 2, Figure 7's thinner Markdown caption and the missing 381/100 series, was not rechecked in full and appears still open.
