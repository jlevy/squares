---
type: is
id: is-01m4evfrfyetfc9yw16yatz6ay
title: "n17 PR404 B3: isolate source enumeration from foreign Git environment"
kind: bug
status: open
priority: 2
version: 1
spec_path: docs/project/reviews/review-2026-10-06-n17-w3-consolidation.md
labels:
  - n-17
dependencies: []
parent_id: is-01m4eq9mdaejkedd1b09qqn09p
created_at: 2026-10-08T22:52:32.637Z
updated_at: 2026-10-08T22:52:32.637Z
---
PR404 full review B3, pinned head 1d1691bf5e6e1115ad1597b5f72bbd12ad9b0b88.

index_tree sanitizes GIT_* variables for git init/add, but its source enumeration
uses tracked_files(REPO, '.') with the inherited environment. A tiny foreign
GIT_INDEX_FILE fixture makes the worker index untracked-output.json and omit the
source repository's tracked-source.py, defeating the source-tracking contract.

Pass an explicit sanitized environment through the shared tracked_files helper
to both its repository check and ls-files call; retain default caller behavior.
Do not mutate the process environment, since worker construction is parallel.
Test foreign index/repository variables, mutated worker bytes, pruned paths and
preservation of the original source index. No snapshot cap or pruning change.

Evidence: attic/n17-merge-readiness-20261008/pr404-foreign-index-reproduction.json
and reproduce_snapshot_foreign_index.py.
