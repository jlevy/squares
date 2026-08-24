---
type: is
id: is-01m0rrhw3a0zqmyw095twj9bn3
title: Basin counts are not stable under 1-ulp perturbation of the LP
kind: bug
status: open
priority: 0
version: 3
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-24-packing-engineering-maturity.md
labels:
  - engineering-maturity
dependencies: []
parent_id: is-01m0rrgqj3esjc4jx1fr3qy1ht
created_at: 2026-08-24T02:10:53.161Z
updated_at: 2026-08-24T21:22:09.836Z
---
The golden basin map's n=3 case changed from distinct_basins: 3 / converged: 3 to distinct_basins: 2 / converged: 4 in response to a change of 2.2e-16 in one constraint coefficient (the choose_cell rewrite in this branch).

What disappeared was a row at side 2.0176058468 with closed_form: null and converged_frequency: 0 -- a quench that ran out of iterations, recorded as a distinct basin. A ulp-scale change was enough to un-stall it.

Why this matters beyond the one case: distinct_basins, quench_frequency and converged_frequency are the primary observables of H-003, H-008, H-012, H-021 and H-023. If they move under ulp-scale perturbation then they also move under a scipy or HiGHS version bump, a different CPU, or a different build of the same code -- silently, and in the direction of whatever the numerics happened to do that day.

Two separable problems:
1. Non-converged endpoints are counted as basins. Whatever the intent, 'distinct_basins' currently conflates real basins with solver stalls. H-008 (false basin rate) is the hypothesis this most directly contaminates.
2. There is no stability control. Nothing measures how sensitive the census is to numerical perturbation.

Suggested work: add a deliberate +/- few-ulp perturbation control over the census inputs and assert the basin partition is unchanged; report converged and non-converged endpoints as separate populations rather than as rows of one table.
