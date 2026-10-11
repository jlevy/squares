---
type: is
id: is-01m3qqpkh2brpqnksyj08wj2gj
title: Fan out post-merge fast validation across the seven proven PR lanes
kind: bug
status: open
priority: 1
version: 1
spec_path: docs/project/reviews/review-2026-09-29-validation-parallelism.md
labels: []
dependencies: []
parent_id: is-01m3p5wj25knm7rbx0g4a4tpvg
created_at: 2026-09-29T23:23:50.663Z
updated_at: 2026-09-29T23:23:50.663Z
---
Hosted post-merge validation leaves the 72-step fast floor serialized in validate after nine deferred workers finish. Reuse the existing seven PR fast selectors concurrently on push/schedule/dispatch, require all seven plus nine deferred workers in the post-merge aggregate, preserve the PR seven-job surface, source binding and failure semantics, and reset post-merge wall declarations to pending for the new topology without inventing measurements.
