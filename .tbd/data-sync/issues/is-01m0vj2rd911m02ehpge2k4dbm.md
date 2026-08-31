---
type: is
id: is-01m0vj2rd911m02ehpge2k4dbm
title: "PR #23 review S1: Preserve git command failures in the campaign runner"
kind: task
status: closed
priority: 3
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
created_at: 2026-08-25T04:15:29.704Z
updated_at: 2026-08-25T04:44:42.085Z
started_at: 2026-08-25T04:16:15.572Z
closed_at: 2026-08-25T04:44:42.084Z
close_reason: "Completed in 69e65eb: runner.git checks exit status and raises an actionable refusal containing the failed command and Git diagnostic."
resolution: null
duplicate_of: null
---
PR 23 review suggestion S1. File: explorations/packing/src/sqpack/campaign/runner.py lines 137-140. Decide whether the git helper should raise or return structured status instead of turning every failure into empty output.
