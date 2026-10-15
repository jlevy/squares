---
type: is
id: is-01m4yckhbnm40kj2r6dyd4vybh
title: Keep supervised timeouts incomplete under concurrent validation
kind: bug
status: in_progress
priority: 1
version: 3
spec_path: docs/project/specs/active/plan-2026-10-14-ci-iteration-cost.md
delegate: codex@spud10.local
labels: []
dependencies: []
parent_id: is-01m4xkf4v65pthd9zbd7a5a3qv
hold: null
hold_until: null
created_at: 2026-10-14T23:40:18.676Z
updated_at: 2026-10-14T23:51:33.003Z
started_at: 2026-10-14T23:40:45.116Z
---
Final7b802broadprepush test_supervise_posix::test_timeout_kills_term_ignoring_group expectedINCOMPLETE for a30s SIGTERM-ignoringchild undermax_seconds0.2 but receiptCOMPLETED. Diagnoseactualreceipt/processdeadline/custody underconcurrency; fixstatus/terminationbug or explicitreal-subprocesspoolownership ifthat is the demonstratedcause. No arbitrarytimeoutincrease, skip or weakerstatusassertion. Preservechildgroupcleanup and allfailureevidence.

## Notes

Astra reproduced deterministic wall-limit and supervisor-signal races: both old-source cases falsely completed. Fix rechecks interruption/deadline after blocking sampling/poll before normal exit; 7 supervisor tests pass in 2.57s. Real 0.2-second TERM-ignoring child retains readiness, INCOMPLETE/wall_limit, SIGKILL, under-2-second and cleanup assertions, and moves to existing automatic pool_heavy lane. Ruff/types zero findings. Source uncommitted pending integrated gates. Red/green log and JUnit retained in primary pr599-integration evidence.
