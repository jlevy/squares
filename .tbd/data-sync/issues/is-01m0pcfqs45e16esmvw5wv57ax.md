---
type: is
id: is-01m0pcfqs45e16esmvw5wv57ax
title: "Diagnose the quench_bracket slow path (n=5 seed 4: 8020 LP solves without converging)"
kind: bug
status: open
priority: 2
version: 1
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-22-minimal-packing-toolkit.md
labels: []
dependencies: []
parent_id: is-01m0p49s01h862tq6wp0dd085c
created_at: 2026-08-23T04:01:31.427Z
updated_at: 2026-08-23T04:01:31.427Z
---
A cell whose LP solves in 5 ms sent quench_bracket past 145 s; now bounded by a 30 s wall budget that reports reason='time budget'. 2-3 of 5 seeds hit it per cell. Likely the line search finding endless sub-tol improvements, or classes re-splitting each sweep. The budget is a guard, not a fix.
