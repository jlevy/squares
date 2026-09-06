---
type: is
id: is-01m1t3t2pr5nrb6hx3r3hv18na
title: "Explainer PDF: one 60 DPI bitmap, from putImageData in the prover canvas"
kind: task
status: open
priority: 3
version: 1
labels: []
dependencies: []
created_at: 2026-09-06T01:02:32.664Z
updated_at: 2026-09-06T01:02:32.664Z
---
Measured 2026-09-06. The PDF is essentially all vector -- the atlas is 41,738 path operations, Figure 4 is 11,416, Figure 5 is 9,280 -- with exactly one raster image in the whole document: 230x230 px placed 3.867in wide, which is 59.5 DPI. Visibly blocky, with crisp vector atoms drawn over a stepped colour field.

It is the heat field inside the prove canvas: createImageData(RES, RES) with RES = 230. Chromium replays a canvas's drawing commands as PDF vector paths, but putImageData data is a genuine bitmap at its authored size.

deviceScaleFactor does NOT help and should not be added: rendered at 1, 2 and 4 the PDFs are byte-identical after normalising the two date fields. It affects screenshots only. Nothing in the browser API can fix this.

Fix: raise RES in the page's own JS for the print path -- 600 to 900 would put the field at 155 to 233 DPI. Worth checking what that costs the interactive page before making it unconditional.
