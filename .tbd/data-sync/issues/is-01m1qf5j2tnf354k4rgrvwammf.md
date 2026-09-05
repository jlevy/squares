---
type: is
id: is-01m1qf5j2tnf354k4rgrvwammf
title: "kpress: position tooltips in page coordinates inside the scroll container"
kind: task
status: open
priority: 2
version: 2
labels:
  - kpress-upstream
dependencies:
  - type: blocks
    target: is-01m1qg6p9snppc21bx7b26sp7v
parent_id: is-01m1q3fmvn9py28rcm0q3jadvk
created_at: 2026-09-05T00:23:19.897Z
updated_at: 2026-09-05T00:41:25.560Z
---
tooltips.js appends the popover to document.body and positions it in viewport coordinates (position: fixed), so it stays on screen while the document scrolls. Append it inside the kpress viewport (the scroll container) with absolute positioning translated by the scroller's offset, so it stays beside its anchor on the page. On squares/page-fixes first.
