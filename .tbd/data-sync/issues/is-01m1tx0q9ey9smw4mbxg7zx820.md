---
type: is
id: is-01m1tx0q9ey9smw4mbxg7zx820
title: "Deep gate: declared-bounds audit reports unguarded n11 verifier limits"
kind: bug
status: closed
priority: 2
version: 4
labels: []
dependencies: []
created_at: 2026-09-06T08:23:04.750Z
updated_at: 2026-09-06T08:36:25.687Z
closed_at: 2026-09-06T08:36:25.687Z
close_reason: Fixed in stacked PR 96 commit 8e0fba99. All required CI checks passed in run 34022006920; all45 selected pre-push steps and31 record steps passed locally, including558 reachable tests. Previously failing bounds audit and all affected negative controls now pass.
resolution: null
duplicate_of: null
---
Full local gate after PR 94 repairs: tests/test_check_declared_bounds.py::test_n68_depth_bound_is_named_by_its_refusal_test fails because receipt violations includes verify_claim.py MAX_ATOMS and MAX_DIRECTIONS. Determine baseline and repair actual guard/audit behavior without suppressing coverage.

## Notes

Fixed in follow-up PR 96 commit 8e0fba99: audit recognizes immediately assigned raise messages; existing verifier ceiling refusal test uses its distinctive diagnostic. Five focused tests and previously failing full-repository bounds audit pass. No verifier behavior changed.
