---
type: is
id: is-01m0tvjc1sk6q8c675s4wgcp7p
title: Guard branch identity at campaign commit boundaries
kind: bug
status: closed
priority: 1
version: 2
spec_path: explorations/packing/campaign/agendas/agenda-001-basin-confidence-ladder.md
labels:
  - packing
  - discipline
  - process
dependencies: []
parent_id: is-01m0ttgympmz814rqyms075mvf
created_at: 2026-08-24T21:42:04.088Z
updated_at: 2026-08-24T21:43:19.063Z
closed_at: 2026-08-24T21:43:19.062Z
close_reason: D-197 records the shared-workspace checkout race. The isolated checker commit now sits on the campaign branch, the engineering-plan ref is restored to its pushed commit, and the remaining campaign uses an immediate branch-and-staged-scope check before commits.
resolution: null
duplicate_of: null
---
A concurrent shared-workspace checkout moved HEAD from the four-hour campaign branch to the engineering-maturity branch between status inspection and the exp-036 instrument commit. The checker-only commit landed one branch too high. Detected immediately from the commit banner; recovered without data loss by switching to the intended branch, cherry-picking the isolated commit, and restoring the other local branch ref to its pushed plan commit. Record D-197 and add a cheap branch/HEAD assertion immediately before future campaign commits; no worktree or lease protocol is required.
