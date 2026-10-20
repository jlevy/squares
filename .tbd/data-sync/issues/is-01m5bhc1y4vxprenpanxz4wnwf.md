---
type: is
id: is-01m5bhc1y4vxprenpanxz4wnwf
title: "Bound pytest temporary output: failed-only retention, reclaim killed sessions, shrink top writers"
kind: bug
status: in_progress
priority: 1
version: 9
spec_path: docs/project/specs/active/plan-2026-08-24-packing-engineering-maturity.md
delegate: lane-pytest-tmp
labels:
  - efficiency
dependencies: []
parent_id: is-01m0rrgqj3esjc4jx1fr3qy1ht
hold: null
hold_until: null
created_at: 2026-10-20T02:13:44.003Z
updated_at: 2026-10-20T06:29:12.465Z
started_at: 2026-10-20T02:13:48.451Z
---
Owner request 2026-10-20: 'fix the ongoing issue with filling up file systems with pytest junk? Either outputs should be smaller and/or cleaned up automatically'. On the remote host /tmp/pytest-of-root reached ~11 GB across ~19 basetemp dirs from runs on 15-16 Oct (pytest-N dirs 0.5-1.6 GB; pytest-132 had 1,325 entries and pytest-3 still existed with 450), filling the 39 GB root filesystem twice. pytest keeps 3 numbered sessions by default (policy 'all', whole trees) and treats a session's .lock as stale only after three days, so a session killed by SIGTERM/SIGKILL (validation deadline or cancel, agent command timeout) keeps its whole tree for three days: pytest-3 surviving 129 later sessions shows that. Fix: failed-only retention with an explicit count in packing's pytest config; reclaim numbered/garbage dirs whose lock names a dead process; measure per-test tmp_path bytes with a reusable tool and shrink the top writers where the test does not weaken; tests and a development.md note. Related: think-y3pe (fresh per-run external TMPDIR on the owner's host).

## Notes

2026-10-20 measurement (lane-pytest-tmp, worktree claude/ecstatic-edison-8en33t-pytest-tmp): full quick lane (19,178 passed) with devtools.pytest_tmp --tmp-usage, -n 2, failed-only retention: 4,669 tests with tmp_path held 2,326 MiB at teardown plus 707 MiB of tmp_path_factory dirs = 3,033 MiB per session that the default 'all' policy keeps (x3 sessions + killed ones). Top writers: test_replay_bc303_t1_witness full git clone 663 MiB in one test; negative-controls module snapshot 345 MiB; test_site_head published 95 MiB; calibration profile 57 MiB; archive annotations 31 MiB x10 tests. pytest's .lock is stale only after 3 days, so SIGTERM/SIGKILL'd sessions (validate's process-group stop, agent timeouts) keep whole trees. Fix in progress: retention failed/count 2, dead-PID lock release, sparse clone for bc303, scoped_tmp_path for module fixtures, per-test budget.

2026-10-20 (resumed after a container restart, lane-pytest-tmp): reviewed the WIP. PID-namespace gap fixed: each shared-root session writes `.lock-owner` (PID + PID namespace) beside its lock; a numbered directory's lock is released only when that record names the lock's PID, this namespace, and an exited process. `garbage-*` keeps the dead-PID rule (nothing live inside). Per-test tmp_path budget withdrawn: slow-lane tests write about 360 MiB by design (negative-controls build caches, fn1 input bindings, evand production clone), so one ceiling either misses a 660 MiB clone or fails them; follow-up bead to follow. Pushed 1f2190c46. Re-measuring the quick lane before (main b16ddeb0a, stock retention) and after.

2026-10-20 04:20Z: draft PR #695 opened at 6deda2581 (S1). Follow-up per-test ceiling: think-2vr1. Release impact: reviewed no-public-change records for packing/pyproject.toml (site, two papers).

2026-10-20 04:48Z baseline (main b16ddeb0a, stock retention all/3; quick lane -m 'not exhaustive_exact and not slow' over tests and ../packages/workbench/tests, -n 2 --dist=loadfile, nice 15, TMPDIR fresh, --tmp-usage-interval 5): one run left 3,188,596,736 B allocated (3.0 GiB, 133,846 files) in TMPDIR; stock keeps three sessions. Peak 3,605.5 MiB at 2,497 s (bc303 clone 1,382.9 MiB of it). Wall 2,795 s; 38 failures came from borrowing wt-pytest's venv (editable sqpack outside the measured checkout), which does not change what 'all' keeps. Branch run started 04:48Z. Measurement trees deleted after recording.

2026-10-20 05:50Z after (branch c6d82b2c7, same command): left 243,347,456 B allocated (232 MiB) because five load-sensitive tests failed (same failures as baseline); a passing run leaves nothing. Peak 346.7 MiB at 322 s (negative-controls snapshot). Wall 2,755 s. Tests' tmp_path at teardown 1,664 MiB (was 2,310). Merged main a5acd570 (99208e210), cut site v0.8.1 (28d4ab249) with the explainer link-revision disposal. --edit passes (373 s); --push running. Review requested via coordinator.

2026-10-20 06:35Z: Review A (id 5581265345) at 28d4ab249: A1-A6 fixed in 2a8a5f691 (boot+namespace scope, Linux only; long locks in doubt; private-root and O_NOFOLLOW dir-fd checks; rename-reverify unlink; record written by getbasetemp; docs wording and command); A7 declined with reasons. Dispositions: https://github.com/jlevy/squares/pull/695#issuecomment-6284737935. Follow-up think-652x (macOS). --edit passes at 2a8a5f691; --push at 28d4ab249 timed out at 1800 s (71% of the quick lane, shared host). Round B requested.

2026-10-20: main 4b8aec9a6 took site v0.8.1 (#688). Merged main at 5998d0c3d (main's claim docs and release history; dropped this branch's v0.8.1 cut and explainer record), re-cut site v0.8.2 at 3d39c2032 with a new explainer link-revision record (a7fb8f2e -> 5998d0c3). check_release_impact, release_pin --check, test_pytest_tmp (18), --edit (377 s) pass. Pushed 3d39c2032; PR MERGEABLE; hosted CI started.
