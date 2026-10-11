---
type: is
id: is-01m18qchbayb5k4a6gcb5782q5
title: "agenda-008 block 2: retain per-sample keys for exp-015 so the n=4 labelled control can score"
kind: task
status: closed
priority: 0
version: 2
labels: []
dependencies: []
created_at: 2026-08-30T06:58:20.650Z
updated_at: 2026-10-06T08:30:38.390Z
closed_at: 2026-10-06T08:30:38.389Z
close_reason: |
  Done (bead review 2026-10-06, origin/main eb43ffe9a): BC-082 complete in agenda-008 (completed): 1c5a3d0f0 retains exp-015's n=4 per-sample keys and scores the relation in devtools/check_identity_relation.py
resolution: null
duplicate_of: null
---
think-byc6's work. Emit geometric_key and contact_certificate for exp-015's 24 labelled states in exp-014's shape, and extend check_identity_relation so 'geometric + contact' stops reading undecidable on the one control that most directly tests the relation the atlas uses today.
