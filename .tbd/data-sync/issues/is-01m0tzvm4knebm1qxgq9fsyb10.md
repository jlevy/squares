---
type: is
id: is-01m0tzvm4knebm1qxgq9fsyb10
title: "PR 24 review R12: keep generated workflow orientation compact"
kind: bug
status: closed
priority: 3
version: 3
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-23-overnight-cartography-run.md
labels:
  - packing
  - pr24-review
dependencies: []
parent_id: is-01m0tz8s4yps8zgqwk8cng9qnx
created_at: 2026-08-24T22:57:01.587Z
updated_at: 2026-08-24T23:24:53.019Z
closed_at: 2026-08-24T23:24:53.018Z
close_reason: "Fixed in 0775c20: ledger shows provenance, entry/current workflow, and phase count; full history remains in the linked session."
resolution: null
duplicate_of: null
---
PR #24 ledger prints each session's full phase chain in the top orientation table, producing unbounded-width rows. Summarize entry/current workflow and phase count there; retain the complete history in the linked session artifact.
