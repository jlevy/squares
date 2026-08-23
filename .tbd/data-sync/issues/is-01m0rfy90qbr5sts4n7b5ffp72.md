---
type: is
id: is-01m0rfy90qbr5sts4n7b5ffp72
title: "D072: direct execute and release paths bypassed the gate marker"
kind: bug
status: open
priority: 1
version: 1
spec_path: explorations/packing/docs/project/reviews/review-2026-08-23-square-packing-program-and-pr14.md
labels:
  - packing
  - review
  - focus-process
  - robustness
dependencies: []
parent_id: is-01m0r7q3zk8x6cg4e30d149698
created_at: 2026-08-23T23:40:22.422Z
updated_at: 2026-08-23T23:40:22.422Z
---
The runner documented mutual exclusion between the in-place mutation gate and campaign execution, but direct execute and release commands did not call the existing marker guard. Add the same cooperative refusal already used by status, claim, and record, exercise both commands under the marker, and record the recurrence of D-035/D-064 without introducing leases or worktrees.
