---
type: is
id: is-01m0sny9yg5f5w6kfmtp1nsv5h
title: Correct misapplied defect-status edit during H-032 integration
kind: bug
status: closed
priority: 2
version: 2
spec_path: explorations/packing/defects.yaml
labels:
  - packing
  - focus-process
dependencies: []
parent_id: is-01m0shdh4arvmv3vyfyfpnqfpx
created_at: 2026-08-24T10:44:29.263Z
updated_at: 2026-08-24T10:48:20.043Z
closed_at: 2026-08-24T10:48:20.041Z
close_reason: D-145 is fixed. D-039 is restored to outstanding and D-140 marked fixed. validate_schemas now rejects any fixed defect whose fix begins with none yet; the exact negative control fires and the full strict/deep gate passes with 145 reconciled records.
resolution: null
duplicate_of: null
---
A broad integration edit changed D-039 from outstanding to fixed while leaving the actually resolved D-140 outstanding. The body of D-039 still said none yet, so the status contradicted its own evidence. Correct both statuses, record the error as D-145, regenerate views, and require schema plus synopsis reconciliation before closing.
