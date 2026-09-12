---
type: is
id: is-01m2asa131hqk3kagma2t2t3ab
title: Name exact interval and dilation directions in partial BC329 receipts
kind: task
status: in_progress
priority: 2
version: 4
spec_path: docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md
delegate: Sol high isolated implementation; root integration
labels:
  - n11
  - tooling
dependencies:
  - type: blocks
    target: is-01m260z2959dmcmn61pn2z7jsk
  - type: blocks
    target: is-01m2aj7q4y8raaw35s0jq3ty2y
parent_id: is-01m26c1jahzgfckegz7fp9wcq7
created_at: 2026-09-12T12:26:06.304Z
updated_at: 2026-09-12T13:51:10.159Z
---
Partial interval and dilation receipts currently retain a count and last row while the filesystem may contain an unpublished sparse tail. They publish no partial scientific summary and cannot produce acceptance, so this is auditability and recovery hardening. Before the BC329 scientific target, record canonical completed-direction labels for each published checkpoint and make readback distinguish the receipt-bound set from valid unpublished tail rows, mirroring raw and exact handling.

## Notes

Implemented in isolation at ecce6dba on codex/think-yiay-partial-direction-sets. Partial interval and dilation receipts now name exact canonical completed-direction sets and readback separates their published set from valid unpublished sparse tails. Target-free integrated controls report 171 passed/3 platform skips; Ruff, BasedPyright, formatting, and diff checks pass. A merge-tree simulation with preflight commit c516a592 found no textual conflicts, but combined receipt validation/readback still needs semantic review before integration. No BC329 target ran.
