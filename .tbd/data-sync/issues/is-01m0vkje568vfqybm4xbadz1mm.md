---
type: is
id: is-01m0vkje568vfqybm4xbadz1mm
title: Fix stale hypothesis-status aggregate in the packing synopsis
kind: bug
status: closed
priority: 1
version: 3
labels:
  - packing
  - defect
  - focus-correctness
dependencies: []
created_at: 2026-08-25T04:41:32.068Z
updated_at: 2026-08-25T04:56:30.002Z
closed_at: 2026-08-25T04:56:30.002Z
close_reason: "Implemented and pushed in PR #27: the synopsis now has a maintainable readiness dashboard and refresh contract; D-226 through D-229 are recorded and fixed; status parsing, owner-link reconciliation, and 57 negative controls pass."
resolution: null
duplicate_of: null
---
SYNOPSIS.md says one hypothesis is confirmed and four are refuted, while the generated ledger derives three confirmed and six refuted. Correct the summary, record the defect in defects.yaml, and extend check_synopsis.py so status aggregates cannot drift behind the per-hypothesis table again.
