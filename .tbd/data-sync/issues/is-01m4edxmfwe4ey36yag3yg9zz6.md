---
type: is
id: is-01m4edxmfwe4ey36yag3yg9zz6
title: "PR #456: bound artifact polling and honor GitHub quota retries"
kind: bug
status: in_progress
priority: 1
version: 4
delegate: codex-pr395-site-review
labels: []
dependencies: []
parent_id: is-01m4e2d5gyj7m218hm9f5g01xd
child_order_hints:
  - is-01m4eha9m30brwgytpq8zt0pwh
hold: null
hold_until: null
created_at: 2026-10-08T18:55:27.219Z
updated_at: 2026-10-08T19:54:47.808Z
started_at: 2026-10-08T18:57:07.159Z
---
PR456 head3d266f8cc81efb54826d80f3d9921d2d26c5d529 Pages run37821312270: screen, typography, PDF and geometry failed joining prepared-page because GitHub returned installation API quota HTTP403. Producer prepare started18:38:20 and passed18:39:22, after consumers'600s windows; queued jobs carried started_at placeholders. Moderate agent's waiter correction has23 focused tests and zero lint/type findings: no queued artifact queries, bounded backoff and explicit quota retry windows, strict deadlines after API responses, exact run/attempt/artifact binding and ordinary403 refusal. Independent Astra reviewer is checking minimal native workflow needs:prepare for seven artifact consumers, keeping the unchanged600s visibility/deadline guard and scope predicates. Final code review, hosted CI and deployed proof remain required under rollout think-7wlz.
