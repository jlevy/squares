---
type: is
id: is-01m0vkje568vfqybm4xbadz1mm
title: Fix stale hypothesis-status aggregate in the packing synopsis
kind: bug
status: in_progress
priority: 1
version: 2
labels:
  - packing
  - defect
  - focus-correctness
dependencies: []
created_at: 2026-08-25T04:41:32.068Z
updated_at: 2026-08-25T04:41:42.238Z
---
SYNOPSIS.md says one hypothesis is confirmed and four are refuted, while the generated ledger derives three confirmed and six refuted. Correct the summary, record the defect in defects.yaml, and extend check_synopsis.py so status aggregates cannot drift behind the per-hypothesis table again.
