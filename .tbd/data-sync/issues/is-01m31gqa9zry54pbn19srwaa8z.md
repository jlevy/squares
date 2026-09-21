---
type: is
id: is-01m31gqa9zry54pbn19srwaa8z
title: check_synopsis docstring item 7 is not implemented; HYPOTHESES is dead
kind: bug
status: open
priority: 3
version: 1
labels: []
dependencies: []
parent_id: is-01m31gn7263sfhfbq8xfabkh3p
created_at: 2026-09-21T08:18:36.476Z
updated_at: 2026-09-21T08:18:36.476Z
---
Found during PR 204 re-review; pre-existing. check_synopsis.py:22 docstring item 7 promises 'the stated hypothesis-artifact count matches the registry directory', but the constant it needs - HYPOTHESES at :58 - appears nowhere else in the 1,180-line file, and check_hypotheses reads only ledger.md (:190). Ruff's zero-findings floor does not flag unused module-level constants. Mitigating: SYNOPSIS no longer states such a count and the directory-to-ledger link is covered transitively (169 files = 169 ledger rows, verified). Stale docstring plus a dead constant, not a soundness hole. Fix: implement it or drop the docstring line and the constant.
