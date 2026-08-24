---
type: is
id: is-01m0tw8egkfk3vpwt9n6n4qaa8
title: Refresh negative-control aggregates after D-197
kind: bug
status: open
priority: 1
version: 2
spec_path: explorations/packing/campaign/agendas/agenda-001-basin-confidence-ladder.md
labels:
  - packing
  - testing
  - bookkeeping
dependencies: []
parent_id: is-01m0tn3kqe19evm1r40wgnpb61
created_at: 2026-08-24T21:54:07.494Z
updated_at: 2026-08-24T21:54:19.423Z
---
The first post-exp-036 strict gate correctly failed because the defect-count and synopsis gate-detector mutation anchors still named the pre-D-197 totals. Record D-198 as a recurrence of D-187, update the anchors only after the new defect total is final, rerun the negative-control step, and preserve the independent deep-golden failure as evidence under outstanding D-126/D-162 rather than weakening that oracle.
