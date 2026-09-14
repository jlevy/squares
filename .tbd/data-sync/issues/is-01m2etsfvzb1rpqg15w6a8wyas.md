---
type: is
id: is-01m2etsfvzb1rpqg15w6a8wyas
title: Integrate the worker-exit and launch-window test race fixes into the stack top
kind: task
status: closed
priority: 1
version: 4
spec_path: docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md
labels:
  - n11
  - validation
  - landing
dependencies:
  - type: blocks
    target: is-01m2ett16m2gz30tsat10zhshr
parent_id: is-01m2etr75jfh3t3ry7kj1ccqrb
created_at: 2026-09-14T02:08:59.261Z
updated_at: 2026-09-14T03:09:15.193Z
closed_at: 2026-09-14T03:09:15.192Z
close_reason: "PR #168 merged into codex/n11-floor-normalized-t2-exploration at 1ea28da4 (hosted checks green: suite, geometry, sweeps, validate, macOS, packing-required). #167 back-merged at 0ea34d98."
resolution: null
duplicate_of: null
---
Integrate the test-only CI stabilization change into the stack top before the full merge checkpoint.

Branch claude/n11-stack-ci-stabilization (based on #166 head 21d511f8), commit 717291d8, changes only two test files; no production module and no BC329 source-closure path:

1. packing/tests/test_fractional_threshold_interval.py::test_real_forked_callback_failure_requests_and_observes_worker_exit (think-glad): after `pool.terminate_workers()`, CPython 3.14's executor manager thread joins the same worker Process objects (`_join_executor_internals`, both the shutdown and `terminate_broken` paths). Two reapers race: the losing `waitpid` gets ECHILD, which `popen_fork.poll()` maps to `None` without setting `returncode`, so a dead worker reads alive. A local diagnostic (two threads joining one forked child) read a dead child as alive in 640/2000 and 549/2000 trials; joining the other reaper first gave 0/2000. The control now captures the manager thread, joins it under a 10 s bound, then requires every worker's exit code, killing stragglers in `finally`.
2. packing/tests/test_fixed_core_packet_calibration.py: the supervisor script published its pid file with a non-atomic write that `test_real_supervisor_signal_reaps_worker_including_launch_window` could read empty (now published by `os.replace`); `test_each_execution_checkpoint_remains_partial_when_terminated` could terminate before the first RSS sample when launch outlasted 0.08 s (now widens the window only while no sample was taken, asserting the partial timeout receipt on every attempt, 10 s bound).

Exit: PR opened against codex/n11-floor-normalized-t2-exploration, hosted checks green, merged into the #166 branch (owner or #166 session), and #167 back-merged. Then close think-glad and this bead.

2026-09-14 addendum: with calibration deferred (think-zwlf), the macOS EPERM reaper fix (think-tdfl, commit 1f43e5c6) joins this branch. It touches packing/devtools/calibrate_fixed_core_packet.py and packing/devtools/fixed_core_packet.py (BC329 source closure); no calibration receipt exists, so none is invalidated. Close think-tdfl's packet-reaper part when merged. CI tier headroom work (checks rollup start_early and suite slow markers) is being measured for the same branch; see the budget beads.
