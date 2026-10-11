---
type: is
id: is-01m45f4fjgczmz88rp23cmq0q3
title: "PR #350 B1 (High): in no formal stack; retarget to main after stack 357 merges, then merge standalone"
kind: task
status: open
priority: 1
version: 1
spec_path: docs/project/reviews/review-2026-10-02-n17-bulk-exclusion-design.md
labels: []
dependencies: []
parent_id: is-01m45f4dj0p0t4bsxjnxcz5whv
created_at: 2026-10-05T07:23:30.255Z
updated_at: 2026-10-05T07:23:30.255Z
---
Review B finding B1 on jlevy/squares#350 (https://github.com/jlevy/squares/pull/350#pullrequestreview-5411026984), at head 9179aab7d. gh api repos/jlevy/squares/stacks?pull_request=350 returns [] (re-checked 2026-10-05) while the base is claude/n17-sessions-167-168. Recommended fix (a): do not merge while the base is #347's branch; after stack 357 merges, merge #347's final head into #350, retarget to main (GitHub does it if the base branch is deleted, else gh pr edit 350 --base main), and merge standalone once CI is green. Alternative (b), only if the owner wants one atomic merge: gh stack link it above #360. Blocked on stack 357 merging.
