---
type: is
id: is-01m1qg6ny5eqkwqhx7b50ykv97
title: "Renderer: copy the composite PNG and PDF beside the page and link them; composite figure support"
kind: task
status: closed
priority: 2
version: 2
labels:
  - explainer
  - pr-79
dependencies: []
parent_id: is-01m1qekyhf4hjcavbdm3xya0bt
created_at: 2026-09-05T00:41:25.188Z
updated_at: 2026-09-05T01:15:14.090Z
closed_at: 2026-09-05T01:15:14.089Z
close_reason: Commit b5e81669.
resolution: null
duplicate_of: null
---
After the renderer refactor releases the renderer: copy packing/atlas/known-best/known-best-1-100.{png,pdf} into the output directory beside index.html at render time; the Markdown's Figure 1 references them by relative path; pages.yml lists the composite in its paths filter.
