---
type: is
id: is-01m0w56abhg68342kennddmgb2
title: Advance the soundness mutation diagnostic denominator
kind: bug
status: closed
priority: 2
version: 2
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-23-overnight-cartography-run.md
labels:
  - packing
  - bookkeeping
  - negative-control
dependencies: []
parent_id: is-01m0vr7g27g67p699aepcdksxd
created_at: 2026-08-25T09:49:29.328Z
updated_at: 2026-08-25T09:50:06.661Z
closed_at: 2026-08-25T09:50:06.661Z
close_reason: "D-267 fixed: soundness mutation expected diagnostic now advances from58/69 to58/70; total and gate anchors reconcile to267 and21; all62 controls required before commit."
resolution: null
duplicate_of: null
---
Adding D-266 advanced soundness defects from69 to70 and updated the mutation anchor, but the expected checker diagnostic still said58 of69. Update it to58 of70, log recurrence of the aggregate-anchor class, and require all62 controls before commit.
