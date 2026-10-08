---
type: is
id: is-01m4edxmfwe4ey36yag3yg9zz6
title: "PR #456: bound artifact polling and honor GitHub quota retries"
kind: bug
status: closed
priority: 1
version: 5
delegate: codex-pr395-site-review
labels: []
dependencies: []
parent_id: is-01m4e2d5gyj7m218hm9f5g01xd
child_order_hints:
  - is-01m4eha9m30brwgytpq8zt0pwh
hold: null
hold_until: null
created_at: 2026-10-08T18:55:27.219Z
updated_at: 2026-10-08T21:51:46.242Z
started_at: 2026-10-08T18:57:07.159Z
closed_at: 2026-10-08T21:51:46.242Z
close_reason: Fixed and independently reviewedE1 at e047331, merged91ca9b8. Seven declared prepared-page job dependencies/nine matrix consumers now wait for successfulprepare; exactrun/attempt/numericartifactbinding, scopepredicates and600s acceptance deadline remain strict. Queued artifacts notpolled; explicit403/429 quota backoff covered by23waiter and focusednegativeworkflow/aggregate controls. Both finalheadPages37847037048 and actualmainPages37848801634 publication/pages-required/deploySUCCESS; no APIquota consumer failure. Production smoke bound91ca9b8 passes28noJScontexts,14metadata,22navigation/math and9delivery controls. Whole final registry/105main checkpoints remain under rolloutthink-7wlz.
resolution: null
duplicate_of: null
---
PR456 head3d266f8cc81efb54826d80f3d9921d2d26c5d529 Pages run37821312270: screen, typography, PDF and geometry failed joining prepared-page because GitHub returned installation API quota HTTP403. Producer prepare started18:38:20 and passed18:39:22, after consumers'600s windows; queued jobs carried started_at placeholders. Moderate agent's waiter correction has23 focused tests and zero lint/type findings: no queued artifact queries, bounded backoff and explicit quota retry windows, strict deadlines after API responses, exact run/attempt/artifact binding and ordinary403 refusal. Independent Astra reviewer is checking minimal native workflow needs:prepare for seven artifact consumers, keeping the unchanged600s visibility/deadline guard and scope predicates. Final code review, hosted CI and deployed proof remain required under rollout think-7wlz.
