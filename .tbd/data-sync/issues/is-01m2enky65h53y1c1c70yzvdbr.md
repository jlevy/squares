---
type: is
id: is-01m2enky65h53y1c1c70yzvdbr
title: Diagnose macOS sandbox ps denial and nested xdist timeouts under local push gates
kind: bug
status: open
priority: 3
version: 3
spec_path: development.md
labels:
  - validation
  - macos
dependencies: []
created_at: 2026-09-14T00:38:34.436Z
updated_at: 2026-09-14T02:26:21.350Z
---
Across the exact PR156 and BC303 stack gates, isolated macOS local runs intermittently denied ps or process-group probes (PermissionError on /bin/ps, EPERM at os.killpg(...,0)) or timed out under concurrent xdist load. Exact reruns with suitable process access and hosted required CI passed. Reproduce the environmental boundary in the maintained validation lifecycle tests, decide whether a narrow test/runner change is warranted, and preserve strict process cleanup assertions; do not change scientific criteria or call a failing exact head green. This is a portability follow-up, not a blocker to already green hosted PRs.

## Notes

2026-09-14: the EPERM-at-os.killpg part of this bead is not sandbox-only; it is a real macOS race in the packet reapers, now split to its own bug under think-j007 with a fix on claude/n11-stack-ci-stabilization (1f43e5c6). This bead keeps the /bin/ps PermissionError under sandboxing and the nested pytest -n 2 hard 30 s timeout under load.
