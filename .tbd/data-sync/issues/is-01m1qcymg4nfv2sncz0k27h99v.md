---
type: is
id: is-01m1qcymg4nfv2sncz0k27h99v
title: "kpress: size KaTeX math to the prose face rather than KaTeX's 1.21em default"
kind: task
status: open
priority: 2
version: 1
labels:
  - kpress-upstream
dependencies: []
parent_id: is-01m1q3fmvn9py28rcm0q3jadvk
created_at: 2026-09-04T23:44:35.842Z
updated_at: 2026-09-04T23:44:35.842Z
---
Found building the certificate page (PR #79). KaTeX's stylesheet sets .katex at 1.21em, matched to Times-like x-heights; against PT Serif every inline formula reads about a fifth too large, and more so inside small sans labels. The page overrides it (prose 1.05em, sans contexts 1em, display 1.1em, in packing/devtools/templates/certificate_page.html); kpress should carry the sizing in its own KaTeX layer so consumers do not.
