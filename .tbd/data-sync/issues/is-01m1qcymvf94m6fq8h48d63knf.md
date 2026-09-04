---
type: is
id: is-01m1qcymvf94m6fq8h48d63knf
title: "kpress: a standalone footnote-preview bundle for self-contained pages"
kind: task
status: open
priority: 3
version: 1
labels:
  - kpress-upstream
dependencies: []
parent_id: is-01m1q3fmvn9py28rcm0q3jadvk
created_at: 2026-09-04T23:44:36.206Z
updated_at: 2026-09-04T23:44:36.206Z
---
Found building the certificate page (PR #79). The page uses kpress's footnote markup and CSS, but the hover previews live in tooltips.js, an ES module over overlay.js, runtime.js and viewport.js with a behaviours registry — too much to inline into a page that loads no runtime. A single classic-script bundle exposing initKpressTooltips would let self-contained pages have the previews.
