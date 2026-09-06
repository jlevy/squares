---
type: is
id: is-01m1tw2mgp8266dxpedg2wprng
title: Make fractional crossing stop and freeze cooperatively
kind: task
status: in_progress
priority: 0
version: 4
labels:
  - fractional
  - safety
  - implementation
dependencies:
  - type: blocks
    target: is-01m1tw2n09x1mq8nt6ejn22vrs
parent_id: is-01m1tvqp2v2js8437xek2xk2gz
created_at: 2026-09-06T08:06:38.869Z
updated_at: 2026-09-06T09:38:36.216Z
---
Implement and test a safe cooperative stop that preserves a row-converged objective below eleven before a later iteration can overwrite it. Record wall time honestly, preserve normal summary and family outputs, and keep existing behavior compatible. This operational fix is outside active research time.

## Notes

Prepared against the final integrated PR89 tree as detached commit 37ca074d2a9e0027d334be03c982b24ffb6acd4a. Exactly four paths retain SHA256 38648bc4, 6ed0043b, 56bd0f1a, and 25769fab. Focused suite passed 18 and edit tier passed 44/66 in 30.72s. Fresh max adversarial review plus eight focused controls found no P0-P3 launch blocker: trigger is finite/converged/objective<n after exact separation, exact ceiling precedes it, defaults/equality/unconverged cases stay unchanged, state feeds the bridge, and floats remain proposers only. Await post-PR89 cherry-pick, final branch gate, and closure.
