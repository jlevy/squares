---
type: is
id: is-01m2b2etdnh14vgy3h8x79y5dj
title: Reject BC329 output paths inside Git administrative storage
kind: bug
status: in_progress
priority: 1
version: 6
spec_path: docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md
delegate: Sol xhigh repair; source-distinct rereview; root integration
labels:
  - n11
  - tooling
dependencies:
  - type: blocks
    target: is-01m2as8hsq3d7dxy1z185zxeah
parent_id: is-01m2as8hsq3d7dxy1z185zxeah
created_at: 2026-09-12T15:06:00.498Z
updated_at: 2026-09-12T15:25:35.474Z
---
The source-distinct repair review reproduced that prepare_output_dir and source_manifest accept an output beneath .git/refs/heads. Creating result.json there makes Git interpret a directory as a ref; git show-ref then fails with status 128 while source_manifest still accepts it because Git status omits administrative files. Before mutation, resolve and reject the worktree Git directory, common Git directory, and descendants, including linked-worktree .git files, separate Git directories, symlinks, and aliases. Retain a .git/refs control asserting no directory or receipt is created. No BC329 target may run until this closes.

## Notes

Repair implemented in d6bbe20172d4048a9f156b1c3c4fcfe8f1b64014. prepare_output_dir resolves the checkout Git directory and common Git directory and rejects either directory or any descendant before mkdir. Maintained real-Git controls cover a normal checkout, linked-worktree administrative directory, common directory, and separate external Git directory, and assert no output was created. Leave open for source-distinct re-review.
