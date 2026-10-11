---
type: is
id: is-01m2ge1fvc8sj4fgkf8w2ja1fc
title: Open the workbench on Animate, ordering the tabs Animate, Pack, Search
kind: task
status: closed
priority: 2
version: 2
spec_path: docs/project/specs/active/plan-2026-09-11-workbench-from-spike-to-product.md
labels:
  - workbench-roadmap
dependencies: []
parent_id: is-01m28p7h39vcykq99dgjmvwv98
created_at: 2026-09-14T17:04:38.762Z
updated_at: 2026-10-06T08:30:55.100Z
closed_at: 2026-10-06T08:30:55.100Z
close_reason: "Done: 77afe1c85 'Open on Animate, ordering the tabs Animate, Pack, Search' is on origin/main; template.html mode-animate first with aria-pressed=true, and packages/workbench/README.md says the page opens on Animate."
resolution: null
duplicate_of: null
---
Owner request 2026-09-14: Animate is the most used aspect, so it is the first tab and the page opens on it, then Pack, then Search. Committed as df7e9704 on claude/workbench-defaults-and-bounds: startup reaches Animate through setMode, check_animation_editor asserts order and arrival, check_pack_panel and check_accessibility choose Pack first.
