---
type: is
id: is-01m1s7exdtr1f7db3xpxbfvqbe
title: Explainer page must print as a clean PDF
kind: feature
status: closed
priority: 1
version: 2
labels: []
dependencies: []
created_at: 2026-09-05T16:47:06.681Z
updated_at: 2026-09-05T17:10:14.280Z
closed_at: 2026-09-05T17:10:14.279Z
close_reason: "Done in 6021f6dc. Two sub-agents, one static and one empirical. The blocking finding: the page printed as ONE page, losing about nine tenths of the document, because kpress's page-reset holds html,body{height:100%;overflow:hidden} and its print stylesheet releases .kpress-viewport but not those two; the paginator saw one viewport and stopped. Now 11 pages. Also added: one certificate deterministically (half the figures are hidden, so a printed copy depended on the reader's last click); panels, sliders and chooser strips hidden, with the four dead instruction strings marked screen-only; canvases capped by height so two figures that ran past a page no longer separate from their captions; link targets printed; .kpress-page-main and --cert-probe forced light, which kpress's print tokens do not reach; and a canvas repaint on print media, since a bitmap drawn from the dark theme cannot be recoloured by CSS. Verified: 11 pages in both light and dark, canvas corner white in both, 0 sliders/panels/choosers, 0 errors. Worth reporting the page-reset gap upstream to kpress."
resolution: null
duplicate_of: null
---
Owner 2026-09-05: the explainer should print cleanly to PDF as well as read well as a page. kpress supports most print CSS cleanly; verify the page's custom work (canvas figures, the certificate chooser, sliders and buttons, footnote popovers, the inlined atlas SVG, the theme tokens) is compatible, and that the whole document prints as a clean PDF.
