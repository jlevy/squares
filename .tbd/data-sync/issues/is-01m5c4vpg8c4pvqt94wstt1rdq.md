---
type: is
id: is-01m5c4vpg8c4pvqt94wstt1rdq
title: Native frontier longest task reached 302 ms against the 300 ms budget on main 476049de1
kind: bug
status: open
priority: 2
version: 1
labels: []
dependencies: []
parent_id: is-01m5c0ftybryt8q817fj95axz8
created_at: 2026-10-20T07:54:19.525Z
updated_at: 2026-10-20T07:54:19.525Z
---
Main Packing validation 39379044487 at 476049de1 (#688 merge) failed test_site_rendering.py::test_native_frontier_passes_the_unchanged_http_load_and_nojs_budgets[390-dark] and [1280-light], each with 'longestTaskMs 302.000 exceeds 300' (identical value in both scenarios). It did not reproduce: main validation passed at 4b8aec9a6 (39379741086) and e43c32b74 (39385433830) with the same content plus #690/#695. The margin is ~1%: measure the longest-task distribution on hosted runners across several runs, identify the task (instrumented navigation artifact native-frontier-*-*.json is retained by the job), and decide on evidence whether it is page growth (#692/#687 add results) or runner noise. Do not raise the budget without that measurement.
