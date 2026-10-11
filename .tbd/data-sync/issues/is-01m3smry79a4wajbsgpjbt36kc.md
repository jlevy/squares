---
type: is
id: is-01m3smry79a4wajbsgpjbt36kc
title: Make complete n11 case-2095 regression respect the bounded test worker budget
kind: bug
status: closed
priority: 1
version: 8
spec_path: docs/project/specs/active/plan-2026-09-29-proof-verification-consolidation.md
labels: []
dependencies: []
parent_id: is-01m3sken298psm0jfn7tmbcqp9
created_at: 2026-09-30T17:11:10.312Z
updated_at: 2026-09-30T19:15:54.454Z
closed_at: 2026-09-30T19:15:54.437Z
close_reason: "Post-merge automatic main run 36761793749 at 3687d9cba3033d6fdd5942150566b5fca4846c5c completed slow-lane job 110045933894 successfully: all 158 tests passed, including test_complete_2095_receipt_has_every_step_and_no_pending_row (43.16 s call). This closes only the test-only case-2095 deadline repair; the run aggregate failed separately on deferred-controls-finer."
resolution: null
duplicate_of: null
---
Deferred checkpoint36746969192 at6a307f6a4: full generic case2095 test returned INCOMPLETE with max_seconds30 and workers3 while running inside the parallel slow lane. Preserve all160 rows, five complete steps, source binding and no-partial-credit assertions; diagnose scheduling and existing reviewed efficient options before changing a finite deadline. Only tests may change; accepted checker/source and proof receipts remain fixed. Sol repairs, Astra reviews; use one targeted execution and keep the expiration refusal control.

## Notes

Fixed in ebbfec10e, test-only. Same pinned 2095 source/seed/audit now replays with the already-reviewed shared sequential exact checker, one worker, finite 60-second clock, all five steps and 160 rows plus empty pending inventory and written-receipt equality. Positive and real deadline/source-tamper controls: 3 passed in 34.48 seconds (positive 34.15 seconds). Ruff/BasedPyright clean. Astra max approved test SHA d651f66dd8e42f70a7d2006edf7c55b7f64a845435f71aabd86d5eddfb45af77. Accepted production checkers and receipts unchanged. Await publication/current-head normal CI.

Reopened: Automatic main slow run 36753195024 at merged d44ec0408 still hit the positive case-2095 deadline: 60.12s, INCOMPLETE; 157 other slow tests passed. Test-only operational-ceiling follow-up is locally reviewed and awaiting publication.

Follow-up after automatic main run 36753195024 at merge d44ec0408: the slow lane dispatched pytest with four xdist workers; 157 other slow tests passed, but the complete case-2095 golden returned INCOMPLETE at its 60-second test clock (60.12 seconds). The test-only repair raises only that positive golden to a finite 300-second operational ceiling. All eight focused file tests passed in 39.32 seconds; Ruff/BasedPyright were clean and Astra approved the scope. All five steps, 160 rows, empty pending census, final source recheck, and the separate real expiry refusal remain required. Production checker, pinned inputs, accepted receipts, and session fast-tier PASS are unchanged. Await hosted slow-lane recheck; no pass credit is inferred from the failed main run. Observed outer --inner-jobs 2 and child pytest -n 4 differ; no scheduler defect is claimed without contract review.
