---
type: is
id: is-01m2y0mzc4qamrt9gz0741phpp
title: "PR199 review R1: repair n18 doubled-net assertion on the bottom of the stack"
kind: bug
status: open
priority: 1
version: 1
labels: []
dependencies: []
parent_id: is-01m2y07hq7kkss9qh386q3h912
created_at: 2026-09-19T23:39:59.233Z
updated_at: 2026-09-19T23:39:59.233Z
---
At c877006b packing/tests/test_fractional_interval.py:405 expects 361 directions; certificate direction_steps=181 gives 182 half-tangents and 363 doubled directions. PR200 inherits the failure; only PR201 dd2b4d7a fixes it. Move the fix to PR199, restack, correct the 181/361 evidence narration, and obtain fresh full checkpoints before merging each layer.
