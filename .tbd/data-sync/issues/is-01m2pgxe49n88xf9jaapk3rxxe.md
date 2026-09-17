---
type: is
id: is-01m2pgxe49n88xf9jaapk3rxxe
title: "Close PR #185 as superseded once PR #188 merges"
kind: task
status: open
priority: 2
version: 4
spec_path: docs/project/specs/active/plan-2026-09-06-validation-efficiency-and-checkpoints.md
labels:
  - ci
  - pr
dependencies: []
parent_id: is-01m2m5zjmj7dsycs1x6yxwcwwt
created_at: 2026-09-17T01:50:18.246Z
updated_at: 2026-09-17T06:35:49.466Z
---
PR #188's description says it replaces the conflicting topology branches in #185 (claude/ci-validation-shard, still OPEN and CONFLICTING) and #186 (closed). After #188 merges, confirm from the merged tree that every #185 contribution is carried or deliberately superseded, close #185 with a comment linking the merge, and move think-t7zm (the lane bead that names #185's branch) to its terminal state.

## Notes

2026-09-16 audit of #185 and #186 against #188 da2259fb: every #185 contribution is carried, deliberately changed (post-collection --suite-a/--suite-b instead of --shard K/N; hosted records re-measured), or fixed (think-ysy5, think-e5os, think-iwxt), except concurrent exact verification, now tracked separately as a W5 task. #186 is fully carried; its wall check now runs inside packing-required and pages-required. Draft closing comment: Superseded by #188, which rebuilds this topology on current main and carries the fixture cuts, recorded-cost sharding (behind --suite-a/--suite-b), the standalone typecheck runner, browser-floor liveness on frontend, the Rust engine cache repair and exact-tree reuse, plus fixes for this PR's review findings (think-ysy5, think-e5os, think-iwxt). Concurrent exact verification was not carried and is tracked for a follow-up port.


2026-09-17 owner request: make PR #185 ready to merge and sequence it with #188 rather than only closing it. Plan: merge #188 first; rebuild #185 as a stacked follow-up on codex/ci-topology-reconcile carrying only the work #188 lacks (think-5hfr's concurrent exact-verification subprocesses and anything else the compatibility analysis finds unique), base codex/ci-topology-reconcile until #188 merges, then main. Close as superseded only if nothing unique remains. Old head f462ccbb will be backed up before the branch is updated.


2026-09-17 superseded by the owner's request to make #185 mergeable: #185 is rebuilt as a stacked follow-up on #188 (branch claude/ci-validation-shard-rebuild, commits 485f9236 concurrent exact verification for think-5hfr and c9596d89 guard tests); everything else in #185 was classified present in or superseded by #188 (attic/pr185/compat.txt in the consolidate-stack worktree). Sequence: #188, then #185 (auto-retargets to main when #188's branch is deleted on merge), then #190 (conflicts with #188 only in SYNOPSIS generated counts), then the workbench PRs. Close this bead when #185 merges.
