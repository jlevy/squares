---
type: is
id: is-01m1tz72zsx4ksbtme6540cjha
title: Name standalone verifier ceilings in the declared-bound guard
kind: bug
status: in_progress
priority: 0
version: 4
labels:
  - validation
  - upstream-reconciliation
dependencies: []
parent_id: is-01m1t5yjssbd51cnnw2zwkqah6
created_at: 2026-09-06T09:01:30.488Z
updated_at: 2026-09-06T09:20:34.280Z
---
The post-PR92 full slow surface found MAX_ATOMS and MAX_DIRECTIONS in cases/n11_fractional_certificate/verify_claim.py without statically named refusal coverage. Bind both limits to the existing runpy verifier test, exercise the exact ceiling and first refusal, run the focused controls, and rerun the full gate before PR89 lands.

## Notes

The standalone verifier ceiling fix remains on the integrated head 00e774de. Exact focused controls passed 2 in 3.36s and old-head hosted required run 34023580880 passed. The old-head local full run was intentionally stopped—not failed—when PR93 landed and moved main. Canonical full validation is now running on the only relevant integrated head; close after that gate and final hosted checks pass.
