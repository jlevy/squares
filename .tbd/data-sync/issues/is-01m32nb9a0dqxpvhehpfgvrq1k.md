---
type: is
id: is-01m32nb9a0dqxpvhehpfgvrq1k
title: check_pr_wall SETTLE_ATTEMPTS=3 produces false reds on GitHub API lag
kind: bug
status: closed
priority: 2
version: 4
labels: []
dependencies: []
parent_id: is-01m32fgxn7yh0skf12a0zxnres
created_at: 2026-09-21T18:58:39.551Z
updated_at: 2026-10-06T08:45:23.081Z
closed_at: 2026-10-06T08:45:23.081Z
close_reason: "Done: packing/devtools/check_pr_wall.py on origin/main raises SETTLE_ATTEMPTS from 3 to 11 reads 5 s apart (up to 50 s), and reports runs GitHub did not schedule in full as an 'infrastructure' verdict."
resolution: null
duplicate_of: null
---
Observed 2026-09-21 on PR 212, run 35639861454 attempt 1: 'the jobs API reported live aggregator pages-required without a started Hold the pull request wall to its budget step after 3 reads'. The step had in fact started; the run was healthy; the same measurement run locally against that exact run id returned 77s, inside the 180s budget, verdict passed.

So a fail-closed check turned an API visibility race into a red pull request. Failing closed is right in principle -- an advisory wall nobody could measure is a wall nobody sees -- but three reads is not enough for the pages aggregator.

Adjacent to think-vq1s (re-running with --failed guarantees a second, different failure) and to the OR-17 work generally: this is a gate costing wall time without adding evidence.

## Notes

Second occurrence 2026-09-30 on PR jlevy/squares#249, run 36722105366 attempt 1 (head 9f1a7f52a): the same 'without a started Hold the pull request's wall to its budget step after 3 reads' message, every pages job green. check_pr_wall --workflow certificate-page run locally against that run id measured 159 s inside the 180 s budget, verdict passed. The whole-run re-run (attempt 2) failed the same way, and so did both aggregators (pages-required, packing-required) on the next head 4548eb2ed. Root cause that time was not the settle window: from about 13:30Z, GitHub's jobs API returned an empty steps list for every job of every new run, completed ones included (the 13:09Z runs list them all); githubstatus.com showed no incident. So a larger SETTLE_ATTEMPTS would not have helped. Proposed: name 'the jobs API reports no steps for any job' as its own refusal message, so the red says what GitHub did rather than blaming the settle window.
