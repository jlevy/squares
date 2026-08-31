---
type: is
id: is-01m0rfbfbyw0fhq0fzavbd1cxn
title: "D067: terminal experiment wall time was omitted from the campaign total"
kind: bug
status: closed
priority: 1
version: 2
spec_path: explorations/packing/docs/project/reviews/review-2026-08-23-square-packing-program-and-pr14.md
labels:
  - packing
  - review
  - focus-process
  - technical-error
dependencies: []
parent_id: is-01m0r7q3zk8x6cg4e30d149698
created_at: 2026-08-23T23:30:06.332Z
updated_at: 2026-08-23T23:58:57.964Z
closed_at: 2026-08-23T23:58:57.964Z
close_reason: Fixed and reconciled in the PR 15 checkpoint. Focused schema/ledger/runner checks and named mutation controls passed; the integrated normal gate passed in 125 seconds with all 29 controls firing and all 73 defect entries reconciled.
resolution: null
duplicate_of: null
---
exp-011 retained five raw summary times but omitted effort.wall_seconds, so the generated campaign total excluded 397.474 seconds. Restore the raw-derived value, require wall time on terminal rounds, make the runner produce it, and add a firing mutation control.
