---
type: is
id: is-01m4yckhbnm40kj2r6dyd4vybh
title: Keep supervised timeouts incomplete under concurrent validation
kind: bug
status: in_progress
priority: 1
version: 2
spec_path: docs/project/specs/active/plan-2026-10-14-ci-iteration-cost.md
delegate: codex@spud10.local
labels: []
dependencies: []
parent_id: is-01m4xkf4v65pthd9zbd7a5a3qv
hold: null
hold_until: null
created_at: 2026-10-14T23:40:18.676Z
updated_at: 2026-10-14T23:40:45.116Z
started_at: 2026-10-14T23:40:45.116Z
---
Final7b802broadprepush test_supervise_posix::test_timeout_kills_term_ignoring_group expectedINCOMPLETE for a30s SIGTERM-ignoringchild undermax_seconds0.2 but receiptCOMPLETED. Diagnoseactualreceipt/processdeadline/custody underconcurrency; fixstatus/terminationbug or explicitreal-subprocesspoolownership ifthat is the demonstratedcause. No arbitrarytimeoutincrease, skip or weakerstatusassertion. Preservechildgroupcleanup and allfailureevidence.
