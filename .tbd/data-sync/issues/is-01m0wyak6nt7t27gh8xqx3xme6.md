---
type: is
id: is-01m0wyak6nt7t27gh8xqx3xme6
title: exp-038/039 were authored to Experiment/v1 after the stacked branch shipped v2
kind: bug
status: closed
priority: 2
version: 2
labels: []
dependencies: []
parent_id: is-01m0wy9s97fwegw5kqrge2p8sy
created_at: 2026-08-25T17:08:43.860Z
updated_at: 2026-08-25T17:49:28.450Z
closed_at: 2026-08-25T17:49:28.450Z
close_reason: Fixed on the PR 33 branch; see review-2026-08-25-tutorial-soundness-iteration-2.md and defects D-320..D-328. Full gate green.
resolution: null
duplicate_of: null
---
Main's exp-038 and exp-039 (sessions 012 era) declared softschema contract Experiment/v1 while the PR 33 branch had already bumped the schema to v2 (assurance/method split). The merged tree failed ledger render until both files were migrated (assurance: verified, method: exact-algebraic). Cross-branch schema divergence: a schema bump on an unmerged branch invisibly forks the contract for concurrent branches. Fixed in the PR 33 merge commit.
