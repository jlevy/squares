---
type: is
id: is-01m5j2m3qtx5xht7ztsn51nx52
title: check_pr_wall's live fallback refuses a running PR attempt when GitHub's API reports the run or aggregator as queued
kind: bug
status: open
priority: 2
version: 2
labels:
  - tooling
dependencies: []
created_at: 2026-10-22T15:10:40.377Z
updated_at: 2026-10-22T18:23:40.817Z
---
Found 2026-10-22 by c-lane-tooling-1022 on jlevy/squares#723; #722 shows the same signature in the same window.

Between 14:20Z and 15:04Z every PR aggregator failed in "Hold the pull request's wall to its budget", while every prerequisite passed:

- #723: `packing-required` and `pages-required` in runs 39793420644 and 39793420636, attempts 1 and 3.
- #722: runs 39795857108 and 39795857112.

Attempt 1 printed `check_pr_wall: the live invocation does not match this PR aggregator and run attempt` about 58 s after the step began, which is the 11 x 5 s settle loop in `_settled_jobs` followed by the refusal in `_admit_live_step_upper_bound` (`packing/devtools/check_pr_wall.py`). Attempt 3 printed the same refusal.

## Cause, observed on attempt 3

The runs and jobs endpoints were reading minutes behind. I polled every 3 s with `gh api`:

- `actions/runs/39793420644` reported `status: queued` from 14:53:20 to 15:01:27, while its jobs had been `in_progress` since 14:52:53.
- It reported `queued` again from 15:02:57 to 15:08:05. That covers the whole wall step (15:03:01 to 15:04:03).
- Through the same window, `jobs?filter=latest` listed `packing-required` as `queued` with no steps. Its steps first appeared, already completed, at 15:08:05.

So the settle loop never saw the wall step start, and the fallback refused on `run.get("status") != "in_progress"`: the run read `queued`. It never measured a wall, so no budget was involved.

A failed-jobs-only re-run cannot pass either. Attempt 2 re-ran only the aggregators and reported "the jobs API did not report the aggregator's required prerequisite set after 11 reads (missing: geometry, measure-verifier, suite-a, ...)".

## To decide

Whether the fallback may accept a run or aggregator that the API reports as `queued`. `GITHUB_RUN_ID`, `GITHUB_RUN_ATTEMPT` and `GITHUB_JOB` already prove the process runs inside that live attempt, and only `completed` would contradict liveness. The `aggregator.get("status") != "in_progress"` test in the timestamp check has the same exposure.

The alternatives are a longer settle window, or naming the mismatched field in the refusal so the next occurrence is diagnosable without polling.

## Notes

2026-10-22 c-lane-tooling-1022: a second form of the same API staleness, on #723's head `e35898d58`. Packing validation run 39827928106 had every prerequisite succeed.

- `packing-required` started at 18:15:44Z. Its wall step exited 1 with "verdict: unmeasurable": "NOT JUDGED: `frontend` has not completed (in_progress)".
- The aggregator's own `needs` context, printed in that step, records `"frontend": {"result": "success"}`. `frontend` is in its `needs`, so it had finished before the aggregator could start.
- The jobs API still listed `frontend` as `in_progress` with no `completed_at` at 18:23Z.
- githubstatus.com had an unresolved incident, "Errors loading Issues, Pull Requests, and search results", investigating since 15:28Z.

Exit 1 here is the measured "unmeasurable" verdict, not the identity refusal (exit 2). A fix could take prerequisite results from `needs` (already passed in as `EXPECTED_PREREQUISITES`) when the jobs API lags, or settle longer.
