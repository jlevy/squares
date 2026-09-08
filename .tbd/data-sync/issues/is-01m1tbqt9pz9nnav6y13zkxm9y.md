---
type: is
id: is-01m1tbqt9pz9nnav6y13zkxm9y
title: Fix invalid bulk tbd launch command in agenda 024
kind: bug
status: closed
priority: 0
version: 2
labels:
  - launch-preflight
dependencies: []
parent_id: is-01m1t2x1q9xxjz7r8s940y2y11
created_at: 2026-09-06T03:21:07.125Z
updated_at: 2026-09-06T03:22:03.456Z
closed_at: 2026-09-06T03:22:03.455Z
close_reason: Agenda 024 now uses supported atomic tbd start for the launch bead and six cells; records validation passed, commit 04e6a2ce was pushed, and the exact seven-bead claim then succeeded before any scientific process began.
resolution: null
duplicate_of: null
---
The T+0 runbook prescribes tbd update with --status across seven beads, but current tbd rejects status changes in bulk. Replace it with the supported atomic tbd start command, verify the documented graph transition, and close this bug before any scientific process starts.
