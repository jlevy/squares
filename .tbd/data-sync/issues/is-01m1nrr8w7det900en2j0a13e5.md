---
type: is
id: is-01m1nrr8w7det900en2j0a13e5
title: Bound exact-coincidence interval diagnostic runtime
kind: bug
status: closed
priority: 1
version: 3
labels: []
dependencies: []
created_at: 2026-09-04T08:32:21.382Z
updated_at: 2026-09-04T08:43:14.364Z
closed_at: 2026-09-04T08:43:14.362Z
close_reason: Added conservative per-direction box budget, explicit budget diagnostics, and enclose-mode C4 bound checks; all 28 interval tests pass across focused/full splits with static checks clean.
resolution: null
duplicate_of: null
---
Diagnose and, if soundly straightforward, fix branch-and-bound explosion in test_an_exact_edge_coincidence_is_reported_undecided_never_accepted while preserving undecided-not-accepted semantics. Limit code changes to fractional/interval.py and its test.
