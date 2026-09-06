---
type: is
id: is-01m1w1x2hxn7was5jgcheqeyh9
title: "PR #98 review R11: receipts embed absolute macOS home/worktree paths"
kind: bug
status: open
priority: 2
version: 2
labels: []
dependencies: []
parent_id: is-01m1w1w81t7vmr0gem6d91wg8b
created_at: 2026-09-06T19:07:42.525Z
updated_at: 2026-09-06T19:13:08.676Z
---
runs/receipts.jsonl and checkpoint tarballs carry /Users/levy/... paths as provenance. Evidence must not be rewritten. Consider repository-relative source_hashes keys in validation_timing.py going forward.
