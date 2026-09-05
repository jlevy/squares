---
type: is
id: is-01m1s8frk9zcp018kbgph4dafv
title: "Typography: the thin space after the italic function name must be consistent in every context"
kind: bug
status: closed
priority: 2
version: 2
labels: []
dependencies: []
created_at: 2026-09-05T17:05:03.081Z
updated_at: 2026-09-05T17:10:13.166Z
closed_at: 2026-09-05T17:10:13.166Z
close_reason: "Done in 6021f6dc: one rule spaces a lone italic function name from its parenthesis, applied on both paths that set mathematics here. kerned_math_spans in render_explainer rewrites the Markdown math kpress renders at build time, and the same regex in the shell's two katex helpers covers the caption and readout spans rendered in the browser; the drawn figures already used the same one-mu offset via SUMMARY_ITALIC_KERN. cos(x) and prose parentheses are untouched, verified by unit check and by measuring the rendered gap in a browser (0.94px in a caption, 1.05px in prose)."
resolution: null
duplicate_of: null
---
Owner 2026-09-05: the atlas SVG now sets s(n) with a thin space after the italic s, but the explainer's diagram captions and math do not, so the parenthesis sits against the s. Make it consistent everywhere: the SVG cards and footer, the page's KaTeX math and captions, and any SVG text labels in the figures.
