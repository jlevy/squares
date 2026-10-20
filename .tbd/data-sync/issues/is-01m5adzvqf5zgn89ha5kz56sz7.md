---
type: is
id: is-01m5adzvqf5zgn89ha5kz56sz7
title: Preserve older managed Squares worktrees for machine handoff
kind: task
status: closed
priority: 1
version: 4
assignee: internal-disk-reclamation
delegate: internal-disk-reclamation
labels: []
dependencies: []
parent_id: is-01m5adjbykkfkammcx2jfymx28
hold: null
hold_until: null
created_at: 2026-10-19T15:55:24.270Z
updated_at: 2026-10-19T16:00:04.221Z
started_at: 2026-10-19T15:55:33.185Z
closed_at: 2026-10-19T16:00:04.220Z
close_reason: null
resolution: null
duplicate_of: null
---
Read-only point-in-time preservation of six older app-managed Squares worktrees: exact HEAD/tree, staged and unstaged binary diffs, selected small untracked source files, explicit exclusions, credential checks without printing values, and before/after race detection. Store external durable evidence; leave originals and owners untouched. Broader archival refs and issues are coordinated by parent.

## Notes

Delivered stable read-only snapshot of six older app-managed Squares worktrees. Durable root /Volumes/spud-ext1/agent-archive/squares-intake-handoff-20261019/older-managed-worktrees-snapshot; manifest.json and per-tree snapshot.json record full HEAD/tree, staged/unstaged paths, tracked-file metadata, private-argument and open-file ownership observations, credential counts, explicit ignored/untracked exclusions and race checks.18 patch files total8,926,132 bytes;6 nonempty patches parsed successfully by git apply --numstat without application. Changes: d57a1 unstaged machine-specific .tbd/config.yml; n17-bb-node-lifetime253 staged/0unstaged; news-significance5 unstaged. Other3 clean. All HEAD/status checks stable;0 credential-pattern findings after rejecting9 sk- substring false positives inside task- words. No untracked source files found.108 ignored entries deliberately uncopied, chiefly caches/pyc, node_modules links, .tbd docs/state and generated dist/site; originals must remain until owner/ignored-data disposition. RESTORE.txt explains archive ref labels and alternative routes: staged.patch with git apply --index then unstaged.patch, OR combined-vs-HEAD.patch; do not apply all3. Root receipt .codex/intake-resume-20261019/older-managed-worktrees-snapshot-receipt.json. No original mutations, commits, GitHub operations, pushes, archive/lifecycle changes or new tests. Parent handles remote archival refs and final handoff issues.
