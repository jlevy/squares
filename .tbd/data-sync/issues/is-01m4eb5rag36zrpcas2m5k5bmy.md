---
type: is
id: is-01m4eb5rag36zrpcas2m5k5bmy
title: "n17 supporting CI: bind retired-notice click wait to destination URL"
kind: bug
status: closed
priority: 2
version: 5
spec_path: docs/project/reviews/review-2026-10-06-n17-w3-consolidation.md
delegate: claude-code@spud10.local
labels:
  - n-17
dependencies: []
parent_id: is-01m4e47f19w8w1d7tyka9raahk
hold: null
hold_until: null
created_at: 2026-10-08T18:07:27.567Z
updated_at: 2026-10-08T19:04:18.748Z
started_at: 2026-10-08T18:07:44.642Z
closed_at: 2026-10-08T19:04:18.747Z
close_reason: "Destination-qualified wait captured in PR #453; focused controls and all required current-head hosted checks passed. Review and merge remain separate."
resolution: null
duplicate_of: null
---
PR453 frontend trace shows generic expect_navigation satisfied on the old URL. Exact kpress scroll history.replaceState can satisfy navigation. Narrow test-only URL-qualified wait; preserve content assertions and timeouts. Confirm with focused browser control and hosted CI.

## Notes

PR #453 at b1948591b00091de2daf01532af516b723206f9e fixes false satisfaction of the generic navigation wait by requiring the exact retired-notice destination URL. A same-URL kpress history.replaceState event was observed; every assertion and timeout remains unchanged. Both T-117 JavaScript variants passed in 30.85 seconds; lint, types and diff checks passed. Current-head hosted frontend job 113466892029, Packing aggregate job 113483328234, Pages aggregate job 113487604916 and mergeability all passed, observed October 8 at 19:01:34 UTC. The original hosted interleaving was not replayed locally. Focused log retained at attic/n17-six-hour-engineering/issue-followthrough-20261008/frontend-qualified-pair.log. Previous-head native Linux controls passed in 74.72/90 seconds; Windows, full same-object and centered-domain adoption remain separate. No proof criterion, admission or bound changed. Bounded navigation repair is complete and captured on the draft; PR review and merge remain separate.
