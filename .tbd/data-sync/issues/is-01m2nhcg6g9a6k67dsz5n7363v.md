---
type: is
id: is-01m2nhcg6g9a6k67dsz5n7363v
title: Make Animate presets truthful and continuous when settings change
kind: bug
status: in_progress
priority: 1
version: 3
spec_path: docs/project/specs/active/plan-2026-09-11-workbench-from-spike-to-product.md
delegate: codex@spud10
labels:
  - workbench
  - animation
dependencies: []
parent_id: is-01m2m2zmky0p8gw5m4zctfnfex
hold: null
hold_until: null
created_at: 2026-09-16T16:39:17.454Z
updated_at: 2026-09-16T16:53:52.997Z
started_at: 2026-09-16T16:49:14.507Z
---
Animate opens on solver A · tween, which does not use the force law or annealing, but the rigidity/repulsion/attraction/range controls and rigid/soft/sticky presets remain enabled. Physical styles also bypass simulation on prefix/shared-picture steps. The same controls are therefore inert in some visible states and path-defining in B/C, without a clear scope indication. In addition, rigidity is actually tolerated penetration: moving it lower makes contact harder and also increases a derived post-knee slope, opposite the intuitive direction of a rigidity control.

Changing a law slider, preset, solver, or motion phase during playback synchronously builds/selects a different trajectory and renders it at the existing playhead. There is no pause, restart, or crossfade, so the setting change itself can cause a spatial discontinuity; main-thread precomputation can also produce a clock jump on the next animation frame.

Acceptance: make force-law and annealing scope explicit and non-interactive where they do not apply; name/invert the contact-hardness control so its direction is truthful; visibly distinguish hardness from annealing perturbation; make rigid/soft/sticky produce tested, meaningfully distinct B/C responses; and define a continuity-preserving setting-change policy (pause/restart or bounded crossfade) with an end-to-end regression test. Snap's final target blend must not be used as evidence that the preceding physical path is smooth.
