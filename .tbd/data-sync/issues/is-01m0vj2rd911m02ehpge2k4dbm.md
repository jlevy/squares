---
type: is
id: is-01m0vj2rd911m02ehpge2k4dbm
title: "PR #23 review S1: Preserve git command failures in the campaign runner"
kind: task
status: in_progress
priority: 3
version: 2
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
updated_at: 2026-08-25T04:16:15.572Z
started_at: 2026-08-25T04:16:15.572Z
---
PR 23 review suggestion S1. File: explorations/packing/src/sqpack/campaign/runner.py lines 137-140. Decide whether the git helper should raise or return structured status instead of turning every failure into empty output.
