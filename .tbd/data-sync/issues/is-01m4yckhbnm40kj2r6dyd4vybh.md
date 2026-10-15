---
type: is
id: is-01m4yckhbnm40kj2r6dyd4vybh
title: Keep supervised timeouts incomplete under concurrent validation
kind: bug
status: in_progress
priority: 1
version: 4
spec_path: docs/project/specs/active/plan-2026-10-14-ci-iteration-cost.md
delegate: codex@spud10.local
labels:
  - pr-620
dependencies: []
parent_id: is-01m4xkf4v65pthd9zbd7a5a3qv
hold: null
hold_until: null
created_at: 2026-10-14T23:40:18.676Z
updated_at: 2026-10-15T13:31:58.300Z
started_at: 2026-10-14T23:40:45.116Z
---
Final7b802broadprepush test_supervise_posix::test_timeout_kills_term_ignoring_group expectedINCOMPLETE for a30s SIGTERM-ignoringchild undermax_seconds0.2 but receiptCOMPLETED. Diagnoseactualreceipt/processdeadline/custody underconcurrency; fixstatus/terminationbug or explicitreal-subprocesspoolownership ifthat is the demonstratedcause. No arbitrarytimeoutincrease, skip or weakerstatusassertion. Preservechildgroupcleanup and allfailureevidence.

## Notes

Independent source audit on 2026-10-15 confirms the timeout race remains on main 31eaf633. The narrow runtime fix and deterministic deadline/signal tests exist only in legacy commit 6756bda8d, which also contains unrelated snapshot work and will not be cherry-picked. A dedicated moderate implementation agent owns only supervise_posix.py and test_supervise_posix.py in the current CI worktree. It will adapt the minimal hunks, preserve all real child-process deadline and cleanup assertions, and run only the bounded supervisor checks with external scratch. Root coordinates source integration, independent final review and PR620 validation. No cap, deadline or mathematical assertion may be weakened.
