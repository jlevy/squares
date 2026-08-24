---
type: is
id: is-01m0s9424pvsd7cz8rae9ry7y0
title: "PR #17 review E15: lint floor must be warning-free"
kind: bug
status: closed
priority: 2
version: 2
labels:
  - packing
  - focus-discipline
dependencies: []
parent_id: is-01m0rwwt8912eq5f3507d581e1
created_at: 2026-08-24T07:00:26.389Z
updated_at: 2026-08-24T07:13:46.601Z
closed_at: 2026-08-24T07:13:46.600Z
close_reason: "Merged in PR #18 at b3545d0: intentional private access is locally suppressed and the gate requires BasedPyright's exact zero-error, zero-warning summary; D-131."
resolution: null
duplicate_of: null
---
The integrated normal gate printed 8 BasedPyright warnings and still reported ALL CHECKS PASSED because warnings do not make the command exit nonzero. Remove the current warnings and make the lint step fail if any warning or error remains, so the advertised lint floor and Python guideline are true.
