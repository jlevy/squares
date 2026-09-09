---
type: is
id: is-01m22hjjb75a2y3gbh3wxn2a4c
title: Render title s(11) as mathematics with an italic s
kind: bug
status: in_progress
priority: 2
version: 3
labels:
  - typography
  - explainer
dependencies: []
created_at: 2026-09-09T07:37:02.054Z
updated_at: 2026-09-09T07:44:56.813Z
---
The explainer hero title currently wraps the whole expression in a plain .symbol span, so s(11) is sans roman text. Render s(11) through the existing KaTeX/prepared-math architecture so s is mathematical italic while the relation and bound retain the designed sans title treatment. Add focused regression coverage for source and rendered output; avoid a CSS font-style workaround.

## Notes

Implemented in the shared worktree without commit: explainer title now renders only s(11) through the existing .tex/KaTeX path; relation and bound remain sans title text. Published Markdown preserves math delimiters around s(11). Regression covers exact heading structure. Validation: 100 focused tests passed across test_explainer.py and test_render_explainer_fonts.py; Ruff passed; prepared render in attic/title-s11 contains custom-sans and system fallback variants with KaTeX .mathnormal s and font-style italic.
