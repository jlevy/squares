---
type: is
id: is-01m1yxsk25gtbjyhredzhqyp4f
title: Subset the inlined KaTeX faces to the glyphs the page's mathematics uses
kind: task
status: open
priority: 2
version: 1
spec_path: docs/project/specs/active/plan-2026-09-07-math-text-face.md
labels:
  - explainer
dependencies: []
parent_id: is-01m1yxs9c3y78m00gqh7wsz9d6
created_at: 2026-09-07T21:53:37.347Z
updated_at: 2026-09-07T21:53:37.347Z
---
The page inlines eight full KaTeX faces (181 KB of base64: Main 89, AMS 37, Math 21, Caligraphic 9, Size1-4 25) though with the math text face they draw only operators, relations, delimiters, Greek and symbols, and only those the explainer's mathematics contains. The page's math is static, so render_explainer can subset each face with fontTools (already a dev dependency) to the code points the rendered KaTeX output uses in both modes (the katex opt-out draws Latin and digits from these faces too, so include the page's Latin and digits for Main and Math), rewrite the data URIs, and keep a --check that the subset covers every glyph the page renders (a Playwright pass with document.fonts and a missing-glyph probe). Expected saving roughly 120 KB; do after kpr-hhdc ships the composite subsets so the two do not overlap.
