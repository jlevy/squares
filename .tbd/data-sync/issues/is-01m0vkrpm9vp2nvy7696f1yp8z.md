---
type: is
id: is-01m0vkrpm9vp2nvy7696f1yp8z
title: Make the synopsis checker reconcile multiword hypothesis statuses
kind: bug
status: closed
priority: 1
version: 2
labels:
  - packing
  - defect
  - focus-correctness
dependencies: []
created_at: 2026-08-25T04:44:57.352Z
updated_at: 2026-08-25T04:56:30.017Z
closed_at: 2026-08-25T04:56:30.017Z
close_reason: "Implemented and pushed in PR #27: the synopsis now has a maintainable readiness dashboard and refresh contract; D-226 through D-229 are recorded and fixed; status parsing, owner-link reconciliation, and 57 negative controls pass."
resolution: null
duplicate_of: null
---
check_synopsis.py parses ledger hypothesis status with a single-token regex, silently omitting every open-question row. Parse the full status cell, add the newly covered aggregate check, and record the checker defect.
