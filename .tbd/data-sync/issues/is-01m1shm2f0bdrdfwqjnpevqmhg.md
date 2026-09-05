---
type: is
id: is-01m1shm2f0bdrdfwqjnpevqmhg
title: "README: the atlas image opens the PDF, and the caption just names the formats"
kind: task
status: closed
priority: 2
version: 2
labels: []
dependencies: []
created_at: 2026-09-05T19:44:41.440Z
updated_at: 2026-09-05T19:47:55.945Z
closed_at: 2026-09-05T19:47:55.945Z
close_reason: "Landed together in b57a77fb on PR 88: the explainer named above the fold, the atlas image opening the Pages-served PDF with a caption that names the three formats, the three bullets linking on their bold lead with the survey bullet stating seven first-party lower bounds, the headline framed as the explainer frames it (first improvement in 23 years), and all fourteen spaced em dashes resolved per common-doc-guidelines."
resolution: null
duplicate_of: null
---
GitHub Pages serves the atlas PDF as application/pdf so a browser renders it natively; the SVG opens as markup in the blob view and the raw URL downloads. Point the image link at the Pages PDF. The caption should not instruct the reader to click: it reads 'The image is available in SVG, PDF, and high-rez PNG' with the formats boldfaced and linked.
