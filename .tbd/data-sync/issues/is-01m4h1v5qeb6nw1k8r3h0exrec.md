---
type: is
id: is-01m4h1v5qeb6nw1k8r3h0exrec
title: Show a gray grid-size reference outline for smaller Row-scaled web packings
kind: feature
status: in_progress
priority: 2
version: 2
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m4e35s7r1e65r1qmpz250h0p
hold: null
hold_until: null
created_at: 2026-10-09T19:22:06.953Z
updated_at: 2026-10-09T19:22:52.594Z
started_at: 2026-10-09T19:22:52.593Z
---
In web Row scale only, draw a gray outer square at the logical-row grid-container reference size for cases whose selected actual enclosing side is smaller than ceil(sqrt(n)). Keep the actual scaled drawing centered inside it. Omit outline for equal/full-grid cases and in Fixed or Global modes. Preserve slots, numbers, row spacing, grid segments, hits and default state; accessible comparison description and meaningful browser tests. No PDF changes. Root sole tracker/committer; delegate to web owner.
