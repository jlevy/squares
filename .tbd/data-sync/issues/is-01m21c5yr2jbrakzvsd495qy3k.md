---
type: is
id: is-01m21c5yr2jbrakzvsd495qy3k
title: "PR127 R7: correct retained-net shrink cap and closed-contact endpoint"
kind: bug
status: open
priority: 1
version: 1
labels: []
dependencies: []
parent_id: is-01m21badm7ednkkxzwgcjmgaam
created_at: 2026-09-08T20:43:31.457Z
updated_at: 2026-09-08T20:43:31.457Z
---
Lane D 239-254 and 1015-1020 uses delta=45-last_deg<0 then cos(delta)+sin(delta), yielding factor below1. Correct sufficient condition is L>B*s_H*(cos(abs(delta))+sin(abs(delta))) with strict inequality to keep closed cores in parent interiors. Equivalent exact threshold uses t=207107/500000: B*(2sqrt(2)+8/3)*2t/(1+t^2). Qualitative cap below U survives; exact claimed endpoint and supporting script need correction.
