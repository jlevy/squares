---
type: is
id: is-01m1tw2mgp8266dxpedg2wprng
title: Make fractional crossing stop and freeze cooperatively
kind: task
status: in_progress
priority: 0
version: 3
labels:
  - fractional
  - safety
  - implementation
dependencies:
  - type: blocks
    target: is-01m1tw2n09x1mq8nt6ejn22vrs
parent_id: is-01m1tvqp2v2js8437xek2xk2gz
created_at: 2026-09-06T08:06:38.869Z
updated_at: 2026-09-06T09:05:49.823Z
---
Implement and test a safe cooperative stop that preserves a row-converged objective below eleven before a later iteration can overwrite it. Record wall time honestly, preserve normal summary and family outputs, and keep existing behavior compatible. This operational fix is outside active research time.

## Notes

Prepared and validated outside the active clock in detached transport commit 3d1496371744bb4e20b5d80d5ffb17b36d7620b8 (parent 601f17f6). Exactly four paths implement opt-in row-converged finite objective below n stopping, pre-publication non-finite refusal, normal terminal artifacts, and scoped timing. Focused suite passed 18 in 0.37s; edit tier passed 44/66 in 28.81s with Ruff and BasedPyright clean. Await cherry-pick onto the post-PR89 branch, exact-head tests, launch binding, and closure.
