---
type: is
id: is-01m2m6z3v57p16x0y2s3npk4cr
title: "PR #181 addendum A1: make KaTeX driver failures legible"
kind: bug
status: closed
priority: 2
version: 3
labels: []
dependencies: []
parent_id: is-01m2m6xx00sabcq5zqkrneavd0
created_at: 2026-09-16T04:17:58.629Z
updated_at: 2026-09-16T06:53:37.622Z
closed_at: 2026-09-16T06:53:37.618Z
close_reason: "Completed at PR #181 head 7f990cbb: check_katex rejects a missing driver explicitly, preserves driver stderr/exit status, and the negative failure-path tests pass."
resolution: null
duplicate_of: null
---
check_katex.py must reject a missing Node driver path explicitly and include captured stderr for module-resolution, ESM/CJS, syntax, and process failures. Add negative tests for the widened path-based failure class.
