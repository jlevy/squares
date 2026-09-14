---
type: is
id: is-01m2gbmk4ayta3zjej4j2xgkz5
title: "PR #167: enforce exact JSON types in witness validation"
kind: bug
status: closed
priority: 3
version: 4
labels: []
dependencies: []
parent_id: is-01m2gce39ed9awfhdpaq8ed3rt
created_at: 2026-09-14T16:22:38.971Z
updated_at: 2026-09-14T19:20:07.611Z
closed_at: 2026-09-14T19:20:07.610Z
close_reason: Fixed in ed68f644; 14 focused tests pass, Ruff/BasedPyright are clean, pre-push functional validation passes, and fresh hosted required CI is green on the exact head.
resolution: null
duplicate_of: null
---
In packing/devtools/analyze_bc303_h162_receipt.py:119-127, witness fields are compared with !=, so Python accepts JSON 0 as false and booleans as integer indices. Parse witness integer fields through _integer and require type(reflected) is bool before equality; add malformed-type tests.

## Notes

Fixed in ed68f644; focused tests and static checks pass. Awaiting clean checkpoint and hosted CI before closure.
