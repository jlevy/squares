---
type: is
id: is-01m1t3t28mj04vs7dp9fr97x2t
title: "Explainer PDF: 17 Type3 fonts, 179 KB, from the variable Source Sans 3"
kind: task
status: open
priority: 2
version: 1
labels: []
dependencies: []
created_at: 2026-09-06T01:02:32.212Z
updated_at: 2026-09-06T01:02:32.212Z
---
Measured 2026-09-06 on the generated explainer PDF. The file carries 17 separate Type3 font objects, all SourceSans3-Roman, totalling 179,531 bytes of CharProcs -- 18% of the whole file, and more than all the real embedded TrueType programs combined (136,182). One copy per page, per weight.

Cause proven by a controlled test rather than inferred: a three-line document using the page's own font-face blocks renders 'Source Sans 3 Variable' (font-weight: 200 900) as Type3 and 'PT Serif' (static, weight 400) as Type0/TrueType. Skia cannot embed a variable-font instance in a PDF and falls back to per-page Type3 outlines.

Measured saving: substituting a static face for the sans removed all 17 Type3 objects and took the file from 999,246 to 783,684 bytes, minus 21.6%, with pagination unchanged.

Nothing is visually or textually broken -- the glyphs are vector and ToUnicode works -- so this is size and profile conformance, not correctness. Type3 is penalised by PDF/A and PDF/UA and handled poorly by some tools.

Fix: a print-only font-face serving a static Source Sans 3 instance (Regular plus Semibold woff2) with --kpress-font-sans pointed at it inside @media print. Needs the static woff2 files, which kpress does not currently vendor, so it is a kpress question as much as a squares one.
