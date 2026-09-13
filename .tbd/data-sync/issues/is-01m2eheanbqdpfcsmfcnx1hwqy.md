---
type: is
id: is-01m2eheanbqdpfcsmfcnx1hwqy
title: Refresh PR125–PR155–PR160 onto current main
kind: task
status: open
priority: 1
version: 1
spec_path: docs/project/specs/active/plan-2026-09-11-workbench-from-spike-to-product.md
labels:
  - workbench-stack
dependencies: []
parent_id: is-01m28p7h39vcykq99dgjmvwv98
created_at: 2026-09-13T23:25:36.296Z
updated_at: 2026-09-13T23:25:36.296Z
---
PR #125 is behind current main and GitHub reports mergeable_state=dirty. Merge current main into #125, resolve the campaign ledger conflict with both histories intact, propagate the resulting parent heads into #155 and #160, run branch-appropriate validation, push all three PR branches, and record final heads and CI. Preserve clean worktrees with no local-only commits; cleanup proceeds only after pushed branch state is verified.
