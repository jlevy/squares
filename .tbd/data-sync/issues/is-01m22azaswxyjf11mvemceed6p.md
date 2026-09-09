---
type: is
id: is-01m22azaswxyjf11mvemceed6p
title: Advance KPress for upstream tooltip dismissal
kind: task
status: closed
priority: 1
version: 3
labels:
  - typography
  - integration
dependencies: []
created_at: 2026-09-09T05:41:40.283Z
updated_at: 2026-09-09T07:54:28.389Z
closed_at: 2026-09-09T07:54:28.388Z
close_reason: "PR #141 merged and the exact GitHub Pages revision passed 34/34 deployment checks."
resolution: null
duplicate_of: null
---
After KPress PR #70 merges, advance vendor/kpress to its merge commit so Squares receives the upstream footnote close control, touch dismissal, balanced padding, and neutral edge without a behavior fork. Refresh the nearby stale tooltip accent-edge comment; make no Squares behavior or component override.

## Notes

Completed by Squares PR #141, merged without squash as 0c424274533598d63b2481bf06241044b3976228. The exact deployed revision reports DRAFT v0.3.0-0c424274, the live footnote exposes the upstream Close tooltip control, and the published-site checker passed 34 of 34 page, artifact, and link contracts.
