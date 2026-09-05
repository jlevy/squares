---
type: is
id: is-01m1qcymg4nfv2sncz0k27h99v
title: "kpress: tune KaTeX math sizing to PT Serif, the default prose face, by default"
kind: task
status: open
priority: 2
version: 2
labels:
  - kpress-upstream
dependencies: []
parent_id: is-01m1q3fmvn9py28rcm0q3jadvk
created_at: 2026-09-04T23:44:35.842Z
updated_at: 2026-09-04T23:46:06.959Z
---
Found building the certificate page (PR #79). KaTeX's stylesheet sets .katex at 1.21em, matched to Times-like x-heights. kpress's default prose face is PT Serif, whose x-height is much larger, so every inline formula in a kpress document reads about a fifth too large, and more so inside the small sans contexts (captions, labels, readouts). kpress should carry the sizing in its own KaTeX layer, tuned to PT Serif by default: about 1.05em in serif prose, 1em wherever the surrounding face is Source Sans, and a display-equation size of its own. The page's override (packing/devtools/templates/certificate_page.html, the '.cert-page .katex' block) is the measured starting point and goes away once kpress carries it.
