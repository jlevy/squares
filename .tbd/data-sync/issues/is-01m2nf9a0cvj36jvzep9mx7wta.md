---
type: is
id: is-01m2nf9a0cvj36jvzep9mx7wta
title: Make post-merge tree reuse classification fail closed
kind: bug
status: open
priority: 1
version: 1
labels: []
dependencies: []
parent_id: is-01m2m5zjmj7dsycs1x6yxwcwwt
created_at: 2026-09-16T16:02:35.659Z
updated_at: 2026-09-16T16:02:35.659Z
---
PR #185 review: Step.reads_beyond_tree defaults False, so a newly added clock/network/git-dependent fast step is silently classified reusable and omitted after merge. Replace it with an explicit safe-default tree_reusable classification, and add a contract that every fast step is deliberately classified before exact-tree reuse may omit it.
