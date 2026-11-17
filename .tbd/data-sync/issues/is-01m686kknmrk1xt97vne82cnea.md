---
type: is
id: is-01m686kknmrk1xt97vne82cnea
title: "Validation backlog: intake pass 2026-10-31 (think-3guf)"
kind: task
status: open
priority: 2
version: 1
labels:
  - validation
dependencies: []
parent_id: is-01m684vnbc5mmkjn950c3edw3w
created_at: 2026-10-31T05:23:35.732Z
updated_at: 2026-10-31T05:23:35.732Z
---
The validation backlog of the 2026-10-31 intake pass (epic think-3guf), by result-import.md stage 4, "The Compute Cap and the Validation Backlog". Cap: the owner's standing 40 CPU-hours per item (think-lh7d); the host has 4 cores shared by five lanes. Opened by lane L3 (bold-ritchie-l3); each lane adds its own rows, and the coordinator owns the table.

| Item | Bead | Serves | Cost (CPU-h) | Basis | Status | Depends on |
| --- | --- | --- | --- | --- | --- | --- |
| zm_mixed.py's complete two-stage pass over the s(44) = 7 cover (depth 24 over 9,800 D4 roots, depth 30 over the 27 left) | think-qvp6 | think-1v4b (#842) | about 138 (143 stated) | the source's per-root records: 403,192 + 92,353 CPU-s | held (over the cap); a subset fits: the 27 depth-30 roots, 25.7 CPU-h | retaining zeromargin.py at evand 659ee62; the owner's word for the spend or a subset |

## Totals by status
- running: 0
- runnable: 0
- gated on decision: 0
- held: 1 item, about 138 CPU-h (#842's second machine method; it raises no rung)

## Not yet priced
- (none from L3)
