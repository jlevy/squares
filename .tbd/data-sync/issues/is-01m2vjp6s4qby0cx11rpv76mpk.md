---
type: is
id: is-01m2vjp6s4qby0cx11rpv76mpk
title: "PR #199 review F-PY-1: HiGHS solver error mapped to M3 kill"
kind: bug
status: closed
priority: 2
version: 2
labels: []
dependencies: []
parent_id: is-01m2vjmfpw370ygezsjr5xbn9z
created_at: 2026-09-19T00:57:30.660Z
updated_at: 2026-09-19T00:57:52.998Z
closed_at: 2026-09-19T00:57:52.997Z
close_reason: "Fixed on faeb4bd2: only HiGHS status 2 is infeasible; status 4 stays unresolved. Test: test_solver_error_without_incumbent_is_unresolved_never_a_kill."
resolution: null
duplicate_of: null
---
https://github.com/jlevy/squares/pull/199#issuecomment-5734563940
packing/src/sqpack/fractional/integral_piercing.py:658. Status 4 with no incumbent was treated as infeasible → killed_coarse_net. Already patched on faeb4bd2; close after confirming.
