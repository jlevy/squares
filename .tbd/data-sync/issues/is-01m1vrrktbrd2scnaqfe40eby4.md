---
type: is
id: is-01m1vrrktbrd2scnaqfe40eby4
title: "W5 efficiency block: fast feedback and justified validation checkpoints"
kind: epic
status: in_progress
priority: 1
version: 25
spec_path: docs/project/specs/active/plan-2026-09-06-validation-efficiency-and-checkpoints.md
labels: []
dependencies: []
child_order_hints:
  - is-01m1vs0edeyqrwptpsptt58v5g
  - is-01m1vs0eqdcqrwf10x8c12xpx7
  - is-01m1vs0f1y49w553rmafgad17k
  - is-01m1vs7vtqsgtnh2m15kc2bw49
  - is-01m1vs7w5wfpwqd5t6z4rmspsx
  - is-01m1vx5qqympzq5pscw414qbap
  - is-01m1w0r4wr8dbry9hazjg0y4nk
  - is-01m1w2ae90hg0fbnanrtehvt8r
  - is-01m1w2rtgc5pv5cvzer6xv0pb2
  - is-01m1w3p66wndg39qyhm4crvgn1
  - is-01m1w3p6hhmhnjqakekbqwa82f
  - is-01m1w1x2hxn7was5jgcheqeyh9
created_at: 2026-09-06T16:27:59.178Z
updated_at: 2026-09-06T20:41:55.001Z
---
User-directed W5 efficiency block: audit end-to-end CI and long checkpoints, preserve independent coverage while reducing feedback latency, retain detailed timing evidence, align project documentation and naming, and prepare reusable upstream tbd guidance. The plan is docs/project/specs/active/plan-2026-09-06-validation-efficiency-and-checkpoints.md. The first implementation slice is PR98; explained family selection and safe reuse follow under think-xejq.

## Notes

PR98 was merged by jlevy at 20:23:10 UTC as 8743cb0dce21314625f9a75f9934a600f21e6de9. Its parents are 6a064e3b0daa9771570e99e56386d912b3ba11b2 (PR100 mathematical changes) and b3b7275fc5b11dd788aecd9f8d1a2d8b9179de16. The landed tree differs from the completed PR checkpoint's tree. Main validation 34057826143 is in progress; it was created 20:23:13 and its first jobs started 20:36:10, after 12m57s in the serialized main queue. Its predecessor 34057077924 failed only the old OR-16 control. The current merge contains the identical fix already verified on PR98. The older run finished naturally at 20:36:08; no cancellation was performed.

The complete PR checkpoint passed on clean tested merge 3663706fdd25bc1ee379167599b6e1eb0dafdeaf, parents c14451f5 and b3b7275f. Ordinary CI 34056428243 passed in 2m56s with 62 fast steps, four macOS checks, 2,354 quick cases and 145 complete command pairs; pytest 108.33s. Deferred checkpoint 34056585319 passed 96 slow cases, all 288 phase rows, all 163 controls and n=40 replay in a 10m50s job; pytest 628.97s, control journal 334.81s, n=40 163.73s. Exhaustive passed all 55 unchanged case identities and 165 phase records in a 21m14s job; pytest 1251.16s. All seven PR timing artifacts and source joins were audited. Quick JUnit records aggregate case times; its console phase filter remains 12s, so complete quick-phase attribution is not claimed.

Main deployment 34057826146 passed: 36s build and 8s deploy. The maintained deployed-site check passed all 20 checks in 11.74s against 8743cb0d, including page/Markdown edition, 14-page PDF, assets and commit-bound repository links. Timing receipts are in /tmp/pr98-post-merge-smoke. Post-merge mathematical validation remains distinct from this live-site result and the prior PR checkpoint.

Completed first-slice items are think-9zr2, think-bd9v, think-z4jz, think-h2jx, think-4ah8 and think-a04i; bounded profiling/allocation think-i2gk is dispositioned separately. The PR contains the component improvements, timing instrumentation, selector repairs, workflow prerequisites, documentation and upstream draft. Three interleaved pairs measured component medians 275.50s to 17.45s and 84.30s to 31.72s. Full hosted observations of 26m56s, 20m56s and 21m14s are source-bound descriptions, not statistical whole-CI speedup estimates. Source/cost limitations remain explicit in the PR and frozen experiment records.

Keep W5 and Phase 3 think-xejq open. The next slice covers explained exhaustive-family planning and complete fresh/reused coverage, bounded scheduling and n=40 duplication, plus queue admission so quick feedback is not held behind a full older main run. Other open work: T-022 fast path think-efke, incremental phases think-uhxt, snapshot dependency/retention think-rx6p, and the parallel review's think-xs1p. Do not close the parallel agent's parent think-r9br blindly.

Upstream think-jogv remains approval-pending. The concrete 16-file patch and linked proposal already separate queue, setup, execution and total work and qualify unconditional full pre-push guidance; 97 focused checks, build, type/lint/format, CLI discovery and pristine apply-check passed. No upstream filing is authorized yet. PR93 was already reviewed, fixed, merged and validated. The task heartbeat verify-pr-98-validation-checkpoint now owns post-merge CI, any authorized failure repair, artifact review and final record updates; stop only after main validation and completion records are verified. Preserve the temporary control worktree and integration stash because automatic approval review rejected their cleanup.
