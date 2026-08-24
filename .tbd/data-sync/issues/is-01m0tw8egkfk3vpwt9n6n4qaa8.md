---
type: is
id: is-01m0tw8egkfk3vpwt9n6n4qaa8
title: Refresh negative-control aggregates after D-197
kind: bug
status: closed
priority: 1
version: 3
spec_path: explorations/packing/campaign/agendas/agenda-001-basin-confidence-ladder.md
labels:
  - packing
  - testing
  - bookkeeping
dependencies: []
parent_id: is-01m0tn3kqe19evm1r40wgnpb61
created_at: 2026-08-24T21:54:07.494Z
updated_at: 2026-08-24T21:55:44.305Z
closed_at: 2026-08-24T21:55:44.304Z
close_reason: D-198 is recorded as a D-187 recurrence. The defect-count and gate-detector anchors now target the final 198-defect and 9-of-198 aggregates, and all 37 negative controls fire in a bounded focused rerun.
resolution: null
duplicate_of: null
---
The first post-exp-036 strict gate correctly failed because the defect-count and synopsis gate-detector mutation anchors still named the pre-D-197 totals. Record D-198 as a recurrence of D-187, update the anchors only after the new defect total is final, rerun the negative-control step, and preserve the independent deep-golden failure as evidence under outstanding D-126/D-162 rather than weakening that oracle.
