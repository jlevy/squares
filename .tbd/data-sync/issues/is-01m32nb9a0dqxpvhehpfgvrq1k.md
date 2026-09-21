---
type: is
id: is-01m32nb9a0dqxpvhehpfgvrq1k
title: check_pr_wall SETTLE_ATTEMPTS=3 produces false reds on GitHub API lag
kind: bug
status: open
priority: 2
version: 1
labels: []
dependencies: []
parent_id: is-01m32fgxn7yh0skf12a0zxnres
created_at: 2026-09-21T18:58:39.551Z
updated_at: 2026-09-21T18:58:39.551Z
---
Observed 2026-09-21 on PR 212, run 35639861454 attempt 1: 'the jobs API reported live aggregator pages-required without a started Hold the pull request wall to its budget step after 3 reads'. The step had in fact started; the run was healthy; the same measurement run locally against that exact run id returned 77s, inside the 180s budget, verdict passed.

So a fail-closed check turned an API visibility race into a red pull request. Failing closed is right in principle -- an advisory wall nobody could measure is a wall nobody sees -- but three reads is not enough for the pages aggregator.

Adjacent to think-vq1s (re-running with --failed guarantees a second, different failure) and to the OR-17 work generally: this is a gate costing wall time without adding evidence.
