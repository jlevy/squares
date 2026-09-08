---
type: is
id: is-01m1tmssajm7a1wwsvhe7pb8ce
title: Detect a pull request that produces no workflow run because its branch conflicts with its base
kind: bug
status: open
priority: 1
version: 1
labels: []
dependencies: []
created_at: 2026-09-06T05:59:28.850Z
updated_at: 2026-09-06T05:59:28.850Z
---
D-459 recurrence. When a PR branch conflicts with its base, GitHub cannot build refs/pull/N/merge, so it creates no workflow run at all. The PR goes silent rather than red and its checks sit pending forever, which is indistinguishable from 'CI has not started yet'. It fired three times on 2026-09-05/06; two pushes produced zero runs before anyone noticed.

Diagnostic that decides it locally, with no API call: git merge-tree --write-tree HEAD origin/main -- a nonzero exit means the merge ref cannot be built and no run will ever appear.

What is owed is a detector rather than the habit. D-459's own entry argued against reaching out to the GitHub API from packing-validate, and that argument still holds; git merge-tree is local, so the check can live in the repository.
