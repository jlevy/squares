---
type: is
id: is-01m1w1x2hxn7was5jgcheqeyh9
title: "PR #98 review R11: receipts embed absolute macOS home/worktree paths"
kind: bug
status: open
priority: 2
version: 3
spec_path: docs/project/specs/active/plan-2026-09-06-validation-efficiency-and-checkpoints.md
labels: []
dependencies: []
parent_id: is-01m1vrrktbrd2scnaqfe40eby4
created_at: 2026-09-06T19:07:42.525Z
updated_at: 2026-09-06T19:49:54.589Z
---
runs/receipts.jsonl and checkpoint tarballs carry /Users/levy/... paths as provenance. Evidence must not be rewritten. Consider repository-relative source_hashes keys in validation_timing.py going forward.

## Notes

Deferred follow-up remains open exactly as the PR98 review disposition requires. Reparented from closed review task think-r9br to active W5 epic think-rwte after PR101 CI identified the open-child/closed-parent invariant failure. Original receipts remain immutable; this is only a tracking repair, not resolution of path portability.
