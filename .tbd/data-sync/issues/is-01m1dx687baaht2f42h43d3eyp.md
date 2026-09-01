---
type: is
id: is-01m1dx687baaht2f42h43d3eyp
title: Bridge Codex task-tree telemetry into session close and PR cost
kind: task
status: closed
priority: 1
version: 3
spec_path: packing/campaign/agendas/agenda-013-nine-hour-autonomous-run.md
labels: []
dependencies: []
parent_id: is-01m1dtfx94hb8ndgdxmmxp3z4m
created_at: 2026-09-01T07:15:58.314Z
updated_at: 2026-09-01T08:48:14.118Z
closed_at: 2026-09-01T08:48:14.101Z
close_reason: Built and independently reviewed the privacy-safe Codex task-tree receipt bridge, cumulative branch attribution, semantic/path/branch/duplicate guards, session close integration, and regression suite; the exact terminal repair tree passes packing-validate --push with 216 reachable tests.
resolution: null
duplicate_of: null
---
W5 preflight found that CodexEfficiencyRollup/v2 parses the live coordinator/subagent tree but close_session and render_pr_rollup consume only Claude rollups. Build a bounded, privacy-preserving branch-window delta from two frozen Codex snapshots, integrate it with terminal session attribution and the generated OR-9 PR cost block, cover the conversion and consumer paths with red-green tests, and retain no prompt/reasoning prose, local log paths, raw task ids, or full command strings. The first publication must stay honest if exact branch attribution cannot be derived.
