---
type: is
id: is-01m0w5qa2g87nyxtp01hej80k8
title: Correct invalid session delegation timing-quality enum
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
created_at: 2026-08-25T09:58:46.096Z
updated_at: 2026-08-25T10:01:32.399Z
closed_at: 2026-08-25T10:01:32.399Z
close_reason: "D-269 is recorded and fixed before commit: the formatter delegation now uses the enforced platform_measured timing-quality value, and packing-ledger check plus the complete 31-step local gate pass."
resolution: null
duplicate_of: null
---
The first phase-11 session update used elapsed_quality=measured_tool_wall, but the enforced schema permits platform_measured, operator_reported_approximate, unavailable, or null. packing-ledger check caught it before commit. Change the value to platform_measured, record the defect and checker receipt, and keep all aggregates and mutation anchors synchronized.
