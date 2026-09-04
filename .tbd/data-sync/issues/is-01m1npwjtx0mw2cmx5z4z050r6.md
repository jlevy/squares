---
type: is
id: is-01m1npwjtx0mw2cmx5z4z050r6
title: Reject signed weights in fractional certificates
kind: bug
status: closed
priority: 1
version: 3
labels: []
dependencies: []
created_at: 2026-09-04T07:59:45.500Z
updated_at: 2026-09-04T08:11:05.780Z
closed_at: 2026-09-04T08:11:05.779Z
close_reason: Implemented Certificate and sweep refusal for signed weights, documented the nonnegative measure dependency, and added the exact n=1 regression; focused Python 3.14 tests, Ruff, and basedpyright pass.
resolution: null
duplicate_of: null
---
Make nonnegative atom weights an explicit Certificate/theorem precondition, prevent verification/replay acceptance of signed weights, document the sweep boundary argument's dependence on nonnegativity, and add an exact regression for the n=1 signed-weight false certificate.
