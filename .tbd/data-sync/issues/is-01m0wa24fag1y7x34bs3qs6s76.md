---
type: is
id: is-01m0wa24fag1y7x34bs3qs6s76
title: Reject zero-step sqsearch regimes before they can hang
kind: bug
status: open
priority: 1
version: 1
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-22-minimal-packing-toolkit.md
labels:
  - packing
  - focus-efficiency
dependencies: []
parent_id: is-01m0p49tf4hqd8d8v13hcgxhyj
created_at: 2026-08-25T11:14:35.105Z
updated_at: 2026-08-25T11:14:35.105Z
---
Order-7 independent count review found that --steps 0 with positive --budget-moves performs zero moves per restart. With the default unlimited max-restarts, run_chain and run_entry_chain never terminate; with a finite restart cap they spin uselessly until the cap. Reject steps=0 for positive budgets at the CLI boundary (and define zero-budget behavior), add focused ordinary and basin-entry failure tests, and preserve bounded diagnostics. Also audit n=0 and chains=0 argument handling without broadening the first repair.
