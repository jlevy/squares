---
type: is
id: is-01m0rbwtd2mvxhcet6feb55wne
title: "Attic: critical-section audit for abandoned isolation prototype"
kind: bug
status: closed
priority: 0
version: 5
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-23-overnight-cartography-run.md
labels:
  - focus-efficiency
dependencies: []
parent_id: is-01m0r7q50gw0wepeaj1dzb7g3r
created_at: 2026-08-23T22:29:40.385Z
updated_at: 2026-08-23T23:23:41.416Z
closed_at: 2026-08-23T23:23:41.416Z
close_reason: "Canceled after the scope reset: this finding belongs to the stashed hostile-isolation prototype, not the stable branch. The prototype remains recoverable in stash@{0}; no claim is made that its fixes landed. Reuse only narrowly useful timeout or crash-recovery patterns if a measured cooperative-workflow need justifies them."
resolution: canceled
duplicate_of: null
---
One-time marker checks leave check-to-read and check-to-format-or-stage races. Make each gate or runner CLI operation own or narrowly borrow an activity lease for its entire critical section; isolation removes the commit-hook mutation race.

## Notes

Canceled after the scope reset: this finding belongs to the stashed hostile-isolation prototype, not the stable branch. The prototype remains recoverable in stash@{0}; no claim is made that its fixes landed. Reuse only narrowly useful timeout or crash-recovery patterns if a measured cooperative-workflow need justifies them.
