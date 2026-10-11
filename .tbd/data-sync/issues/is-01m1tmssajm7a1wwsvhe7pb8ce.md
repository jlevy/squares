---
type: is
id: is-01m1tmssajm7a1wwsvhe7pb8ce
title: Detect a pull request that produces no workflow run because its branch conflicts with its base
kind: bug
status: closed
priority: 1
version: 2
labels: []
dependencies: []
created_at: 2026-09-06T05:59:28.850Z
updated_at: 2026-10-06T08:41:41.892Z
closed_at: 2026-10-06T08:41:41.892Z
close_reason: "Done: .github/workflows/branch-mergeability.yml (a77172ad8, 2026-09-06) runs git merge-tree --write-tree against the pull request's base on every push, so a branch whose merge ref cannot be built reports red instead of silently producing no run (D-459)."
resolution: null
duplicate_of: null
---
D-459 recurrence. When a PR branch conflicts with its base, GitHub cannot build refs/pull/N/merge, so it creates no workflow run at all. The PR goes silent rather than red and its checks sit pending forever, which is indistinguishable from 'CI has not started yet'. It fired three times on 2026-09-05/06; two pushes produced zero runs before anyone noticed.

Diagnostic that decides it locally, with no API call: git merge-tree --write-tree HEAD origin/main -- a nonzero exit means the merge ref cannot be built and no run will ever appear.

What is owed is a detector rather than the habit. D-459's own entry argued against reaching out to the GitHub API from packing-validate, and that argument still holds; git merge-tree is local, so the check can live in the repository.
