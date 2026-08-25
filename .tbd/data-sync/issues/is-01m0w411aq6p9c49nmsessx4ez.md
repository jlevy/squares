---
type: is
id: is-01m0w411aq6p9c49nmsessx4ez
title: Align delegation deadlines with declared budgets
kind: bug
status: closed
priority: 2
version: 2
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-23-overnight-cartography-run.md
labels:
  - packing
  - bookkeeping
  - session
dependencies: []
parent_id: is-01m0vr7g27g67p699aepcdksxd
created_at: 2026-08-25T09:29:07.670Z
updated_at: 2026-08-25T09:30:42.530Z
closed_at: 2026-08-25T09:30:42.529Z
close_reason: "D-265 fixed: design and first-implementation delegation budgets now match their full 15- and 17-minute deadline windows; ledger validates deadline arithmetic."
resolution: null
duplicate_of: null
---
Two phase-8 delegation records declared deadline intervals longer than budget_minutes. Correct the budget receipts to match their actual bounded windows and retain the ledger check as the regression.
