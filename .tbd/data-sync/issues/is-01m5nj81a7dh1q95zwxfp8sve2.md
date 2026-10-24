---
type: is
id: is-01m5nj81a7dh1q95zwxfp8sve2
title: "PR #745 A2: certifying deep-gate run at the final head after #753; slow lane against its ceiling"
kind: bug
status: in_progress
priority: 1
version: 4
delegate: c-land-745-1024
labels: []
dependencies: []
parent_id: is-01m5ndfyhknd8p766m3pnpgn4a
hold: null
hold_until: null
created_at: 2026-10-23T23:41:25.191Z
updated_at: 2026-10-24T02:10:25.222Z
started_at: 2026-10-24T01:05:26.098Z
---
A2 of PR #745's review A (https://github.com/jlevy/squares/pull/745#issuecomment-6372288301), Medium: the full checkpoint for the four whole 2,073-direction fine-net sweeps, and the deferred slow lane's wall against its 1250 s ceiling (OR-13, OR-17).

Done so far (lane c-fix-745-1023, 23 October):
- Deep-gate dispatch 40033801674 at b39bd7cec (`gh workflow run deep-gate.yml --ref claude/intake-2026-10-23-lower-bounds`) ran every deep job. All passed but `deferred-slow-lane`, which failed only on register-id contiguity (`test_unmutated_results_checker_is_green_inside_a_worker`; T-231 is on #753).
- All four whole sweeps passed hosted: n27 338.92 s, n19 256.43 s, n20 200.55 s, n31 157.35 s of call.
- The lane's job wall was 1477 s (step 1418.5 s) against its 1250 s ceiling. That selection is recorded in the PR body: this lane chose it, for the hosted evidence of the four whole sweeps (OR-17).
- How to bring the lane back inside its ceiling is the decision think-znx8.

Waiting on:
1. #753's merge, the re-merge of main, and the explainer re-cut and re-pin (the coordinator's merge order). Then a certifying dispatch at that final head, with `deferred-slow-lane` read against its ceiling. Record the run in the PR body, and the selection again if the lane is still over.
2. think-znx8's choice and landing.

Done when the certifying run at the merge head is green but for nothing, its slow-lane wall is recorded against the ceiling in force, and think-znx8 is resolved or its selection recorded for that run.

## Notes

2026-10-24 c-land-745-1024 (landing lane of coord-intake-1023), PR #745:
- think-znx8 option (a) landed in 569ad25b5. packing/devtools/gate-budgets.yaml: deep-gate deferred-slow-lane re-recorded from dispatch 40033801674 at 1477 s (54 s setup, Step 1418.5 s at -n 4, 284 tests, 4,979.8 test-seconds; one contiguity failure, 23.9 s), spread 1.00, ceiling 1250 -> 1850 s (the least the gate's 1.25x drift band admits; about the Step's 1800 s cap plus setup); 921.7 s record moved to history; attribution (test-seconds) to the four nodes, n27 338.92, n19 256.43, n20 200.55, n31 157.35 (JUnit artifact 12536764221), with main's post-merge slow-lane at 1140 s without them (run 40034964765) and 698-1140 s across six main runs on 23 October. Gate wall re-recorded 1133 -> 1517 s (critical path now the slow lane; was screen 1111 s), attributed, ceiling 1900 s unchanged (1.25x). Post-merge slow-lane derived estimate 1250 -> 1850 s, still pending think-0atx. test_deep_gate_workflow.py reads both superseded walls (2540.6, 1133). development.md Validation Loops: one slow-lane paragraph. check_gate_budgets passes; 650 consumer tests pass.
- Certifying dispatch 40050481868 at final head d8138ad5f (gh workflow run deep-gate.yml --ref claude/intake-2026-10-23-lower-bounds): conclusion success, every deep job success. check_ci_gate_walls: deferred-slow-lane 1785 s of 1850 s (96%; 1.21x the 1477 s record, inside the 1.25x band); queue 18 s, setup 96 s, work 1684 s, Step 1680.3 s passed (288 tests, 4,739.6 test-seconds, 0 failures). The four sweeps 761.39 s (n19 233.74, n27 196.03, n20 183.21, n31 148.42). Gate wall 1838 s of 1900 s (97%). Reporting-only notes outside this change: regularized-views 592 s over its 450 s ceiling, resolve-tree 32 s over 30 s, atlas-grid 1.41x and controls-finer 1.38x of record.
- Risk for think-o8to: on 40050481868 xdist put all four sweeps on worker gw2 (span 1676 s; gw0, gw1, gw3 1102-1128 s); on 40033801674 they split two and two. The Step reached 93% of its 1800 s subprocess cap (FAST_SUITE_BUDGET_SECONDS), so a slower draw could time the Step out. Spreading the four across workers (an xdist group or their own job) is the cheap part of think-o8to.
- Done criteria met: the certifying run at the final head is green, its slow-lane wall is recorded against the ceiling in force (1785 / 1850 s), and think-znx8 is landed. Left open for the coordinator to close (with think-znx8) after review B; a re-merge before the merge invalidates this certification.
