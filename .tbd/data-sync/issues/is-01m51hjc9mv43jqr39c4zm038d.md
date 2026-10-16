---
type: is
id: is-01m51hjc9mv43jqr39c4zm038d
title: Refine News chooser states, shared topic colors and article spacing
kind: bug
status: in_progress
priority: 2
version: 8
spec_path: docs/project/specs/active/plan-2026-10-13-site-changelog.md
delegate: codex@spud10
labels: []
dependencies: []
child_order_hints:
  - is-01m51hqspk8m12zgc20zpq0egm
  - is-01m51hqtms76wqmackh51re6ck
  - is-01m51hqvh38qx5w756bs9wsjak
  - is-01m51hqw58eewgc9g3bcqkte65
  - is-01m51hqwp9pv33x85ztqskn49g
hold: null
hold_until: null
created_at: 2026-10-16T05:04:46.887Z
updated_at: 2026-10-16T05:07:47.529Z
started_at: 2026-10-16T05:05:12.360Z
---
Ship the requested News UI corrections: gray inactive topic filters, topic-colored active states and paler colored hover without text or inset underlines; borders follow wrapped button rows; remove both All controls and retain one unboxed Reset filters button. Give Optimality, Project and Engineering distinct shared colors, separate from lower/upper bounds and verification. Tighten title/date/tag/body spacing on shared homepage and News cards. Make significance meters horizontally tighter with borders matching label color, and shorten level tooltips while retaining detailed rationale in source records/docs. Reuse design tokens, preserve accessibility/filter semantics, verify desktop/mobile and light/dark behavior, document design changes, independently review, PR, merge and verify deployment.
