---
type: is
id: is-01m0tas8msq5rqx78fd1cyv3qn
title: Give D-165 a dedicated bead instead of reusing D-132 tracking
kind: bug
status: closed
priority: 1
version: 2
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-23-overnight-cartography-run.md
labels:
  - packing
  - focus-process
dependencies: []
parent_id: is-01m0t3n7z9fj0p7wwt1kn4nzqk
created_at: 2026-08-24T16:48:44.184Z
updated_at: 2026-08-24T16:50:47.992Z
closed_at: 2026-08-24T16:50:47.992Z
close_reason: Fixed in e3357be. D-165 now references dedicated bead think-007f; the unrelated D-132/D-120 tracker think-9qz0 was preserved. D-170 records the mismatch, its consequence, correction, and regression policy; defect views, schema, synopsis, README, and exact defect-count control pass.
resolution: null
duplicate_of: null
---
D-170. defects.yaml pointed D-165 at think-9qz0, whose title, description, notes, and close reason belong to D-132. This made the D-165 closure state impossible to read safely and risked closing an unrelated bead. Acceptance: create a dedicated D-165 bead, update the defect cross-reference, preserve think-9qz0 unchanged, and add a durable logbook entry.
