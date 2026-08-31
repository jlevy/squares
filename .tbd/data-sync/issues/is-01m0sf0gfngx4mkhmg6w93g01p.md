---
type: is
id: is-01m0sf0gfngx4mkhmg6w93g01p
title: Make the Trump branch record preserve and replay one-to-one coverage
kind: bug
status: closed
priority: 1
version: 2
spec_path: explorations/packing/tools/check_trump_tangent.py
labels:
  - packing
  - focus-discipline
dependencies: []
parent_id: is-01m0sd9662q9t69eyaxcxgx2j3
created_at: 2026-08-24T08:43:21.460Z
updated_at: 2026-08-24T08:48:53.861Z
closed_at: 2026-08-24T08:48:53.861Z
close_reason: Retained the alias-weighted 512-to-128 map, complete expected active tables and 42-row guards, unique digest coverage, ordered certificate rows, recomputed determination/scope, and duplicate-record selftest. Logged as D-137 before scientific execution.
resolution: null
duplicate_of: null
---
The first uncommitted H-026 checker collapsed derivative aliases without preserving raw multiplicities and its separate replay accepted 128 duplicates of one valid matrix as coverage of all 128 matrices. Preserve the exact 512 raw nonlinear selections to 128 derivative-distinct matrix map, assert the complete active tables and 42-row systems, reject duplicate or missing digests, and recompute the determination from replayed witnesses before any scientific execution. Record the validity error in defects.yaml and add a focused duplicate-record regression.
