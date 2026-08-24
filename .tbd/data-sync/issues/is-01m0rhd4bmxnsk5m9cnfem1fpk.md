---
type: is
id: is-01m0rhd4bmxnsk5m9cnfem1fpk
title: "D074: provenance regression checked receipt parsing but not artifact mapping"
kind: bug
status: closed
priority: 1
version: 2
spec_path: explorations/packing/docs/project/reviews/review-2026-08-23-square-packing-program-and-pr14.md
labels:
  - packing
  - review
  - focus-process
  - testing
dependencies: []
parent_id: is-01m0r7q3zk8x6cg4e30d149698
created_at: 2026-08-24T00:05:57.747Z
updated_at: 2026-08-24T00:12:40.120Z
closed_at: 2026-08-24T00:12:40.108Z
close_reason: Fixed by centralizing the five execution-owned artifact fields, adding a direct preflight assertion and a mutation control; final 126-second gate passed with 30/30 controls and 74 reconciled defects.
resolution: null
duplicate_of: null
---
The new D-070 defect record said runner preflight proved that record preserved execution provenance, but the check only parsed the JSONL receipt and never exercised the mapping into subject.engine_commit, method.commit, verdict.commit, method.dirty, or effort.wall_seconds. Centralize that mapping, exercise it in preflight, add a mutation control, and reconcile the review and defect log before committing.
