---
type: is
id: is-01m0rbwvahqzsexrv6kwgv35g0
title: "Attic: crash/concurrency rehearsal for abandoned isolation prototype"
kind: bug
status: closed
priority: 1
version: 5
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-23-overnight-cartography-run.md
labels:
  - focus-efficiency
dependencies: []
parent_id: is-01m0r7q50gw0wepeaj1dzb7g3r
created_at: 2026-08-23T22:29:41.328Z
updated_at: 2026-08-23T23:23:41.432Z
closed_at: 2026-08-23T23:23:41.432Z
close_reason: "Canceled after the scope reset: this finding belongs to the stashed hostile-isolation prototype, not the stable branch. The prototype remains recoverable in stash@{0}; no claim is made that its fixes landed. Reuse only narrowly useful timeout or crash-recovery patterns if a measured cooperative-workflow need justifies them."
resolution: canceled
duplicate_of: null
---
The current crash selftest bypasses the standalone lease and checker subprocess, while the atomic control tests an already-held marker rather than simultaneous acquisition. Replace these with end-to-end process death and exactly-one-winner rehearsals.

## Notes

Canceled after the scope reset: this finding belongs to the stashed hostile-isolation prototype, not the stable branch. The prototype remains recoverable in stash@{0}; no claim is made that its fixes landed. Reuse only narrowly useful timeout or crash-recovery patterns if a measured cooperative-workflow need justifies them.
