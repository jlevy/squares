---
type: is
id: is-01m1ntw9d15bq6zkfk09dc4kty
title: Return feasible witnesses from exact fractional sweep
kind: bug
status: closed
priority: 1
version: 3
labels: []
dependencies: []
created_at: 2026-09-04T09:09:30.143Z
updated_at: 2026-09-04T09:15:50.033Z
closed_at: 2026-09-04T09:15:50.029Z
close_reason: Confirmed exact infeasible-midpoint counterexample; minimum_covered_mass now returns an exact point in the open cell intersected with the feasible centre polygon, with regression and focused validation.
resolution: null
duplicate_of: null
---
Investigate and fix minimum_covered_mass returning a raw event-cell midpoint outside the feasible-centre polygon when the open cell merely intersects it. Add an exact regression and keep changes scoped to sweep implementation/tests.
