---
type: is
id: is-01m1q3fqyxv8v6ez73dz3p1raz
title: "kpress: help consumers subset the KaTeX faces for a self-contained build"
kind: task
status: open
priority: 3
version: 3
labels:
  - kpress-upstream
dependencies: []
parent_id: is-01m1q3fmvn9py28rcm0q3jadvk
created_at: 2026-09-04T20:59:10.685Z
updated_at: 2026-09-04T21:00:06.792Z
---
`katex.min.css` declares all ~20 KaTeX faces. A page inlining them as data URIs pays roughly 300 KB for faces it never reaches. `render_certificate_page.py` hardcodes the ten this page uses and drops the rest with a regex over the `@font-face` blocks, which is fragile: a page that later uses `\mathfrak` silently loses its glyphs.

Proposal: a helper returning the KaTeX CSS with fonts inlined for a named subset, or documentation of which faces each construct reaches so a consumer can subset deliberately. Lower priority than think-iy3l, which would carry this if it took the inlining.
