---
type: is
id: is-01m1tw2mgp8266dxpedg2wprng
title: Make fractional crossing stop and freeze cooperatively
kind: task
status: closed
priority: 0
version: 7
labels:
  - fractional
  - safety
  - implementation
dependencies:
  - type: blocks
    target: is-01m1tw2n09x1mq8nt6ejn22vrs
  - type: blocks
    target: is-01m1v2yhy02qmka8ez4d2f5bde
parent_id: is-01m1tvqp2v2js8437xek2xk2gz
created_at: 2026-09-06T08:06:38.869Z
updated_at: 2026-09-06T10:07:27.310Z
closed_at: 2026-09-06T09:48:20.106Z
close_reason: The opt-in safe crossing stop is implemented, independently reviewed, hash-bound, twice focused-tested, edit-tier green, and pushed on PR97.
resolution: null
duplicate_of: null
---
Implement and test a safe cooperative stop that preserves a row-converged objective below eleven before a later iteration can overwrite it. Record wall time honestly, preserve normal summary and family outputs, and keep existing behavior compatible. This operational fix is outside active research time.

## Notes

Landed on continuation branch as 228806215149549032522506325bd524a71cbd4d with the four frozen file hashes. Two exact-branch focused runs passed 18 tests in 0.47s and 0.38s; both edit tiers passed 44/66 in 29.31s and 29.57s with Ruff and BasedPyright clean. Max adversarial review found no P0-P3 blocker and corrected only the non-atomic publication wording in the launch doc. PR97 is open and the implementation is fully bound.
