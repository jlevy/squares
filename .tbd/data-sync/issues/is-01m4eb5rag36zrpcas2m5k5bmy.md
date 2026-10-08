---
type: is
id: is-01m4eb5rag36zrpcas2m5k5bmy
title: "n17 supporting CI: bind retired-notice click wait to destination URL"
kind: bug
status: in_progress
priority: 2
version: 2
spec_path: docs/project/reviews/review-2026-10-06-n17-w3-consolidation.md
delegate: claude-code@spud10.local
labels:
  - n-17
dependencies: []
parent_id: is-01m4e47f19w8w1d7tyka9raahk
hold: null
hold_until: null
created_at: 2026-10-08T18:07:27.567Z
updated_at: 2026-10-08T18:07:44.642Z
started_at: 2026-10-08T18:07:44.642Z
---
PR453 frontend trace shows generic expect_navigation satisfied on the old URL. Exact kpress scroll history.replaceState can satisfy navigation. Narrow test-only URL-qualified wait; preserve content assertions and timeouts. Confirm with focused browser control and hosted CI.
