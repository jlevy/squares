---
type: is
id: is-01m0t0t4pshb047zr7j052t1we
title: H-010 integration patch updated D-002 instead of D-151
kind: bug
status: closed
priority: 2
version: 2
spec_path: explorations/packing/defects.yaml
labels: []
dependencies: []
parent_id: is-01m0srsphtekzmgp8vrs05v8n5
created_at: 2026-08-24T13:54:27.154Z
updated_at: 2026-08-24T14:10:25.558Z
closed_at: 2026-08-24T14:10:25.550Z
close_reason: The misapplied D-002 regression was caught before render or commit, D-002 was restored exactly, D-151 was updated under explicit ID context, D-160 records the D-145 recurrence, and defect/synopsis reconciliation passes.
resolution: null
duplicate_of: null
---
A broad apply-patch hunk matched the first 'regression: none' in defects.yaml, attaching the new H-010 root-replay regression to D-002 while leaving D-151 unprotected. Caught immediately by the targeted diff audit before render, commit, or scientific promotion. Acceptance: restore D-002 exactly, update D-151 under explicit ID-scoped context, log as a D-145 recurrence, verify generated defect/synopsis views, and keep the final diff auditable.
