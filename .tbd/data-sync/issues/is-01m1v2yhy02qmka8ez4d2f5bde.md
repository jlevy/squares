---
type: is
id: is-01m1v2yhy02qmka8ez4d2f5bde
title: Suspend stale launch authorization and structurally gate both T+2 lanes
kind: bug
status: in_progress
priority: 0
version: 4
labels:
  - orchestration
  - release-blocker
dependencies:
  - type: blocks
    target: is-01m1tw2n09x1mq8nt6ejn22vrs
  - type: blocks
    target: is-01m1tw2ns895rs4qe4xf45m5q1
parent_id: is-01m1tvqp2v2js8437xek2xk2gz
created_at: 2026-09-06T10:06:45.183Z
updated_at: 2026-09-06T10:07:29.487Z
---
The 2026-09-06T09:43:25Z release authorization predates post-authorization proof/state blockers. Add a current landing receipt that explicitly suspends/revokes it until every pre-release blocker is terminal; encode dependency edges from one umbrella release gate or each blocker to both think-6yx2 and think-gab1 so release is structural, not prose-only. Bind the replacement authorization/restart UTC only at the integrated pushed head.
