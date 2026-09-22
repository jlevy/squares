---
type: is
id: is-01m356gsjz9rg590k4sagxy090
title: "D-490 returns: name the explainer PDF's one-line layout wobble and make the check bound it"
kind: bug
status: open
priority: 1
version: 1
labels: []
dependencies: []
created_at: 2026-09-22T18:37:14.710Z
updated_at: 2026-09-22T18:37:14.710Z
---
PR 218 run 35764316182 failed the pages `pdf` job: `render_explainer_pdf --check-artifact` reported 843296 then 843299 bytes, first difference in object 163, a page content stream. Decompressed, the only difference in the whole document is one inline KaTeX math box's text matrix: three `Tm` lines move from y=14906 to y=14905.2188, a 0.78125 CSS px baseline shift on the math `500000000/498684619`. Object 1 (the dates) is the only other object that differs. Reproduced locally from the run's own prepared page. D-490 records the incident class.
