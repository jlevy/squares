---
type: is
id: is-01m2y4rc2vd88gs3aht7295an5
title: Size workers for costly partial pre-push test selections
kind: task
status: open
priority: 2
version: 4
labels: []
dependencies: []
created_at: 2026-09-20T00:51:44.858Z
updated_at: 2026-09-20T01:34:17.246Z
---
Session 142 exposed a local scheduling gap at 4c202aeb: `packing-validate --push --since 2aaa296d` selected 72 of 350 test files, including expensive atlas and evidence tests, but ten implicit outer jobs left pytest serial under the 900-second command cap. Every non-test step passed; pytest printed an `F`, but the timeout prevented the final traceback and summary. A direct ten-worker diagnostic completed the same selection in 814.31 seconds under a different `PACK_JOBS` shape; it is an observed workaround, not a controlled validation of the proposed allocation. The final local push used `--jobs 2 --inner-jobs 2 --timeout-seconds 1800 --since 4c202aeb` and passed 49 steps and 1,619 tests in 392.33 seconds, but it selected a different change set and likewise does not validate the proposal. Follow up in an efficiency block: use measured selection cost to allocate workers without relaxing per-test or tier ceilings. This does not block mathematical correctness or replace H-216 as the selected research entry.

## Notes

2026-09-19 pipeline follow-up at `4c202aeb8daaf15133bb15fd2244d1f60e1efdef`:

- `packing-validate --push --since 2aaa296de815e5048b013ea268cc72d0c273b7ac` selected
  72/350 test files on a ten-CPU host.
  Implicit `jobs=10` and `inner_jobs=3` made `_pytest_workers(10)` return one, so the
  dynamic reachable-test step ran serial.
  Every other push step passed.
  Pytest printed an `F`, but the timeout prevented the final traceback and summary.
  The command artifact timed out after 901.012 seconds; the tier wall was 941.59 seconds
  and remained below its 1,800-second ceiling.
- Seven selected files contain measured slow tests.
  Of the 72 selected files, 65 have quick-lane cost entries totaling 192.0 of 545.746
  recorded test-seconds.
  Treat 192.0 as a lower bound: the quick record omits the selected slow nodes.
- Narrow recommendation: extend only the implicit push resource decision.
  Have the selector report a structured costly-partial classification using measured
  slow-test coverage plus the committed file-cost record.
  A costly implicit partial selection may reuse the whole-suite `jobs=1`, `inner_jobs=1`
  allocation, which would give xdist the host CPUs and prevent nested pools.
  This allocation remains unimplemented and needs a measured validation.
  Cheap partial selections and explicit resource settings should remain unchanged.
  Do not relax the 900-second subprocess or 1,800-second tier ceilings; missing or
  malformed cost evidence must fail conservatively.
- `packing-validate --push --only "reachable behavioral tests"` cannot isolate the
  dynamic step because static `--only` filtering runs before that step is appended.
  The diagnostic retry therefore called the selector directly with `PACK_JOBS=2` and
  `-n10`; it had no validator 900-second wrapper cap.
  It finished in 814.31 seconds with one failure, 1,858 passes, and four warnings.
  Because it changed both xdist and `PACK_JOBS`, it is an observed workaround rather
  than a controlled speedup or validation of the proposed `jobs=1`, `inner_jobs=1`
  allocation.
- The retry’s sole failure was a separate test-fixture race: a 200 ms deadline expired
  before a new Python child printed `partial`. The artifact test now uses a
  deterministic `_run_command` boundary fixture that writes and flushes partial output
  before raising `StepTimeoutError`; the separate slow real-subprocess test retains
  process/output coverage.
  `tests/test_validation_cli.py` passed 125 tests in 25.04 seconds, Ruff passed, and
  BasedPyright reported zero findings.
  This fixed defect is tracked by `think-u5zn`, which remains open for closure after
  final CI.
- The final local push used
  `packing-validate --push --since 4c202aeb --jobs 2 --inner-jobs 2 --timeout-seconds 1800`
  and passed 49 steps and 1,619 tests in 392.33 seconds.
  It selected a different change set from the 72-file run, so it does not provide a
  controlled validation of the proposed allocation.

Detailed analysis: `/private/tmp/stack-review-pipeline-followup.md`. Leave this bead
open for the future efficiency block.
This work does not replace `think-qqzs`, selected research H-216, or the existing `g4n9`
work.
