---
type: is
id: is-01m1tshbfjj9ydt1gbb7w5h9cz
title: "test_colgen_checkpoint: the clock-stop test is timing-dependent and fails on the two-core pull-request runner"
kind: bug
status: in_progress
priority: 2
version: 2
labels: []
dependencies: []
created_at: 2026-09-06T07:22:15.409Z
updated_at: 2026-09-06T07:49:10.799Z
---
tests/test_colgen_checkpoint.py::test_a_clock_stop_between_column_rounds_keeps_the_converged_optimum measures a full run's wall time, then reruns with deadline_seconds at fractions 0.2 to 0.7 of it and asserts converged_at_column is an int whenever any round completed. On PR #94's validate job (run 34018542490, 2026-09-06, -n 2 on a two-core runner) it failed at that assertion (converged_at_column was None with rounds non-empty). The branch does not touch colgen. A run that stops after a row loop but before the first column round converges has rounds and no converged column; the test should accept that state (converged False, frozen None) or pin the deadline to a round count rather than a wall fraction. Reproduce with a loaded machine or by shrinking elapsed.
