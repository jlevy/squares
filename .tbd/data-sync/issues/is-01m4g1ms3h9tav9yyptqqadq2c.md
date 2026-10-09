---
type: is
id: is-01m4g1ms3h9tav9yyptqqadq2c
title: Stabilize the real partial-response timeout control
kind: bug
status: in_progress
priority: 1
version: 2
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m4fqjt02p8hxaxbgq056z2mq
hold: null
hold_until: null
created_at: 2026-10-09T09:59:22.992Z
updated_at: 2026-10-09T09:59:42.914Z
started_at: 2026-10-09T09:59:42.896Z
---
The complete 98ccc9ad push gate passed all normal tests but the exclusive partial-line transport control timed out before native readiness (no identities and no angles). Isolate its intended response phase using a genuine prevalidated engine while retaining real transport, the verifier-created 0.5-second deadline, all seven original assertions, and the total elapsed bound below two seconds including preparation and cleanup. Preserve actual failed evidence; review the test-only correction independently; require the complete new push gate and hosted verification before closeout. The underlying historical host cause remains unproved.
