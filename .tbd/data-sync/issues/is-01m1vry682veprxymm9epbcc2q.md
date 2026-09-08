---
type: is
id: is-01m1vry682veprxymm9epbcc2q
title: "PR #94 review R94-3: keep third-party package identity independent of renderer order"
kind: bug
status: closed
priority: 2
version: 2
labels: []
dependencies: []
parent_id: is-01m1vr1cwbx9h9c8gm65jrgpg6
created_at: 2026-09-06T16:31:01.889Z
updated_at: 2026-09-06T16:57:15.135Z
closed_at: 2026-09-06T16:57:15.135Z
close_reason: Fixed in the final reviewed PR94/96/95 candidates; focused regressions, broad local validation, and independent cross-review passed. Parent review and landing tasks remain open while final hosted CI and disposition publication complete.
resolution: null
duplicate_of: null
---
Supplemental independent review: render with headline certificate first describes the fixed third-party package as containing 381/100, although thirdparty/certificate.json outer_side is 19/5. Template uses DEFAULT_L_FRAC at line556. Bind prose to packaged certificate identity and test normal, solo, reversed selections.
