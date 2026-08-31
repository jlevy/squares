---
type: is
id: is-01m0t4tnzhbhf3j6px053wtveg
title: Make the historical-regression gate propagate checker failure
kind: bug
status: closed
priority: 0
version: 2
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-23-overnight-cartography-run.md
labels:
  - packing
  - focus-process
dependencies: []
parent_id: is-01m0rkz14t04yjme92gnfncfv7
created_at: 2026-08-24T15:04:39.151Z
updated_at: 2026-08-24T15:12:22.233Z
closed_at: 2026-08-24T15:12:22.232Z
close_reason: "D-163 fixed: the historical-regression gate now propagates checker failure, and a negative control proves a synthetic failing checker cannot be masked by later probes. Ordinary historical regressions pass."
resolution: null
duplicate_of: null
---
D-163. test.sh step_historical_regressions continued into later command-line checks after tools/regression_test.py returned 1, so the function returned the final successful probe and the focused gate printed PASSED. Add explicit failure propagation and a command-level regression that proves a failing historical checker makes the step and gate nonzero. Acceptance: the current D-029 failure makes --only historical regressions nonzero; after the scientific issue is resolved the ordinary step passes; a synthetic failing checker cannot be masked by later commands.
