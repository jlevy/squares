---
type: is
id: is-01m0vj2htars5bk2m87zn1396m
title: "PR #23 review R4: Make stale validation marker failures recoverable"
kind: bug
status: closed
priority: 2
version: 3
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-24-packing-engineering-maturity.md
delegate: codex@spud10
labels:
  - engineering-maturity
  - pr-review
  - pr-23
dependencies: []
parent_id: is-01m0vj13yefxcxhhew81ewfpvq
hold: null
hold_until: null
created_at: 2026-08-25T04:15:22.953Z
updated_at: 2026-08-25T04:44:36.065Z
started_at: 2026-08-25T04:16:15.461Z
closed_at: 2026-08-25T04:44:36.064Z
close_reason: "Completed in 69e65eb: a stale validation marker now explains both waiting and safe crash recovery, with a focused failure-path test."
resolution: null
duplicate_of: null
---
PR 23 review R4. File: explorations/packing/src/sqpack/cli/validate.py lines 702-712. Give an actionable stale .gate-running remedy and add an explicit owner or staleness contract if warranted.
