---
type: is
id: is-01m6jgc9h4tk4s0h73jasbny19
title: "Review Özden's 299 and 204 certificates (stage 4) and adopt both with both regularizations (#893, #894)"
kind: task
status: closed
priority: 1
version: 3
labels:
  - validation
  - regularization
dependencies: []
parent_id: is-01m6jf7mh886ywnp58vnkzq8xb
child_order_hints:
  - is-01m6jrqgkrdfpxas3rpssbx5fx
created_at: 2026-11-04T05:26:46.052Z
updated_at: 2026-11-04T13:55:50.767Z
closed_at: 2026-11-04T13:55:50.767Z
close_reason: Imported, reviewed (strong-max stage 4), adopted at V3/C3 in https://github.com/jlevy/squares/pull/897 (merged 0dc4eaa7b); closing replies posted after deploy and recorded in https://github.com/jlevy/squares/pull/901 (merged c5e1f3da9).
resolution: null
duplicate_of: null
---
Stage 4 mathematical review of Doğa Özden's certificates at 299 (#893) and 204 (#894), registered on PR #897 (lane L36) at V0/C0, and their adoption at both counts under the house rule, each being the smallest side reported there.

## Validation
- Claim: s(299) <= 3560247706795812422293947620670679551/(2*10^35) by n-299-candidate.yaml at kenaznia-doga/s299-upper-bound@6486ead (packet ozden-s299-upper-bound-2026-11-03), 1.54e-8 below T-258; s(204) <= 7403810497792604009019579959/(5*10^26) by n-204-candidate.yaml at kenaznia-doga/s204-upper-bound@d4b8b05 (packet ozden-s204-upper-bound-2026-11-03), 6.48e-6 below T-257. Both rational centre-basis Witness/v2 files, read by upper_bound_reports' witness-center-basis adapter. Checkers: the two maintained exact routes (done on PR #897, with the duplicate-square and outside-container controls and the sharp controls at 1e-30 past contact; identity measured against T-258 and T-257), and a clean-room exact checker the reviewer writes.
- Run: a separately prompted tbd-strong-max review sub-agent, at maximum reasoning, in a worktree of its own, reading both packets as data and running only code it writes (result-import.md, stage 4, "Who reviews, and when"). It re-derives each certificate's feasibility exactly (every wall, every pair, by two methods, with sharp controls), reads the side against the issue's prints (#893's 12-place print 17.801238533979 is 6.21e-14 below the exact side, so the bound is the exact fraction; #894's 14.807620995586 rounds up correctly), checks the identity receipts against T-258's and T-257's packings and the lineage the issues state, and confirms or changes the draft significance S2; the review is written to be shared with the author, names no T-NNN not yet on main, and lands as docs/project/reviews/review-2026-11-04-ozden-893-894-299-204.md with its programs retained under the packets' review/ directories and registered in verifiers.yaml. Then the adoption at 299 and 204 on the same branch: select_houses, upper_bound_houses and adopt_houses, both strong generators on each re-housed count (regularize_evand run; regularize_grid_slack at 0.5, 1 and 5 degrees), regularize_select and layer, the render step and the flip, stamp_landed.
- Cost: the review about 0.05 CPU-hours (T-258's review: a clean-room checker over 44,551 pairs in minutes); the regularization 10 to 50 CPU-minutes for two counts (5 to 25 a count, result-import.md); an estimate.
- Budget status: runnable, under the owner's standing 40 CPU-hour item cap; the review is gated on the coordinator launching a separately prompted lane.
- Possible subset under the cap: not needed.
- Depends on: a strong-tier review lane the coordinator launches (the import lane may not review its own import).
- Done when: the review is mapped on both entries (reviews, external_review on the report evidence, the review's exact-feasibility evidence), check_results derives V3/C3, and both counts are adopted and regularized with select_houses --check, default_drawings --check-state --base-ref origin/main and flip_regularization --check passing.
- Machine note: minutes of CPU for the review; run the regularization apart from a gate, at most two cores.
