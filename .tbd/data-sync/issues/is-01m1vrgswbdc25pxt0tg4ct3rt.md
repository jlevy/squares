---
type: is
id: is-01m1vrgswbdc25pxt0tg4ct3rt
title: "PR #94 review R94-2: describe certificate rejection by validity"
kind: bug
status: closed
priority: 3
version: 3
labels: []
dependencies: []
parent_id: is-01m1vr1cwbx9h9c8gm65jrgpg6
created_at: 2026-09-06T16:23:43.242Z
updated_at: 2026-09-06T16:57:15.121Z
closed_at: 2026-09-06T16:57:15.121Z
close_reason: Fixed in the final reviewed PR94/96/95 candidates; focused regressions, broad local validation, and independent cross-review passed. Parent review and landing tasks remain open while final hosted CI and disposition publication complete.
resolution: null
duplicate_of: null
---
Senior review https://github.com/jlevy/squares/pull/94#issuecomment-5560547382. Explainer template sentence implies every certificate from a wrong program is rejected; valid certificate bytes must remain acceptable regardless of generator correctness. State the actual trust boundary.
