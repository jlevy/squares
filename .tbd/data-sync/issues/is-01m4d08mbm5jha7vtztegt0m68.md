---
type: is
id: is-01m4d08mbm5jha7vtztegt0m68
title: "PR #395 C7: validate recent and complete tables with actual static drawing assets"
kind: bug
status: in_progress
priority: 1
version: 3
delegate: codex-pr395-site-review
labels: []
dependencies: []
parent_id: is-01m4cecqqmt13gys8265mpra32
hold: null
hold_until: null
created_at: 2026-10-08T05:37:33.031Z
updated_at: 2026-10-08T11:19:55.101Z
started_at: 2026-10-08T05:40:52.017Z
---
Hosted frontend fails 24 legacy table tests. Independent Astra triage confirms 12 SVG-only probes miss cached IMG drawings, ten tests conflate recent home subset with complete all-results, one long-list selector excludes wrapping groups and one intrinsic-width expectation needs measured fit/invariance evidence. Correct retained tests and stale table documentation, preserve every fit/visibility/scroll/control assertion and verify hosted frontend. Run 37732462293 frontend 113164467669.
