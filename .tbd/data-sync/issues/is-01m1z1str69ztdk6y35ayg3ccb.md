---
type: is
id: is-01m1z1str69ztdk6y35ayg3ccb
title: "No font swap on the explainer's math at load: verify the composite faces are loaded before the first render"
kind: task
status: open
priority: 1
version: 1
spec_path: docs/project/specs/active/plan-2026-09-07-math-text-face.md
labels:
  - explainer
  - typography
dependencies: []
parent_id: is-01m1yxs9c3y78m00gqh7wsz9d6
created_at: 2026-09-07T23:03:39.523Z
updated_at: 2026-09-07T23:03:39.523Z
---
Owner (2026-09-07): digits in formulas visibly change font when the page loads, on the built page and the live site. Cause and fix are kpress bead (see the kpress fonts epic kpr-b4mq): katex-init renders before the composite's PT Serif slot is decoded, and the faces have no font-display. Adopt the kpress fix (gitlink bump) and add a check to inspect_explainer_typography (or a Playwright test) that loads the built page with an init script recording the first .katex insertion against each KPress Math Text face's status, asserting every composite face and every KaTeX face the page inlines is loaded before the first math node is inserted, in screen and print media; run it against the live site once deployed. Record the measured timeline before and after in the plan spec's Font Consistency section.
