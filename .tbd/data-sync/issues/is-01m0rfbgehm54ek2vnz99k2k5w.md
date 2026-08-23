---
type: is
id: is-01m0rfbgehm54ek2vnz99k2k5w
title: "D070: exp-011 execution provenance was rewritten to a later record commit"
kind: bug
status: open
priority: 1
version: 1
spec_path: explorations/packing/docs/project/reviews/review-2026-08-23-square-packing-program-and-pr14.md
labels:
  - packing
  - review
  - focus-process
  - provenance
dependencies: []
parent_id: is-01m0r7q3zk8x6cg4e30d149698
created_at: 2026-08-23T23:30:07.439Z
updated_at: 2026-08-23T23:30:07.439Z
---
The first exp-011 artifact recorded runtime HEAD 60a50cc. A later cleanup rewrote subject.engine_commit and method.commit to 6f94be6, the commit that recorded the round, while the synopsis retained 60a50cc. Restore execution provenance and make the runner carry execution-time identity across claim, execute, and record.
