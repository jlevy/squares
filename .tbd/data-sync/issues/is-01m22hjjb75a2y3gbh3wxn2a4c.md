---
type: is
id: is-01m22hjjb75a2y3gbh3wxn2a4c
title: Render title s(11) as mathematics with an italic s
kind: bug
status: in_progress
priority: 2
version: 2
labels:
  - typography
  - explainer
dependencies: []
created_at: 2026-09-09T07:37:02.054Z
updated_at: 2026-09-09T07:38:54.409Z
---
The explainer hero title currently wraps the whole expression in a plain .symbol span, so s(11) is sans roman text. Render s(11) through the existing KaTeX/prepared-math architecture so s is mathematical italic while the relation and bound retain the designed sans title treatment. Add focused regression coverage for source and rendered output; avoid a CSS font-style workaround.
