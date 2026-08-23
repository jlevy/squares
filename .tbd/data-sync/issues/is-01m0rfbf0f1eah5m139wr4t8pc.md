---
type: is
id: is-01m0rfbf0f1eah5m139wr4t8pc
title: "D066: active baseline script still classified open n=12 as a negative control"
kind: bug
status: open
priority: 1
version: 1
spec_path: explorations/packing/docs/project/reviews/review-2026-08-23-square-packing-program-and-pr14.md
labels:
  - packing
  - review
  - focus-process
  - technical-error
dependencies: []
parent_id: is-01m0r7q3zk8x6cg4e30d149698
created_at: 2026-08-23T23:30:05.966Z
updated_at: 2026-08-23T23:30:05.966Z
---
The active run_baseline.sh instruction contradicted the corrected campaign contract and could teach an arriving agent to discard a valid sub-4 n=12 candidate. Correct the instruction, log the recurrence of D-042, and keep the open-case policy synchronized.
