---
type: is
id: is-01m21mgmrpatjx0n66y23mmjc8
title: Refresh the CI suite timing baseline from current hosted runs
kind: bug
status: in_progress
priority: 1
version: 3
spec_path: docs/project/specs/active/plan-2026-09-07-math-text-face.md
labels: []
dependencies: []
parent_id: is-01m20v1mq20k9d9p1wg9s5qdsq
created_at: 2026-09-08T23:09:10.292Z
updated_at: 2026-09-09T00:01:20.313Z
---
Final rendering CI run34288782986 at a10569d1 passed all4,283 behavioral tests in88.84s but failed the existing lower timing bound against the old162.62s one-sample baseline. Preserve the current tests and regression policy, inspect comparable prior hosted readings and refresh the timing record honestly. Track broader noisy single-point policy under existing think-be1s. Product rendering checks and Pages all passed.

## Notes

CI baseline refresh verified on merged-main integration131b9758: all Squares checks pass, including suite34291135875/job102277711311 and packing-required aggregator. Previous too-fast result was4283testsPASS88.84s against stale162.62s record; refreshed118.72geomean/237ceiling retains policy. Final typography integration will receive a fresh gate before closing.
