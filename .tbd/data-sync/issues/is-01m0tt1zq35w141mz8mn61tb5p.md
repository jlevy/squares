---
type: is
id: is-01m0tt1zq35w141mz8mn61tb5p
title: Log and prevent broad defect-status patch recurrence
kind: bug
status: open
priority: 1
version: 1
spec_path: explorations/packing/campaign/agendas/agenda-001-basin-confidence-ladder.md
labels:
  - packing
  - bookkeeping
  - process
dependencies: []
parent_id: is-01m0tpn9ej3z97jr6nq97fb9gt
created_at: 2026-08-24T21:15:38.593Z
updated_at: 2026-08-24T21:15:38.593Z
---
While terminalizing exp-035, a context-poor status edit changed D-034 from outstanding to fixed instead of changing D-194. The diff audit caught it before commit. Restore D-034, set D-194 explicitly under its id, record D-196 as a recurrence of D-160, and require the final defect diff plus generated aggregate checks before commit.
