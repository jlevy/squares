---
type: is
id: is-01m5bhc1y4vxprenpanxz4wnwf
title: "Bound pytest temporary output: failed-only retention, reclaim killed sessions, shrink top writers"
kind: bug
status: in_progress
priority: 1
version: 5
spec_path: docs/project/specs/active/plan-2026-08-24-packing-engineering-maturity.md
delegate: lane-pytest-tmp
labels:
  - efficiency
dependencies: []
parent_id: is-01m0rrgqj3esjc4jx1fr3qy1ht
hold: null
hold_until: null
created_at: 2026-10-20T02:13:44.003Z
updated_at: 2026-10-20T04:16:05.840Z
started_at: 2026-10-20T02:13:48.451Z
---
Owner request 2026-10-20: 'fix the ongoing issue with filling up file systems with pytest junk? Either outputs should be smaller and/or cleaned up automatically'. On the remote host /tmp/pytest-of-root reached ~11 GB across ~19 basetemp dirs from runs on 15-16 Oct (pytest-N dirs 0.5-1.6 GB; pytest-132 had 1,325 entries and pytest-3 still existed with 450), filling the 39 GB root filesystem twice. pytest keeps 3 numbered sessions by default (policy 'all', whole trees) and treats a session's .lock as stale only after three days, so a session killed by SIGTERM/SIGKILL (validation deadline or cancel, agent command timeout) keeps its whole tree for three days: pytest-3 surviving 129 later sessions shows that. Fix: failed-only retention with an explicit count in packing's pytest config; reclaim numbered/garbage dirs whose lock names a dead process; measure per-test tmp_path bytes with a reusable tool and shrink the top writers where the test does not weaken; tests and a development.md note. Related: think-y3pe (fresh per-run external TMPDIR on the owner's host).

## Notes

2026-10-20 measurement (lane-pytest-tmp, worktree claude/ecstatic-edison-8en33t-pytest-tmp): full quick lane (19,178 passed) with devtools.pytest_tmp --tmp-usage, -n 2, failed-only retention: 4,669 tests with tmp_path held 2,326 MiB at teardown plus 707 MiB of tmp_path_factory dirs = 3,033 MiB per session that the default 'all' policy keeps (x3 sessions + killed ones). Top writers: test_replay_bc303_t1_witness full git clone 663 MiB in one test; negative-controls module snapshot 345 MiB; test_site_head published 95 MiB; calibration profile 57 MiB; archive annotations 31 MiB x10 tests. pytest's .lock is stale only after 3 days, so SIGTERM/SIGKILL'd sessions (validate's process-group stop, agent timeouts) keep whole trees. Fix in progress: retention failed/count 2, dead-PID lock release, sparse clone for bc303, scoped_tmp_path for module fixtures, per-test budget.

2026-10-20 (resumed after a container restart, lane-pytest-tmp): reviewed the WIP. PID-namespace gap fixed: each shared-root session writes `.lock-owner` (PID + PID namespace) beside its lock; a numbered directory's lock is released only when that record names the lock's PID, this namespace, and an exited process. `garbage-*` keeps the dead-PID rule (nothing live inside). Per-test tmp_path budget withdrawn: slow-lane tests write about 360 MiB by design (negative-controls build caches, fn1 input bindings, evand production clone), so one ceiling either misses a 660 MiB clone or fails them; follow-up bead to follow. Pushed 1f2190c46. Re-measuring the quick lane before (main b16ddeb0a, stock retention) and after.

2026-10-20 04:20Z: draft PR #695 opened at 6deda2581 (S1). Follow-up per-test ceiling: think-2vr1. Release impact: reviewed no-public-change records for packing/pyproject.toml (site, two papers).
