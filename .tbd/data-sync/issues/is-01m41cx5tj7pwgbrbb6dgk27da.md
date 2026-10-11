---
type: is
id: is-01m41cx5tj7pwgbrbb6dgk27da
title: Measure whether the atlas's SVG renderings should be committed or drawn at the Pages build
kind: task
status: closed
priority: 3
version: 4
labels:
  - session-169
dependencies: []
parent_id: is-01m41cx3q2pckpmsmmwq1rsngz
created_at: 2026-10-03T17:27:36.018Z
updated_at: 2026-10-03T17:58:55.383Z
closed_at: 2026-10-03T17:58:55.383Z
close_reason: "Measured (lane C, session-169): keep both drawing sets committed; drawing at build saves working-tree bytes only and loses the renderer golden test, colour data and linked figures. Optional: linguist-generated in .gitattributes. Slimming the encoding (D3) is folded into the repository-growth measurement."
resolution: null
duplicate_of: null
---
The house atlas commits 324 SVG renderings (52 MB, packing/atlas/known-best/rendering/) and PR 305 adds 51 regularized ones (11 MB). Measure: what reads them (render_overview, the tiles' packing_svg reduction, check_frontend, the Pages partial checkout), how long drawing all of them takes on a hosted runner, what they add to a clone and to the repository's packs, and what a build-time render would cost the Pages critical path (OR-14) and its determinism checks. Recommend keep or change, with the evidence; the change itself is the owner's decision.

## Notes

2026-10-03, lane C (session-169) measured and recommends keeping both drawing sets committed (option A), with `linguist-generated=true` in .gitattributes as an optional review aid (D2). Measured: house set 53.4 MB working tree / 4.53 MB packed, regularized set 11.2 MB / 1.45 MB; all history of both about 10-12 MB, about 1% of the repository's packs; drawing all 375 takes 13 s on 4 workers here (estimated 12-19 s on a hosted runner) and is byte-for-byte deterministic. Drawing at the Pages build (option B) would save working-tree bytes, not history, and would remove the renderer's corpus-wide golden test, the colour data the workbench and test_render_colors read, and the drawings SYNOPSIS, the atlas README and the explainer link to; about 15 readers would change. Gzipping them (C) saves nothing git does not already do and costs diffs. If growth becomes the concern, slim the encoding first (D3: each square is written twice with 28-digit coordinates; about 60% of n-306's bytes). Scratch measurement scripts were not retained (OR-1 would put them in devtools.measure_release_assets --timings if the owner wants them repeatable).
