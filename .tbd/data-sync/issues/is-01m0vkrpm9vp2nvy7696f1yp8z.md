---
type: is
id: is-01m0vkrpm9vp2nvy7696f1yp8z
title: Make the synopsis checker reconcile multiword hypothesis statuses
kind: bug
status: open
priority: 1
version: 1
labels:
  - packing
  - defect
  - focus-correctness
dependencies: []
created_at: 2026-08-25T04:44:57.352Z
updated_at: 2026-08-25T04:44:57.352Z
---
check_synopsis.py parses ledger hypothesis status with a single-token regex, silently omitting every open-question row. Parse the full status cell, add the newly covered aggregate check, and record the checker defect.
