---
type: is
id: is-01m2phtqcr35drpbd01xrh0g8q
title: Tree-reuse allowlist includes a step that reads the git graph and tbd
kind: bug
status: open
priority: 3
version: 1
spec_path: docs/project/specs/active/plan-2026-09-06-validation-efficiency-and-checkpoints.md
labels:
  - ci
  - validation
dependencies: []
parent_id: is-01m2m5zjmj7dsycs1x6yxwcwwt
created_at: 2026-09-17T02:06:18.006Z
updated_at: 2026-09-17T02:06:18.006Z
---
At PR #188 da2259fb, TREE_REUSABLE_FAST_STEPS (packing/src/sqpack/cli/validate.py ~4443-4512) includes 'terminal sessions name the gate that certified them' (~4508), whose checker runs git merge-base --is-ancestor and tbd show (packing/devtools/check_session_gate.py ~236-266). The allowlist's own comment says steps that read the git graph or outside state must not be reused. It is likely harmless with merge commits and no tbd in CI, but not under squash or rebase merges. Decide whether to drop it from the allowlist or document why its inputs are tree-determined, with a test.
