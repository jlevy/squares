---
type: is
id: is-01m4b3jr83kgj8ffe98d3xd1d0
title: Profile and bound the n17 committed-ledger regression test
kind: task
status: closed
priority: 1
version: 4
delegate: codex@17e132e9b179
labels: []
dependencies: []
parent_id: is-01m4ajdxfkfqyr1yj5d4wm5npt
hold: null
hold_until: null
created_at: 2026-10-07T11:57:01.570Z
updated_at: 2026-10-07T12:04:20.154Z
started_at: 2026-10-07T11:57:11.899Z
closed_at: 2026-10-07T12:04:20.153Z
close_reason: Completed in test-only commit 99b20f6f37f8e6fadf0027fd96460aa692bf7762 after independent Astra acceptance. Quiet module32pass:27.452 to21.037 wall; flagged call12.04 to6.52sec; all65assertion ASTs identical. Quick plugin guard2pass. Production, geometry, caps and budgets unchanged. Full shard A verification remains tracked under parent/engineering child.
resolution: null
duplicate_of: null
---
W7 bounded engineering. Diagnose the n17 committed-ledger recheck-flag test exceeding its 12-second quick-lane ceiling. Preserve every assertion, production numerical decisions and historical caps; optimize only equivalent duplicated setup or profiled helper work. Retain baseline/profile/after measurements and affected module outcomes.

## Notes

N17 committed-ledger regression: bounded test-only deduplication

Source baseline: a1a67f0dc1fa06e5b91ba6601626862c148b1774.
Interpreter: CPython 3.14.7; installed frozen project environment.
Instrument: packing/benchmarks/validation_timing.py.
Regime: one pytest process, PACK_JOBS=1, native threads=1, warm filesystem.
The quiet pair ran with other engineering validations held. Lightweight editing
continued. These are samples, not a statistical speedup claim.

Diagnosis: the flagged-ledger test ran both the default flagged census and the
same bare census separately exercised by the bare-ledger test. Profiling the
flagged test found two census calls at 16.955 cumulative profiled seconds; repeated
ledger/certificate-byte checks and exact state/orbit computations dominate.

Fix: share the bare committed census through a module-scoped pytest fixture used
by those two read-only consumers. The flagged census still independently runs
the production admission, selector, certificate-byte, Burnside and canonical
checks. No production source, mathematical inputs, caps, budgets, markers or
expected outcomes changed. All 65 assertion ASTs are identical in source order.
Both consumers only read the shared nested data and construct separate sets/maps.
The module never mutates the committed ledger/receipts; mutable fixture tests use
temporary paths. Quick-lane loadfile scheduling retains module-local sharing.

Initial instrument pair (32 passed each):
before/88e7d16f590a45d1904d493b182b8381: 26.505 wall, 25.94 pytest;
target call 11.88, separate bare call 5.84 seconds.
after/5f9ede32ee434557967c084942859630: 26.025 wall, 25.43 pytest;
target call 6.95, shared fixture setup 7.53 seconds.
Other phases drifted upward; this pair shows only 1.8% total wall improvement.

Quiet instrument pair (32 passed each):
before-quiet/7eeb4d4b08fa4055b024f457750d2d62: 27.452 wall, 26.89 pytest;
target call 12.04, separate bare call 6.36 seconds.
after-quiet/25d961fb543c41748fc8c206202a9b08: 21.037 wall, 20.41 pytest;
target call 6.52, shared fixture setup 5.61 seconds.
Observed whole-module wall saving: 6.415 seconds (23.4%). The 6.52-second call
fits the unchanged 12-second ceiling with 5.48 seconds of measured headroom.

An isolated flagged test still computes one bare census in setup and one flagged
census in call. Its total work is not reduced; the genuine savings occur when
both module consumers share their bare census. This is not merely setup movement.

Raw profile, all four instrument receipts, streamed logs, JUnit, source snapshots,
and candidate.patch are retained beside this summary. Ruff check/format passed;
BasedPyright reported zero errors, warnings and notes. Final two-consumer guard
using devtools.suite_files shard 1/4 and devtools.cpu_durations passed 2 tests,
30 deselected in 12.79 seconds: target call 5.77, fixture setup 6.38 seconds.
Independent Astra review accepted the unchanged semantics and genuine module
savings, with the isolated-test caveat. Plugin guard raw output/JUnit are retained.
