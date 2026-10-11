---
type: is
id: is-01m3wvq4vs04p774e2atfzxea6
title: "Housekeeping after 1 October: worktrees, merged branches, scratch builds, orphaned processes"
kind: task
status: open
priority: 3
version: 2
spec_path: docs/project/specs/active/plan-2026-09-29-github-pages-overview.md
labels: []
dependencies: []
parent_id: is-01m3p52z585a2zb9jmy19b0r96
created_at: 2026-10-01T23:10:14.903Z
updated_at: 2026-10-02T01:04:40.239Z
---
The external drive is 96% full. After the open PRs land: remove merged agent worktrees under /Volumes/spud-ext1/agent-scratch/worktrees (keep those with open branches), delete merged remote branches (claude/site-polish-*, claude/prose-*, claude/result-kinds, claude/site-coherence, claude/paper-*, claude/awaiting-replay, claude/register-rung-residue, claude/release-assets-on-demand, and the per-lane branches), remove the squares-site-* preview builds except the one being served on localhost:8000, and check for orphaned playwright and multiprocessing processes from stopped agents (several were found idle or spinning for four to five hours on 1 October). Nothing is deleted without looking at it first.

## Notes

Added 2026-10-02 01:30 UTC. Worktrees under /Volumes/spud-ext1/agent-scratch/worktrees/ whose branches are merged and can be removed: audit-main (detached at 07f014386; was claude/atlas-triangle, #286), ci-runner-variance (#287), overview-papers (claude/v0.5.0, #291; also held claude/ladder-heads, #288), overview-page-impl (#285), overview-intro (#277), overview-fixes, overview-rows (#267), math-everywhere-phase3, n11-paper-261, n11-paper-261-review, epistemics-ladder, epistemics-ladder-impl, prose-ceremony. In use: overview-result-pop (claude/overview-structure, think-f1tu). Not this session's: result-import-run (#292), result-intake (#290). Scratch to clear: /Volumes/spud-ext1/agent-scratch/triangle-tmp, papers-one-structure-shots, int-tmp; /Users/levy/wrk/github/squares/attic/triangle-preview/. Merged remote branches to delete: claude/atlas-triangle, claude/ladder-heads, claude/papers-one-structure, claude/v0.5.0, claude/ci-shard-balance, claude/paper-slugs, claude/release-assets-on-demand and the earlier site-polish branches. The drive was 96 percent full.
