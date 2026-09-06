---
type: is
id: is-01m1vrrktbrd2scnaqfe40eby4
title: "W5 efficiency block: fast feedback and justified validation checkpoints"
kind: epic
status: in_progress
priority: 1
version: 23
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
updated_at: 2026-09-06T20:04:13.326Z
---
User-directed W5 efficiency block: audit end-to-end CI and long checkpoints, preserve independent coverage while reducing feedback latency, retain detailed timing evidence, align project documentation and naming, and prepare reusable upstream tbd guidance. The plan is docs/project/specs/active/plan-2026-09-06-validation-efficiency-and-checkpoints.md. The first implementation slice is PR98; explained family selection and safe reuse follow under think-xejq.

## Notes

PR98 is on b3b7275fc5b11dd788aecd9f8d1a2d8b9179de16, integrating main c14451f5378e55dd072327d6d8f55dc957fbc5c3 and parallel review 3d661e20. The working tree is clean. The current ordinary CI run 34056428243 passed in 2m56s; the site build 34056428215 passed with a 41s build job. Five timing artifacts were downloaded to /tmp/pr98-combined-fast-artifacts for source and coverage audit. Full checkpoint 34056585319 was requested only after ordinary CI passed and is running.

This first W5 slice implements two measured component improvements (three interleaved pairs each: medians 275.50s to 17.45s and 84.30s to 31.72s), detailed timing capture, bounded certificate workers, corrected configuration and limit-tool selection, linked documentation, and the upstream draft. These are component observations, not a statistical whole-CI speedup. Quick JUnit records all aggregate case times; quick console phase logs retain their 12s filter. All slow/exhaustive phases are retained on normal completion. Complete incremental phase records remain under think-uhxt.

The current-base full run 34054616340 failed on the deferred checkout lacking historical Git objects and the operating-rule mutation colliding with the newly added OR-16. Its 96 slow cases and 163 controls have complete failure records: 95 cases and 162 controls passed. Commit fc72f05e supplies full deferred history and computes the next contiguous rule inside the specific control. The actual historical review passed all six tests in 33.72s, and the real control passed in 0.476s. Three rule-count fixtures (16, 17, 25) verify the intended refusal and restoration. Main also has the same control failure until this repair lands. Cancelled checkpoints on superseded heads do not count as completed coverage.

The combined review retained all 409 archive evidence payloads byte-for-byte while removing AppleDouble metadata. New archive packing follows OR-16 and creates no checksum sidecars; existing legacy manifests remain checkable. Twenty archive-contract tests passed in 0.11s. The combined affected test selection passed 126 tests in 12.54s after isolating a fake-PID signal call. Static checks, documentation coverage for 526 durable documents, canonical handoff, gate budgets, and all 163 control anchors passed.

Historical checkpoints retain their actual source: bc65e779/edccf294 passed ordinary CI 34052688114 in 2m12s and full 34052836364 with 55 exhaustive cases in a 20m56s job (1234.35s pytest), plus 95 slow cases, 163 controls and n=40 replay in a concurrent 12m30s job. The preceding fb1a987d/edccf294 exhaustive job took 26m56s. Both have complete audited timing records; serial costs also changed, so the six-minute difference is not a causal worker-speedup claim. The earlier eff5587f/c14451f5 ordinary run took 3m03s, crossing the investigation trigger: exact verification ended last at 90.23s and T-022 replay alone took 52.13s.

After the final current-head full checkpoint passes and artifacts are audited, close completed first-slice beads think-9zr2, think-bd9v, think-z4jz, think-h2jx, think-4ah8 and think-a04i, and disposition the bounded profiling/allocation work in think-i2gk. Keep epic think-rwte and Phase 3 think-xejq open. Other open follow-ups are T-022 fast-path work think-efke, snapshot dependency/retention think-rx6p, incremental phases think-uhxt, and the parallel review's think-xs1p. Do not close the parallel agent's parent think-r9br blindly.

The 16-file upstream tbd patch is prepared and checked (97 focused tests, build, CLI discovery, type/lint/format and pristine application). Filing think-jogv awaits the owner's confirmation required by the contribution shortcut. PR93 was already reviewed, fixed, merged and validated. PR98 has no authorization for automatic merge. The task heartbeat verify-pr-98-validation-checkpoint continues CI monitoring and final records. Retain the temporary control worktree and integration stash; automatic approval review rejected their potentially destructive cleanup.

Final ordinary artifact audit: /tmp/pr98-combined-fast-artifact-audit.json verifies clean tested merge 3663706fdd25bc1ee379167599b6e1eb0dafdeaf and parents c14451f5/b3b7275f, 62 Linux fast steps plus four macOS steps, 145 complete command pairs, and 2,354 unique quick JUnit cases with no failures/errors/skips. Pytest took 108.33s; the slowest fast step took 109.14385s. All emitted quick phases match JUnit identities; subthreshold phases are not claimed as recorded. All five artifacts are present. The 2m56s workflow is still above the 2–2.5 minute target.
