---
type: is
id: is-01m57gjhwmrv6cw4dxtpper5h5
title: Use fresh per-run external TMPDIR for full validation
kind: chore
status: open
priority: 2
version: 1
labels:
  - efficiency
dependencies: []
created_at: 2026-10-18T12:42:50.643Z
updated_at: 2026-10-18T12:42:50.643Z
---
Follow-up from PR #671, exact unchanged source head ccb2e5e912e73bc041a7ddf3683aea70d87dc010. Keep this separate from the n108 import; no validation source or test ceiling changed in that PR.

Observed receipts on the external scratch volume:
- Persistent task TMPDIR: required --push --jobs 2 ended at 1369.65 s real (1368.27 s tier, 1800 s ceiling), with four timing-only failures and 19,012 quick tests passing. Both signal subprocess controls exceeded 5 s; vendored content matched all 351 files but took 6.38 s against 5 s; Lean retained receipt was valid but took 1.62 s against 1 s.
- The unchanged four-test probe passed signal/Lean controls but took 154.34 s overall. lsof confirmed pytest in U/I/O wait deleting an old pytest-of-levy/garbage-06cfe9c4-.../popen-gw8/control-snapshot0/snapshot/.git/objects/db tree after test execution. The vendored check still passed contents but took 7.81 s. A fresh explicit external --basetemp singleton passed that same assertion in 0.08 s (0.75 s overall).
- Fresh per-run external TMPDIR, same exact head/--push --jobs 2/1800 s ceiling and failed-only retention flags: 69/69 selected steps passed in 990.15 s real (988.54 s tier). Quick suite: 19,016 passed, 55 skipped, one xfailed; pool lane: 10 passed. This is observed recovery, not a controlled speedup claim: cache and host load also differed.

Implement a task-owned fresh external TMPDIR for each full validation invocation, propagated to nested subprocesses. Verify the volume is mounted/writable, retain failed-only pytest retention flags and per-worktree Cargo targets, and keep source/unique evidence outside disposable scratch. Clean inactive stale trees separately from the timed validation path with bounded, recoverability-aware cleanup.

Do not put a fixed --basetemp in global PYTEST_ADDOPTS: nested pytest subprocesses inherit it and can collide or change contract tests. The parallel #676 investigation also observed global inherited -x changing nested-test behavior. An isolated singleton --basetemp probe is different from global full-gate configuration.

Acceptance: explicit per-invocation scratch ownership; nested pytest isolation; unchanged test/step ceilings and retention rules; measured full-gate comparison with receipts; no internal-disk fallback. Leave this open for the next efficiency slice under OR-12/OR-17.

Durable host receipts: /Volumes/spud-ext1/agent-source/squares-671-retention-evidence-20261018/{push-final-ccb2e5e9.log,push-timing-failures-isolated-ccb2e5e9.log,push-vendored-isolated-ccb2e5e9.log,push-fresh-tmp-ccb2e5e9.log}. The local files are retained evidence; hosted #671 CI is separate.
