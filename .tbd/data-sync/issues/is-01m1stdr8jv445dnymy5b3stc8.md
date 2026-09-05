---
type: is
id: is-01m1stdr8jv445dnymy5b3stc8
title: "Explainer: 115 KB of never-drawn font faces sit on the render-blocking critical path"
kind: task
status: open
priority: 1
version: 1
labels: []
dependencies: []
created_at: 2026-09-05T22:18:31.570Z
updated_at: 2026-09-05T22:18:31.570Z
---
Measured 2026-09-05 by extracting all 111 TeX strings the page contains (71 kpress-math-render nodes plus 40 from the interactive figures), rendering every one through the page's own extracted KaTeX 0.16.45 at its real display mode, and walking the output's class stack against the page's own class-to-font CSS. Zero render failures.

Drawn: KaTeX_Main-Regular, KaTeX_Main-Bold, KaTeX_Math-Italic, KaTeX_Size1, KaTeX_Size2. Never drawn, with bytes in the HTML: Source Sans 3 Variable italic 38,435; PT Serif 700 italic 38,386; KaTeX_AMS 37,572; KaTeX_Main 400 italic 22,789; KaTeX_Caligraphic 9,356; KaTeX_Size4 6,710; KaTeX_Size3 4,970.

The two prose faces are provable by selector rather than by content: every italic-producing selector resolves to .kpress-prose h4 (no h4 exists; the document is 1 h1 and 12 h2), .kpress .hero h1 i (the hero h1 has no i, only span.symbol) and .cert-page .hero .deck (no .deck exists). What does fire is .subtitle and one em, both weight 400, so PT Serif 700 italic is unreachable and sans italic has no reachable selector at all.

Effect of dropping all seven: raw 1,130,624 -> 972,406; gzip 514,169 -> 396,318, a saving of 115.1 KB. All of it is in head -- head ends at byte 621,725, 55% of the file, 69% of it base64 woff2 -- so the render-blocking prefix goes 371.9 KB -> 257.0 KB.

Do it in the renderer, not by hand: the renderer already inlines per document, so it can select faces from the document it just rendered, and the saving then stays correct when content changes. A hand-pruned list breaks the day someone writes an h4 or uses \\mathbb.

Two further levers, noted not prescribed: KaTeX_Main-Bold (33,905 B) is carried for one glyph, the bold D of \\mathbf{D}_4, which appears twice; and subsetting the used faces to the 91 distinct characters the article contains is a further large win (unmeasured, fontTools not installed).
