---
type: is
id: is-01m0vxn1fyzy17r1prygqcfaap
title: Make AgentSession validation receipts explicit about their working directory
kind: bug
status: open
priority: 2
version: 1
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-23-overnight-cartography-run.md
labels:
  - packing
  - process
dependencies: []
parent_id: is-01m0vr7g27g67p699aepcdksxd
created_at: 2026-08-25T07:37:43.153Z
updated_at: 2026-08-25T07:37:43.153Z
---
Session-010's first boundary check failed when a bare uv command was replayed from repository root rather than explorations/packing. The active artifact now uses uv run --directory explorations/packing. Record the error in the next defect-log checkpoint and decide whether the session checker or runbook should require root-replayable commands without adding a new scheduler.
