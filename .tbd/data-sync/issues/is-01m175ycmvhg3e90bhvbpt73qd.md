---
type: is
id: is-01m175ycmvhg3e90bhvbpt73qd
title: "Retier the gate from first principles: fast, standard, complete"
kind: task
status: open
priority: 0
version: 1
labels: []
dependencies: []
created_at: 2026-08-29T16:34:16.859Z
updated_at: 2026-08-29T16:34:16.859Z
---
agenda-006 BC-075, an efficiency-loop block scheduled immediately after the W8 documentation pass. The fast tier is not fast: measured today at 484s, 538s and 631s on the same container as its content grew, with a single step (fast behavioural tests) accounting for nearly all of it. The question is not how to make the current tiers quicker but whether the tiers are the right ones -- what must run on every edit, what belongs at a block boundary, and what only needs running once or twice a session. Absorbs BC-062's reachability-scoped selector as one candidate mechanism rather than as the goal.
