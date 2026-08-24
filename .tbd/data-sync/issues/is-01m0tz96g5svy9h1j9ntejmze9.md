---
type: is
id: is-01m0tz96g5svy9h1j9ntejmze9
title: Audit all frontier cases under a strict source-and-assurance contract
kind: task
status: open
priority: 1
version: 4
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-24-frontier-assurance-and-verification.md
labels: []
dependencies: []
parent_id: is-01m0typjn7s866m042zsemybj6
created_at: 2026-08-24T22:46:57.796Z
updated_at: 2026-08-24T23:02:56.751Z
---
Review n=1..100 row by row against primary sources. Separate standing published value, attribution, geometry availability, assurance (external claim, numerically checked, or verified), arithmetic method (numerical-f64, numerical-multiprecision, interval-certified, exact-algebraic), verification origin (named external party, this repository, or both), certificate and replay command, independent-replay status, numerical precision/tolerance, conflicts, and last source review. Migrate the mixed verified_here field to an honest evidence structure. No hash counts as mathematical evidence. Regenerate reader views and fail on missing required assurance metadata without inventing facts.
