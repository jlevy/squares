---
type: is
id: is-01m5kb1vs27g9vh059yktetzwz
title: Repair retired Results action and contributor-route CI assertions
kind: task
status: closed
priority: 2
version: 3
spec_path: docs/project/specs/active/plan-2026-10-22-site-navigation.md
delegate: sol-upstream-final
labels: []
dependencies: []
parent_id: is-01m5k19kqedc9vp30sk9wm3s5f
hold: null
hold_until: null
created_at: 2026-10-23T02:57:14.016Z
updated_at: 2026-10-23T03:01:51.928Z
started_at: 2026-10-23T02:57:20.429Z
closed_at: 2026-10-23T03:01:51.915Z
close_reason: Replaced retired Recent Results browser fixture/action with single All Results keyboard/pointer contract (3 viewport cases passed in 36.29s); restricted contributor route assertion to obsolete site hrefs while preserving legitimate GitHub source paths (1 test passed in 10.30s). Ruff check/format and diff check clean. Committed/pushed bf38442f2.
resolution: null
duplicate_of: null
---
Late PR737 CI exposed old Recent Results browser test fixture and a contributor route assertion matching legitimate GitHub source paths. Update semantic test expectations only; run focused tests and stage for coordinator.
