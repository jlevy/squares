---
type: is
id: is-01m134xc5mawp4cjv2d6b6tgay
title: "PR #50 review R11: Low: 'until interval certification discharges it' names the wrong mechanism"
kind: bug
status: open
priority: 2
version: 1
labels:
  - packing
dependencies: []
parent_id: is-01m134wbw78hcnh0fsgqtej4rk
created_at: 2026-08-28T02:59:17.299Z
updated_at: 2026-08-28T02:59:17.299Z
---
atlas plan:151-153, repeated in agenda-005's may-not-claim list. The pipeline's own success path discharges by exact substitution and exact verification, which is strictly stronger, yet the rule as written would forbid that path from ever moving the verified bound.
