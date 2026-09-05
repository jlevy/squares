---
type: is
id: is-01m1stegy156vepvzth51vbypz
title: "Explainer: four small rendering and contrast defects found by the page audit"
kind: bug
status: open
priority: 2
version: 1
labels: []
dependencies: []
created_at: 2026-09-05T22:18:56.833Z
updated_at: 2026-09-05T22:18:56.833Z
---
Four independent, each small, measured 2026-09-05. Grouped because each is a one-to-three line change in the same file.

1. A CSS rule silently discards Figure 3's accent. explainer-shell.html: '.line-fig svg text, .chart svg text { fill: var(--kpress-doc-muted); }'. CSS beats presentation attributes, so Figure 3's own label, authored as fill=var(--cert-probe) to mark the new bound, renders #5b6472 instead of #b15300. The line and circle at x=284 keep the accent because they use stroke/fill on non-text elements, so the new bound is an orange tick with a grey label. The bound labels 3.7888543... and 3.8770835... lose their --kpress-doc-text fill the same way. Not a WCAG failure (the grey measures 5.98:1 and the words carry the meaning), a rendering bug with a visual-emphasis cost.

2. Figure 5's legend swatch --cert-near #c9a13a is 2.43:1 against white, below the 3:1 WCAG 1.4.11 needs for a graphical object that conveys meaning. Dark is fine at 7.6:1. Its neighbour --cert-below #e26e82 passes by a hair at 3.09:1.

3. The PDF chip is a link doing a button's job: <a class=chip href='#' data-print=page>, whose handler preventDefaults and calls window.print(). It announces as 'PDF, link' pointing at #. It should be a button. Separately 'MD' is a cryptic accessible name whose explanation lives in title, which screen readers do not reliably announce.

4. Figure 2's SVG description is provenance, not description: the accessible name is 'Known-best packing of 11 unit squares / The retained known-best n=11 construction, normalized to Witness/v2 and rendered with the repository's deterministic house renderer.' A reader who cannot see it learns nothing about how eleven squares sit in the container -- how many axis-aligned, how many tilted, at what angle. Source is upstream at packing/atlas/known-best/rendering/n-011.svg line 4, so the fix belongs in the atlas renderer and improves every rendering at once.
