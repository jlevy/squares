---
type: is
id: is-01m1w1x1sk8mx92tjv91c8e5xt
title: "PR #98 review R9: run_negative_controls --timings existing file raises bare FileExistsError"
kind: bug
status: closed
priority: 2
version: 3
labels: []
dependencies: []
parent_id: is-01m1w1w81t7vmr0gem6d91wg8b
created_at: 2026-09-06T19:07:41.746Z
updated_at: 2026-09-06T19:16:34.992Z
closed_at: 2026-09-06T19:16:34.992Z
close_reason: "Fixed: existing --timings journal prints an actionable message to stderr and returns 1; test updated."
resolution: null
duplicate_of: null
---
packing/devtools/run_negative_controls.py:745. Fix: catch, print actionable message to stderr, return 1.
