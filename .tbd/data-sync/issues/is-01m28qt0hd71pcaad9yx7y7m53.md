---
type: is
id: is-01m28qt0hd71pcaad9yx7y7m53
title: Set the panel's mathematics the way the explainer sets it
kind: task
status: closed
priority: 1
version: 2
spec_path: docs/project/specs/active/plan-2026-09-09-packing-strategies-as-a-shared-language.md
labels: []
dependencies: []
created_at: 2026-09-11T17:21:24.012Z
updated_at: 2026-09-11T18:53:57.999Z
closed_at: 2026-09-11T18:53:57.998Z
close_reason: "Done in b0fa05a6: the panel's three lines and the gap bar's two ends are rendered by KaTeX at build time through the explainer's own inliner, so kpress's katex-text-face composite comes with it; fractions are dfrac; the degree note is text-face ink rather than grey small-caps sans."
resolution: null
duplicate_of: null
---
The panel's proved facts are drawn with hand-placed spans: an italic serif 's', an upright '(n)', a relation glyph from a KaTeX-subset face, and a value in tabular figures. The exactness note is worse -- 'ALGEBRAIC · DEGREE 8' in grey small-caps sans, which makes a proved fact look like a caption.

The owner: proved facts and exact formulas should be in serif with proper KaTeX math typesetting, the same visual formatting as the explainer paper and kpress. And the algebraic/degree note should be black serif like the other proved facts, just smaller.

What this needs, and why it is not a CSS change: the explainer renders its mathematics through KaTeX at build time with devtools/prepare_explainer_math.py, which stamps the measured geometry into the page before it draws -- the same machinery that makes the explainer's formulas correct is what the panel is missing. The workbench build would do the same for its own small set of expressions: s(n) <= value, s(n) >= value, the closed forms like (7/2) + (3/2)sqrt(2), and the degree note.

The set is small and fixed per n, so this is a build-time render into inline SVG or KaTeX HTML, not a runtime dependency -- the page stays self-contained, which the Pages build checks.

Related: Phase 6A wants the palette to come from sqpack rather than a copy; this is the same argument for the typesetting.
