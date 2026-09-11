---
type: is
id: is-01m292qs1re33kvh0tvnm6xctd
title: Switching Pack and Animate carried the run across
kind: bug
status: closed
priority: 1
version: 2
spec_path: docs/project/specs/active/plan-2026-09-11-workbench-from-spike-to-product.md
labels: []
dependencies: []
parent_id: is-01m28p7h39vcykq99dgjmvwv98
created_at: 2026-09-11T20:32:25.143Z
updated_at: 2026-09-11T20:33:10.050Z
closed_at: 2026-09-11T20:33:10.049Z
close_reason: "Fixed: setMode ends the run, zeroes the clock and rebuilds the stage; each mode keeps its own n. Measured after: Pack(17) -> Animate -> Pack round-trips, and again at n=11 after a 108-step run."
resolution: null
duplicate_of: null
---
Switching modes kept whatever was on the stage, on the reasoning that a run is work and work is not thrown away. What it produced was a page describing one thing and drawing another.

Measured before, on the built page:
- Leaving Pack mid-run put the optimiser's arrangement under Animate's header: 'showing the step 10 -> 11' over a stage holding eleven squares pushed around for 110 steps, the Pack clock still reading '0.92 s . 110 steps' in Animate.
- Entering Animate re-keyed the bar to the pair's first n while the stage still held the second's: n=16 on the bar, the 17-square arrangement on the stage, total overlap 1.0, valid=false.

Neither is recoverable by looking at it.

Fixed: setMode ends the run (opt=null, optimizing=false), zeroes the clock, and rebuilds the stage from the mode being entered; and each mode keeps its own n -- state.packN beside the existing state.animate -- so Pack(17) -> Animate -> Pack is Pack(17) again, and Animate always opens at the first step of its range. unstagePack, whose one caller this replaced, is gone.

Measured after: the round trip is stable at n=17 and at n=11 after a 108-step run; Animate opens at 'showing the step 1 -> 2', clock 0.000/2.400, no carried step count.
