---
type: is
id: is-01m15j7cjmd67c2a0meabjttc4
title: Wall-clock assertions make the run-timeout test flake under load
kind: bug
status: open
priority: 3
version: 1
labels: []
dependencies: []
created_at: 2026-08-29T01:30:25.739Z
updated_at: 2026-08-29T01:30:25.739Z
---
`tests/test_validation_cli.py::test_run_timeout_terminates_child_and_reports_captured_output` asserts `1 <= elapsed < 3` around a 0.25s timeout, and reads a pid file the child writes.

On 2026-08-28, with the machine at load average 26-42, it failed with FileNotFoundError on that pid file: the child never got scheduled far enough to write it. It passes in 2.33s in isolation at load 8.5.

This is pre-existing and unrelated to the repository reorg -- the test file is byte-identical across that move, and the code it exercises (subprocess timeout handling) was not touched. Recording it because a bounded wall-clock assertion will flake the same way on a busy CI runner, where it reads as a real failure and teaches people to re-run rather than look.

Worth either widening the bound, retrying on the pid-file read, or asserting on ordering rather than elapsed time.
