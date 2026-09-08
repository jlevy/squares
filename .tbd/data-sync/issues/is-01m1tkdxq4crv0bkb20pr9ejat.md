---
type: is
id: is-01m1tkdxq4crv0bkb20pr9ejat
title: "verify_claim.py: short-circuit after a failed condition and bound the event grid (F9b)"
kind: task
status: closed
priority: 3
version: 3
labels:
  - review-gpt6
dependencies: []
parent_id: is-01m1tkdspk8c3n71xsc2e2t4g7
created_at: 2026-09-06T05:35:31.555Z
updated_at: 2026-09-06T06:21:09.318Z
closed_at: 2026-09-06T06:21:09.318Z
close_reason: "Implemented in 41fb401a on claude/pdf-paper-small-fixes (PR #92); reviewed by the coordinator; CI green"
resolution: null
duplicate_of: null
---
Finding 9b, partly confirmed: verify_claim.py prints every condition (line ~203-208) and so continues into the quadratic event-grid sweep after Conditions 1-4 have already failed, and it lacks the size and schema limits the retention loader applies. Harmless for the two hashed certificates; matters for malformed or oversized inputs fed to the embedded verifier. Decide: keep 'one line per condition' but skip the sweep once an earlier condition fails, and add a documented atom/direction ceiling. Low severity.
