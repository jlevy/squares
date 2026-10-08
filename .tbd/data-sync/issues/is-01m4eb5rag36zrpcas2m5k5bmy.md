---
type: is
id: is-01m4eb5rag36zrpcas2m5k5bmy
title: "n17 supporting CI: bind retired-notice click wait to destination URL"
kind: bug
status: in_progress
priority: 2
version: 3
spec_path: docs/project/reviews/review-2026-10-06-n17-w3-consolidation.md
delegate: claude-code@spud10.local
labels:
  - n-17
dependencies: []
parent_id: is-01m4e47f19w8w1d7tyka9raahk
hold: null
hold_until: null
created_at: 2026-10-08T18:07:27.567Z
updated_at: 2026-10-08T18:56:00.310Z
started_at: 2026-10-08T18:07:44.642Z
---
PR453 frontend trace shows generic expect_navigation satisfied on the old URL. Exact kpress scroll history.replaceState can satisfy navigation. Narrow test-only URL-qualified wait; preserve content assertions and timeouts. Confirm with focused browser control and hosted CI.

## Notes

PR453b1948591b00091de2daf01532af516b723206f9e fixesgenericnavigationwaitfalse satisfaction with exactretired-notice targetURL. SameURLkpresshistory.replaceStateeventobserved; everyassertion/timeoutunchanged. T117JSon/off2PASS30.85s;lint/types/diffPASS. HostednewheadfrontendPASS job113466892029 andPackingrequiredPASS job113483328234 at18:52UTC; Pagesaggregatepending. Focusedlogretained attic/n17-six-hour-engineering/issue-followthrough-20261008/frontend-qualified-pair.log. Native9aa4a65f priorLinux28+world+6namedreceiptcontrolsPASS74.72/90s, notWindows/fullsameobject/centeredadoption. No sourceproofcriteria/boundchange.
