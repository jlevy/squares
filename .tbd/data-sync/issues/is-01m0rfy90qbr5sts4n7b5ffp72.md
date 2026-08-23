---
type: is
id: is-01m0rfy90qbr5sts4n7b5ffp72
title: "D072: direct execute and release paths bypassed the gate marker"
kind: bug
status: closed
priority: 1
version: 2
spec_path: explorations/packing/docs/project/reviews/review-2026-08-23-square-packing-program-and-pr14.md
labels:
  - packing
  - review
  - focus-process
  - robustness
dependencies: []
parent_id: is-01m0r7q3zk8x6cg4e30d149698
created_at: 2026-08-23T23:40:22.422Z
updated_at: 2026-08-23T23:58:57.989Z
closed_at: 2026-08-23T23:58:57.989Z
close_reason: Fixed and reconciled in the PR 15 checkpoint. Focused schema/ledger/runner checks and named mutation controls passed; the integrated normal gate passed in 125 seconds with all 29 controls firing and all 73 defect entries reconciled.
resolution: null
duplicate_of: null
---
The runner documented mutual exclusion between the in-place mutation gate and campaign execution, but direct execute and release commands did not call the existing marker guard. Add the same cooperative refusal already used by status, claim, and record, exercise both commands under the marker, and record the recurrence of D-035/D-064 without introducing leases or worktrees.
