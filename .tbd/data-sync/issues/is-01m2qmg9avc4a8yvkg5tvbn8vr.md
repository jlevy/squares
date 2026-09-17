---
type: is
id: is-01m2qmg9avc4a8yvkg5tvbn8vr
title: check_readme scans the gitignored attic for retired workflow identifiers
kind: bug
status: open
priority: 3
version: 1
labels:
  - ci
dependencies: []
created_at: 2026-09-17T12:12:16.091Z
updated_at: 2026-09-17T12:12:16.091Z
---
Found 2026-09-17 (think-4woh): packing/devtools/check_readme.py skips several directories when scanning for retired workflow identifiers (around lines 121-131) but not attic/, although its own layout list excludes attic (around line 83). A raw tbd dump saved under a worktree's gitignored attic/ failed 'README agrees with the directory' locally in packing-validate --records; CI cannot see attic, so the failure is local-only but blocks the local push tier. Fix: exclude attic/ from that scan as the layout list does, with a regression test.
