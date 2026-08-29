---
type: is
id: is-01m17m53v9d8tgmmy7wqvq1d4s
title: Move the exact grid replay out of the schema step
kind: task
status: open
priority: 0
version: 1
spec_path: docs/project/specs/active/plan-2026-08-29-gate-validation-speed.md
labels: []
dependencies: []
created_at: 2026-08-29T20:42:37.289Z
updated_at: 2026-08-29T20:42:37.289Z
---
Phase 1. verify_grid costs 3.58s inside soft-schema validation. Nothing about the check changes, only which step reports it.
