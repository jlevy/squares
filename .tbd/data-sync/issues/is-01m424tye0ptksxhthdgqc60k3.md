---
type: is
id: is-01m424tye0ptksxhthdgqc60k3
title: The typecheck tier's 111 s wall ceiling sits inside hosted-runner variance
kind: task
status: closed
priority: 2
version: 10
delegate: claude-code@vm
labels:
  - ci
dependencies: []
parent_id: null
hold: null
hold_until: null
created_at: 2026-10-04T00:25:48.735Z
updated_at: 2026-10-04T08:12:20.970Z
started_at: 2026-10-04T08:03:08.205Z
closed_at: 2026-10-04T08:12:20.970Z
close_reason: "Fixed by #338 (merged): ceiling 130 s, record 86.71 s, band 54-123 s."
resolution: null
duplicate_of: null
---
Hosted typecheck tier walls (basedpyright alone, --jobs 1) read on 3-4 October 2026 across eight branches: 59.6, 80.7, 81.4, 81.8, 93.8, 96.2, 98.8, 104.0, 105.2, 105.7, 106.6, 107.5, 108.2, 108.2, 108.9, 110.9, 114.9 and 115.2 s against a 111 s ceiling (recorded 76.5 s). The same Python tree read 107.5 s and then 115.2 s on consecutive runs (PR 305 at d56b9f503 and 0952efb57, which differ only in a Markdown record), so the breaches are runner variance, not code: the distribution is bimodal near 80 and 105-115 s. Each breach costs a re-run, and a partial re-run then makes check_pr_wall unmeasurable, which fails packing-required. Decide: re-derive the ceiling from these readings under gate-budgets.yaml's rule, make the typecheck wall advisory like the PR wall (think-g4n9), or reduce basedpyright's cost.

## Notes

2026-10-04: the full re-run of PR 305's run 37164605808 (attempt 3, same commit 0952efb57) read 70.67 s, 44.5 s below the breaching attempt's 115.20 s.
2026-10-04: PR 323 at 3b1dde308 read 119.63 s (fail; its one re-run already spent), PR 305 at 99defa2ea 80.99 s (pass). Local, back to back on one idle host, basedpyright --stats Check: 176.6 s on main d303e9ef8 (1,339 files) and 176.2 s on PR 305's head (1,357 files; 180.7 s on an earlier run), so the branch adds no measurable type-check cost. Files over 3 s to check, all main's: contact_realization.py 10.1 s, build_candidate.py 5.4 s, cover.py 3.5 s.

2026-10-04 01:05 UTC: moved out from under think-gmef to the top level. think-gmef was closed at 00:37 UTC with this bead open, and an open bead under a closed parent fails check_bead_tree (D-025's first invariant) in every pull request's validate job (jlevy/squares#315 at 6c5036895). Kept open as the owner decision it is; re-parent it wherever it belongs.
2026-10-04 01:55 UTC (import coordinator): more breaches with 0 type errors: PR 328 run 37158946117 at 114.8 s and PR 332 run 37169296592 at 116.4 s (PR 332 changes no Python: census data and SOUNDNESS.md only); passes on PR 328 at 93.8 s and about 105 s. A partial re-run of the typecheck job alone then fails packing-required as unmeasurable (check_pr_wall), so the only clean recovery is a full re-run. Duplicate think-xlxj closed into this bead. Candidate fixes for the owner: run basedpyright with parallel threads if the pinned 1.39.10 supports it, re-record the ceiling on a measured distribution, or split the program.

2026-10-04 08:03 UTC (think-pr19, PR jlevy/squares#338): decided. #338 raises the typecheck ceiling from 111 s to 130 s and re-records the tier on the hosted serial cohort, commit b13c82ad7 on top of fca477d3d (not yet pushed when this was written). Cohort: 174 jobs-API walls of the type-floor step, every completed pull-request run 2026-10-02T07:49Z to 10-04T06:21Z on 17 branches, read with check_pr_wall's per-job split. Median 93.5 s, p90 111 s, max 123 s, geometric mean 86.71 s, band 54-123 s, two regimes (medians 69 and 104 s). 8% of runs read over 111 s; 3-6% breached it at the gate's figure (1.5-3.4 s under step time). New record 86.71 s, band 54/123, ceiling 130 s (1.50x the record, under the 184.5 s drift edge, setup plus step 174 s against OR-14's 180 s). The 76.5 s record moves to history with an attribution of no step grew. Parallel basedpyright (--threads 4) was tried in fca477d3d and rejected: 90.46 s on its only hosted run (37185790574, job 111387285346), 0.75-0.79x on a reviewer's box, and a hang until the 900 s timeout when a worker dies. No pending fields reference this bead any more. Close it when #338 merges.
