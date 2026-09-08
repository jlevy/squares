---
type: is
id: is-01m1tdk0b963qq9aqcpxqdyvmv
title: Classify two newly measured CI tests on the slow surface
kind: bug
status: closed
priority: 1
version: 4
labels: []
dependencies: []
parent_id: is-01m1t71c4hyfw28d5nc5m6jv6b
created_at: 2026-09-06T03:53:26.631Z
updated_at: 2026-09-06T04:06:44.133Z
closed_at: 2026-09-06T04:06:44.131Z
close_reason: Commit 8cc0af43 marks the two hosted measurements (6.10s motion-lab service and 5.82s n40 contact model) slow, records them in the exact registry, and updates the 64-function/94-test count. Four focused selection/registry tests passed locally. Hosted run 34010163744 now passes validate, macos-portability, sweeps, and packing-required.
resolution: null
duplicate_of: null
---
PR #89 validate run 34009724046 measured tests/test_motion_lab_interactive.py::test_service_serves_live_and_exact_profiles_with_scenario_refresh at 6.10s and tests/test_n40_rigidity.py::test_the_contact_model_is_measured_not_assumed at 5.82s, above the pull-request surface's 5s ceiling. Add measured slow markers, update the exact marker registry and its current counts, and run the focused marker/validation tests. This is separate from think-xfl9's snapshot fix.

## Notes

Fixed in 8cc0af43 after origin/main merge a70e002e. Added measured slow markers for the 6.10s motion-lab service test and 5.82s n40 contact-model test, registered both exactly, and updated the current 64-function/94-test count. Focused marker registry and pull-request selection tests: 4 passed in 0.46s. Hosted run 34010163744 pending.
