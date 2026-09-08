---
type: is
id: is-01m2109hrm68xk1gkbtkz23rfg
title: Fix KPress Python CI after cross-browser font coverage
kind: bug
status: open
priority: 1
version: 1
spec_path: docs/project/specs/active/plan-2026-09-07-math-text-face.md
labels: []
dependencies: []
parent_id: is-01m20v1mq20k9d9p1wg9s5qdsq
created_at: 2026-09-08T17:15:46.320Z
updated_at: 2026-09-08T17:15:46.320Z
---
KPress PR61 run34255381364 passes strict browser, lint and distribution jobs but all three Python matrix jobs fail after adding Firefox/WebKit font regressions. Investigate the exact failing logs and preserve strict cross-browser coverage without requiring optional browser binaries in ordinary Python jobs. Runtime345b9eb is frozen and passed actual Squares correctness matrix; change runtime only if evidence requires it.
