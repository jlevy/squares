---
type: is
id: is-01m1nqqymzdbdmzrq4srw19dap
title: Prevent partial and overflowing interval-verifier acceptance
kind: bug
status: closed
priority: 1
version: 3
labels: []
dependencies: []
created_at: 2026-09-04T08:14:42.334Z
updated_at: 2026-09-04T08:25:33.756Z
closed_at: 2026-09-04T08:25:33.748Z
close_reason: Implemented interval verifier soundness guards and regressions; focused and full-net validation pass.
resolution: null
duplicate_of: null
---
Restricted direction runs must never produce a theorem-accepted verdict; exact Python-int preflight must refuse weights or totals that could overflow NumPy int64 mass arithmetic; add adversarial regressions and clarify nonnegative-weight theorem wording.
