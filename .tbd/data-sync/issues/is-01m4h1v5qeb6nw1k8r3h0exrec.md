---
type: is
id: is-01m4h1v5qeb6nw1k8r3h0exrec
title: Show a gray grid-size reference outline for smaller Row-scaled web packings
kind: feature
status: closed
priority: 2
version: 3
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m4e35s7r1e65r1qmpz250h0p
hold: null
hold_until: null
created_at: 2026-10-09T19:22:06.953Z
updated_at: 2026-10-10T11:24:58.118Z
started_at: 2026-10-09T19:22:52.593Z
closed_at: 2026-10-10T11:24:58.118Z
close_reason: Final accepted atlas behavior implemented and published in PR474 at d83b7c03d, containing main657cc4861. Local repair-delta66PASS; hosted Fast94+actualDeferred13=107PASS on immutable mergec78974427 with identical headtree; Pages17 dependencies+required aggregatePASS; formal seniorI/correctnessJ no findings in declared scopes. Required CI PASS, no unresolvedthreads, CLEAN/MERGEABLE finalreadback. Canonical exports qualified; prior failures retained without acceptance relaxation. Later user refinements supersede earlier styling/layout requirements. Completed ready-to-merge scope; no GitHub merge performed. Browser hold, future intake and performance follow-ups remain open. Final evidence full107-final-proof.json and final-freshness.json under external final/ci-final-head-d83b7c03d.
resolution: null
duplicate_of: null
---
In web Row scale only, draw a gray outer square at the logical-row grid-container reference size for cases whose selected actual enclosing side is smaller than ceil(sqrt(n)). Keep the actual scaled drawing centered inside it. Omit outline for equal/full-grid cases and in Fixed or Global modes. Preserve slots, numbers, row spacing, grid segments, hits and default state; accessible comparison description and meaningful browser tests. No PDF changes. Root sole tracker/committer; delegate to web owner.
