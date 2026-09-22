---
type: is
id: is-01m356gsjz9rg590k4sagxy090
title: "D-490 returns: name the explainer PDF's one-line layout wobble and make the check bound it"
kind: bug
status: open
priority: 1
version: 3
labels: []
dependencies: []
created_at: 2026-09-22T18:37:14.710Z
updated_at: 2026-09-22T19:29:42.548Z
---
PR 218 run 35764316182 failed the pages `pdf` job: `render_explainer_pdf --check-artifact` reported 843296 then 843299 bytes, first difference in object 163, a page content stream. Decompressed, the only difference in the whole document is one inline KaTeX math box's text matrix: three `Tm` lines move from y=14906 to y=14905.2188, a 0.78125 CSS px baseline shift on the math `500000000/498684619`. Object 1 (the dates) is the only other object that differs. Reproduced locally from the run's own prepared page. D-490 records the incident class.

## Notes

Cause named and measured (2026-09-22).

WHAT DIFFERED. Both renders from run 35764316182 were retained. A whole-document object
diff finds exactly two objects changed: object 1, the two clock fields, and object 163, a
page content stream. Decompressed, object 163 differs in three `Tm` lines, all belonging
to one inline KaTeX math box (`500000000/498684619`): y = 14905.2188 against y = 14906, a
0.78125 CSS px baseline shift. Same glyphs, same advances, same fonts, same pagination,
1298 objects otherwise equal.

CAUSE. `page.emulate_media(media=print)` answers `@media print` but fires neither
`beforeprint` nor `afterprint`; a real print fires both. packing/devtools/explainer/
certificate.js ends with `window.addEventListener("beforeprint", repaint)` and the same
for `afterprint`; `repaint` re-runs `boot()`, which reaches eleven `tex(...)` calls, i.e.
`squaresMath.render`, asynchronously. Measured with a MutationObserver installed across
`page.pdf()`: a settled page left alone 1500 ms records 0 mutations; every print records
366 attribute writes, 183 at print-enter and 183 at print-exit, on math boxes whose inline
`style` carries KaTeX width/height/vertical-align in em. The print layout runs over a
moving DOM, and four consecutive prints each record the same 366, so no wait absorbs it.

RATE. Reproduced locally from that run's own prepared-page artifact on the pinned headless
shell: 1 render in 30 differed, a different box (a formula's `sin`) by 0.609375 px.

FIX IN THIS LANE. `render_explainer_pdf._draw_reproduced` prints until two consecutive
prints of one loaded page agree once the clock fields are normalised, returns that pair's
second, and refuses after 4. Every repeat is logged with the object it disagreed in, so
the runner's own rate becomes readable. Verified with an injected one-shot transient: a
single draw produced a different document, the repeated draw produced the settled one.

STILL OPEN. The cause-level fix -- do not re-render math from the print handlers, or make
`squaresMath.render` a no-op on unchanged TeX -- belongs in
packing/devtools/explainer/certificate.js, which this lane did not own.
