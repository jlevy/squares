---
type: is
id: is-01m1tz72zsx4ksbtme6540cjha
title: Name standalone verifier ceilings in the declared-bound guard
kind: bug
status: in_progress
priority: 0
version: 3
labels:
  - validation
  - upstream-reconciliation
dependencies: []
parent_id: is-01m1t5yjssbd51cnnw2zwkqah6
created_at: 2026-09-06T09:01:30.488Z
updated_at: 2026-09-06T09:03:58.614Z
---
The post-PR92 full slow surface found MAX_ATOMS and MAX_DIRECTIONS in cases/n11_fractional_certificate/verify_claim.py without statically named refusal coverage. Bind both limits to the existing runpy verifier test, exercise the exact ceiling and first refusal, run the focused controls, and rerun the full gate before PR89 lands.

## Notes

Fixed on 957e5abe and pushed. The runpy refusal test now explicitly names MAX_ATOMS and MAX_DIRECTIONS, accepts each exact ceiling, and refuses the next value. Focused controls passed 2 in 3.36s. Await exact-head full and hosted gates before closure.
