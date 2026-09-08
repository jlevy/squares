---
type: is
id: is-01m2109hrm68xk1gkbtkz23rfg
title: Fix KPress Python CI after cross-browser font coverage
kind: bug
status: closed
priority: 1
version: 2
spec_path: docs/project/specs/active/plan-2026-09-07-math-text-face.md
labels: []
dependencies: []
parent_id: is-01m20v1mq20k9d9p1wg9s5qdsq
created_at: 2026-09-08T17:15:46.320Z
updated_at: 2026-09-08T18:40:08.417Z
closed_at: 2026-09-08T18:40:08.417Z
close_reason: KPress PR61 merged at 20a7d2b after the final browser, JavaScript, lint, distribution and Python3.12/3.13/3.14 CI matrix passed (run34256487179). It adds correct per-family font readiness/hydration, the canonical architecture document, and the optional-browser availability repair.
resolution: null
duplicate_of: null
---
KPress PR61 run34255381364 passes strict browser, lint and distribution jobs but all three Python matrix jobs fail after adding Firefox/WebKit font regressions. Investigate the exact failing logs and preserve strict cross-browser coverage without requiring optional browser binaries in ordinary Python jobs. Runtime345b9eb is frozen and passed actual Squares correctness matrix; change runtime only if evidence requires it.
