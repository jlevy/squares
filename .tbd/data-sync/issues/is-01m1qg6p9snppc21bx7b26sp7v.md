---
type: is
id: is-01m1qg6p9snppc21bx7b26sp7v
title: "Take the kpress popover-position fix: bump the submodule, re-render, verify, commit"
kind: task
status: closed
priority: 2
version: 3
labels:
  - explainer
  - pr-79
  - kpress
dependencies: []
parent_id: is-01m1pnpwvpjydts81pffmp1nt7
created_at: 2026-09-05T00:41:25.560Z
updated_at: 2026-09-05T01:15:14.398Z
closed_at: 2026-09-05T01:15:14.397Z
close_reason: Commit b5e81669.
resolution: null
duplicate_of: null
---
After the kpress agent pushes squares/page-fixes with the popover in page coordinates: stage the vendor/kpress gitlink at the pushed commit, re-render so the bundle carries the new tooltips.js, verify in the browser that a footnote popover scrolls with the page, commit and push.
