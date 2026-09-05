---
type: is
id: is-01m1sc1e7zbqbp4vz6301hk2c0
title: "Explainer PDF: the >= glyph prints heavier than the digits beside it"
kind: task
status: closed
priority: 2
version: 2
labels: []
dependencies: []
created_at: 2026-09-05T18:07:08.031Z
updated_at: 2026-09-05T18:39:04.429Z
closed_at: 2026-09-05T18:39:04.429Z
close_reason: "The >= was a literal U+2265 in the hero: Source Sans 3 lacks it, and at weight 550 CSS matching searches upward, so the fallback family answered with Bold (DejaVu Sans Bold in the printed file, 18% heavier in stroke). Fixed by naming the weight on a .rel span, family inherited. DejaVuSans-Bold no longer appears in the PDF at all."
resolution: null
duplicate_of: null
---
In s(11) >= 381/100 = 3.81 the relation symbol reads bold against its neighbours in the printed PDF. Measured in the DOM under both screen and print media, every part computes to font-weight 400 and resolves to KaTeX_Main (custom), so the cause is not the CSS cascade. Under forensics on the PDF artifact itself.
