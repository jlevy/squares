---
type: is
id: is-01m0tbtgpb92e81ndvw4xm9be6
title: Review and absorb stacked PR 20 into the basin campaign branch
kind: task
status: open
priority: 0
version: 2
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-23-overnight-cartography-run.md
labels:
  - packing
  - review
dependencies: []
parent_id: is-01m0t3n7z9fj0p7wwt1kn4nzqk
created_at: 2026-08-24T17:06:53.762Z
updated_at: 2026-08-24T17:07:28.354Z
---
Carefully review PR #20 (claude/square-packing-concepts-ifkyzr), which is stacked on codex/packing-post-merge-research-runs. Inspect every commit and changed claim against current experiment, defect, source, and tooling state; inspect all GitHub comment/review/check surfaces; reconcile its closed beads; identify stale statements caused by later n=3/n=4 BasinEvent/v3 work; rebase or merge cleanly onto the current branch; retain only sound documentation; run affected checks plus the normal gate; commit/push the integrated result; and close or otherwise disposition PR #20 without losing history. Do not overwrite the current uncommitted exp-024 checkpoint; integrate only from a clean checkpoint.

## Notes

2026-08-24 PR #20 is draft/open, head b320559b, 5 documentation files, stacked on this branch. Integration waits for the current exp-024/agenda checkpoint to be committed and pushed. A read-only parallel review is active; root will independently review all claims and current-status drift before merge/rebase.
