---
type: is
id: is-01m1w4m7c2c22c2swpqfa5ew6v
title: "PR #100 review R8: proved ceiling statement prints a bare rational"
kind: bug
status: closed
priority: 3
version: 2
labels: []
dependencies: []
parent_id: is-01m1w4krded865yyd393yn5my5
created_at: 2026-09-06T19:55:18.274Z
updated_at: 2026-09-06T19:55:32.515Z
closed_at: 2026-09-06T19:55:32.515Z
close_reason: Fixed in 956cc6d9 on the PR branch.
resolution: null
duplicate_of: null
---
CeilingVerdict.statement lost its decimal; now rational with _decimal_approximation beside it. Fixed in 956cc6d9.
