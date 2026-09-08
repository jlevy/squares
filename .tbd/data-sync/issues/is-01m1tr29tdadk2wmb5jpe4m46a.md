---
type: is
id: is-01m1tr29tdadk2wmb5jpe4m46a
title: Remove obsolete slow marker from n=12 symmetry refusal test
kind: bug
status: closed
priority: 1
version: 3
labels:
  - ci
  - testing
dependencies: []
parent_id: is-01m1t71bsncn7adg02er2hyk6d
created_at: 2026-09-06T06:56:33.611Z
updated_at: 2026-09-06T07:08:48.907Z
closed_at: 2026-09-06T07:08:48.906Z
close_reason: The obsolete slow marker and registry entry were removed; focused checks and the full slow-test surface pass.
resolution: null
duplicate_of: null
---
The full packing-validate checkpoint measured tests/test_fractional_certificate.py::test_breaking_the_symmetry_of_the_n12_atoms_is_refused at 0.80s, below the enforced one-second slow-marker floor. Remove its pytest.mark.slow decorator and registry entry in tests/test_module_boundaries.py without changing the test, run the focused test and registry checks, then rerun the failed slow behavioral surface.

## Notes

Full packing-validate ran all 66 surfaces: fast 2,145 passed, exhaustive-exact 53 passed, and 65 surfaces were green; only the slow-marker floor failed because this test measured 0.80s. Removed only the obsolete pytest.mark.slow decorator and registry entry, preserving the test. Focused regression and registry suite passed 15/15. The failed slow surface then passed 95 tests (2,199 deselected) in 782.88s with no below-floor marker.
