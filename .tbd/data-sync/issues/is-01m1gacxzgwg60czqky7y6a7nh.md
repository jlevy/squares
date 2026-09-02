---
type: is
id: is-01m1gacxzgwg60czqky7y6a7nh
title: Exp-056 lease and checkpoint were not durable across the coordinator host handoff
kind: bug
status: closed
priority: 0
version: 2
labels:
  - packing
  - agenda-015
  - trust-boundary
dependencies: []
created_at: 2026-09-02T05:45:17.551Z
updated_at: 2026-09-02T05:55:14.042Z
closed_at: 2026-09-02T05:55:14.041Z
close_reason: Owner clarified that matched Claude-to-Codex and Linux-to-macOS exact-algebraic handoffs are valid continuations. OR-10 now records the bridge contract; exp-056 resumed from its verified chain, so the provisional handoff defect does not stand.
resolution: canceled
duplicate_of: null
---
Session-078 recorded a live Linux/Claude exp-056 process and lease, but PR head aed41ae carried none of its fresh checkpoint/progress/result paths and the old PID was unreachable after interruption. A macOS/Codex restart under the same experiment would change subject.host_system, method.operator, lease.host and the one-process observation regime. Preserve the typed stop and design a durable, host-bound handoff/recovery contract before any later H-052 continuation.
