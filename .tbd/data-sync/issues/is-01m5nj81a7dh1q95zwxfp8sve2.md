---
type: is
id: is-01m5nj81a7dh1q95zwxfp8sve2
title: "PR #745 A2: certifying deep-gate run at the final head after #753; slow lane against its ceiling"
kind: bug
status: open
priority: 1
version: 1
labels: []
dependencies: []
parent_id: is-01m5ndfyhknd8p766m3pnpgn4a
created_at: 2026-10-23T23:41:25.191Z
updated_at: 2026-10-23T23:41:25.191Z
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
