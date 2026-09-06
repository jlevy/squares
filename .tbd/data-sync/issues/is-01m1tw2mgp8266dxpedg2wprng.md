---
type: is
id: is-01m1tw2mgp8266dxpedg2wprng
title: Make fractional crossing stop and freeze cooperatively
kind: task
status: open
priority: 0
version: 2
labels:
  - fractional
  - safety
  - implementation
dependencies:
  - type: blocks
    target: is-01m1tw2n09x1mq8nt6ejn22vrs
parent_id: is-01m1tvqp2v2js8437xek2xk2gz
created_at: 2026-09-06T08:06:38.869Z
updated_at: 2026-09-06T08:06:39.364Z
---
Implement and test a safe cooperative stop that preserves a row-converged objective below eleven before a later iteration can overwrite it. Record wall time honestly, preserve normal summary and family outputs, and keep existing behavior compatible. This operational fix is outside active research time.
