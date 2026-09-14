---
type: is
id: is-01m2eph4pfcjjjaam7hsjfy4k2
title: Stabilize Linux fork-worker exit assertion in hosted suite
kind: bug
status: in_progress
priority: 2
version: 5
spec_path: development.md
refs:
  - kind: other
    url: https://github.com/jlevy/squares/actions/runs/34793833499
    at: 2026-09-14T00:59:32.714Z
labels:
  - validation
  - linux
dependencies:
  - type: blocks
    target: is-01m2em2x6rf1he27b64856ny7z
created_at: 2026-09-14T00:54:31.373Z
updated_at: 2026-09-14T01:18:36.839Z
---
PR #166 hosted suite attempt on exact documentation-only head 21d511f8 failed tests/test_fractional_threshold_interval.py::test_real_forked_callback_failure_requests_and_observes_worker_exit at line 879: after a synthetic callback failure and process.join(timeout=5), one ForkProcess remained is_alive. The same run passed 5,398 tests and other required jobs; PR #165 at the identical code base and the PR166 exact local push gate passed. GitHub run 34793833499, suite job 103822994286, first attempt; a failed-job rerun was requested. Diagnose whether fork from an xdist worker with live threads, cleanup sequencing, or a genuinely leaked child explains this; retain a test that checks termination without an arbitrary timing race. Do not weaken worker-reaping guarantees or misattribute this docs-only PR as changing the behavior.

## Notes

2026-09-13/14 independent diagnosis on exact docs-only PR166 head 21d511f8: hosted run 34793833499 attempt 1 suite job 103822994286 and attempt 2 suite job 103823870438 both fail test_fractional_threshold_interval.py:879 after join(timeout=5), ForkProcess-4 alive (PIDs 3625 and 3420); both 5,398 passed, 6 skipped, xdist -n4 gw1, multithreaded-fork warning. PR165 head 93c5e217 has identical test blob d5b22c55 and implementation blob 74bf50eb and passing suite job 103819328059; PR166 changes only docs/records. Current logs prove live at five seconds, not omitted signal or permanent leak. CPython 3.14.7 terminate_workers is asynchronous attempt: shutdown(wait=False), then signal living workers. Recommended next: isolated diagnostic test branch records attempted PIDs/signals, elapsed/exitcode, /proc State/SigBlk/SigIgn/SigCgt at deadline, kills/reaps any straggler in finally; run targeted Linux -n0 and -n4 repeated. Fix scheduler if missing signal; otherwise isolate real-fork exit control from multithreaded xdist while retaining actual exit assertion and process-group watchdog. Full report /private/tmp/pr166-fork-worker-suite-diagnosis.md. No PR edit/push.

2026-09-14 diagnostic scratch branch codex/think-glad-linux-diagnostic from exact PR166 21d511f8: commit 47a68e52 added only failing-test instrumentation (record BaseProcess.terminate PID/time, original 5-second real-exit assertion, /proc state on failure, bounded kill/join cleanup) plus push-only Linux diagnostic workflow. Run 34795020799: isolated exact test passed 10/10 -n0 and 10/10 -n4; -n4 still warned about fork from multithreaded worker. Workflow follow-up commit 351f14f4 changed only scratch workflow to one normal hosted suite command, with 20-minute bound and retained validation artifacts. Run 34795179214 suite job 103826750568: 5,399 passed, 6 skipped, 12 warnings in 246.22s; the fork test ran and its original assertion did not reproduce. Passing log does not reveal whether BaseProcess.terminate was called because recorded attempts render only on failure. This is one full-suite nonreproduction, not clearance of two PR166 hosted failures. PR166 untouched. See /private/tmp/think-glad-linux-n0.log, /private/tmp/think-glad-linux-n4.log, /private/tmp/think-glad-linux-full-suite.log and run URLs above.
