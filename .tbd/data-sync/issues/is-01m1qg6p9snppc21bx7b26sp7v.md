---
type: is
id: is-01m1qg6p9snppc21bx7b26sp7v
title: "Take the kpress popover-position fix: bump the submodule, re-render, verify, commit"
kind: task
status: open
priority: 2
version: 2
labels:
  - explainer
  - pr-79
  - kpress
dependencies: []
parent_id: is-01m1pnpwvpjydts81pffmp1nt7
created_at: 2026-09-05T00:41:25.560Z
updated_at: 2026-09-05T00:42:00.689Z
---
After the kpress agent pushes squares/page-fixes with the popover in page coordinates: stage the vendor/kpress gitlink at the pushed commit, re-render so the bundle carries the new tooltips.js, verify in the browser that a footnote popover scrolls with the page, commit and push.
