---
type: is
id: is-01m4yckhbnm40kj2r6dyd4vybh
title: Keep supervised timeouts incomplete under concurrent validation
kind: bug
status: closed
priority: 1
version: 6
spec_path: docs/project/specs/active/plan-2026-10-14-ci-iteration-cost.md
delegate: codex@spud10.local
labels:
  - pr-620
dependencies: []
parent_id: is-01m4xkf4v65pthd9zbd7a5a3qv
hold: null
hold_until: null
created_at: 2026-10-14T23:40:18.676Z
updated_at: 2026-10-15T18:55:27.095Z
started_at: 2026-10-14T23:40:45.116Z
closed_at: 2026-10-15T18:55:27.095Z
close_reason: "Source delivery completed in PR620: reviewed head 32ffac9dd8d8756ec619e808d0d3034b58640e6d merged as 4c9af6902e517bfff7d9f50d7cd6a042a15f60ed. Exact-head ordinary Packing 38787870695 and Pages 38787870830 passed; actual JUnit confirms all 46 targeted policy/selection controls passed without skips. Final reviews O5538212826, P5538213019 and Q5538223370 have no open findings and carry unchanged earlier M/N coverage. The historical full43 aggregate remains failed on CALL timing, while its actual 241 slow-lane nodes including all five moved operations passed. Hosted policy now explicitly reports at12s and enforces45s; strict/local/enforce remain12s, and mathematical/functional/child-deadline guards remain. The bounded retrospective, safety removal, supervision, invocation-local input sharing, measured-node placement, native ownership and selection fixes are delivered; no controlled speedup or three-minute success is claimed. Post-merge publication and complete native main coverage remain OPEN and owned in think-bmix; broader measured CI program remains open in think-kxmq/think-jpto/think-h96x. Evidence retained in primary .codex/regularization-closeout-evidence-2026-10-13/."
resolution: null
duplicate_of: null
---
Final7b802broadprepush test_supervise_posix::test_timeout_kills_term_ignoring_group expectedINCOMPLETE for a30s SIGTERM-ignoringchild undermax_seconds0.2 but receiptCOMPLETED. Diagnoseactualreceipt/processdeadline/custody underconcurrency; fixstatus/terminationbug or explicitreal-subprocesspoolownership ifthat is the demonstratedcause. No arbitrarytimeoutincrease, skip or weakerstatusassertion. Preservechildgroupcleanup and allfailureevidence.

## Notes

Independent source audit on 2026-10-15 confirms the timeout race remains on main 31eaf633. The narrow runtime fix and deterministic deadline/signal tests exist only in legacy commit 6756bda8d, which also contains unrelated snapshot work and will not be cherry-picked. A dedicated moderate implementation agent owns only supervise_posix.py and test_supervise_posix.py in the current CI worktree. It will adapt the minimal hunks, preserve all real child-process deadline and cleanup assertions, and run only the bounded supervisor checks with external scratch. Root coordinates source integration, independent final review and PR620 validation. No cap, deadline or mathematical assertion may be weakened.
