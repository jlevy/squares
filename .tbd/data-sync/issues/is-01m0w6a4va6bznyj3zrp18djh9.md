---
type: is
id: is-01m0w6a4va6bznyj3zrp18djh9
title: Use the declared phase-transition enum for the phase-11 hard stop
kind: bug
status: closed
priority: 2
version: 2
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-23-overnight-cartography-run.md
labels:
  - packing
  - bookkeeping
dependencies: []
parent_id: is-01m0vr7g27g67p699aepcdksxd
created_at: 2026-08-25T10:09:03.337Z
updated_at: 2026-08-25T10:17:42.674Z
closed_at: 2026-08-25T10:17:42.673Z
close_reason: "D-271, D-273, and D-274 are recorded and fixed before integration: the phase transition uses the enforced enum, the workflow test proves a single exact blocking command with no advisory escape, and corrected focused checks plus the complete gate pass."
resolution: null
duplicate_of: null
---
The first phase-12 record used entered_by=timebox_rotation, but the enforced session contract permits only session_start, planned_checkpoint, evidence_checkpoint, or user_request. packing-ledger check caught it before commit. Replace it with planned_checkpoint, record D-271, and resynchronize defect aggregates and mutation anchors.
