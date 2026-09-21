---
type: is
id: is-01m32mqqnq9np89mnrpe07hgw3
title: gh run rerun --failed can never fix a pull-request wall failure; it guarantees a new one
kind: bug
status: open
priority: 2
version: 1
labels: []
dependencies: []
parent_id: is-01m32fgxn7yh0skf12a0zxnres
created_at: 2026-09-21T18:47:58.903Z
updated_at: 2026-09-21T18:47:58.903Z
---
Measured 2026-09-21 on PR 212, run 35639861454.

check_pr_wall.py measures the wall from the RUN's start to the start of the 'Hold the pull request's wall to its budget' step inside the aggregator. Re-running only the failed aggregator job (gh run rerun --failed) produces a run where every other job is a carried-over skip, so the measured wall collapses -- 10s on this attempt -- and the checker reports 'NOT JUDGED: neither the budget nor the regression rule was applied to this run' and exits 1, because an unmeasurable run fails even under advisory enforcement.

So the obvious operator response to a red pages-required is guaranteed to fail again, and the second failure looks like confirmation of the first. It is not: attempt 1 failed for an unrelated and genuine reason ('the jobs API reported live aggregator pages-required without a started ... step after 3 reads', i.e. API lag, failing closed as designed), and attempt 2 failed only because of how it was re-run.

Two things to decide:
1. Whether check_pr_wall should detect that it is running in a partial re-run (run_attempt > 1 with carried-over jobs) and say so, rather than reporting an unmeasurable wall as if the branch were at fault.
2. Whether the SETTLE_ATTEMPTS = 3 reads is enough for the pages aggregator. Attempt 1's failure is a pure API-visibility race on a step that had in fact started; the run was otherwise healthy and the same measurement passed locally against the same run id (77s, inside the 180s budget).

Operationally, until then: re-run the WHOLE run, or push, never --failed, for any wall failure.
