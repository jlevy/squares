---
type: is
id: is-01m3wf67f0dyqzadgw5b1ccxmr
title: "Type consistency: what the site-wide measurement found and left"
kind: task
status: open
priority: 3
version: 1
spec_path: docs/project/specs/active/plan-2026-09-29-github-pages-overview.md
labels: []
dependencies: []
parent_id: is-01m3p52z585a2zb9jmy19b0r96
created_at: 2026-10-01T19:31:17.599Z
updated_at: 2026-10-01T19:31:17.599Z
---
From the typography lane's report, 2026-10-01 (think-jc3w): (1) off macOS the two papers keep text-rendering geometricPrecision on formulas while site pages are auto; unifying needs a Linux measurement and changes the first paper's bytes. (2) The optimality paper's diagram labels type ≤ ≥ τ and subscripts as text, drawn from .SF NS and Apple Symbols on a Mac and embedded in the PDF. (3) TUTORIAL.md and SYNOPSIS.md write some mathematics and diagrams as code (≥, μ(Q) = Σ {…}, 2 + 4/√5, box-drawing arrows), drawn from Menlo. (4) The recent-bound star and the atlas's '✓ same' are characters no shipped face has. (5) The homepage hero caption is a literal 0.85; the site subtitle is italic by KPress's .subtitle, which paper-design.md does not say. (6) The workbench's formulas are stock KaTeX_Main without MathML at 1.18x and 4.14x of their text. (7) result/t-NNN.html opened directly is an unstyled fragment with math untypeset. (8) Math inside medium or bold text stays regular.
