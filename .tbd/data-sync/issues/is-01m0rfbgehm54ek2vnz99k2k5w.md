---
type: is
id: is-01m0rfbgehm54ek2vnz99k2k5w
title: "D070: exp-011 execution provenance was rewritten to a later record commit"
kind: bug
status: closed
priority: 1
version: 3
spec_path: explorations/packing/docs/project/reviews/review-2026-08-23-square-packing-program-and-pr14.md
labels:
  - packing
  - review
  - focus-process
  - provenance
dependencies: []
parent_id: is-01m0r7q3zk8x6cg4e30d149698
created_at: 2026-08-23T23:30:07.439Z
updated_at: 2026-08-23T23:58:57.984Z
closed_at: 2026-08-23T23:58:57.984Z
close_reason: Fixed and reconciled in the PR 15 checkpoint. Focused schema/ledger/runner checks and named mutation controls passed; the integrated normal gate passed in 125 seconds with all 29 controls firing and all 73 defect entries reconciled.
resolution: null
duplicate_of: null
---
The first exp-011 artifact recorded runtime HEAD 60a50cc. A later cleanup rewrote subject.engine_commit, method.commit, and verdict.commit to 6f94be6, the commit that recorded the round, while the synopsis retained 60a50cc. Restore all execution-provenance fields and make the runner carry execution-time identity across execute, record, and release.
