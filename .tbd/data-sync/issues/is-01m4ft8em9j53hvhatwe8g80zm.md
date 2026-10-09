---
type: is
id: is-01m4ft8em9j53hvhatwe8g80zm
title: "check_math_startup self-test: delayed control compared against a cold-start baseline"
kind: bug
status: open
priority: 2
version: 1
labels: []
dependencies: []
parent_id: is-01m4fdxw81pt2v4k29y9n58rn6
created_at: 2026-10-09T07:50:19.017Z
updated_at: 2026-10-09T07:50:19.017Z
---
packing/devtools/check_math_startup.py:394 requires delayed.parameters_ready_ms - control.parameters_ready_ms >= 150. The 'control' run is the first browser launch and absorbs warm-up: on #459 run 37898417552 (typography job 113716869137) control=173 ms, no-warmup=125 ms, later controls ~15 ms, delayed=317 ms -> 144 < 150 -> FAIL. Compare against a warmed baseline (e.g. min/median of the non-delayed controls, or a discarded warm-up load) so the control tests the injected 300 ms delay, not launch noise.
