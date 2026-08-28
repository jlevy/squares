---
type: is
id: is-01m134xbrqm4hg7jnszjetamym
title: "PR #50 review R10: Low: the phase-2 negative control is not well posed"
kind: bug
status: closed
priority: 2
version: 2
labels:
  - packing
dependencies: []
parent_id: is-01m134wbw78hcnh0fsgqtej4rk
created_at: 2026-08-28T02:59:16.886Z
updated_at: 2026-08-28T03:20:05.950Z
closed_at: 2026-08-28T03:20:05.949Z
close_reason: "Addressed in a236598; disposition map posted to PR #50"
resolution: null
duplicate_of: null
---
impl spec:225-227. The raw system is redundant: 89 incidences plus angle identities against 88 raw unknowns. Dropping a redundant incidence leaves it exactly as solvable, so the control as written fails. Dropping an equation cannot make a solvable system unsolvable.
