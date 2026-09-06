---
type: is
id: is-01m1w1wyxcxtv3zh7rset43am6
title: "PR #98 review R1: artifact layer overrides quick-lane --durations-min and duplicates flags"
kind: bug
status: closed
priority: 2
version: 3
labels: []
dependencies: []
parent_id: is-01m1w1w81t7vmr0gem6d91wg8b
created_at: 2026-09-06T19:07:38.796Z
updated_at: 2026-09-06T19:16:33.469Z
closed_at: 2026-09-06T19:16:33.469Z
close_reason: "Fixed: _run injects --durations flags only when the step chose none; junitxml always; test_artifacts_keep_a_steps_own_durations_filter pins it."
resolution: null
duplicate_of: null
---
packing/src/sqpack/cli/validate.py:726 appends --durations=0 --durations-min=0 in artifact mode; _quick_lane_command (:1090) passes --durations-min=12 and pytest takes the last value. Exhaustive/slow steps hardcode the same flags (:1181). Fix: inject only when no --durations flag present; one layer owns it; add a test.
