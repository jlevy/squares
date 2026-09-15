---
type: is
id: is-01m2hh6zjhk7bdw2edsytjvhkz
title: "PR #160 review D12: the page's global key handler acts while Search is visible"
kind: bug
status: closed
priority: 1
version: 2
labels: []
dependencies: []
parent_id: is-01m2hb40z4hvrre5f0219zp1m9
created_at: 2026-09-15T03:19:18.858Z
updated_at: 2026-09-15T03:32:50.304Z
closed_at: 2026-09-15T03:32:50.303Z
close_reason: "Fixed on codex/review-workbench-stack (PR #160) in 1ca13c91: one catalogueOwnsPage() guard for the global key handler, the stage handlers and the atlasTransitions proxy, holding from load; check_animate_view checks a bare c behind Pack at load, and 8c7cdfb8 adds check_search_panel's keyboard case (typing and arrows in the seeds field, c and Space on a focused Start), which fails with the guard removed."
resolution: null
duplicate_of: null
---
Canonical defect D12 from the 2026-09-14 stack triage (High). Sources: #160 R6; #160 R17 (Search-checker keyboard case).

The page's global key handler still acted while Search was visible: Space and ArrowLeft/Right in `#search-seeds`, `#search-n` or `#search-steps` blurred the field and ran the hidden Animate transport; Space on a focused Search button was preventDefaulted, so Start could not be activated with Space; letter shortcuts fired (`c` entered capture mode). The early return checked only `packPanel?.visible()`. Since #171 the handler is live from page load.

Files: `packages/workbench/src/application.js` (window keydown handler, then ~:5663-5750; early return ~:5669), the stage keydown and pointerdown handlers and the `atlasTransitions` proxy; keyboard case in `packages/workbench/tools/workbench_tools/check_search_panel.py`.
