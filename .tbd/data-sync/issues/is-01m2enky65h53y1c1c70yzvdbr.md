---
type: is
id: is-01m2enky65h53y1c1c70yzvdbr
title: Diagnose macOS sandbox process-test portability under local push gates
kind: bug
status: open
priority: 3
version: 1
spec_path: development.md
labels:
  - validation
  - macos
dependencies: []
created_at: 2026-09-14T00:38:34.436Z
updated_at: 2026-09-14T00:38:34.436Z
---
Across the exact PR156 and BC303 stack gates, isolated macOS local runs intermittently denied ps or process-group probes (PermissionError on /bin/ps, EPERM at os.killpg(...,0)) or timed out under concurrent xdist load. Exact reruns with suitable process access and hosted required CI passed. Reproduce the environmental boundary in the maintained validation lifecycle tests, decide whether a narrow test/runner change is warranted, and preserve strict process cleanup assertions; do not change scientific criteria or call a failing exact head green. This is a portability follow-up, not a blocker to already green hosted PRs.
