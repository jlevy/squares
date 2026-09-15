---
type: is
id: is-01m2heyzcfw5n7s7xaprp8kg22
title: "PR #160 review D67: checks lost in the move over the candidate checker and the spike views"
kind: bug
status: closed
priority: 2
version: 3
labels: []
dependencies: []
parent_id: is-01m2hb40z4hvrre5f0219zp1m9
created_at: 2026-09-15T02:39:59.375Z
updated_at: 2026-09-15T02:40:58.490Z
closed_at: 2026-09-15T02:40:58.489Z
close_reason: "Fixed on #160 at 9baad048: check_candidate no longer claims the frozen spike views (README, NOTES and docstring say they are frozen at 0281a508), builds with --all, and the false facts-layer opacity loop and candidate/facts_opacities.js are removed."
resolution: null
duplicate_of: null
---
Review finding, PR #160 stack triage (2026-09-14), lane D-tools.

Checks lost in the move: `check_candidate` no longer compared retained views to a fresh build and omitted `--all`; the generated spike views were unchecked; the stale `facts_opacities.js` was still called. Coordinator decision: retire `check_candidate`'s claim over the generated spike views, which are frozen historical output.

Sources: #160 R21 (non-wiring items); #155 R19 (`facts_opacities.js` item). Related: think-yz20, think-tn0j, think-cqfc.

Files: `packages/workbench/tools/workbench_tools/check_candidate.py:126-133`, `:801-815`, `:1285-1293`; `packages/workbench/probes/candidate/facts_opacities.js`; `spikes/v2-transitions/{transition-stats.json,stats-summary.md}`.
