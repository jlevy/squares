---
type: is
id: is-01m336y6n04th664pbvpnkyx4e
title: Whole diagram shrinks then grows on some steps, e.g. n = 10 -> 11
kind: bug
status: closed
priority: 0
version: 2
spec_path: docs/project/specs/active/plan-2026-09-11-workbench-from-spike-to-product.md
labels: []
dependencies: []
parent_id: is-01m32t2yc3xenfb97kxn844rc7
created_at: 2026-09-22T00:06:05.215Z
updated_at: 2026-09-22T01:18:12.035Z
closed_at: 2026-09-22T01:18:12.034Z
close_reason: "Fixed at 06029438e. Cause: the physics view was centered on the breathing simulated container and then unioned with the room's canonical box, which grew and shrank with each breath (reversals at frame 37 into 10 and into 50), and taking n + 1's side from frame 0 jumped the view 3.270 -> 3.796 across the 9/10 boundary. The view is anchored where the room's box is and starts from n's side. check_transitions' view_jerks and boundary_jerk rules hold it across the corpus."
resolution: null
duplicate_of: null
---
Owner's report: a jerk where the whole diagram shrinks then grows, visible on the step 10 -> 11 and others, but not on 9 -> 10 or 8 -> 9.

That split is the clue. 10 -> 11 is the step where ceil(sqrt(n)) goes 4 -> 4 but the best-known side of 11 (3.877) is not an integer, so openSide and the settled side differ; 9 -> 10 and 8 -> 9 are grid-adjacent. The last fix eased the view open over the dwell, but the view is held to openSide(n+1) during the step and returns to the settled side at the boundary -- if those differ, the view steps down at the next step's start, which reads as growing back.

Reproduce with the transition contract checker at the frame and across the step boundary, then fix so the view is monotone.
