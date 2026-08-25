---
type: is
id: is-01m0w943qydjjq7xdn58tg55qz
title: Stopped session retained a completed final phase
kind: bug
status: closed
priority: 3
version: 2
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-23-overnight-cartography-run.md
delegate: codex-root
labels: []
dependencies: []
parent_id: is-01m0vr7g27g67p699aepcdksxd
created_at: 2026-08-25T10:58:11.314Z
updated_at: 2026-08-25T11:00:40.431Z
closed_at: 2026-08-25T11:00:40.430Z
close_reason: "Fixed in pushed terminal checkpoint eb1473a: phase 15 and session-010 are both stopped; packing-ledger check passes."
resolution: null
duplicate_of: null
---
The first session-010 terminal update set the session status to stopped but left phase 15 completed. The ledger requires terminal session and final phase statuses to agree. Change only phase 15 to stopped and rerender.
