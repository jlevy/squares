---
type: is
id: is-01m1t3tm3hwtsjby69cnmvzvf7
title: "Explainer PDF: the square root vanishes from the text layer, and the atlas depends on host fonts"
kind: bug
status: open
priority: 2
version: 1
labels: []
dependencies: []
created_at: 2026-09-06T01:02:50.480Z
updated_at: 2026-09-06T01:02:50.480Z
---
Two findings from the 2026-09-06 print-quality measurement, both about text fidelity rather than layout.

1. The radical is not a character. 's(10) = 3 + 1/sqrt(2)' extracts from the PDF as 's(10) = 3 + 1/'. There are zero occurrences of U+221A in the entire document: KaTeX draws the radical as an inline SVG path, and KaTeX_Size2 maps one glyph to U+FFFF. A reader who copies that expression out of the PDF gets a DIFFERENT NUMBER, which for a mathematics paper is the worst class of extraction bug. Reading order around inline math is also scrambled -- the math is pulled out of its sentence. Inherent to KaTeX's HTML output, not a Chromium fault. The fix is aria-label or an x-tex annotation, or rendering display math with output 'htmlAndMathml' so a MathML annotation carries the true expression.

2. The atlas labels and every code span depend on fonts the host happens to have. PT Serif and Source Sans 3 are embedded as woff2 data URIs, so prose is stable anywhere. But known-best-1-100.svg sets font-family='Helvetica, Arial, sans-serif' in 468 places and neither is installed on a Linux runner -- the PDF picked up LiberationSans-Bold and LiberationSerif. --kpress-font-mono is unset, so code fell back to DejaVuSansMono. On a Mac the same export uses Helvetica and Menlo. So the PDF is not reproducible across machines for the atlas labels and all code, even though the prose is. Point those at the already-embedded families.

Also measured and worth keeping: only 3 of 10 Figure structs carry /Alt -- the SVGs with role='img' and aria-label. The three canvas figures and four other SVGs give a screen reader nothing, which is the same gap think-2ges records for the page.
