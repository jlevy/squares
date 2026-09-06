---
type: is
id: is-01m1vrgswbdc25pxt0tg4ct3rt
title: "PR #94 review R94-2: describe certificate rejection by validity"
kind: bug
status: open
priority: 3
version: 2
labels: []
dependencies: []
parent_id: is-01m1vr1cwbx9h9c8gm65jrgpg6
created_at: 2026-09-06T16:23:43.242Z
updated_at: 2026-09-06T16:23:54.092Z
---
Senior review https://github.com/jlevy/squares/pull/94#issuecomment-5560547382. Explainer template sentence implies every certificate from a wrong program is rejected; valid certificate bytes must remain acceptable regardless of generator correctness. State the actual trust boundary.
