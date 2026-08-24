---
type: is
id: is-01m0td7rar54g83je7jmphch98
title: Separate quench point-basins from terminal components
kind: bug
status: closed
priority: 1
version: 2
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-23-overnight-cartography-run.md
labels:
  - packing
  - review
  - soundness
dependencies: []
parent_id: is-01m0tbtgpb92e81ndvw4xm9be6
created_at: 2026-08-24T17:31:36.151Z
updated_at: 2026-08-24T17:36:31.735Z
closed_at: 2026-08-24T17:36:31.735Z
close_reason: "D-181 fixed: point-basins are defined separately from connected terminal components, preserving the exact D-034 blocker; normal gate passed."
resolution: null
duplicate_of: null
---
TUTORIAL and SYNOPSIS say a quench endpoint may not be a point. A deterministic quench still returns a pose; the problem is that point-preimages split one connected terminal family and are not the component-level object the atlas wants. Correct definitions and record D-181 as a D-034 recurrence.
