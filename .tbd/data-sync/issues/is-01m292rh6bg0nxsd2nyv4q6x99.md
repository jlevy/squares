---
type: is
id: is-01m292rh6bg0nxsd2nyv4q6x99
title: The first frame of every step is an invalid packing, so the pointer hides through the dwell
kind: bug
status: open
priority: 2
version: 1
spec_path: docs/project/specs/active/plan-2026-09-11-workbench-from-spike-to-product.md
labels: []
dependencies: []
parent_id: is-01m28p7h39vcykq99dgjmvwv98
created_at: 2026-09-11T20:32:49.867Z
updated_at: 2026-09-11T20:32:49.867Z
---
Noticed while measuring the mode-switch reset, not caused by it.

At t=0 of any step the incoming square is already on the stage at its start pose, sitting exactly on top of the existing arrangement: measured total overlap is 1.0 -- one whole unit square -- at the first frame of the step into 2 and of the step into 17 alike. The validity rule then hides the bar's pointer for as long as that lasts.

Two things to establish before fixing anything:
1. How long it lasts. If it is one frame the cost is nothing; if it covers the dwell, the pointer is missing for a third of every step, which is the opposite of what the validity work was for.
2. Whether the right answer is to stage the incoming square outside the container until its arrival begins, or to exclude a square that has not arrived from the overlap sum. The first keeps one definition of overlap; the second keeps the staging.

Related: think-3quo (valid intermediate frames).
