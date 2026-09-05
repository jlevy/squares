---
type: is
id: is-01m1stehnxfjd4g4h6wpe9p1bx
title: "Explainer: the published Markdown mentions a control it does not have, and carries less of Figure 7 than the page"
kind: bug
status: open
priority: 3
version: 1
labels: []
dependencies: []
created_at: 2026-09-05T22:18:57.597Z
updated_at: 2026-09-05T22:18:57.597Z
---
Measured 2026-09-05. The Markdown edition otherwise stands on its own: one image (Figure 1, same 196-char alt), Figures 2-7 as caption-only paragraphs whose captions state what the figure shows rather than deferring to it, no 'see Figure 3' pattern, and every pointer-only instruction correctly stripped by the screen-only spans.

Two gaps. Line 60 reads 'The chooser under each figure switches every figure between the two at once', a reference to an interactive control the Markdown edition does not have; in the HTML that sentence is inside a screen-only span, in the .md it is unconditional. And Figure 7's data is thinner than the HTML's: the rendered SVG's aria-label enumerates all five points (K=10 gives 0, K=30 gives 0.3256, K=60 gives 0.82113, K=90 gives 0.907055, K=180 gives 1.00006) where the Markdown caption gives only the summary, and the .md carries only the 19/5 variant's caption so the 381/100 series is absent entirely.
