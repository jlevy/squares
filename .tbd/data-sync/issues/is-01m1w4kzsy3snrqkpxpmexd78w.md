---
type: is
id: is-01m1w4kzsy3snrqkpxpmexd78w
title: "PR #100 review R4: a verifier refusal loses the oracle's reproduction data"
kind: bug
status: closed
priority: 2
version: 2
labels: []
dependencies: []
parent_id: is-01m1w4krded865yyd393yn5my5
created_at: 2026-09-06T19:55:10.526Z
updated_at: 2026-09-06T19:55:30.691Z
closed_at: 2026-09-06T19:55:30.691Z
close_reason: Fixed in d663da6d on the PR branch.
resolution: null
duplicate_of: null
---
check_cases caught only AssertionError; minimal_verify signals failure with ValueError, so a refusing verifier died in a traceback without seed and case. Fixed in d663da6d.
