---
type: is
id: is-01m0y2ysmar7tr0efzanbsmhtg
title: Repair merge-reintroduced synopsis result drift
kind: bug
status: closed
priority: 1
version: 2
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-23-overnight-cartography-run.md
labels:
  - documentation
  - defect
dependencies: []
parent_id: is-01m0y16d21crjnn9tqa0120way
created_at: 2026-08-26T03:48:54.537Z
updated_at: 2026-08-26T04:03:59.275Z
closed_at: 2026-08-26T04:03:59.259Z
close_reason: Recorded D-337, reconciled H-023 and campaign totals with the ledger, restored H-024's unresolved boundary, added two regression helpers and controls, and passed the full 32-area packing validation checkpoint (126 tests, 67 negative controls, 292.22s).
resolution: null
duplicate_of: null
---
Merging upstream tutorial/provenance work reintroduced three stale statements into the living packing synopsis: H-023 showed 6 rounds instead of the ledger's 11; the experiment section stated 39 rounds/933 agent-minutes/28.3 wall-minutes instead of 44/1061/30.7; and exp-012 was said to refute H-024 although its canonical verdict and hypothesis remain unresolved. Reconcile all three with the ledger and experiment artifacts, retain historical checkpoint counts untouched, register the defect, regenerate views, and pass synopsis/document/full validation.
