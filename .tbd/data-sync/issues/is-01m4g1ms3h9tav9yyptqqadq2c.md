---
type: is
id: is-01m4g1ms3h9tav9yyptqqadq2c
title: Stabilize the real partial-response timeout control
kind: bug
status: in_progress
priority: 1
version: 3
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m4fqjt02p8hxaxbgq056z2mq
hold: null
hold_until: null
created_at: 2026-10-09T09:59:22.992Z
updated_at: 2026-10-09T10:05:09.996Z
started_at: 2026-10-09T09:59:42.896Z
---
The complete 98ccc9ad push gate passed all normal tests but the exclusive partial-line transport control timed out before native readiness (no identities and no angles). Isolate its intended response phase using a genuine prevalidated engine while retaining real transport, the verifier-created 0.5-second deadline, all seven original assertions, and the total elapsed bound below two seconds including preparation and cleanup. Preserve actual failed evidence; review the test-only correction independently; require the complete new push gate and hosted verification before closeout. The underlying historical host cause remains unproved.

## Notes

Committed 1a7e4744c13dc6fcf7e911058dfa829ac03d2ff6 after independent root and web source acceptance. The local read-only observation subclass preserves real transport and cleanup. A genuine readiness handshake counts inside the original total elapsed bound below two seconds; the same table/path-bound live engine receives the verifier-created unchanged real half-second response deadline. All seven original assertions remain; actual partial bytes, matching identities and reaped/cleared child are added. Seven native cases passed before final accessor cleanup, then the affected final case passed; final Ruff/format/types are clean. Actual failed98 fixture, trace and JUnit retained. New complete default-allocation/normal-retention push gate is running and all 64 prechecks passed. Historical host cause remains unproved. No production change or full-gate pass claimed yet.
