---
type: is
id: is-01m2hk24qpbm21qn8tqqqr7ycz
title: "PR #171 review D17: the Animation studio (and Pack) draw no container and a stale catalogue box"
kind: bug
status: open
priority: 1
version: 1
labels: []
dependencies: []
parent_id: is-01m2hb41hy7fx18dy67asht84d
created_at: 2026-09-15T03:51:37.461Z
updated_at: 2026-09-15T03:51:37.461Z
---
Canonical defect D17 from the 2026-09-14 stack triage (High). Source: #171 R1.

The Animation studio draws no container and shows a stale catalogue box. #171 set `#container` to `stroke="none"` because the catalogue's `drawBounds` now draws the box, but the animation panel draws imported traces into the same stage with the same `#container`, and `render()` returns before `drawBounds` while the panel is active, so `#bound-box` stays at the catalogue step's side.

Files: `packages/workbench/assets/template.html:24-29`, `packages/workbench/src/app/animation-panel.ts:86`, `:215`, `packages/workbench/src/application.js:3693` @bb3f7c99; `check_animation_editor.py` imports the fixture and never looks at the stage.

Found while addressing: the independent Pack panel shares `#container` and the stage the same way, and draws a 5 x 5 container with no outline and the catalogue's stale side-4 box over it. Feature bead: think-31ln.
