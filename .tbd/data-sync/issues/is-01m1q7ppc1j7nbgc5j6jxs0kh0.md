---
type: is
id: is-01m1q7ppc1j7nbgc5j6jxs0kh0
title: Figure 3 handle folds at 45° instead of rotating freely
kind: bug
status: closed
priority: 1
version: 2
labels:
  - explainer
  - pr-79
dependencies: []
parent_id: is-01m1q0p63s2evef5mhkyn16e41
created_at: 2026-09-04T22:12:52.736Z
updated_at: 2026-09-04T22:40:10.226Z
closed_at: 2026-09-04T22:40:10.225Z
close_reason: "Commit 3f080baa: the handle sets a free angle; mass, heat map and centre domain computed at it (inset = B(|cos|+|sin|)/2); readout shows φ and the net direction it reduces toward; slider and reset return to the net. Driven in the browser: 36-step full-circle sweeps on both articles track the target exactly, no folds."
resolution: null
duplicate_of: null
---
Review feedback on PR #79. In devtools/templates/certificate_page.html the prover figure's rotation handle snaps to the nearest net direction via nearestNet(), which folds the pointer angle into [0, pi/4] by the D4 reduction. Dragging the handle past 45° therefore reverses the square instead of following the pointer. Fix: the handle rotates the square freely through 360°, the mass field is computed at the free angle (massAt is already angle-generic), the readout shows the free angle and the net direction it reduces to, and the slider keeps its exact net snapping. inset() must become B(|cos|+|sin|)/2 for the admissible domain to be right outside [0, pi/4].
