---
type: is
id: is-01m1tz72zsx4ksbtme6540cjha
title: Name standalone verifier ceilings in the declared-bound guard
kind: bug
status: closed
priority: 0
version: 6
labels:
  - validation
  - upstream-reconciliation
dependencies: []
parent_id: is-01m1t5yjssbd51cnnw2zwkqah6
created_at: 2026-09-06T09:01:30.488Z
updated_at: 2026-09-06T09:40:21.308Z
closed_at: 2026-09-06T09:40:21.307Z
close_reason: Verifier ceilings are explicitly named and both focused and full integrated controls pass.
resolution: null
duplicate_of: null
---
The post-PR92 full slow surface found MAX_ATOMS and MAX_DIRECTIONS in cases/n11_fractional_certificate/verify_claim.py without statically named refusal coverage. Bind both limits to the existing runpy verifier test, exercise the exact ceiling and first refusal, run the focused controls, and rerun the full gate before PR89 lands.

## Notes

Completed at integrated head 00e774de. MAX_ATOMS and MAX_DIRECTIONS are explicitly bound to exact-ceiling and first-refusal controls; focused pair passed 2 in 3.36s; integrated hosted suite passed; canonical full gate passed all checks in 1232.88s, including the declared-bound guard.
