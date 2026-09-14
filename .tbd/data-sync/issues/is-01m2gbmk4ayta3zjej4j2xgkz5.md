---
type: is
id: is-01m2gbmk4ayta3zjej4j2xgkz5
title: "PR #167: enforce exact JSON types in witness validation"
kind: bug
status: open
priority: 3
version: 1
labels: []
dependencies: []
parent_id: is-01m2gbcm4afdzz4r8x790g898q
created_at: 2026-09-14T16:22:38.971Z
updated_at: 2026-09-14T16:22:38.971Z
---
In packing/devtools/analyze_bc303_h162_receipt.py:119-127, witness fields are compared with !=, so Python accepts JSON 0 as false and booleans as integer indices. Parse witness integer fields through _integer and require type(reflected) is bool before equality; add malformed-type tests.
