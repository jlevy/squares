---
type: is
id: is-01m134wdcg8ctfygvw62gs9xbg
title: "PR #50 review R3: High: '~7 unknowns' is an off-by-one; correct count is 6"
kind: bug
status: closed
priority: 2
version: 2
labels:
  - packing
dependencies: []
parent_id: is-01m134wbw78hcnh0fsgqtej4rk
created_at: 2026-08-28T02:58:45.775Z
updated_at: 2026-08-28T03:20:01.502Z
closed_at: 2026-08-28T03:20:01.500Z
close_reason: "Addressed in a236598; disposition map posted to PR #50"
resolution: null
duplicate_of: null
---
The six orientation classes INCLUDE the axis class (15 squares at 0deg), so tilted classes are 5 and unknowns are s+5=6. Proven by the source's own 6x6 FindRoot system. Propagated through X-004, both specs, agenda-005, ledger, PR body.
