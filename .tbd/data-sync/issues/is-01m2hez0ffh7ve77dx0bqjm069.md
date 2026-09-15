---
type: is
id: is-01m2hez0ffh7ve77dx0bqjm069
title: "PR #160 review D88: smaller check weakenings from the move"
kind: bug
status: closed
priority: 2
version: 3
labels: []
dependencies: []
parent_id: is-01m2hb40z4hvrre5f0219zp1m9
created_at: 2026-09-15T02:40:00.495Z
updated_at: 2026-09-15T02:40:59.426Z
closed_at: 2026-09-15T02:40:59.425Z
close_reason: "Fixed on #160: visible-count.js uses !(x > 0.01) with a Node test (c0aba3b9); export_svg refuses a script element and --out works beside the positional path (a093ec7a). animation_from_trace's summary CLI printed frame, square and distinct-side counts; muting_from_animation and trajectory_from_animation survive in animation_render.py, so the retirement is recorded here."
resolution: null
duplicate_of: null
---
Review finding, PR #160 stack triage (2026-09-14), lane D-tools.

Smaller check weakenings from the move: NaN opacity counted as drawn in `stage/visible-count.js`; `export_animation_svg` no longer refused `<script` and changed `--out` to positional; `animation_from_trace`'s summary CLI was retired unrecorded.

Source: #160 R22 (non-self-contained items). Related: think-yz20.

Files: `packages/workbench/probes/stage/visible-count.js:8`; `packages/workbench/tools/workbench_tools/export_animation_svg.py`; `animation_render.py:135`, `:149`.
