---
type: is
id: is-01m21c5yr2jbrakzvsd495qy3k
title: "PR127 R7: correct retained-net shrink cap and closed-contact endpoint"
kind: bug
status: closed
priority: 1
version: 2
labels: []
dependencies: []
parent_id: is-01m21badm7ednkkxzwgcjmgaam
created_at: 2026-09-08T20:43:31.457Z
updated_at: 2026-09-08T23:03:18.443Z
closed_at: 2026-09-08T23:03:18.443Z
close_reason: Corrections are committed in ef8a2e72 and cbe9fd76 and documented in docs/project/reviews/review-2026-09-08-pr127-research-readiness.md. The completed checkpoint combines actual passing cbe9fd76 fast, negative-control, slow and exhaustive receipts with four unchanged geometry passes from the failed ef8a2e72 full run. Scientific limits and unrun complements remain explicit.
resolution: null
duplicate_of: null
---
Lane D 239-254 and 1015-1020 uses delta=45-last_deg<0 then cos(delta)+sin(delta), yielding factor below1. Correct sufficient condition is L>B*s_H*(cos(abs(delta))+sin(abs(delta))) with strict inequality to keep closed cores in parent interiors. Equivalent exact threshold uses t=207107/500000: B*(2sqrt(2)+8/3)*2t/(1+t^2). Qualitative cap below U survives; exact claimed endpoint and supporting script need correction.
