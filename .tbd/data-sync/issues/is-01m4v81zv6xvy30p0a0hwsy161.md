---
type: is
id: is-01m4v81zv6xvy30p0a0hwsy161
title: Build sq17-lean's statement and endpoint closures here and print their axioms (cheap partial check)
kind: task
status: open
priority: 2
version: 1
labels: []
dependencies: []
parent_id: is-01m4v5ne8b1dq1gyybx5mj689d
created_at: 2026-10-13T18:23:06.086Z
updated_at: 2026-10-13T18:23:06.086Z
---
From the review of 13 October: elaborate the statement and endpoint modules (at most 20, all in the Git tree) against the Mathlib v4.34.1 cache and #print axioms Sq17.EndpointRoot.unique_root; then build the EndpointPacking (18 modules) and PackingStatement (241 modules) closures and run lean4checker, which gives a kernel-only check of the upper half and of the statement. Needs Lean 4.34.1 installed here and the Mathlib cache; no native_decide is in those closures. As devtools.audit_n11_lean did for n = 11, the route is a first-party audit tool (OR-1).
