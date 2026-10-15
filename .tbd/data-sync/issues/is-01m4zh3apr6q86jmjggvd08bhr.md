---
type: is
id: is-01m4zh3apr6q86jmjggvd08bhr
title: Keep site release checks within component-owned validation
kind: bug
status: in_progress
priority: 1
version: 4
spec_path: docs/project/specs/active/plan-2026-10-13-site-changelog.md
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m4wtv34pphy5w434wk13b85x
child_order_hints:
  - is-01m4zhskq7z8atpw93q5qyafmj
hold: null
hold_until: null
created_at: 2026-10-15T10:18:04.887Z
updated_at: 2026-10-15T10:41:11.369Z
started_at: 2026-10-15T10:20:56.536Z
---
A site release cut currently schedules the same cross-component pytest list as infographic/paper cuts, including whole-atlas composites and exhaustive proof sweeps. A manual invocation during PR617 integration entered unchanged exhaustive_exact cases; it was interrupted and a focused release/date/claim selection retained. Make cut_release validation component-aware and use the shared quick-tier predicate for ordinary cut iteration, with deeper evidence selected explicitly at the owning checkpoint. Preserve every scientific assertion and full checkpoint obligation; prove selection identities and component ownership without duplicating expensive runs.

## Notes

Implemented in 9581241b2 and threshold coverage follow-up 934c68019, part of the nine-file quick-push delivery. Component-owned mappings preserve generators and shared release/date checks; ordinary tests use QUICK_TESTS, --include-deep-tests deliberately includes owning slow/exhaustive tests, and final matching-source/base full checkpoint remains explicit. Cut-tool 22 passed; initial ordinary site plan 85 passed with 13 exhaustive cases deselected in7.54s; reviewer Q1 added independent T-025/T-026 embedding and refusal coverage, verified by 48 tests in4.41s with two exhaustive sweeps deselected. Q1 child rohx closed after independent senior confirmation. Ruff/type clean; all three reviews clear. Awaiting final integration/release/canonical push/hosted delivery with gg64.
