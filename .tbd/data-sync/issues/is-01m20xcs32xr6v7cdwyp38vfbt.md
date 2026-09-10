---
type: is
id: is-01m20xcs32xr6v7cdwyp38vfbt
title: The exhaustive tier is one serial pytest and most of its tests do not use the inner pool
kind: task
status: open
priority: 2
version: 1
labels: []
dependencies: []
created_at: 2026-09-08T16:25:06.401Z
updated_at: 2026-09-08T16:25:06.401Z
---
`_exhaustive_exact_tests` in `sqpack/cli/validate.py` runs `pytest -m "slow or exhaustive_exact"`-style selection in one process with no `-n`, unlike both behavioural lanes and (after D-485) the pre-push tier. In CI the job passes `--jobs 1 --inner-jobs 4`, so the parallelism is meant to come from inside the tests.

Evidence that most of it does not arrive. On run 34214731500 (main at 33cd4760) the exhaustive job cost 1668.47s by the gate's clock, and pytest's own line for the same process reads "55 passed, 4246 deselected in 1666.88s" — so the step is one serial pytest and its wall is the sum of its tests by construction. Of the files holding its heaviest tests, only `tests/test_fractional_sweep_integer.py` (223.44s) reads `sqpack.workers.worker_count`; the single longest, `tests/test_n40_rigidity.py::test_the_record_round_trips` at 250.73s, does not, nor do the four `test_fractional_interval.py` members at 106.98/90.03/53.86/26.96s or `test_minimal_verify.py` at 77.50s. So for most of twenty-eight minutes a four-cpu runner is running one busy cpu.

This matters because the exhaustive job is the second-longest job in the post-merge gate and one of the two that set its wall (1691s of job wall against `validate`'s 1819s on that run).

What to measure before changing anything: (a) actual cpu utilisation of the job, which the timing artifacts do not currently carry; (b) the wall under `-n 2` or `-n 4` with `--inner-jobs` reduced so the pools and the workers do not multiply (BC-218 is the oversubscription lesson, and D-484's screen readings are the warning that more workers is not automatically faster); (c) whether any exhaustive test is order- or resource-coupled in a way that xdist's `--dist load` would break. D-472 applies: one reading per shape is a sample.

Found by the same sweep that produced D-485, which checked all five pytest call sites in the gate. The `--collect-only` probe in the slow lane's exit-5 handler is correctly serial; the two lanes carry the distribution; this one and the push tier did not.
