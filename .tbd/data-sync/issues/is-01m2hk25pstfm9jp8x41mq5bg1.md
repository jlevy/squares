---
type: is
id: is-01m2hk25pstfm9jp8x41mq5bg1
title: "PR #171 review D69: the separator's Home and End also rewind or finish the step"
kind: bug
status: open
priority: 2
version: 1
labels: []
dependencies: []
parent_id: is-01m2hb41hy7fx18dy67asht84d
created_at: 2026-09-15T03:51:38.456Z
updated_at: 2026-09-15T03:51:38.456Z
---
Canonical defect D69 from the 2026-09-14 stack triage (Medium). Source: #171 R5.

The separator's Home and End also rewind or finish the step. `onKeyDown` calls `preventDefault()` but not `stopPropagation()`, and the window's shortcut handler maps Home to `seek(0)` and End to `seek(duration())` (with an imported animation active, it seeks the animation). `check_stage_resize.py:82-87` presses both keys and checks only the stage height.

Files: `packages/workbench/src/view/resize-handle.ts:117-128`, `packages/workbench/src/application.js:5857-5918` @bb3f7c99, `packages/workbench/tools/workbench_tools/check_stage_resize.py:82-87`. Feature bead: think-bau0.
