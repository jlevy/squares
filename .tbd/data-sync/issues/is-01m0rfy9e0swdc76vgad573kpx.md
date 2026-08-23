---
type: is
id: is-01m0rfy9e0swdc76vgad573kpx
title: "D073: agent-session filename and id agreement was not checked"
kind: bug
status: closed
priority: 2
version: 2
spec_path: explorations/packing/docs/project/reviews/review-2026-08-23-square-packing-program-and-pr14.md
labels:
  - packing
  - review
  - focus-process
  - bookkeeping
dependencies: []
parent_id: is-01m0r7q3zk8x6cg4e30d149698
created_at: 2026-08-23T23:40:22.847Z
updated_at: 2026-08-23T23:58:57.994Z
closed_at: 2026-08-23T23:58:57.994Z
close_reason: Fixed and reconciled in the PR 15 checkpoint. Focused schema/ledger/runner checks and named mutation controls passed; the integrated normal gate passed in 125 seconds with all 29 controls firing and all 73 defect entries reconciled.
resolution: null
duplicate_of: null
---
The new session artifacts were schema-validated and duplicate-checked, but ledger naming() omitted the sessions collection, so a schema-valid session id could disagree with its filename while the ledger stayed green. Wire sessions into the existing naming invariant and add one mutation control.
