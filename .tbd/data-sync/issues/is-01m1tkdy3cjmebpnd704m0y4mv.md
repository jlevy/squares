---
type: is
id: is-01m1tkdy3cjmebpnd704m0y4mv
title: "Minimal verifier: the cross-check's cell midpoint is not shown to be a feasible centre (F9c)"
kind: task
status: closed
priority: 3
version: 3
labels:
  - review-gpt6
dependencies: []
parent_id: is-01m1tkdspk8c3n71xsc2e2t4g7
created_at: 2026-09-06T05:35:31.947Z
updated_at: 2026-09-06T06:21:09.324Z
closed_at: 2026-09-06T06:21:09.324Z
close_reason: "Implemented in 41fb401a on claude/pdf-paper-small-fixes (PR #92); reviewed by the coordinator; CI green"
resolution: null
duplicate_of: null
---
Finding 9c, reported by the review and not re-derived in triage (the word 'midpoint' does not appear in thirdparty/verify.py; locate the direct-mass cross-check first). The reviewer reports the cross-check evaluates a cell's constant mass at its midpoint without proving the midpoint lies in the feasible centre domain; a cell can intersect the domain while its midpoint is outside. Not an acceptance bug (the intersection test decides), but a weaker witness than a point constructed inside the intersection. Confirm, then either construct such a point or document the weaker witness.
