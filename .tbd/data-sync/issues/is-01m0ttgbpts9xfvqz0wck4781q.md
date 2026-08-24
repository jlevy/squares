---
type: is
id: is-01m0ttgbpts9xfvqz0wck4781q
title: Audit Bash and migrate application logic to Python
kind: task
status: closed
priority: 2
version: 2
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-24-packing-engineering-maturity.md
labels:
  - engineering-maturity
  - python
dependencies: []
parent_id: is-01m0rrgqj3esjc4jx1fr3qy1ht
created_at: 2026-08-24T21:23:29.625Z
updated_at: 2026-08-24T22:55:28.560Z
closed_at: 2026-08-24T22:55:28.560Z
close_reason: Installed descriptive packing-validate, packing-campaign, and packing-ledger commands; replaced test.sh and all application-like shell entry points with typed Python; help and failure contracts pass and the complete gate is green.
resolution: null
duplicate_of: null
---
Classify every remaining shell script by complexity and failure cost. Move scripts that own structured state, parsing, parallel orchestration, timeouts, process groups, nontrivial branching, or reusable behavior into typed Python with focused tests and actionable errors. Retain only short transparent launchers or direct tool glue whose behavior is obvious on one screen. Do not translate tiny shell into a framework for uniformity. Acceptance: each shell file has a recorded retain or migrate decision, migrated callers and docs are updated together, and focused plus full validation cover the replacements.
