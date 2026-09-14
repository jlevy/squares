---
type: is
id: is-01m2eph4pfcjjjaam7hsjfy4k2
title: Stabilize Linux fork-worker exit assertion in hosted suite
kind: bug
status: open
priority: 2
version: 3
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
updated_at: 2026-09-14T01:00:14.281Z
---
PR #166 hosted suite attempt on exact documentation-only head 21d511f8 failed tests/test_fractional_threshold_interval.py::test_real_forked_callback_failure_requests_and_observes_worker_exit at line 879: after a synthetic callback failure and process.join(timeout=5), one ForkProcess remained is_alive. The same run passed 5,398 tests and other required jobs; PR #165 at the identical code base and the PR166 exact local push gate passed. GitHub run 34793833499, suite job 103822994286, first attempt; a failed-job rerun was requested. Diagnose whether fork from an xdist worker with live threads, cleanup sequencing, or a genuinely leaked child explains this; retain a test that checks termination without an arbitrary timing race. Do not weaken worker-reaping guarantees or misattribute this docs-only PR as changing the behavior.
