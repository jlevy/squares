---
type: is
id: is-01m0pdhw0j8329gez9sw0efd86
title: "Soundness perimeter: check every validity-asserting component against sqpack"
kind: task
status: open
priority: 0
version: 1
spec_path: docs/project/research/research-2026-08-22-packing-11-unit-squares.md
labels: []
dependencies: []
parent_id: is-01m0pdh5bj67ca8vk7ct53g5qt
created_at: 2026-08-23T04:20:09.873Z
updated_at: 2026-08-23T04:20:09.873Z
---
The systemic gap behind D-014. sqsearch is differential-tested against sqpack (differential_test.py); the quench is not, and the quench is what produced the false record claim. Enumerate every component that can emit or accept a configuration -- sqsearch, quench/solve_cell, quench_bracket, the basin-entry scorer -- and require each to be checked against sqpack.verify. Add the missing checks to the gate.
