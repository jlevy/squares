---
type: is
id: is-01m1ybsgmykx4dtn6xb1a81jjq
title: "Research: harmonize PT Serif prose with KaTeX math in the explainer page"
kind: task
status: closed
priority: 2
version: 5
spec_path: vendor/kpress/docs/math-text-face.research.md
labels:
  - research
  - kpress
dependencies:
  - type: blocks
    target: is-01m1ycfpc3pv67mt54g7857vk6
created_at: 2026-09-07T16:39:00.508Z
updated_at: 2026-09-07T17:42:05.973Z
closed_at: 2026-09-07T16:51:08.283Z
close_reason: "Research brief written: docs/project/research/research-2026-09-07-text-font-math-font-harmony.md. Metrics measured, eight prototype variants compared, prior art surveyed (LaTeX, KaTeX/MathJax/Temml/MathML Core, CSS). Recommendation: route letters and digits to PT Serif via a unicode-range composite plus PT Serif metrics through katex.__setFontMetrics; operators stay KaTeX. Implementation tracked in the follow-up bead."
resolution: null
duplicate_of: null
---
Review how the explainer page loads fonts and whether KaTeX letters and digits can be drawn from PT Serif while symbols stay in the KaTeX faces. Survey prior art in LaTeX (mathastext, unicode-math ranges, newtx), MathJax/Temml/MathML Core, and CSS font mechanics (unicode-range composites, size-adjust, font-size-adjust). Measure the metrics, prototype the CSS routes on the rendered page, and record the findings in the research brief.
