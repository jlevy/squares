---
type: is
id: is-01m0tzvk2jm8ky96ge868pnqkb
title: "PR 24 review R9: establish one machine workflow authority"
kind: bug
status: in_progress
priority: 2
version: 2
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-23-overnight-cartography-run.md
labels:
  - packing
  - pr24-review
dependencies: []
parent_id: is-01m0tz8s4yps8zgqwk8cng9qnx
created_at: 2026-08-24T22:57:00.497Z
updated_at: 2026-08-24T22:58:08.500Z
---
PR #24 duplicates workflow enums/order across schema fields, check_readme.py, ledger.py, README, and SYNOPSIS; entry_workflow also duplicates the first phase. Derive machine vocabulary/order and entry from one canonical schema definition while retaining cross-document drift checks.
