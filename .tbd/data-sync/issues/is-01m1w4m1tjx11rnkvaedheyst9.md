---
type: is
id: is-01m1w4m1tjx11rnkvaedheyst9
title: "PR #100 review R5: oracle invariant failure reported as a verifier disagreement"
kind: bug
status: closed
priority: 3
version: 2
labels: []
dependencies: []
parent_id: is-01m1w4krded865yyd393yn5my5
created_at: 2026-09-06T19:55:12.594Z
updated_at: 2026-09-06T19:55:30.693Z
closed_at: 2026-09-06T19:55:30.693Z
close_reason: Fixed in d663da6d on the PR branch.
resolution: null
duplicate_of: null
---
least_mass raised AssertionError for its own reduction failure, which main labelled a disagreement. Now OracleInvariantError, exit 2. Fixed in d663da6d.
