---
type: is
id: is-01m1vrfr6zstmz05m40pa0peqg
title: "PR #96 review PR96-R1: reject incidental f-string audit evidence"
kind: bug
status: closed
priority: 1
version: 3
labels: []
dependencies: []
parent_id: is-01m1vr1d6g9t24jr67z6dwkyh1
created_at: 2026-09-06T16:23:08.766Z
updated_at: 2026-09-06T16:57:15.147Z
closed_at: 2026-09-06T16:57:15.147Z
close_reason: Fixed in the final reviewed PR94/96/95 candidates; focused regressions, broad local validation, and independent cross-review passed. Parent review and landing tasks remain open while final hosted CI and disposition publication complete.
resolution: null
duplicate_of: null
---
Senior review https://github.com/jlevy/squares/pull/96#issuecomment-5560542817: packing/devtools/check_declared_bounds.py:205 and 343. Assigned f-string expressions and short fragments incorrectly name untested bounds. Extract rendered text only, require sufficiently long matching fragments, and restore precise negative/positive attribution controls.
