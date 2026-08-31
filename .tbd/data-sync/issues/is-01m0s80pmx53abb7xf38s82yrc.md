---
type: is
id: is-01m0s80pmx53abb7xf38s82yrc
title: "PR #17 review E9: targeted gate must avoid unrelated engine builds"
kind: bug
status: closed
priority: 1
version: 2
labels:
  - packing
  - focus-infrastructure
dependencies: []
parent_id: is-01m0rwwt8912eq5f3507d581e1
created_at: 2026-08-24T06:41:07.741Z
updated_at: 2026-08-24T07:13:45.022Z
closed_at: 2026-08-24T07:13:45.001Z
close_reason: "Merged in PR #18 at b3545d0: targeted gates now avoid unrelated Rust builds and expose skips; D-122 and command-level regressions record the fix."
resolution: null
duplicate_of: null
---
The #17 engineering review's stacked implementation makes --only build sqsearch even for a non-engine check and can print a partial-pass line before surfacing a build skip. Select build dependencies from the chosen steps, report every skip before success, and verify a non-engine --only command does not build.
