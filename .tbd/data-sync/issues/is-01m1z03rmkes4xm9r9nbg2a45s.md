---
type: is
id: is-01m1z03rmkes4xm9r9nbg2a45s
title: "Italic variable in the title: the s in s(11), and sans mathematics in headings once it exists"
kind: task
status: open
priority: 2
version: 1
spec_path: docs/project/specs/active/plan-2026-09-07-math-text-face.md
labels:
  - explainer
  - typography
dependencies: []
parent_id: is-01m1yxs9c3y78m00gqh7wsz9d6
created_at: 2026-09-07T22:34:07.886Z
updated_at: 2026-09-07T22:34:07.886Z
---
Owner (2026-09-07): the s in s(11) in the title is a variable and should be italic, as it is in the prose mathematics. Two parts. Now: set the s italic in the title's symbol line (a var or italic span at the title's weight, with the parentheses and digits upright), confirm the print instance set covers italic at that weight (PRINT_FACES has 550 italic), and check the screen and PDF. Later, once kpress's sans math (kpr-7f9z, adopted by think-n4y7) exists: evaluate setting the title's s(11) and any other heading symbol (s(n) in section headings, the hero relation line) as KaTeX with the sans composite at the heading's weight, so the italic s, the digits and the relations all come from the heading's own face with proper metrics; compare against the hand-set italic on screen and in the PDF and record the choice in the plan spec's Font Consistency section.
