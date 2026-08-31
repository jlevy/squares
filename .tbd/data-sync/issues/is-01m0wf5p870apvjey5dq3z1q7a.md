---
type: is
id: is-01m0wf5p870apvjey5dq3z1q7a
title: Repair session-012 clock contract
kind: bug
status: closed
priority: 2
version: 2
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-23-overnight-cartography-run.md
labels:
  - packing
  - bookkeeping
  - process
dependencies: []
parent_id: is-01m0w9a47h5zrn7jf16pp2kpxs
created_at: 2026-08-25T12:43:54.496Z
updated_at: 2026-08-25T12:50:48.910Z
closed_at: 2026-08-25T12:50:48.909Z
close_reason: Corrected the active phase recording mode and non-understated wall budget; AgentSession/v2 validation passes. D-309 retains the draft error.
resolution: null
duplicate_of: null
---
The first uncommitted session-012 draft used retrospective recording for an active clocked phase and rounded its 184m03s wall span down to 184 minutes. Mark the publicly declared active phase contemporaneous, use a non-understated 185-minute budget, and rerun the session schema.
