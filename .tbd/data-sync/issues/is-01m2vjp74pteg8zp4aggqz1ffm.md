---
type: is
id: is-01m2vjp74pteg8zp4aggqz1ffm
title: "PR #199 review F-PY-2: milp called at 0s after encoding wall"
kind: bug
status: closed
priority: 2
version: 2
labels: []
dependencies: []
parent_id: is-01m2vjmfpw370ygezsjr5xbn9z
created_at: 2026-09-19T00:57:31.030Z
updated_at: 2026-09-19T00:57:53.265Z
closed_at: 2026-09-19T00:57:53.264Z
close_reason: "Fixed on faeb4bd2: encoding that consumes the wall records timeout, optimizer_ran=False, and does not call milp."
resolution: null
duplicate_of: null
---
https://github.com/jlevy/squares/pull/199#issuecomment-5734563940
packing/devtools/pierce_t018_sites.py remaining<=0 still called milp. Already patched on faeb4bd2; close after confirming.
