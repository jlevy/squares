---
type: is
id: is-01m0pdhxdvjmyttts8e3c42sd0
title: Correct research docs and the plan where soundness findings contradict them
kind: task
status: open
priority: 1
version: 1
spec_path: docs/project/research/research-2026-08-22-packing-11-unit-squares.md
labels: []
dependencies: []
parent_id: is-01m0pdh5bj67ca8vk7ct53g5qt
created_at: 2026-08-23T04:20:11.322Z
updated_at: 2026-08-23T04:20:11.322Z
---
Known inconsistencies: the search-philosophy report calls the quench endpoint 'exact' when it is exact only to solver tolerance (~1e-11, D-021); the standing review's R-2 and the plan spec claim the LP polish has 'rational output', which scipy/HiGHS does not provide; the claim that quenching makes basins 'discrete, nameable, exactly-valued' is qualified by class_tol dependence (D-020). Correct the living documents; leave the review's historical register entries alone per the ownership rule.
