---
type: is
id: is-01m5c4vpg8c4pvqt94wstt1rdq
title: Native frontier longest task reached 302 ms against the 300 ms budget on main 476049de1
kind: bug
status: open
priority: 2
version: 3
labels: []
dependencies: []
parent_id: is-01m5c0ftybryt8q817fj95axz8
created_at: 2026-10-20T07:54:19.525Z
updated_at: 2026-10-21T13:26:34.151Z
---
Main Packing validation 39379044487 at 476049de1 (#688 merge) failed test_site_rendering.py::test_native_frontier_passes_the_unchanged_http_load_and_nojs_budgets[390-dark] and [1280-light], each with 'longestTaskMs 302.000 exceeds 300' (identical value in both scenarios). It did not reproduce: main validation passed at 4b8aec9a6 (39379741086) and e43c32b74 (39385433830) with the same content plus #690/#695. The margin is ~1%: measure the longest-task distribution on hosted runners across several runs, identify the task (instrumented navigation artifact native-frontier-*-*.json is retained by the job), and decide on evidence whether it is page growth (#692/#687 add results) or runner noise. Do not raise the budget without that measurement.

## Notes

21 Oct 2026, 12:3xZ (coordinator): recurred on main 51ac9d7ee (#713, records only, no frontier JS change): Packing validation run 39586891017, validate, test_native_frontier_passes_the_unchanged_http_load_and_nojs_budgets[1280-light] longestTaskMs 310.000 > 300; the other three viewports passed. Prior main runs at 2e6d528de and 9dda92240 passed. Failed jobs re-run once (the one permitted re-run); no budget raised.


The parent of this bead is:
---
type: is
id: is-01m5c0ftybryt8q817fj95axz8
title: "Intake pass 2026-10-20: land #692/#687, stage-7 replies after #688/#649/#657, unrecorded reply records, three new reports"
kind: epic
status: open
priority: P1
version: 6
labels: []
dependencies: []
child_order_hints:
  - is-01m5c0fvwya9ep8kqttmerv14z
  - is-01m5c0fwsxga70rszkjy1zbp2f
  - is-01m5c0fxm92eqjcj2cnapa6hms
  - is-01m5c4vpg8c4pvqt94wstt1rdq
  - is-01m5cm2y1myb3jwdvqjp1gt5af
created_at: 2026-10-20T06:37:56.555Z
updated_at: 2026-10-20T12:20:25.266Z
---
Coordinator session_014ZKp7R takeover of the intake (handoff #684). Replies audit of 27 'reply due' issues at main 4b8aec9a6: 14 record lag, 6 owed now, 6 blocked on owner/PRs, 1 closeable.


21 Oct 2026, 13:26Z: the one re-run (attempt 2 of run 39586891017) passed validate and post-merge-required on the same commit, so the 310 ms reading is draw variance on unchanged work, which is what think-09ju is to measure.
