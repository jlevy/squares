---
type: is
id: is-01m1w3p6hhmhnjqakekbqwa82f
title: Provide retained Git history to deferred review checks
kind: bug
status: closed
priority: 1
version: 5
spec_path: docs/project/specs/active/plan-2026-09-06-validation-efficiency-and-checkpoints.md
labels: []
dependencies: []
parent_id: is-01m1vrrktbrd2scnaqfe40eby4
created_at: 2026-09-06T19:38:54.384Z
updated_at: 2026-09-06T20:42:43.569Z
closed_at: 2026-09-06T20:41:54.284Z
close_reason: First-slice implementation landed in PR98. Ordinary run 34056428243 and full checkpoint 34056585319 passed on b3b7275f/c14451f5 with all seven timing artifacts audited. Separate post-merge validation of 8743cb0d plus PR100 continues under think-rwte; Phase 3 and documented timing/performance follow-ups remain open.
resolution: null
duplicate_of: null
---
The new slow Trump review reads exact retained theorem and archive bytes with git show. Both commits and paths exist, but the deferred workflow still uses a shallow checkout. PR98 run 34054616340 fails on the missing historical object; main integration fetches full history and passes. Provide fetch-depth: 0 for the deferred job and test this prerequisite without changing retained source bindings.

## Notes

First-slice implementation is complete in PR98. Ordinary CI 34056428243 and full checkpoint 34056585319 passed on head b3b7275fc5b11dd788aecd9f8d1a2d8b9179de16 with base c14451f5378e55dd072327d6d8f55dc957fbc5c3, testing clean merge 3663706fdd25bc1ee379167599b6e1eb0dafdeaf. All seven timing artifacts were audited: 62 fast steps and four macOS checks, 2,354 quick tests, 96 slow tests, 163 controls, n=40 replay, and 55 exhaustive cases passed. Ordinary workflow took 2m56s; deferred job 10m50s; exhaustive job 21m14s. All slow/exhaustive phases and command/step joins are complete. Quick JUnit records aggregate times; subthreshold console phases are not claimed as recorded.

The implementation preserves independent mathematical coverage, repairs repository-relative and limit-tool selection, records timings and failure evidence, reconciles project documentation, and fixes the historical-checkout prerequisite and evolving-rule mutation. Focused checks and the real repaired control passed before hosted CI. Detailed results and source-bound historical observations are in https://github.com/jlevy/squares/pull/98 and the linked W5 plan/report.

jlevy merged PR98 at 20:23:10 UTC as 8743cb0dce21314625f9a75f9934a600f21e6de9. That merge also includes PR100 via parent 6a064e3b, so its tree differs from the PR-tested source. Main run 34057826143 remains in progress; its result is tracked under think-rwte and the task heartbeat. Main deployment passed and the live-site check verified all 20 checks in 11.74s against the landed commit.

Closing these implementation items does not close W5. Explained family selection/reuse remains think-xejq, the T-022 fast-path investigation think-efke, complete incremental phase timing think-uhxt, snapshot retention think-rx6p, and upstream filing think-jogv pending owner approval. No statistical whole-CI speedup is claimed.
