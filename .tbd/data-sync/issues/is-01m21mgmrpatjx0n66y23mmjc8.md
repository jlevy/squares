---
type: is
id: is-01m21mgmrpatjx0n66y23mmjc8
title: Refresh the CI suite timing baseline from current hosted runs
kind: bug
status: open
priority: 2
version: 8
spec_path: docs/project/specs/active/plan-2026-09-07-math-text-face.md
labels: []
dependencies: []
parent_id: is-01m2kb4xhaqh3bv0cnnqnqvvsp
created_at: 2026-09-08T23:09:10.292Z
updated_at: 2026-09-16T03:00:08.866Z
closed_at: null
close_reason: null
resolution: null
duplicate_of: null
---
Final rendering CI run34288782986 at a10569d1 passed all4,283 behavioral tests in88.84s but failed the existing lower timing bound against the old162.62s one-sample baseline. Preserve the current tests and regression policy, inspect comparable prior hosted readings and refresh the timing record honestly. Track broader noisy single-point policy under existing think-be1s. Product rendering checks and Pages all passed.

## Notes

CI baseline refresh verified on merged-main integration131b9758: all Squares checks pass, including suite34291135875/job102277711311 and packing-required aggregator. Previous too-fast result was4283testsPASS88.84s against stale162.62s record; refreshed118.72geomean/237ceiling retains policy. Final typography integration will receive a fresh gate before closing.


2026-09-15 (think-z121): reopening at P2, because this bead's done-when is contradicted by its own lane. The 118.72 s record written here was superseded the same week by 183.44 s, and on 2026-09-15 `packing/devtools/read_tier_walls.py` read `suite` at 210.21 s across seven hosted pull-request runs (34924677097, 34925616821, 34926777301, 34929890466, 34930296150, 35012847055, 35013703659) -- 1.15x the standing record, on a lane that has grown from 4,639 to about 5,700 quick tests since this closed. The baseline is stale again in exactly the way this bead existed to stop. Lane 2 (think-t7zm) shards `suite` and owns the new record; under rule 6 that think-z121 adds to `packing/devtools/check_gate_budgets.py`, the next record above 123.40 s -- 1.2x of the 102.83 s that heads this tier's history -- has to carry per-file test-cost attribution rather than another re-base.

2026-09-15 (think-z121): moved under think-xfqk, the CI speed epic, because its old parent -- the closed math-startup rendering epic -- is terminal and an open bead under a closed parent fails the repository's bead-tree record check (D-025). The obligation is a CI one now: the suite record is stale in the unflattering direction and lane 2 (think-t7zm) writes the next one.
